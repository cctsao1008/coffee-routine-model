# Tiny Model Comparison Arena 🗺️☕🐣

CSRDM is not allowed to win merely by comparing against itself.

The arena gives several model variants the **same synthetic timeline**, the same seed, and the same held-out scoring rules.

```text
Winner != truth.
Simpler != worse.
One metric != model quality.
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

## First arena roster 🐣🏁

```text
CSRDM-6 hand-set PF
CSRDM-6 learned observation
CSRDM-6 fixed-lag smoother
CSRDM-6 frozen context memory
CSRDM-5 reconstruct C
static prior non-hybrid
```

A few caveats matter:

- `CSRDM-6 hand-set PF` is the fixed-mode-transition / no-smoothing baseline.
- `CSRDM-6 learned observation` learns only the small parameter family from the parameter-learning spoon.
- `CSRDM-6 frozen context memory` is a memory ablation: the C reservoir is frozen rather than accumulated/decayed.
- `CSRDM-5 reconstruct C` is still the projection/reconstruction diagnostic from the chair test, **not** a fully retrained five-state PF.
- `static prior non-hybrid` estimates no modes, so mode accuracy is intentionally reported as missing instead of assigning a fake zero.

## Same basket, held-out scoring ☕📏

The first 60% of the synthetic timeline may be used by competitors that explicitly learn something.

All reported model-quality metrics use the held-out final 40%:

```text
mean state RMSE / MAE
relationship-index RMSE
95% coverage where intervals exist
mode accuracy where modes exist
binary observation NLL / Brier
Recovery-mode relationship-index RMSE
runtime
memory footprint proxy
```

Observation NLL and Brier are evaluated with the **synthetic true mode fixed**. That intentionally isolates state-representation quality.

```text
Synthetic scoring convenience != real-world deployable information.
```

The arena says this out loud instead of sneaking the answer key under the table. XD

## Change-point metrics ✂️

The default arena uses one stationary synthetic weather world, so change-point metrics are explicitly marked:

```text
n/a for one stationary arena basket
```

When a later arena introduces multi-regime datasets, change-point timing/probability can become a comparable metric.

`N/A` is better than manufacturing a number that answers the wrong question.

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

That is the point. ☕🧠
