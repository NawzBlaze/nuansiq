# Contributing to Nuansiq

Nuansiq is deliberately small. The useful contribution is usually a sharper instruction, a better eval case, or an example of the method failing, not more material.

## Before you start

- Read [`skills/nuansiq/SKILL.md`](skills/nuansiq/SKILL.md). It is the working surface; everything else supports it.
- Read the [Agent Skills specification](https://agentskills.io/specification) if you are changing frontmatter or structure.
- Open an issue for anything that changes the method's behaviour, so the reasoning is recorded before the diff.

## What is welcome

- **Eval cases** that expose a failure mode the current set misses, with the criteria and the failure written down.
- **Examples** that show a real, specific choice being made, including ones where the right answer was restraint.
- **Instruction fixes**: places where the skill is vague, contradictory, too long, or activates on the wrong requests.
- **Host reports**: "I installed it in X on date Y, it loaded/ did not load." Evidence about real hosts is more useful than speculation.
- **Cuts.** Removing a paragraph that does not change behaviour is a good pull request.

## What will be declined

- Marketing language, claims about "real feelings", or guarantees of quality.
- Benchmarks, scores, testimonials, or star counts that cannot be reproduced.
- Installation commands or integrations that have not been verified against the host's own documentation.
- Telemetry, analytics, network calls, dependencies, backends, dashboards, or installers.
- A second skill that overlaps with `nuansiq` without a clear reason to be separate.

## Editorial standards

1. **Concrete over abstract.** "Name the cost once, with a consequence" beats "be thoughtful about preferences".
2. **No instruction that only says "avoid AI slop".** Name the observable symptom and the replacement behaviour.
3. **No invented facts.** Prices, dates, product features, and compatibility claims need a source or must be removed.
4. **Keep `SKILL.md` under 500 lines** and lean. Move detail into `references/` and tell the agent when to read it. If a paragraph would not change what an agent does, cut it.
5. **No em dash bans and no typo injection.** Nuansiq does not teach agents to fake human imperfection.
6. **Uncertainty is stated, not performed.** Do not add hedges to everything.

## Local checks

Run the repository self-check before opening a pull request. It uses only the Python standard library:

```bash
python3 scripts/validate.py
```

It verifies skill frontmatter against the specification (required fields, name rules including directory match, description length, allowed keys), that relative links and referenced files exist, that no unfilled template text remains, that the core body stays within size budgets, and that no invented package-manager install command has crept into the documentation.

For the authoritative frontmatter check, install the reference library and run it against the skill directory:

```bash
python3 -m venv .venv
.venv/bin/pip install skills-ref
.venv/bin/agentskills validate skills/nuansiq
```

The PyPI package is named `skills-ref`; the command it installs is `agentskills`. The specification site refers to it as `skills-ref validate`; use whichever binary your install provides.

## Changing an eval case

Each case in [`evals/`](evals/README.md) is a brief plus criteria, not a golden output. When you add or change one:

- keep the brief copy-pasteable, with the available tools stated;
- give three to five task-specific criteria with observable anchors;
- write down at least two failure modes you expect;
- do not include a model's answer as "the correct answer". Record real runs separately, with model, host, date, and skill version, and label them as observations from one run.

## Pull request checklist

- [ ] `python3 scripts/validate.py` passes.
- [ ] `agentskills validate skills/nuansiq` passes (if you touched frontmatter).
- [ ] `SKILL.md` still answers the question "what would an agent get wrong without this?" for every paragraph.
- [ ] Any new link, path, or command was actually opened or run.
- [ ] No new dependency, network call, or storage.
- [ ] Behaviour changes are described in the pull request body, including what you tested manually.

## Licensing

There is currently no `LICENSE` file, so contributions have no settled terms. The maintainer should resolve this before accepting substantial contributions.

A recommendation for the owner, not yet applied: **MIT** if the goal is maximum adoption and minimal friction, or **Apache-2.0** if a patent grant and explicit contribution terms matter more than brevity. Both are compatible with the rest of this project's design, which has no dependencies and no runtime. Do not add a license file in a pull request unless the owner has stated a decision in an issue.
