# 06 — A Routine Can Remember Slowly 🧠🌱

Shared Context is different from a daily mood-like variable.

A synthetic routine may accumulate:

```text
familiar shorthand
recurring handoff conventions
remembered exceptions
callbacks that depend on earlier interactions
ordinary coordination that no longer needs to be re-explained
```

One quiet day should not erase all of that.

## The modeling problem

If every state uses the same generic daily mean-reversion and process-noise path, `C = Shared Context` can become too forgetful.

That would create behavior like:

```text
many days of accumulated context
        ↓
one quiet day
        ↓
context suddenly collapses
```

That is not the behavior this state was designed to represent.

So `C` gets a dedicated memory mechanism.

## The slow memory law

CSRDM uses a bounded accumulation-and-decay form:

```math
C_{t+1}=C_t+\eta I_t(1-C_t)-\lambda C_t+w_t^C
```

where:

```text
C_t     = current Shared Context state
I_t     = bounded observable shared-context input
η       = accumulation rate
λ       = slow decay rate
w_t^C   = dedicated memory noise
```

The saturation term `(1 - C_t)` keeps accumulation from growing without bound.

The design intuition is more important than the exact constants:

```text
repeated context-bearing events
        → gradual accumulation

one quiet day
        → no instant forgetting

long absence without reinforcement
        → slow decay may matter
```

## Why `C` skips ordinary daily drift

This is a structural invariant of architecture `0.3`:

```text
C does not use ordinary state mean reversion
C does not take generic mode drift
C does not take generic process noise
C changes through its dedicated memory path
```

That separation prevents two mechanisms from trying to control the same state at once.

See [`../memory-garden.md`](../memory-garden.md) for the exact implementation and synthetic tests.

## Shared Context still is not hidden human memory

The word “memory” can sound stronger than the model means.

`C` does not claim to measure what either person privately remembers.

It represents the model's accumulated evidence that the **routine has recurring shared context**.

```text
Shared Context state != someone's private memory
```

## A useful correction

Initial intuition:

```text
no event today = no context today
```

Correction:

```text
absence of a new context-bearing event does not erase previously accumulated context
```

This is the same reason many engineering systems distinguish a stored state from the newest measurement.

## The next question

Slow memory solves one temporal problem, but not another.

A routine can also move through qualitatively different kinds of days:

```text
ordinary
busy
leave
special
recovery
```

Trying to represent all of those only by nudging the same six continuous numbers makes the model harder to interpret.

Continue to [`07-weather-and-recovery.md`](07-weather-and-recovery.md).
