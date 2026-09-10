# Tiny Sensitivity Map 🧪🗺️☕

## Why this exists

Observability asks whether a clue family helps distinguish latent states. Sensitivity asks a different question:

> **If one clue or one estimator assumption changes, which outputs move the most?**

This is one of the challenge labs linked from [`tutorial/09-challenge-the-model.md`](tutorial/09-challenge-the-model.md).

```text
Sensitivity != causality
Big model effect != psychological importance
Small model effect != useless clue
```

## What gets poked 🐾

The map changes one thing at a time while reusing the same synthetic timeline and random seed.

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

Transition temperature preserves every row as a valid probability distribution. A lower temperature sharpens the fixed transition table; a higher temperature flattens it.

## What gets measured 📏

For every poke and each state `P / M / V / C / E / F`, the tool records:

```text
RMSE = root mean squared error
relative RMSE change
Pearson correlation
mean 95% interval width
95% interval coverage
mode accuracy
```

The heatmap uses signed relative RMSE change:

```text
(RMSE_variant - RMSE_baseline) / RMSE_baseline
```

Positive means the perturbation made estimation worse under that synthetic experiment. Negative means it happened to improve RMSE.

The sign is diagnostic, not moral.

## How to read a strong sensitivity

If one assumption strongly changes an output, the correct conclusion is:

```text
this model output depends strongly on this assumption
```

not:

```text
this assumption is therefore a real-world causal driver
```

Sensitivity is especially useful for deciding which assumptions deserve calibration, additional diagnostics, or a simpler alternative model.

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

The benchmark stays synthetic and generic. No private messages, names, or raw human timelines belong in this basket.

## Epistemic boundary

```text
Sensitivity != causality
Parameter influence != human importance
Synthetic robustness != real-world validity
```
