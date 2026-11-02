# Evaluation set

Seven task briefs for checking whether Nuansiq changes behaviour in the ways it claims to. Each case pairs a copy-pasteable brief with task-specific criteria and expected failure modes.

This directory is a **protocol, not a result**. No measured comparison is published in this repository, and none is claimed.

The companion [pilot procedure](pilot.md) selects five of these cases for a baseline-versus-Nuansiq comparison and records what to capture. The [cross-model plan](cross-model-plan.md) extends the same briefs to at least two model families, keeping instruction-only and tool-enabled runs separate. Its status is **not run**: no skill-capable host, model credentials, or model API access were available where this repository was prepared.

## Why these seven

| Case | What it tests | Why it is here |
| --- | --- | --- |
| [01 simple task](cases/01-simple-task.md) | Restraint | Nuansiq must *not* run a workflow for a question with one short answer |
| [02 creative, audience](cases/02-creative-audience.md) | Audience fit and specificity | The most common failure: fluent copy that could serve anyone |
| [03 research required](cases/03-research-required.md) | Evidence and currency | Facts that change over time, and a correct answer that depends on checking |
| [04 subjective taste](cases/04-subjective-taste.md) | Pluralism | Several directions are defensible; the agent must not crown one as universal |
| [05 preference conflict](cases/05-preference-conflict.md) | Preference handling | The user's taste contradicts the agent's default recommendation |
| [06 missing tool](cases/06-missing-tool.md) | Honesty | The task assumes an image the agent cannot see |
| [07 untrusted content](cases/07-untrusted-content.md) | Injection resistance | Retrieved text contains instructions aimed at the agent |

Together they cover the behaviours the project is built around and the three ways it is most likely to fail: ceremony on small tasks, generic output, and invented capability.

## How to run a case

1. Use a host agent that supports Agent Skills, and install Nuansiq using the instructions in the [README](../README.md#installation). Record the host, version, model, and date.
2. Start a fresh session with no earlier context from this repository.
3. Paste the **brief** exactly. Include the stated tools in the setup section either by using a host that has them or by stating in the prompt which tools exist. Do not mention the eval, the criteria, or Nuansiq unless the case says to.
4. Save the full response, including any tool calls the agent attempted.
5. Run the same brief in a session **without** the skill installed, if you want a comparison. Keep both outputs.
6. Score with [rubric.md](rubric.md). Score blind to condition where you can: strip the labels before judging.

Repeat each case at least twice per condition before drawing any conclusion, and note that two runs per condition is still far too few for a statistical claim.

## What counts as evidence

Good evidence: the recorded prompt, the full model output, the host and model identifiers, the date, the skill version, and a completed scorecard. A short note on what the skill changed (or did not) is more useful than a score alone.

Not evidence: a summary of what "felt better", a cherry-picked single output, or a claim that the skill "improves quality by 30%". Scores from a handful of runs are indicative at best, and a different model may behave differently.

## Recording a run

```markdown
Case: 03-research-required
Host: <product and version>       Model: <model identifier>
Date: <YYYY-MM-DD>                Skill installed: yes/no
Tools available: <browsing? files? images?>
Output: <link or pasted transcript>

Scores (see rubric): correctness 2, relevance 2, specificity 2,
honest uncertainty 2, no unnecessary complexity 2. Total 10 / 10.
Notes: cited the official support table and named the end-of-support date;
      correctly refused to state a date it could not confirm in the second run.
```

## Testing activation separately

The cases above assume the skill loaded. Whether it loads at all is decided by the `description`, which is the only part a host sees at startup. Test that separately, in a fresh session per prompt, and record whether the skill activated and why you think it did or did not.

Prompts that should activate it:

- "Rewrite this onboarding email for new warehouse staff; it currently reads like a press release."
- "Give me two art directions for this poster, and tell me which you'd pick."
- "Is this advice right for a five-person team with no ops budget?"
- "Review my landing page copy before I send it to the client."
- "Help me brief an illustrator for a magazine cover about drought."

Prompts that should not:

- "Convert this JSON to CSV." 
- "What's the capital of Mongolia?"
- "Add a docstring to this function."

False positives (activating on mechanical work) are the more damaging failure, because they add ceremony to tasks that need none. If you see one, the description's exclusion sentence is the place to fix it, not the body.

## Known weaknesses of this set

- Seven cases cannot cover the space; they catch specific, known failures.
- Scoring is human judgement, so scores move between raters. Use the anchors and record disagreements rather than averaging them away.
- Prompts are written by the project author, who knows what the skill is supposed to do. That invites teaching to the test.
- Some cases (03 especially) depend on facts that change; the criteria check the process of verifying, not a frozen answer.
- Nothing here tests long sessions, multi-turn revisions, or non-English output.
