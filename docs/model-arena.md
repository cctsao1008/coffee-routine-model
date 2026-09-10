# Tiny Model Comparison Arena 🗺️☕🐣

## Why this exists

CSRDM should not win merely by comparing against itself.

The arena gives several model variants the **same synthetic timeline**, the same seed, and the same held-out scoring rules.

This is the final comparison lab behind [`tutorial/10-let-the-model-lose.md`](tutorial/10-let-the-model-lose.md).

```text
Winner != truth
Simpler != worse
One metric != model quality
```

## Common little contract 🧺

Every competitor returns an `ArenaRun` containing:

```text
estimated states
optional 95% intervals
optional mode estimates
runtime
memory estimate
latent dimension count
hybrid / smoothing flags
learned-parameter count
whether synthetic hidden truth was used for training
notes
```

That keeps comparison code from quietly giving one model a different exam.

## Current arena roster 🐣🏁

The roster uses `PF` as shorthand for **Particle Filter**:

```text
CSRDM-6 hand-set PF
CSRDM-6 learned observation
CSRDM-6 fixed-lag smoother
CSRDM-6 frozen context memory
CSRDM-5 reconstruct C
static prior non-hybrid
```

Important caveats:

- `CSRDM-6 hand-set PF` is the fixed-mode-transition / no-smoothing baseline.
- `CSRDM-6 learned observation` learns only the bounded parameter family in [`learning-spoon.md`](learning-spoon.md).
- `CSRDM-6 frozen context memory` is a memory ablation: the `C` reservoir is frozen rather than accumulated/decayed.
- `CSRDM-5 reconstruct C` is the projection/reconstruction diagnostic from [`state-chair-test.md`](state-chair-test.md), **not** a fully retrained five-state Particle Filter.
- `static prior non-hybrid` estimates no modes, so mode accuracy is reported as missing rather than assigned a fake zero.

## Same basket, held-out scoring ☕📏

The first 60% of the synthetic timeline may be used by competitors that explicitly learn something.

The scorecard uses these common metric names once, then their short forms below:

```text
RMSE = root mean squared error
MAE  = mean absolute error
NLL  = negative log likelihood
```

Reported model-quality metrics use the held-out final 40%:

```text
mean state RMSE / MAE
relationship-index RMSE
95% coverage where intervals exist
mode accuracy where modes exist
binary observation NLL / Brier score
Recovery-mode relationship-index RMSE
runtime
memory footprint proxy
```

Observation NLL and Brier score are evaluated with the **synthetic true mode fixed**. That intentionally isolates state-representation quality for this experiment.

```text
Synthetic scoring convenience != deployable real-world information
```

The answer key is explicit rather than hidden.

## Change-point metrics ✂️

The default arena uses one stationary synthetic weather world, so change-point metrics are marked **not applicable (`N/A`)**:

```text
N/A for one stationary arena basket
```

`N/A` is better than manufacturing a number that answers the wrong question.

If a different arena recipe contains explicit multi-regime synthetic data, change-point timing/probability can be evaluated as a separate comparable metric.

## Run the tiny arena 🗺️

```bash
python -m tiny_tools.run_model_arena \
  --scenario special-day-sparkle \
  --days 240 \
  --particles 400 \
  --seed 20260908
```

Outputs:

```text
comparison.csv
state-rmse.csv
arena-state-rmse.png
arena-runtime.png
arena-notes.md
```

There is deliberately **no combined winner score**.

A model can have:

```text
better RMSE
worse calibration
better mode accuracy
higher memory cost
more synthetic-trained parameters
```

and the arena leaves those trade-offs visible.

## What the arena can and cannot say

It can support statements such as:

```text
variant A had lower held-out synthetic RMSE on this recipe
variant B used less runtime or memory
variant C produced better probability calibration
```

It cannot establish:

```text
variant A is universally true
more complex is automatically better
one synthetic winner is the final ontology
```

That is the point of the arena: let the model lose when the evidence says it should. ☕🧠
