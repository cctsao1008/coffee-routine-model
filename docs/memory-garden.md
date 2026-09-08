# Tiny Shared-Memory Garden 🧠🌱☕

`C = Shared Context` is not a daily mood score anymore.

It now behaves like accumulated history with slower gravity:

```text
C[t+1] = C[t]
       + eta * I[t] * (1 - C[t])
       - lambda * C[t]
       + tiny process noise
```

where:

- `I[t]` is bounded shared-context input from observable coordination actions
- `eta` is the accumulation rate
- `lambda` is the slow decay rate
- `(1 - C[t])` creates saturation instead of infinite memory growth

## What feeds the tiny reservoir? ☕🧺

The current structural prototype gives memory input to generic things such as:

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
Observable action != intention.
Memory input != emotional meaning.
```

## What changed from the old C? 🐣

Previously, `C` lived inside the same generic state update as the other soft states:

```text
mean reversion
+ mode effect
+ action drift
+ daily process noise
```

That made Shared Context too easy to wiggle like a daily variable.

Now:

```text
P / M / V / E / F  -> ordinary soft-state dynamics
C                  -> dedicated memory reservoir
```

The direct `C` column in `ACTION_EFFECTS` is intentionally zero. Actions feed `C` through `shared_context_input()` instead.

## Quiet is not forgetting 🌿

A quiet day produces:

```text
I[t] = 0
```

not:

```text
C[t] = 0
```

So one quiet day only applies slow decay.
A long disconnected period can reduce `C`, but the shared history does not vanish overnight.

## Saturation matters ✨

Repeated callbacks and familiar coordination can keep building context, but `(1 - C[t])` makes new additions smaller as the reservoir gets fuller.

That prevents:

```text
shared context = 1.8 coffees XD
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
No event today != no shared history.
Memory != mood.
```

Tiny memories deserve slower gravity. 🧠🌱🐾
