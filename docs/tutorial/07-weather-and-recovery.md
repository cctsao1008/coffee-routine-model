# 07 — Busy, Leave, Special, and Coming Back 🌦️🌱

A continuous state vector is useful, but some days differ in kind, not only in degree.

Synthetic examples:

```text
ordinary day
busy day
leave / pause
special day
ordinary return after interruption
```

Trying to explain all of those by moving only `P / M / V / C / E / F` can blur an important distinction.

## The modeling problem

A temporary interruption is not necessarily a structural change.

Likewise, a special day should not automatically redefine the long-run baseline.

So CSRDM adds a discrete routine mode:

```text
☕ Normal
🌧️ Busy
🏖️ Leave
🎂 Special
🌱 Recovery
```

The continuous state and discrete mode answer different questions:

```text
x[t]  → what soft routine properties are plausible?
m[t]  → what kind of local operating condition is plausible?
```

## Disturbance != rupture

A small sequence can be:

```text
Normal → Busy → Leave → Leave → Recovery → Normal
```

The important modeling rule is:

```text
Disturbance != rupture
```

A Leave mode means the current routine context is different. It does not automatically mean the routine has failed or that the generating process has permanently changed.

## Mode != regime

Another distinction matters:

```text
Mode   = local operating condition
Regime = more persistent change in the data-generating process
```

One unusual day is not enough to declare a new regime.

```text
Mode != regime
Anomaly != change point
```

The change-point detector exists precisely because persistent shifts require different evidence from temporary mode changes. See [`../change-point-garden.md`](../change-point-garden.md).

## Recovery deserves its own language

Suppose a pause ends and ordinary coordination returns without extraordinary repair.

That is a useful observable pattern:

```text
interruption
    ↓
resume
    ↓
return toward the nominal routine set
```

CSRDM therefore measures recovery instead of hiding everything inside one generic “good / bad” score.

A simple resilience summary uses recovery time and repair cost:

```math
R_{resilience}=\frac{1}{1+T_r+\lambda C_r}
```

The exact metric is secondary to the idea:

> **How a routine returns can be more informative than whether an interruption occurred at all.**

See [`../recovery-garden.md`](../recovery-garden.md) for the recovery-set definition and synthetic experiments.

## Ordinary return is intentionally ordinary

The model should not require a dramatic explanation for every resumption.

If observable events simply return to the normal routine grammar, that is enough to represent Recovery → Normal.

```text
ordinary day = ordinary day
```

This keeps the story layer from inventing significance that the observations do not support.

## A useful correction

Initial intuition:

```text
interruption = failure
```

Correction:

```text
interruption may be a temporary mode;
recovery behavior tells us whether the modeled routine returns toward its nominal set
```

## The next question

We now have:

```text
six continuous hidden states
five hidden modes
known actions
observable clues
slow Shared Context memory
```

But none of the hidden state is directly visible.

Several explanations may fit the same quiet day.

So we need an estimator that can keep more than one hypothesis alive at once.

Continue to [`08-why-particles.md`](08-why-particles.md).
