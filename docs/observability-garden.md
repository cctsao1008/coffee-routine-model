# Tiny Observability Garden 🐣🔍☕

The Particle Filter can estimate six soft states:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = State Sharing
F = Friction
```

But a tiny estimator being able to produce six numbers does **not** automatically mean all six states are independently visible.

So this garden asks a more careful question:

> Which behavior-level clues actually help distinguish which hidden states?

## What kind of observability is this? 🌱

This is **practical synthetic identifiability**, not a formal nonlinear observability proof.

We already know the synthetic truth, so we can hide one clue family at a time and watch what happens to estimation quality.

```text
all clues
all - reaction
all - state_share
all - response_delay
...
```

If hiding one clue makes a state estimate much worse, that clue was carrying useful visibility for that state.

If nothing changes, the clue may be redundant, weak, or simply unnecessary in that synthetic world.

## Tiny scorecards 🧺

Run:

```bash
python -m tiny_tools.diagnose_observability
```

The default basket appears at:

```text
examples/observability-garden/
├── scorecard.csv
├── clue-visibility.csv
└── state-identifiability.csv
```

### `scorecard.csv` ☕

For the full baseline and every ablation, it records:

- RMSE
- MAE
- Pearson correlation
- mean 95% interval width
- 95% interval coverage
- mode accuracy

### `clue-visibility.csv` 🔍

For each removed clue family and each hidden state, it records the change relative to the full baseline:

```text
RMSE penalty
correlation loss
credible-interval width increase
```

No mysterious single "observability score" is invented just to make the table look tidy. XD

### `state-identifiability.csv` 🧩

Each estimated state is compared with every synthetic truth state through cross-correlation.

The little summary keeps:

```text
self-truth correlation
strongest other-truth correlation
identification margin
```

A small or negative margin is a reason to look more closely for state cross-talk.
It is not automatic proof that two states should be merged.

## The important tiny warning 🧠✨

```text
Estimable != identifiable.
Narrow posterior != automatically correct.
Correlation != causal meaning.
Synthetic visibility != real-human validity.
```

The garden exists to make the model more skeptical of its own tiny brain. ☕🐾
