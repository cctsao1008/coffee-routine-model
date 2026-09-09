# 02 — Event != Meaning ☕➡️🧠

Once events repeat, people naturally develop shorthand.

A tiny synthetic exchange might be:

```text
Cheng: +1?
Linda: 要
☕
👍
```

The same four tokens can look obvious to a human reader. A model still needs to decide which parts are protocol semantics and which parts are interpretation.

## A protocol is a grammar, not a psychology engine

The useful abstraction is:

```text
raw token
   ↓
contextual protocol meaning
   ↓
generic event field
```

For example:

```text
+1?      → invite
要        → opt_in
☕        → routine_maintenance
👍 after ☕ → reaction
```

But `👍` by itself is ambiguous.

```text
after +1?  → it may function as opt-in
after ☕   → it may function as acknowledgment / reaction
alone      → it may remain unresolved
```

That is why `coffee_brain.protocol_adapter` uses sequence context instead of pretending every token has one universal meaning.

```text
Ambiguous clue != forced story
Missing clue != zero
```

## Persona vocabulary belongs at the edge

Readable examples can use names:

```text
cheng_invite
linda_choice
linda_reaction
```

But the mathematical core should receive:

```text
invite
opt_in
reaction
```

So the dependency direction stays:

```text
Cheng / Linda teaching story
        ↓
Persona Adapter
        ↓
Generic protocol semantics
        ↓
CSRDM Core
```

This gives the repository a story without making the model depend on a specific pair of people.

```text
Persona != core ontology
```

## Implementation detail != routine semantics

Another useful modeling lesson comes from harmless variation.

Imagine the same routine using:

```text
shop A today
shop B tomorrow
bean X next week
another pickup detail later
```

Those details may matter to a real implementation, but they do not automatically change the higher-level grammar:

```text
invite
→ opt-in / pass
→ delivery if applicable
→ acknowledgment / continuation
```

So we separate:

```text
implementation detail
        !=
shared routine semantics
```

This is ordinary software architecture too: keep volatile details near the boundary and stable semantics closer to the core.

## Why a protocol still is not enough

At this point we can parse events correctly.

But a protocol parser can only tell us what happened.

It still cannot answer questions like:

```text
Is the routine becoming easier to anticipate?
Are both sides still participating in different ways?
Can someone freely say pass?
Does accumulated shared context survive one quiet day?
```

Those questions require a state model.

Before we invent one, however, there is one especially important edge case to get right:

> **What should `pass` mean?**

Continue to [`03-pass-is-not-failure.md`](03-pass-is-not-failure.md).
