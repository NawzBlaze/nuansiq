# Cross-model evaluation plan

**Status: NOT RUN.** No model was available where this repository was prepared: no host or API credentials, and no route to model APIs. Every table below is a record to fill in, not a result.

## Question

Does the method change behaviour in the same *directions* across model families?

It is not a question about which model is better, and this plan cannot answer that.

## Design

Two model families, at minimum, chosen from what you have access to. Four cells per family:

| Cell | Instructions | Tools | What it isolates |
| --- | --- | --- | --- |
| A | none | none | baseline, instruction-only |
| B | Nuansiq text | none | instruction-only effect |
| C | none | tools the host provides | baseline, tool-enabled |
| D | Nuansiq text | same tools | tool-enabled effect |

Keeping instruction-only (A/B) separate from tool-enabled (C/D) matters: browsing can mask a fabrication failure, and a missing-tool case behaves differently when a tool exists.

## Tasks

Use the existing briefs verbatim so the criteria stay comparable. Do not reword them for different models.

| Case | Cell | Why |
| --- | --- | --- |
| [01 simple task](cases/01-simple-task.md) | A, B | Instructions must not add ceremony |
| [02 creative audience](cases/02-creative-audience.md) | A, B | Audience fit and specificity |
| [04 subjective taste](cases/04-subjective-taste.md) | A, B | Pluralism and stated preferences |
| [03 research](cases/03-research-required.md) | A, B, C, D | Currency, sourcing; tool-enabled comparison |
| [06 missing tool](cases/06-missing-tool.md) | B, D | Does it refuse to invent what it cannot see |

Where the case has an optional variant (04's preference, 06's no-vision setup), use the same variant across families and record which one.

## Conditions to hold and record

- **Instructions:** identical text in every family — the same build of [`standalone/nuansiq-manual.md`](../standalone/nuansiq-manual.md), Part 1 plus the matching appendix, with the digest recorded.
- **Settings:** temperature, top-p, reasoning or effort setting, max output length — whatever the access channel exposes. Record "not exposed" where it is hidden; do not guess.
- **Tool access:** list each tool and whether it was actually callable. A family with browsing and one without are different experiments, not a fair comparison.
- **Runs:** two per cell, fresh conversation each time, alternating order (A, B, B, A) to reduce warm-up effects.
- **Scorer:** a human, blind to condition where possible. Note where blinding was impossible.

## Recording fields

```markdown
Family: <e.g. family A>               Model id and version:
Access channel: API / chat UI / CLI   Host or product:
Settings: <temperature, effort, max tokens, or "not exposed">
Tools callable: <list, or none>       Case: <01/02/03/04/06>   Cell: A/B/C/D
Instruction digest: sha256:<...>      Run: 1 or 2        Date:
Prompt: <verbatim>                    Output: <full transcript, incl. tool calls or refusals>
Scores: <per rubric.md and the case's own anchors>
Scorer: <initials> (blind: y/n)       Notes:
```

## What to look for

Recurring failure modes across families are more informative than scores:

- ceremony or clarifying questions on the simple task (a regression introduced by the instructions);
- the stated preference in case 04 overridden or diluted toward a default aesthetic;
- confident dates or citations in case 03 when no tools exist;
- invented visual detail in case 06 when no image input exists;
- length growth without new checkable claims.

## Analysis rules

- Report per-cell observations. Do not average across families into a single score.
- Do not rank families. Different refusal policies, context windows, tool schemas, and tokenizers make scores non-comparable; a difference may be the harness, not the model.
- With two runs per cell, nothing here is statistically meaningful. Write "in these runs" and stop there.
- Report regressions with the same prominence as improvements, and keep the outputs.
- Self-scoring by the person who wrote the skill is not independent evidence. Say who scored and whether they could see the condition.

## Results

Nothing to report. All cells are empty.

| Family | Model id | Cell A | Cell B | Cell C | Cell D |
| --- | --- | --- | --- | --- | --- |
| — | not run | not run | not run | not run | not run |

## Prerequisites when access exists

- Two model families reachable through an interface that lets you set instructions before the first user turn.
- The ability to disable tools deliberately, and to confirm whether a tool was called.
- A place to store full transcripts, including refusals and tool calls.
- About 40 runs for the table above (5 cases × 4 cells × 2 runs), which is a few hours of scoring.

Until that exists, the repository claims no cross-model behaviour and no model is listed as supported.
