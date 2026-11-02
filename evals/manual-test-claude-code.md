# Manual test guide: Claude Code

A short procedure for one host, covering four different questions that are easy to blur together:

1. Is it **installed** (files where the host looks)?
2. Does **explicit activation** work (`/nuansiq`)?
3. Does **automatic activation** work (a matching request with no slash)?
4. Does it **improve the result** on a task?

Only the first has been checked in this repository. Steps 2–4 have not been run by anyone here, so this guide describes what to do and what to record, not what you will see.

Host documentation used: <https://code.claude.com/docs/en/skills>. That page documents personal skills at `~/.claude/skills/<skill-name>/SKILL.md`, project skills at `.claude/skills/<skill-name>/SKILL.md`, the `/skill-name` invocation, and automatic use based on the `description`. It does not promise a specific on-screen indicator that a skill was loaded, so this guide does not ask you to trust one.

## What you need

- Claude Code installed and working in a terminal. It is not assumed to be present. If you are unsure, run `claude doctor`, which reports installation health without starting a session.
- A shell with `git`.
- A project directory you can run Claude Code in.
- No API keys or tokens for this guide. Do not paste credentials into a session, a prompt, or an issue to test Nuansiq. If a step asks you for one, stop and report it as a bug.

## Step 1 — Installation

```bash
git clone --branch arena/05108cd1-nuansiq https://github.com/NawzBlaze/nuansiq.git
cd nuansiq
mkdir -p ~/.claude/skills
cp -R skills/nuansiq ~/.claude/skills/
find ~/.claude/skills/nuansiq -type f
```

Expected: four files, `SKILL.md` and three files in `references/`. If `find` shows fewer, the copy or checkout is incomplete; see Troubleshooting.

Optional format check (not a host check):

```bash
python3 -m venv .venv
.venv/bin/pip install skills-ref
.venv/bin/agentskills validate ~/.claude/skills/nuansiq
```

**Record:** did all four files appear? Did validation pass?

## Step 2 — Explicit activation

Start a session in any project:

```bash
cd /path/to/your/project
claude
```

Then type the command and a real request:

```text
/nuansiq review this paragraph for a skeptical CFO: "Our platform leverages cutting-edge synergies to unlock unprecedented value."
```

Distinguish three outcomes:

- **Command not recognised.** Installation or discovery problem, not a judgement about the skill. Try a new session, then re-check the folder name is exactly `nuansiq` and contains `SKILL.md`.
- **Command recognised, generic answer.** Activation worked; the output did not show the method. Record what was generic.
- **Command recognised, specific answer.** Note what it did that a plain request would not have: an audience observation, a rewritten draft, a named criterion.

**Record:** command resolved? (yes / no) — what the response did — verbatim output.

## Step 3 — Automatic activation

This tests the `description`, which is the only part the host sees before loading anything.

1. Start a **fresh session**, with the skill still installed.
2. Send a matching request with no slash command:

```text
Rewrite the intro of our onboarding email for new warehouse staff. It currently reads like a press release.
```

3. Then remove the skill (`rm -rf ~/.claude/skills/nuansiq`), start another fresh session, and send the identical message.

There is no documented indicator to read, so judge by difference: if the installed run behaves like the uninstalled one, treat automatic activation as **unconfirmed** regardless of what the transcript implies. Record the two outputs side by side.

**Record:** installed / not installed outputs; your call (activated / not activated / cannot tell) and the evidence.

## Step 4 — Whether it improves the result

Installing and activating are not the same as helping. Use the eval briefs so the judgement is not improvised:

1. Pick two cases: [01-simple-task](cases/01-simple-task.md) and [02-creative-audience](cases/02-creative-audience.md).
2. For each: fresh session, literal brief, once **with** the skill and once **without** it. Same model, same settings, same tools.
3. Change the order on the second case (with, then without) so warm-up does not favour one condition.
4. Strip the labels, then score with [rubric.md](rubric.md) plus the case's own criteria.

Two runs per condition is exploratory. It can show you a failure mode; it cannot show that Nuansiq "improves quality" in general. Do not average the scores into a single number or compare across models.

**Record:** the fields in [pilot.md](pilot.md#recording-fields), especially anything worse in the with-skill run — case 1 gaining headings or a clarifying question is a regression worth reporting.

## Record sheet

```markdown
Host: Claude Code <version from `claude doctor`>      Date:
Model (as shown by the host):                         Settings:
Skill commit: <git rev-parse HEAD>                    Invocation: explicit / automatic
Tools available: browsing=<y/n> files=<y/n> images=<y/n>

Step 1 installed: <y/n>  files=<count>  validate=<pass/fail>
Step 2 explicit: command resolved=<y/n>  output notes:
Step 3 automatic: call=<activated/not/cannot tell>  evidence:
Step 4 comparison: case 01 <A/B scores>  case 02 <A/B scores>  regressions:
```

## Troubleshooting

- **`/nuansiq` not found:** confirm `~/.claude/skills/nuansiq/SKILL.md` exists, the folder is not nested twice (`.../nuansiq/nuansiq/SKILL.md`), and start a new session.
- **Skill seems stale after an update:** re-copy the whole folder; a half-updated `references/` will disagree with `SKILL.md`.
- **Everything looks fine but answers are unchanged:** that is a real finding, not a failure of the test. Record it; the description or the instructions may need work.
- **You pasted a secret while testing:** rotate it. Do not include it in an issue.

## Limits of this guide

It is written from the host's documentation, not from a session run in this repository. Command names, skill discovery, and indicator behaviour can change between versions, so record the version you used. The guide also cannot tell you whether the skill is good, only whether it loaded and what changed in two tasks.
