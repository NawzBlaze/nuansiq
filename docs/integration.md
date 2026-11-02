# Supplying Nuansiq as model context (developer integration)

For applications that call a model directly and have no skill runtime: you add Nuansiq's text to the instructions your app already sends.

## What this is not

- Not an API, SDK, package, hosted service, or endpoint. There is nothing to install from a registry, no library version to pin, no account, and no key.
- Not a repository reference that does anything by itself. A GitHub URL in a config file injects nothing; your application must read the text and send it.
- Not a server component. This repository has no runtime and makes no network calls.

The mechanism is the one your provider already documents for instructions that outrank per-turn user text. Providers call it different things and shape it differently; this guide deliberately does not name a universal field, endpoint, or parameter.

## Where the text goes

Put it in the highest-priority instruction channel your provider offers for application-level guidance — commonly a system or developer message, a project instruction file, or a custom-instructions setting. Do not put it in a user turn: user turns are lower priority, look like user intent, and can be overridden by the next turn.

Keep three blocks separate so they can be versioned and updated independently:

1. **Nuansiq instructions** — the generated file, unmodified.
2. **Product rules** — your own constraints: format, tone of your brand, refusal policy, what the product is.
3. **Per-user preferences** — from your own store, with user consent and controls.

## Provider-neutral pseudocode

The calls below are pseudocode. They are not a real SDK, and no provider example is included because none was verified for this repository.

```pseudo
# Build or deploy step: ship the text with your app.
instructions = read_text("standalone/nuansiq-manual.md")
# Use only "Part 1" instead if your context budget is tight; see below.

# Per request: compose, then call whatever your provider offers.
system_prompt = join([
    instructions,                 # Nuansiq, unmodified and versioned by digest
    product_rules,                # your own constraints
    user_preferences              # from your store, with consent
], separator="\n\n")

response = llm.generate(
    system=system_prompt,
    messages=conversation_turns,  # user and assistant turns
    tools=available_tools,        # omit entirely if your app exposes none
    max_output_tokens=budget
)
```

Rules that survive any provider rename:

- **Do not merge** the three blocks into one blob; you will need to change them at different speeds.
- **Do not rewrite** the Nuansiq text. Edit the source and use `python3 scripts/build_standalone.py`.
- **Do not imply tools.** If your app exposes no browsing, file, or image access, the text tells the model not to claim it. Do not add tool descriptions you do not implement.

## Versioning and cost

- The generated file's HTML header carries a `Source digest: sha256:…`. Store that digest with your prompt configuration and log it with each request or release, so you can tell which instruction version produced an output.
- Size: about 1,700 tokens for Part 1, about 6,600 for all four parts (four characters per token, estimated by the build script). Measure with your provider's tokenizer before shipping; estimates drift by model.
- If your provider caches prompt prefixes, changing the instructions invalidates the cache. Prefer deliberate, versioned updates over per-request assembly.
- Trimming to Part 1 is a real trade: you lose the detailed judgement, research, and critique appendices. Say which variant you ship in your own release notes.

## Checking that it took effect

1. Send one fixed probe prompt **without** the instructions and one **with** them. A useful probe is a mechanical task, where the correct behaviour is a short direct answer: the instructions should not add a workflow.
2. Compare structure, not length: did the instructed run ask a clarifying question where none was needed, add headings, or restate the prompt? Those are regressions.
3. For a judgement probe, use a brief from [`evals/`](../evals/README.md) with its criteria, and keep both outputs.
4. Keep the digest, the prompt, and both outputs with the result. "It looked better" is not a record.

There is no measured integration in this repository, and installing text is not evidence that it improved anything.

## Multitenancy, privacy, and safety

- Per-user preferences belong in your own store, injected as a separate block, inspectable and deletable by the user. Never infer or store sensitive traits; the skill's own rules say the same.
- Your application's safety policy and your provider's policy still apply. Nuansiq's text explicitly defers to them and does not grant capabilities.
- Never place credentials, tokens, or customer data in the instruction block.
- Treat user-supplied and retrieved content as untrusted. The instructions tell the model to treat retrieved text as data, but your app should also fence or quarantine that content before it reaches the model. See the prompt-injection section of the skill, or Part 3 of the standalone file.

## What remains unverified

- No provider-specific example is given because no provider integration was verified here.
- No integration was built, run, or benchmarked. If you build one, record what you tested, with the prompt digest and model identifiers, and consider adding it to the capability matrix in the [README](../README.md#capability-matrix).
