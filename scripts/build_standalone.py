#!/usr/bin/env python3
"""Generate standalone/nuansiq-manual.md from the canonical skill files.

The standalone document is a *derived artefact*, never a second source of
behavioural truth. It is produced deterministically from:

  skills/nuansiq/SKILL.md          -> Part 1 (core instructions)
  skills/nuansiq/references/*.md   -> Parts 2-4 (appendices)

Determinism: the output contains no timestamps, commit hashes, or host names.
The only variable content is the source files themselves, plus a digest of
their bytes. Running this twice on the same sources produces byte-identical
output.

Usage:
  python3 scripts/build_standalone.py            # write the file
  python3 scripts/build_standalone.py --check    # fail if the file is stale
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = ROOT / "skills" / "nuansiq" / "SKILL.md"
REFS_DIR = ROOT / "skills" / "nuansiq" / "references"
OUTPUT = ROOT / "standalone" / "nuansiq-manual.md"
LICENSE_FILE = ROOT / "LICENSE"

# Fixed order, fixed titles. Changing these changes the generated document,
# so the digest changes too and --check will report the file as stale.
PARTS = [
    ("judgement", "Part 2 — Judgement", "choosing well for one specific person"),
    ("research", "Part 3 — Research", "getting facts without pretending"),
    ("critique", "Part 4 — Critique", "review that ends in a decision"),
]

# Links that only make sense inside the skill package are rewritten to part
# references. Any other relative link is an error: the standalone file must
# not depend on repository files that a reader may not have.
LINK_REWRITES = {
    "references/judgement.md": "Part 2 (Judgement)",
    "references/research.md": "Part 3 (Research)",
    "references/critique.md": "Part 4 (Critique)",
}

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,5})(\s)")


class BuildError(RuntimeError):
    pass


def split_frontmatter(text: str, path: Path) -> str:
    """Return the Markdown body of a file that may start with YAML frontmatter."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) < 3:
            raise BuildError(f"{path}: frontmatter is not closed")
        return parts[2].lstrip("\n")
    return text


def transform(body: str, path: Path) -> str:
    """Strip the leading H1, demote headings, rewrite package-relative links.

    Fenced code blocks are left untouched: they may contain example files.
    """
    lines = body.splitlines()
    out: list[str] = []
    in_fence = False
    heading_dropped = False

    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue

        if not in_fence:
            # Drop the document title only; the part heading supplies it.
            if not heading_dropped and not line.strip():
                out.append(line)
                continue
            if not heading_dropped and re.match(r"^#\s", line):
                heading_dropped = True
                continue

            line = HEADING_RE.sub(r"#\1\2", line)

            def replace(match: re.Match) -> str:
                target = match.group(2)
                if target in LINK_REWRITES:
                    return LINK_REWRITES[target]
                if target.startswith(("http://", "https://", "#")):
                    return match.group(0)
                raise BuildError(
                    f"{path}: link target {target!r} is not handled by the standalone build. "
                    "Add it to LINK_REWRITES or remove it from the source."
                )

            line = LINK_RE.sub(replace, line)

        out.append(line)

    if not heading_dropped:
        raise BuildError(f"{path}: expected a leading H1 title to drop; the format changed")

    return "\n".join(out).strip("\n")


def sources() -> list[tuple[str, str, Path]]:
    """Return (part name, subtitle, path) for all parts, in fixed order."""
    files = [("Part 1 — Core instructions", "the part that always applies", SKILL_MD)]
    for slug, title, subtitle in PARTS:
        files.append((title, subtitle, REFS_DIR / f"{slug}.md"))
    for _, _, path in files:
        if not path.exists():
            raise BuildError(f"missing canonical source: {path}")
    return files


def digest(files: list[tuple[str, str, Path]]) -> str:
    sha = hashlib.sha256()
    for _, _, path in files:
        sha.update(path.relative_to(ROOT).as_posix().encode())
        sha.update(path.read_bytes())
    return sha.hexdigest()[:12]


def word_count(text: str) -> int:
    return len(re.sub(r"[#*`|>_-]", " ", text).split())


def token_count(text: str) -> int:
    """Rough estimate at four characters per token, rounded to the nearest hundred."""
    return int(round(len(text) / 4, -2))


def header(files: list[tuple[str, str, Path]], stats: list[tuple[str, int, int]]) -> str:
    part1_words, part1_tokens = stats[0][1], stats[0][2]
    total_words = sum(words for _, words, _ in stats)
    total_tokens = sum(tokens for _, _, tokens in stats)
    return f"""<!--
GENERATED FILE — do not edit by hand.
Built from the Nuansiq skill package (SKILL.md plus three reference files)
by scripts/build_standalone.py. Rebuild that way; verify with --check.
Source digest: sha256:{digest(files)}
-->

# Nuansiq — manual instructions

**Manual instruction fallback, v0.1.0. This is not a skill installation and not equivalent to one.**

Copy this text into whatever instruction channel your tool provides: a system or developer prompt, a custom-instructions setting, a project instruction file, or the first message of a conversation. Nothing loads automatically. The host will not discover it, will not load parts on demand, and will apply it to every request until you remove it.

**What it is.** Behavioural guidance for judgement on open-ended work: understanding the job and its audience, deciding when facts need checking, choosing an approach deliberately, making the deliverable, and reviewing it proportionately. It is text only. It contains no tools, no model, no telemetry, and no storage, and it does not grant you capabilities of any kind.

**What it cannot do.** It cannot browse, read files, inspect images, run commands, or remember an earlier session unless the host already provides those abilities. Never claim a capability this text does not give you, and never present an assumption as something you verified.

**How to use it.**

- Smallest useful setup: paste **Part 1** only. That is the core method, and it is the part that always applies.
- Fuller setup: paste **Part 1** plus the appendix that matches the task — Part 2 for choosing between approaches or handling preferences, Part 3 for questions about facts, sources, or missing tools, Part 4 for reviewing or revising a draft.
- If context is tight, prefer Part 1 over pasting everything.

**Boundaries.** Follow the user's requested format, length, and language, and follow the safety rules of whatever host you are running in. This document does not override either. For simple or mechanical requests, answer directly; do not run the method as a procedure.

**Size.** Part 1 is about {part1_words:,} words, roughly {part1_tokens:,} tokens at four characters per token. All four parts together are about {total_words:,} words, roughly {total_tokens:,} tokens.

**Licence.** MIT, copyright (c) 2026 NawzBlaze. The full licence text is at the end of this document; keep it with the document, and do not present the text as a different licence, if you redistribute it.
"""


def license_text() -> str:
    """The licence is copied verbatim from the single LICENSE file."""
    if not LICENSE_FILE.exists():
        raise BuildError("LICENSE is missing; the standalone document must carry a licence")
    return LICENSE_FILE.read_text(encoding="utf-8").strip()


def render() -> str:
    files = sources()
    chunks: list[str] = []
    parts_markdown: list[str] = []
    stats: list[tuple[str, int, int]] = []

    for title, subtitle, path in files:
        body = transform(split_frontmatter(path.read_text(encoding="utf-8"), path), path)
        parts_markdown.append(f"## {title}\n\n*{subtitle}*\n\n{body}")
        stats.append((title, word_count(body), token_count(body)))

    parts = "\n\n---\n\n".join(parts_markdown)
    chunks.append(header(files, stats))
    chunks.append(parts)
    chunks.append("## Licence\n\nThe full licence text follows.\n\n" + license_text())
    text = "\n\n---\n\n".join(chunk.strip("\n") for chunk in chunks) + "\n"

    # Guards: the output must not depend on repository files or host syntax.
    for forbidden in ("](references/", "](skills/", "](/", ".claude/", ".agents/"):
        if forbidden in text:
            raise BuildError(f"generated document still contains {forbidden!r}")
    return text


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    try:
        text = render()
    except BuildError as exc:
        print(f"build error: {exc}", file=sys.stderr)
        return 1

    if check_only:
        if not OUTPUT.exists():
            print(f"stale: {OUTPUT.relative_to(ROOT)} is missing", file=sys.stderr)
            return 1
        if OUTPUT.read_text(encoding="utf-8") != text:
            print(
                f"stale: {OUTPUT.relative_to(ROOT)} does not match its sources.\n"
                "Run: python3 scripts/build_standalone.py",
                file=sys.stderr,
            )
            return 1
        print(f"up to date: {OUTPUT.relative_to(ROOT)}")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(text):,} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
