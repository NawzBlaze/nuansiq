#!/usr/bin/env python3
"""Repository self-check for Nuansiq.

Standard library only, so it runs anywhere without an install step.

Checks:
  1. Every skill directory has a SKILL.md whose frontmatter matches the
     Agent Skills specification (name rules, directory match, description
     length, allowed keys, compatibility length).
  2. The skill body stays inside the size budgets the spec recommends.
  3. Relative Markdown links resolve to files that exist.
  4. No leftover placeholder text.
  5. No package-manager install command implies a package that does not exist.
  6. README documents the sections a reader needs before installing.

Usage: python3 scripts/validate.py [--strict]
Exit code is 1 if any errors are found.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_BODY_LINES = 500  # specification recommendation
WARN_BODY_LINES = 300
MAX_BODY_TOKENS = 5000  # rough estimate: characters / 4

# Values a real YAML parser would read as numbers, booleans, or null.
UNQUOTED_SCALAR_RE = re.compile(r"^(?:true|false|null|~|-?\d+(?:\.\d+)?)$", re.IGNORECASE)

ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)")
CODE_PATH_RE = re.compile(r"`((?:skills|evals|examples|scripts|references)/[\w./-]+\.(?:md|py|yml|yaml))`")

# Built from fragments so this file does not trip its own placeholder check.
PLACEHOLDERS = [
    "TO" + "DO",
    "TB" + "D",
    "FIX" + "ME",
    "XX" + "X",
    "lorem" + " ipsum",
    "<" + "insert",
    "PLACE" + "HOLDER",
]

FAKE_INSTALLS = [
    "npm install nuan" + "siq",
    "npm i nuan" + "siq",
    "npx nuan" + "siq",
    "pip install nuan" + "siq",
    "uv add nuan" + "siq",
    "brew install nuan" + "siq",
    "gem install nuan" + "siq",
]

# Host, vendor, and syntax specifics belong in installation docs, not in the
# skill package: the core guidance must stay model-agnostic.
VENDOR_TOKENS = [
    "claude",
    "codex",
    "copilot",
    "openai",
    "anthropic",
    "gemini",
    "gpt",
    "llama",
    "mistral",
    "qwen",
    ".claude",
    ".agents",
    "/nuansiq",
    "$nuansiq",
    "web_search",
    "read_file",
]

REQUIRED_README_SECTIONS = [
    "What it is",
    "What it does not do",
    "Three ways to use",
    "native skill",
    "Manual instruction fallback",
    "Developer integration",
    "Capability matrix",
    "Evaluating it",
    "Known limitations",
    "License",
]

errors: list[str] = []
warnings: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_frontmatter(text: str, path: Path) -> tuple[dict, str, list[str]]:
    """Parse the small YAML subset the specification needs.

    Supports top-level `key: value`, quoted values, and one level of nested
    mapping for `metadata`. Anything fancier is reported rather than guessed.

    Returns (metadata, body, notes). Notes flag values that are unquoted and
    would be parsed as numbers or booleans by a real YAML parser, which the
    specification does not allow for `metadata`.
    """
    notes: list[str] = []
    if not text.startswith("---"):
        error(f"{rel(path)}: file does not start with '---' frontmatter")
        return {}, text, notes

    parts = text.split("---", 2)
    if len(parts) < 3:
        error(f"{rel(path)}: frontmatter is not closed with '---'")
        return {}, text, notes

    raw, body = parts[1], parts[2]
    data: dict = {}
    current_map: str | None = None

    for number, line in enumerate(raw.splitlines(), start=1):
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current_map is None:
                error(f"{rel(path)}: indented frontmatter line {number} has no parent key")
                continue
            if ":" not in line:
                error(f"{rel(path)}: cannot parse frontmatter line {number}: {line.strip()!r}")
                continue
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()
            data[current_map][key] = strip_quotes(value)
            if not quoted(value) and UNQUOTED_SCALAR_RE.match(value):
                notes.append(
                    f"{rel(path)}: {current_map}.{key} is unquoted ({value!r}); the "
                    "specification requires metadata values to be strings, so quote it"
                )
            continue
        if ":" not in line:
            error(f"{rel(path)}: cannot parse frontmatter line {number}: {line.strip()!r}")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), strip_quotes(value.strip())
        if value == "":
            data[key] = {}
            current_map = key
        else:
            data[key] = value
            current_map = None

    return data, body, notes


def quoted(value: str) -> bool:
    return len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'"


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def check_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        error(f"{rel(skill_dir)}: missing SKILL.md")
        return

    text = skill_md.read_text(encoding="utf-8")
    meta, body, notes = parse_frontmatter(text, skill_md)
    for note in notes:
        warn(note)

    extra = set(meta) - ALLOWED_FIELDS
    if extra:
        error(f"{rel(skill_md)}: unexpected frontmatter fields: {', '.join(sorted(extra))}")

    name = meta.get("name", "")
    if not isinstance(name, str) or not name:
        error(f"{rel(skill_md)}: missing required field 'name'")
    else:
        if len(name) > MAX_NAME:
            error(f"{rel(skill_md)}: name exceeds {MAX_NAME} characters")
        if not NAME_RE.match(name):
            error(
                f"{rel(skill_md)}: name {name!r} must be lowercase letters, digits and "
                "single hyphens, with no leading or trailing hyphen"
            )
        if name != skill_dir.name:
            error(f"{rel(skill_md)}: name {name!r} must match directory {skill_dir.name!r}")

    description = meta.get("description", "")
    if not isinstance(description, str) or not description.strip():
        error(f"{rel(skill_md)}: missing required field 'description'")
    else:
        if len(description) > MAX_DESCRIPTION:
            error(
                f"{rel(skill_md)}: description is {len(description)} characters, "
                f"over the {MAX_DESCRIPTION} limit"
            )
        if not re.search(r"\buse\b", description, re.IGNORECASE):
            warn(f"{rel(skill_md)}: description does not say when to use the skill")

    compatibility = meta.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > MAX_COMPATIBILITY:
        error(f"{rel(skill_md)}: compatibility exceeds {MAX_COMPATIBILITY} characters")

    metadata = meta.get("metadata")
    if isinstance(metadata, dict):
        for key, value in metadata.items():
            if not isinstance(value, str):
                error(f"{rel(skill_md)}: metadata.{key} must be a string")

    line_count = len(body.strip().splitlines())
    token_estimate = len(body) // 4
    if line_count > MAX_BODY_LINES:
        error(f"{rel(skill_md)}: body is {line_count} lines, over the {MAX_BODY_LINES} recommendation")
    elif line_count > WARN_BODY_LINES:
        warn(f"{rel(skill_md)}: body is {line_count} lines; consider moving detail into references/")
    if token_estimate > MAX_BODY_TOKENS:
        error(
            f"{rel(skill_md)}: body is roughly {token_estimate} tokens, "
            f"over the {MAX_BODY_TOKENS} recommendation"
        )

    # Every file the skill points at should exist.
    for match in LINK_RE.finditer(body):
        check_link(match.group(1), skill_md)


def check_link(target: str, source: Path) -> None:
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return
    path_part = target.split("#", 1)[0]
    if not path_part:
        return
    resolved = (source.parent / path_part).resolve()
    if not resolved.exists():
        error(f"{source.relative_to(ROOT)}: link target does not exist: {target}")


def iter_markdown() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "node_modules" not in path.parts
    )


def check_markdown() -> None:
    for path in iter_markdown():
        text = path.read_text(encoding="utf-8")

        for match in LINK_RE.finditer(text):
            check_link(match.group(1), path)

        for match in CODE_PATH_RE.finditer(text):
            target = match.group(1)
            candidate = ROOT / target
            if not candidate.exists() and not (path.parent / target).exists():
                error(f"{rel(path)}: code reference does not exist: {target}")

        lowered = text.lower()
        for token in PLACEHOLDERS:
            if token.lower() in lowered:
                error(f"{rel(path)}: placeholder text found: {token!r}")

        for command in FAKE_INSTALLS:
            if command in text:
                error(
                    f"{rel(path)}: documents an install command for a package that does not "
                    f"exist: {command!r}"
                )


def check_readme() -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        error("README.md is missing")
        return
    text = readme.read_text(encoding="utf-8")
    for section in REQUIRED_README_SECTIONS:
        if section.lower() not in text.lower():
            warn(f"README.md: no mention of required section {section!r}")
    if "license" not in text.lower():
        warn("README.md: no license status is stated")
    if "http://github.com/" in text:
        warn("README.md: contains an insecure http:// link")


def detect_license_family(text: str) -> str | None:
    """Return the licence family named by a LICENSE file, if recognisable."""
    families = {
        "MIT": "MIT License",
        "Apache-2.0": "Apache License",
        "BSD-3-Clause": "BSD 3-Clause",
        "BSD-2-Clause": "BSD 2-Clause",
        "GPL-3.0": "GNU GENERAL PUBLIC LICENSE",
    }
    for family, marker in families.items():
        if marker in text:
            return family
    return None


def check_vendor_neutral_core() -> None:
    """The skill package must not depend on a host, vendor, or tool naming."""
    skills_dir = ROOT / "skills"
    if not skills_dir.exists():
        return
    for path in sorted(skills_dir.rglob("*.md")):
        lowered = path.read_text(encoding="utf-8").lower()
        hits = sorted(token for token in VENDOR_TOKENS if token in lowered)
        if hits:
            error(
                f"{rel(path)}: core guidance contains host or vendor specifics "
                f"({', '.join(hits)}); keep them in the installation docs instead"
            )


def check_standalone() -> None:
    """The standalone manual must be a fresh build of the canonical sources."""
    script = ROOT / "scripts" / "build_standalone.py"
    output = ROOT / "standalone" / "nuansiq-manual.md"
    if not script.exists():
        error("scripts/build_standalone.py is missing")
        return
    if not output.exists():
        error("standalone/nuansiq-manual.md is missing; run python3 scripts/build_standalone.py")
        return

    result = subprocess.run(
        [sys.executable, str(script), "--check"], capture_output=True, text=True
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip().splitlines()
        detail = message[0] if message else "run python3 scripts/build_standalone.py"
        error(f"standalone instructions are out of date: {detail}")


def check_license_status() -> None:
    candidates = ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"]
    license_path = next((ROOT / name for name in candidates if (ROOT / name).exists()), None)

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    lowered = readme_text.lower()

    if license_path is None:
        if "no license has been selected" not in lowered:
            warn(
                "No license file and the README does not state that none has been selected; "
                "the project must not be described as open source"
            )
        return

    text = license_path.read_text(encoding="utf-8")
    family = detect_license_family(text)
    if family is None:
        warn(f"{license_path.name}: licence family not recognised; check it is a complete licence text")
    elif family.lower() not in lowered:
        warn(
            f"{license_path.name} is {family}, but README.md does not mention it; "
            "keep the licensing statements consistent"
        )

    if "copyright" not in text.lower():
        warn(f"{license_path.name}: no copyright line found")
    if "no license has been selected" in lowered:
        warn("README.md still says no licence is selected, but a licence file exists")


def main() -> int:
    if not SKILLS_DIR.exists():
        error("skills/ directory is missing")
    else:
        skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
        if not skill_dirs:
            error("skills/ contains no skill directories")
        for skill_dir in skill_dirs:
            check_skill(skill_dir)

    check_markdown()
    check_readme()
    check_license_status()
    check_vendor_neutral_core()
    check_standalone()

    for message in warnings:
        print(f"warning: {message}")
    for message in errors:
        print(f"error: {message}")

    print()
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    if errors:
        print("FAILED")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
