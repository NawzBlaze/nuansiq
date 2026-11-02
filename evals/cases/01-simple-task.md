# Case 01: a simple task that must stay simple

Tests restraint. This case fails when the agent applies ceremony to a question that needs three sentences.

## Brief

> What is the difference between `git fetch` and `git pull`? I just want to know which one to use before I rebase.

## Setup

- No tools required.
- Do not mention Nuansiq; let the description match or not match as it will.

## What a good run looks like

A short answer, roughly: `git fetch` downloads remote changes without touching your branch; `git pull` is fetch plus an integration step (merge or rebase, depending on config). For someone about to rebase deliberately, `git fetch` then an explicit rebase is the predictable choice, because `git pull` may merge or rebase according to configuration the user may not have checked.

Length: a few sentences, no headings, no bullets required, no workflow narration, no question back.

## Criteria

### Correctness

- **2** — Both commands described accurately, including that `pull` integrates and that the integration strategy is configurable.
- **1** — Correct but incomplete on the configuration point.
- **0** — Confuses the commands or states something false.

### Restraint (does not overcomplicate)

- **2** — Answer arrives in the first sentence, stays under ~120 words, no headings, no lists of "factors to consider", no follow-up question, no offer to explain more.
- **1** — Correct but padded: a heading, a bulleted comparison, or a closing "let me know if you'd like me to explain rebasing in detail".
- **0** — Produces a multi-section explainer, a decision framework, or interrogates the user about their workflow before answering.

### Direct usefulness

- **2** — Tells the user which to use in their stated situation.
- **1** — Explains the difference but leaves the recommendation to the user.
- **0** — Answers a general question about Git without addressing "before I rebase".

## Expected failure modes

- A "Understanding git fetch vs git pull" heading with a comparison table for a two-line question.
- Asking "what's your team's workflow?" before answering anything.
- Sounding uncertain about stable mechanics. Uncertainty belongs to changeable facts, not to how these commands work.
- Volunteering a rebase tutorial nobody asked for.

## Notes

This is the case that catches the most likely cost of installing Nuansiq: a judgement method that turns every question into a brief. A good run here is evidence that restraint instructions landed; a bad run is a reason to tighten them.
