# Behavioural pilot (five cases)

**Status: NOT RUN.** No result from this procedure exists, and none is claimed.

## Why it was not run

The repository was prepared in a sandboxed environment with:

- no skill-capable host installed (`claude`, `codex`, `gemini`, `copilot`, and `cursor` were all absent from `PATH`);
- no model credentials of any kind;
- no network route to model APIs (`api.anthropic.com` and `api.openai.com` were unreachable);
- therefore no model that could produce an output, with or without the skill installed.

Writing outputs by hand and calling them a pilot would be fabrication. The procedure below is what an owner or contributor with a real host should run.

## What the pilot can and cannot show

It is **exploratory**. Two runs per condition, one host, one model, and criteria scored by the person who wrote the skill: that is enough to notice a failure mode and not enough to claim general improvement. Report it as "what changed in these ten runs", never as "Nuansiq improves quality".

Self-scoring is not independent evidence. Where possible, have a second person score blind to condition, and report disagreements rather than averaging them.

## Prerequisites

- A host that discovers skills from a documented path (Claude Code, Codex, or VS Code Copilot), installed and working.
- One model, held constant across both conditions, with its settings recorded if the host exposes them (temperature, reasoning effort, tool policy).
- Web or search access for case 4; a host without image input for case 5.
- A clean way to toggle the skill: install it for condition B, remove it for condition A. Do not leave a second copy in another skills directory.
- The skill content pinned to a commit (`git rev-parse HEAD`) and recorded.

## The five cases

Identical prompts in both conditions. Prompts are copied from the case files, with one deliberate addition in case 3 (a stated preference, which is the point of that case).

| # | Case file | What it probes |
| --- | --- | --- |
| 1 | [cases/01-simple-task.md](cases/01-simple-task.md) | Stays simple; no ceremony |
| 2 | [cases/02-creative-audience.md](cases/02-creative-audience.md) | Writes for a stated audience |
| 3 | [cases/04-subjective-taste.md](cases/04-subjective-taste.md) | Handles explicit preferences and plural taste |
| 4 | [cases/03-research-required.md](cases/03-research-required.md) | Verifies changeable facts; states uncertainty |
| 5 | [cases/06-missing-tool.md](cases/06-missing-tool.md) | Refuses to invent what it cannot see |

### Exact prompts

**1. Simple task**

```text
What is the difference between `git fetch` and `git pull`? I just want to know which one to use before I rebase.
```

**2. Writing with an audience**

```text
Write a 90-word audio-guide stop for a 12th-century stone sculpture of a dancing Shiva in our city museum. Visitors are general, including families with children around 8–10. The tone should be curious and plain, not academic and not condescending. We cannot confirm the sculptor or the original temple, so do not state either.
```

**3. Subjective, with explicit user preferences**

```text
We are opening a small specialty coffee bar in a 1930s building with a lot of original tile. Give me two or three art-direction directions for the interior. We have ~₹6 lakh for everything except equipment, and the lease is three years. We want to be a neighbourhood place, not an Instagram destination. I personally dislike anything that looks like a Scandinavian café, and I want the original tile kept visible rather than covered.
```

**4. Research**

```text
We are starting a Django project this month. Which Python versions does the current Django LTS support, and when does that LTS stop receiving security fixes? I need to know whether we can stay on Python 3.10.
```

**5. Missing tool** (attachment required; see the case file for the no-vision setup)

```text
Attached is a screenshot of our checkout button. Is the contrast good enough, and does it look clickable? Tell me what to change.
```

## Procedure

1. Record host, version, model, settings, date, skill commit, and tool availability.
2. For each case, start a **fresh session**. Do not carry context between cases.
3. Run condition A (skill removed) with the exact prompt. Save the full transcript, including any tool calls attempted.
4. Run condition B (skill installed). For behaviour testing, invoke it explicitly (`/nuansiq` or `$nuansiq`) so a failed description match does not masquerade as a behavioural result. Run one additional implicit-activation variant of case 2 and record whether the skill loaded.
5. Repeat each condition twice, alternating order (A, B, B, A) to reduce warm-up and drift.
6. Strip condition labels, then score with [rubric.md](rubric.md) plus the case's own criteria.

## Recording fields

```markdown
Case: <1-5>                          Condition: A (no skill) / B (Nuansiq)
Host and version:                    Model:
Settings (if exposed):               Date:
Skill commit:                        Invocation: explicit / implicit
Tools available: browsing=<y/n> files=<y/n> images=<y/n>
Prompt: <verbatim>
Output: <full transcript, including tool calls and refusals>
Scores: correctness / relevance / preference fit / complexity / uncertainty / specificity
Case-specific scores:                Scored by: <initials> (blind: y/n)
Notes and failures:
```

## Results

No rows. Nothing has been run.

| Case | Condition A | Condition B | Observation |
| --- | --- | --- | --- |
| 1 simple | not run | not run | — |
| 2 audience | not run | not run | — |
| 3 preferences | not run | not run | — |
| 4 research | not run | not run | — |
| 5 missing tool | not run | not run | — |

## Regressions worth watching for

The pilot should record these specifically, because they are the likely costs of the skill:

- case 1 gaining structure, headings, or a clarifying question it did not need;
- case 3 overriding or diluting the stated preference in the name of better taste;
- case 5 inventing visual detail, or refusing so completely that the user gets no usable next step;
- case 4 producing more confident dates when no tools exist than when they do;
- any output that grows in length without adding a checkable claim.
