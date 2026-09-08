# Tiny Sensitivity Map 🧪🗺️☕

The observability garden asks whether a clue family helps the estimator at all.

This sensitivity map asks a wider question:

> **If one clue or one estimator assumption changes, which soft states wobble the most?**

```text
Sensitivity != causality.
Big model effect != psychological importance.
Small model effect != useless clue.
```

## What gets poked 🐾

The first map changes one thing at a time while reusing the exact same synthetic timeline and random seed.

### Clue ablations 🙈

Each observable family is hidden in turn:

```text
opt_in / pass
text_reply
reaction
state_share
proactive_update
routine_maintenance
resume_signal
tone_warmth
response_delay
```

### Continuous observation assumptions 🎛️

The map perturbs:

```text
warmth sigma
warmth intercept
reply-delay sigma
reply-delay base minutes
```

### Dynamics assumptions 🌦️

The map also perturbs:

```text
shared-context decay
continuous-state process noise
fixed mode-transition temperature
```

Transition temperature preserves every row as a valid probability distribution. A lower temperature sharpens the old fixed transition table; a higher temperature flattens it.

## What gets measured 📏

For every poke and each state `P / M / V / C / E / F`, the tool records:

```text
RMSE
relative RMSE change
Pearson correlation
CI95 mean width
CI95 coverage
mode accuracy
```

The heatmap uses signed relative RMSE change:

```text
(RMSE_variant - RMSE_baseline) / RMSE_baseline
```

Positive means the poke made estimation worse under that synthetic experiment. Negative means it happened to improve RMSE.

That sign is diagnostic, not moral. XD

## Run the tiny map 🧺

```bash
python -m tiny_tools.map_sensitivity \
  --days 120 \
  --particles 800 \
  --seed 20260908
```

Outputs:

```text
sensitivity.csv
summary.csv
sensitivity-map.png
```

The public benchmark stays synthetic and generic. No private messages, names, or raw human timelines belong in this basket.
