# Nuansiq

Nuansiq gives an existing AI agent a working method for human-centered judgement: clarify the job and its audience, choose an approach deliberately, research when facts could change the answer, and critique concrete problems before handing work over.

**Preview status.** v0.1.0, one skill. This work is on the branch `arena/05108cd1-nuansiq`; the default branch `main` does not contain it, and there is no release. Licensed MIT (see [License](#license)). No model or product is listed as supported; see the [capability matrix](#capability-matrix).

**Use it three ways.** As a [native Agent Skill](#installing-as-a-native-skill-host-specific), as a [manual instruction file](#manual-instruction-fallback-no-native-skills) for hosts without skill support, or as [programmatic context](#developer-integration-programmatic-context) in your own app. The behavioural guidance is the same in all three; only the delivery differs.

**Example (an illustration, not an observed result).** In a host where the skill is installed and invoked by name:

```text
/nuansiq review this onboarding email for warehouse staff; it currently reads like a press release.
```

The shape aimed at: a note on who the email is actually for, a rewritten draft at the requested length, one concrete tradeoff named, and no closing offer to keep going. In manual mode the same request is just the request, sent after pasting the [standalone instructions](standalone/nuansiq-manual.md). Nobody has run either path in a host and recorded the output.

**Testing status.** The skill is format-valid and was copied to all four documented host paths with its frontmatter revalidated there. Activation and task behaviour are untested in every host. The [behavioural pilot](evals/pilot.md) and the [cross-model plan](evals/cross-model-plan.md) have **not been run**. A step-by-step check for one host is in [evals/manual-test-claude-code.md](evals/manual-test-claude-code.md).

## What it is

- A portable [Agent Skills](https://agentskills.io/specification) package: one `SKILL.md` plus three reference files, structured for hosts that load reference material on demand.
- The same guidance as a single [standalone document](standalone/nuansiq-manual.md), generated from those sources, for environments with no skill support.
- A method, not a persona. Nothing in it asks an agent to pretend to have feelings, taste memories, or a human voice.
- Aimed at writing, visual briefs and image prompts, research-backed recommendations, and practical advice, with authored examples and eval briefs for each.
- Its instructions require an agent to separate verified facts from assumptions, treat retrieved text as data rather than instructions, and avoid claiming tools or memory it does not have. This describes the text, not a tested runtime behaviour.

## What it does not do

- It does not give an agent consciousness, emotion, or a universal standard of taste, and it does not claim to.
- It does not guarantee that output is good, original, popular, or correct. A judgement method reduces specific failure modes; it does not certify quality.
- It does not make specialist advice safe. Medical, legal, financial, and safety-critical work still needs qualified people.
- It does not add tools. Research, image inspection, file access, and memory work only if your host agent already provides them.
- It does not store data, phone home, or collect telemetry. There is nothing to run and nothing to sign up for.
- It does not make any model, product, or vendor "supported". Accepting instruction text is not support, and one good answer is not evidence.
- It is not a replacement for your own review of the output.

## Who it is for

- People who use an AI agent for open-ended work and are tired of fluent, generic results.
- Teams that want a shared vocabulary for critique: task success, audience fit, specificity, tradeoffs, honest uncertainty.
- Developers wiring instruction text into their own application, who want guidance that does not assume a particular vendor.
- Skill authors looking for a worked example of progressive disclosure: a short always-loaded body and deeper guidance behind it.

## Three ways to use Nuansiq

| Path | What it needs from the host | Where it lives |
| --- | --- | --- |
| Native Agent Skill | A host that implements the Agent Skills format and scans a skills directory | [`skills/nuansiq/`](skills/nuansiq/SKILL.md), installed per host below |
| Manual instructions | Any interface that accepts instruction text: system prompt, custom instructions, project rules, or a first message | [`standalone/nuansiq-manual.md`](standalone/nuansiq-manual.md) |
| Programmatic context | Your application's own mechanism for passing instructions to a model | [docs/integration.md](docs/integration.md) |

They differ in delivery, not in content. Native skills can load reference material only when needed and can be removed by deleting a folder. Pasting the manual file loads all of it at once and has to be removed from the text itself. Programmatic injection is versioned by your app and is invisible to the end user.

## What is in this repository

On the branch `arena/05108cd1-nuansiq`:

```
README.md
CONTRIBUTING.md
LICENSE                         # MIT, copyright 2026 NawzBlaze
skills/
  nuansiq/
    SKILL.md                    # name, description, and the core loop
    references/
      judgement.md              # approach choice, taste, preference conflicts
      research.md               # evidence, uncertainty, untrusted content, no-tool cases
      critique.md               # review, revision limits, handoff
standalone/
  nuansiq-manual.md             # GENERATED from the files above; do not edit by hand
docs/
  integration.md                # provider-neutral developer integration
examples/                       # four illustrative cross-domain walkthroughs
evals/                          # seven task briefs with criteria and failure modes
  pilot.md                      # five-case pilot procedure (status: not run)
  cross-model-plan.md           # two-family evaluation plan (status: not run)
  manual-test-claude-code.md    # step-by-step check in one host
scripts/
  validate.py                   # repository self-check, standard library only
  build_standalone.py           # builds standalone/ from the skill sources
.github/workflows/validate.yml  # runs the checks on pushes and pulls
```

The standalone file is a build artefact, not a second specification. `scripts/validate.py` fails if it does not match the skill sources, and the CI workflow runs the same check.

## Installing as a native skill (host-specific)

Everything host-specific lives in this section. The skill package itself contains no host names, no slash-command syntax, and no tool names; a check in `scripts/validate.py` enforces that.

> **Preview, not a released install.** The repository's default branch is `main`, which still contains only the initial commit. The skill lives on the branch `arena/05108cd1-nuansiq` and has not been merged. A plain clone of the repository URL therefore retrieves **no skill at all** until the owner merges this work; the commands below fetch the branch explicitly.

There is no package on npm or PyPI and no installer script; copying one folder is the whole installation.

### 1. Get the files

```bash
git clone --branch arena/05108cd1-nuansiq https://github.com/NawzBlaze/nuansiq.git
cd nuansiq
```

When this work is merged into `main` (owner decision, not done), drop `--branch arena/05108cd1-nuansiq`; the rest of these instructions do not change.

### 2. Copy the skill into your host

Run these from the clone root. Paths are the ones each host documents; see the [capability matrix](#capability-matrix) for what has and has not been tested.

**Claude Code, personal (all your projects):**

```bash
mkdir -p ~/.claude/skills
cp -R skills/nuansiq ~/.claude/skills/
```

**Claude Code, project-scoped:**

```bash
mkdir -p /path/to/your/project/.claude/skills
cp -R skills/nuansiq /path/to/your/project/.claude/skills/
```

**Codex, personal:**

```bash
mkdir -p ~/.agents/skills
cp -R skills/nuansiq ~/.agents/skills/
```

**Codex repository scope; also the path GitHub Copilot in VS Code uses:**

```bash
mkdir -p /path/to/your/project/.agents/skills
cp -R skills/nuansiq /path/to/your/project/.agents/skills/
```

### 3. Invoke it, as each host documents

These are documented routes, **none tested in a live session**:

- **Claude Code:** `/nuansiq`, or a request that matches the description.
- **Codex:** `$nuansiq`, or `/skills` to list what loaded.
- **VS Code Copilot:** ask a matching question in Agent mode; `/skills` lists installed skills.

Direct invocation does not depend on the description matching, so it is the predictable route.

### 4. Check what you got

```bash
find ~/.claude/skills/nuansiq -type f     # SKILL.md and references/*.md
```

You can validate the frontmatter with the reference library the specification points to. The PyPI package is called `skills-ref`; the command it installs is `agentskills`:

```bash
python3 -m venv .venv
.venv/bin/pip install skills-ref
.venv/bin/agentskills validate ~/.claude/skills/nuansiq
```

A passing check means the folder is a well-formed skill. It does not mean your host loaded it.

### Updating a native install

```bash
cd nuansiq
git pull
cp -R skills/nuansiq ~/.claude/skills/     # or your host's path
```

Replace the whole folder rather than individual files. A skill is a directory, so a stale `references/` copy will quietly disagree with `SKILL.md`.

## Manual instruction fallback (no native skills)

[`standalone/nuansiq-manual.md`](standalone/nuansiq-manual.md) is a self-contained document: core method, plus judgement, research, and critique appendices, with no links to other repository files. It is generated from the skill sources, so the guidance cannot drift from the skill's.

**This is a manual fallback, not an installation, and not equivalent to one.**

- Nothing is discovered: the host will not find it, will not load parts on demand, and will not remove it.
- It applies to every request until you delete the text, including small ones where process is harmful.
- Each request pays for the text you paste. Part 1 alone is about 1,700 tokens; all four parts about 6,600.
- Updates are manual: pull, rebuild, re-paste.

**How to use it:** paste the document into whatever instruction channel your tool provides — a system prompt, custom-instructions setting, project rules file such as `AGENTS.md`, or the first message of a conversation. Part 1 is the minimum useful setup; add Part 2 for approach and preference questions, Part 3 for facts and missing tools, Part 4 for review. Keep the user's requested format and the host's safety rules in force; the document says so explicitly.

**Rebuild after changing the skill:**

```bash
python3 scripts/build_standalone.py          # rewrite the file
python3 scripts/build_standalone.py --check  # fail if it is stale
```

Do not edit the generated file by hand; the check will reject it and the skill and fallback would drift apart.

## Developer integration (programmatic context)

If your application calls a model directly, you supply the same text through your provider's own instruction mechanism — a system or developer message, a custom-instructions setting, or an equivalent. There is no Nuansiq API, SDK, package, or endpoint, and a repository URL injects nothing on its own.

[docs/integration.md](docs/integration.md) covers where the text goes, provider-neutral pseudocode, versioning by content digest, context budgeting, how to check that injection took effect, and the privacy rules. It uses pseudocode only: no provider-specific example has been verified for this repository.

## Capability matrix

Labels used in this table:

- **Documented** — the host or provider documents the mechanism; nothing here exercised it.
- **File installation tested** — files were copied to the documented path and revalidated in place, with no host process involved.
- **Activation tested** — a host discovered the skill and used it in a live session.
- **Behaviour tested** — output was assessed against criteria in [`evals/`](evals/README.md).
- **Not tested** — no evidence.

| Capability | Depends on | Status today (2026-11-02) |
| --- | --- | --- |
| Native skill discovery | A host that implements the Agent Skills format and scans a skills directory | **Documented** for Claude Code, Codex, and VS Code Copilot; **file installation tested** on all four documented paths; activation **not tested**; behaviour **not tested** |
| Manual instruction use | Any interface that accepts instruction text in a system prompt, custom instructions, project rules, or a first message | Mechanism **documented** by every chat interface in general terms; the standalone file exists and builds cleanly; **not tested** in any host |
| Programmatic context injection | Your application's own instruction channel | **Documented** as a pattern in [docs/integration.md](docs/integration.md); **not tested**; no integration built |
| Browsing and other tools | The host must provide them; Nuansiq adds none | **Not provided**, and not tested. The skill tells an agent to say so rather than pretend |
| Persistent memory | The host must provide it; Nuansiq stores nothing | **Not used**, not designed for. Preferences apply to the current conversation only |
| Behavioural evaluation | A host session, a model, and a human scorer | **Not tested**. [Pilot](evals/pilot.md) and [cross-model plan](evals/cross-model-plan.md) are written and not run |

Copying files and validating a `SKILL.md` is not evidence of runtime compatibility. **No model is "supported"**: accepting instruction text is not support, and results will differ by model, host, version, and tool access. Nothing in this repository measures those differences yet.

## How preferences work

Nuansiq keeps three inputs separate: hard constraints, your stated preferences, and the agent's own judgement. When they conflict, it says which is which instead of quietly picking one.

- Stated preferences are used first, including ones that contradict the agent's default taste. The agent may name a cost once, concretely, then comply.
- Missing information is filled with a stated assumption unless the gap would change the shape of the result, in which case the agent asks.
- Nothing is stored by Nuansiq. If you explicitly ask for a preference to be remembered and the host can write files, the agent writes only what you stated to a file you name or approve, shows you the content, and deletes it on request.
- Inferred or sensitive traits (health, politics, religion, ethnicity, sexuality, finances) are never stored.
- In manual and injected modes there is no persistence at all unless you add it yourself.

Details and a preference-file template: [Part 2 of the standalone file](standalone/nuansiq-manual.md), or `skills/nuansiq/references/judgement.md`.

## When browsing, image tools, or memory are unavailable

The following is what the skill *instructs* an agent to do. It is not a record of observed behaviour; no host sessions have been run (see [capability matrix](#capability-matrix)).

- **No browsing:** the agent is told to say so, separate what it knows from what it assumes, and name what would change if the fact were checked. It must not produce a citation-shaped guess.
- **No image inspection:** the agent is told it may review an image *prompt* or a written brief, but must not claim to have looked at a generated image, a screenshot, or a design file.
- **No memory:** preferences apply to the current conversation only. Nothing is stored by the skill, and nothing is claimed about past sessions.
- **Hosts without file access:** no read, no write, no persistence; the skill is instructions only.

## Evaluating it

[`evals/`](evals/README.md) contains seven task briefs with task-specific criteria, covering a simple request that must not be overcomplicated, a creative task where audience matters, a task that needs research, a subjective task with several valid tastes, a conflict between a user's preference and the agent's recommendation, a missing-tool case, and a retrieved-content prompt-injection case.

The eval set is a protocol, not a result. No measured comparison is published in this repository, and none is claimed.

- [Pilot](evals/pilot.md): five cases, baseline versus Nuansiq, one host. **Not run**, because no skill-capable host, model credentials, or model API access were available here.
- [Cross-model plan](evals/cross-model-plan.md): at least two model families, instruction-only and tool-enabled cells kept separate, with recording fields for settings and tool access. **Not run** for the same reason.
- [Examples](examples/README.md): hand-written illustrations, authored without running an agent, and not evidence of improved output.

## Known limitations

- **Judgement, not verification.** Nuansiq cannot make an agent's facts correct. It changes how the agent handles uncertainty, not what it knows.
- **No cross-model evidence.** It is designed to be model-agnostic, but only text-level portability has been checked. Behaviour will vary by model, host, version, context window, and tool access; none of that is measured.
- **Activation is untested.** Descriptions can fail to match when they should, or match when they should not. The wording here is designed to reduce the second failure, but that design is unmeasured; direct invocation is the predictable route.
- **Taste is contested.** Where two directions are equally defensible, Nuansiq aims to make the choice explicit and reversible, not to settle it.
- **The manual fallback is a blunt instrument.** It loads all at once, cannot load appendices on demand, costs context on every request, and drifts from your copy unless you rebuild it.
- **No measured outcomes.** The eval briefs are small, and scoring them requires a human or a careful grader. Treat any future scores as indicative, not statistically meaningful.
- **Host behaviour varies.** Skill support, tool availability, and invocation syntax differ between products and versions.
- **No specialist safety.** Nothing here qualifies an agent to give medical, legal, or financial advice.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions that add unverifiable claims, invented compatibility, telemetry, or dependencies will be declined; the project is deliberately small. If you change anything under `skills/nuansiq/`, rebuild the standalone file and commit both.

## License

MIT. See [LICENSE](LICENSE). Copyright (c) 2026 NawzBlaze.

You may use, modify, and redistribute Nuansiq, including commercially, provided the copyright notice and permission notice are retained. The software is provided without warranty of any kind.

**Third-party material.** Apart from the standard MIT licence text, the repository contains no vendored code, no images or fonts, no passages copied from other projects, and no distributed dependencies; the skill text, references, examples, and eval briefs were written for this project. The `skills-ref` package and the GitHub Actions used by CI are development tools, not part of the distributed skill. The `fastyaml-lite` package in one eval fixture is invented, and the documentation links in [References](#references) are cited, not reproduced. No separate notices are required on that basis. If you believe something here is unaccounted for, open an issue and it will be corrected or removed.

## References

- Agent Skills specification: <https://agentskills.io/specification>
- Agent Skills documentation index: <https://agentskills.io/>
- Agent Skills quickstart (VS Code and GitHub Copilot paths): <https://agentskills.io/skill-creation/quickstart>
- Claude Code skills documentation: <https://code.claude.com/docs/en/skills>
- Codex skills documentation: <https://learn.chatgpt.com/docs/build-skills>

These links were checked in November 2026. Nuansiq is not affiliated with any of these projects, and naming a host here describes where its documentation places skills, not a partnership or a support claim.
