# Tiny Shared-Memory Garden 🧠🌱☕

## Why this exists

`C = Shared Context` represents accumulated routine context, so treating it like an ordinary daily variable makes it forget too quickly.

The design question is:

> **How can repeated context-bearing coordination accumulate without letting one quiet day erase the reservoir?**

This is the deeper lab for [`tutorial/06-shared-context-memory.md`](tutorial/06-shared-context-memory.md).

## The memory law

```math
C_{t+1}=C_t+\eta I_t(1-C_t)-\lambda C_t+w_t^C
```

where:

- `I_t` is bounded shared-context input from observable coordination actions;
- `η` (`eta`) is the accumulation rate;
- `λ` (`lambda`) is the slow decay rate;
- `(1 - C_t)` creates saturation instead of unbounded growth;
- `w_t^C` is dedicated memory noise.

## What feeds the reservoir? ☕🧺

The current structural prototype gives memory input to generic events such as:

```text
callback
notify
exception sync
closure
invite + opt-in
coffee delivered + acknowledged
```

These weights are **model assumptions**, not learned human constants.

```text
Observable action != intention
Memory input != emotional meaning
```

## Why `C` owns a separate path 🐣

`P / M / V / E / F` use ordinary soft-state dynamics.

`C` deliberately bypasses:

```text
ordinary target pull
generic mode drift
generic process noise
direct action drift
```

Actions feed `C` through `shared_context_input()` instead.

```text
P / M / V / E / F → ordinary soft-state dynamics
C                 → dedicated memory reservoir
```

This prevents two update mechanisms from competing over the same semantic state.

## Quiet is not forgetting 🌿

A quiet day can produce:

```text
I_t = 0
```

without implying:

```text
C_t = 0
```

So one quiet day applies only the reservoir's slow decay. A long disconnected period can reduce `C`, but accumulated context does not vanish overnight.

## Saturation matters ✨

Repeated context-bearing events can continue adding evidence, but `(1 - C_t)` makes each new addition smaller as the reservoir fills.

That keeps `C` bounded and makes “more history” different from unbounded accumulation.

## What memory means here

`C` does **not** measure either person's private memory.

It represents the model's accumulated evidence that the routine contains recurring shared context.

```text
Shared Context state != someone's private memory
Memory != mood
```

## Tiny inspection tool 🔍

```bash
python -m tiny_tools.inspect_memory
```

It grows one synthetic memory reservoir through three phases:

```text
🌱 build
☕ quiet
🍂 long pause
```

and writes:

```text
memory-story.csv
summary.csv
memory-story.png
```

## Tiny law 🌟

```text
No event today != no shared history
Memory != mood
```

Tiny memories deserve slower gravity. 🧠🌱🐾
