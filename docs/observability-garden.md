# Tiny Observability Garden 🐣🔍☕

## Why this exists

The Particle Filter can produce estimates for six soft states:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = Everyday State Sharing
F = Friction
```

But producing six numbers does **not** prove that the observations can distinguish six independent latent dimensions.

This garden asks:

> **Which behavior-level clue families actually help distinguish which hidden states in the synthetic test world?**

This is the first diagnostic question in [`tutorial/09-challenge-the-model.md`](tutorial/09-challenge-the-model.md).

## What kind of observability is this? 🌱

This is **practical synthetic identifiability**, not a formal nonlinear observability proof.

Because synthetic hidden truth is known, the experiment can hide one clue family at a time and measure what changes:

```text
all clues
all - reaction
all - state_share
all - response_delay
...
```

If hiding one clue makes a state estimate worse, that clue was carrying useful visibility for that state under that experiment.

If little changes, the clue may be redundant, weak, or unnecessary in that synthetic world.

None of those outcomes is a causal statement about real people.

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

The scorecards use these standard short names:

```text
RMSE = root mean squared error
MAE  = mean absolute error
```

### `scorecard.csv` ☕

For the full baseline and every ablation, it records:

- RMSE;
- MAE;
- Pearson correlation;
- mean 95% interval width;
- 95% interval coverage;
- mode accuracy.

### `clue-visibility.csv` 🔍

For each removed clue family and each hidden state, it records the change relative to the full baseline:

```text
RMSE penalty
correlation loss
credible-interval width increase
```

No single “observability score” is invented just to make the table look tidy.

### `state-identifiability.csv` 🧩

Each estimated state is compared with every synthetic truth state through cross-correlation.

The summary keeps:

```text
self-truth correlation
strongest other-truth correlation
identification margin
```

A small or negative margin is a reason to inspect state cross-talk. It is not automatic proof that two states should be merged.

## What this garden cannot prove

A strong synthetic result can support:

```text
these clues distinguish these injected synthetic states under this model family
```

It cannot establish:

```text
these six states are uniquely real in humans
this correlation proves causal meaning
this narrow posterior proves the ontology is correct
```

## Important boundaries 🧠✨

```text
Estimable != identifiable
Narrow posterior != automatically correct
Correlation != causal meaning
Synthetic visibility != real-human validity
```

The garden exists to make the model skeptical of its own output. ☕🐾
