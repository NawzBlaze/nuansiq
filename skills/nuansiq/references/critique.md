# Critique

Review that ends in a decision about what to change, not a mood about the work.

## 1. Review in proportion to the stakes

| Stakes | Reasonable depth |
| --- | --- |
| A sentence in a chat reply | One reread for correctness and fit |
| A short draft the user will send | Checklist against the brief, one revision pass |
| Anything public, legal, financial, or medical | Full check, explicit uncertainty, human review recommended |
| Code or configuration | Correctness and failure modes before style |

Review order, always: task success, then correctness, then fit to audience and constraints, then specificity and clarity, then polish. Polishing a paragraph whose claim is unsupported is wasted work.

## 2. Diagnose concretely

Turn a vague impression into a symptom, a cause, and a fix. "This feels like AI" is not actionable; the traits behind it are.

| Symptom you can point at | Usual cause | Fix |
| --- | --- | --- |
| Every paragraph is the same length and shape | Rhythm never varies | Merge two short ones, split the longest, cut one entirely |
| Confidence with no evidence | Claims asserted, not shown | Add the measurement, name the source, or soften to what you know |
| "It's not just a tool, it's a partner" | Symmetric antithesis used as decoration | Say the concrete thing, or cut the sentence |
| The answer restates the prompt | Filling space before committing | Delete the restatement; lead with the claim |
| Adjectives doing the work ("robust, seamless, powerful") | No specific detail available | Replace with a number, a name, a mechanism, or remove |
| Lists where reasoning was needed | Format chosen before thinking | Write the argument in prose, then list only if enumerable |
| Decoration with no load (icons, dividers, flourish sentences) | Effort aimed at perceived completeness | Remove; spend the effort on one substantive moment |
| Advice that ignores the user's real constraint | Template applied without the brief | Re-read the constraint, name it, change the recommendation |

The specific defects worth naming in any kind of work:

- **Contradictory requirements** (a 60-word summary that must cover 12 pages; a calm dashboard of live alerts).
- **Irrelevant detail**: true, interesting to the writer, useless to the reader.
- **Unsupported claims**: statistics, superlatives, and compatibility statements with nothing behind them.
- **Generic imagery**: stock compositions unrelated to the brief, prompts with no subject or light, illustrations that could illustrate anything.
- **Dialogue that explains rather than reveals**: characters narrating their own subtext.
- **Inaccessible choices**: contrast below 4.5:1 for body text, motion with no reduced-motion path, text baked into images, no focus state, caption-less video, tables used for layout.
- **Excessive effects**: several simultaneous animations, drop shadows under every element, transitions that delay the task.
- **Advice that ignores practical constraints**: a recommendation requiring a team the user does not have, a budget they mentioned excluding, or a migration with no rollback.

## 3. Build a rubric from the brief

Write three to five criteria specific to this task, then check each one. Criteria you cannot check (how an audience will actually react, whether a generated image looks right when you cannot see it) should be named as unchecked rather than scored.

Example for a product page rewrite: does a first-time visitor know what it is in the first line; is the primary action unambiguous; is every claim supportable; does it address the objection the brief names; does it hold at 320 px wide.

## 4. Revise deliberately

- Revise when you can name the expected improvement. If you cannot say what gets better and how you would notice, leave it alone.
- Keep what already works. A revision that replaces a good paragraph with a merely different one is a regression.
- Two passes is the normal ceiling. A third pass happens only when a check surfaced a new concrete defect, not because the draft could still be different.
- Watch for regressions the fix introduces: tightening prose can drop a needed qualifier; simplifying a layout can remove a hidden accessibility affordance.
- Do not smooth away choices that were deliberate, including the user's. If you disagree with a stated preference, the place for that is one sentence of named cost, not a silent revision.
- Log what changed and why, briefly, when the user will read the diff.

## 5. The limits of self-review

What self-review genuinely catches: missed requirements, internal contradictions, unsupported claims, over-length, tone that contradicts a stated preference, broken links and names, missing accessibility basics.

What it cannot establish: whether the work is actually good, how it will land with a real audience, whether a fact is true without a source, which of two valid aesthetics is better, whether generated images look right without the ability to see them.

So never write "I reviewed it, so it's ready." Write what you checked and what remains open. Review reduces the chance of specific errors; it does not certify quality.

## 6. Reviewing someone else's work

- Ask what the work is for if it is not stated, or state the assumption you are reviewing against.
- Lead with the issue that most affects the outcome, not with the first thing you noticed.
- Separate defect from preference explicitly: "This caption is inaccurate" and "I would have chosen a warmer register" are different claims.
- When it is a taste call, say so and give the criterion behind your preference; do not convert preference into a standard.
- Respect constraints you do not know about. Before rewriting, check whether the awkward phrasing is a legal requirement or the odd layout is a legacy platform.
- Offer the smallest change that fixes the problem. If a rewrite is warranted, say what it preserves.

## 7. Handoff

When the work is going back to the user, include only what helps them act:

- what you changed and the reason, in one line each;
- what you chose not to change, if they might expect it;
- what is still uncertain or unchecked;
- the criteria you used, if they might want to argue with them.
