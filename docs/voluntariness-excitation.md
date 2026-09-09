# Voluntariness Excitation Bench 🌿☕

## Why this exists

The observation-only 365-day reference currently gives `V = Voluntariness` relatively little truth variation and an awkward negative Pearson correlation.

That result is **Observed** for that synthetic recipe. The explanation is still **Probable / Undefined** until a more focused test separates weak excitation from a genuine tracking mismatch.

```text
Awkward metric != bug
Low excitation != zero information
Probability != fact
```

This bench deliberately gives synthetic truth `V` a wider dynamic range while leaving the Particle Filter and architecture `0.3` unchanged.

## What is deliberately controlled 🧪

The truth path is a focused diagnostic clamp:

```text
high V hold
    ↓
ramp down
    ↓
low V hold
    ↓
ramp up
    ↓
high V return
```

During this test:

```text
P / M / E / F → held at nominal estimator targets
C             → follows ordinary quiet-memory decay
mode          → Normal
V             → deliberately excited
```

This path is **Assumed synthetic test structure**, not ordinary CSRDM truth dynamics and not a claim about how real people change.

```text
Synthetic clamp != human law
Focused diagnostic != new model feature
```

## Which clues directly carry V? 🎛️

Under the current observation model, direct V coefficients exist only in a subset of channels:

```text
opt_in               +1.20
reaction             +0.40
routine_maintenance  +0.90
tone_warmth          +0.18
```

The remaining current direct coefficients are zero.

That statement means:

> the **current model specification** gives those channels no direct V term.

It does **not** mean a broader real-world relationship has been proven absent.

```text
model coefficient = 0
!=
real relationship proven absent
```

`pass_event` is especially important here: in the observation-only likelihood it has no direct V coefficient. A voluntary pass can preserve V through the **action-aware transition path**, but that is a different architecture path and belongs to the separate controlled-reference work in #33.

The diagnostic writes `channel-sensitivity.csv` directly from `DEFAULT_OBSERVATION_MODEL` so this map does not need to be maintained by hand.

## Run the bench 🌱

```bash
python -m tiny_tools.excite_voluntariness \
  --days 180 \
  --particles 1200 \
  --low-v 0.58 \
  --high-v 0.94 \
  --seed 20260908 \
  --out .tiny-v-excitation
```

Outputs:

```text
summary.csv
v-track.csv
channel-sensitivity.csv
recipe.json
v-excitation.png
```

`summary.csv` includes both the deliberate excitation result and, when available, the committed observation-only 365-day baseline for context.

## What to inspect 🔍

The important numbers are:

```text
truth std / span
estimate std
RMSE / MAE
Pearson r
95% interval coverage
mean estimate - truth bias
```

Correlation should not be interpreted without the excitation scale beside it.

A useful question is:

> Does V become directionally trackable when the synthetic truth actually moves enough to make tracking measurable?

## Decision gate 🚪

If deliberate excitation produces clear positive tracking:

```text
Observed
→ the unchanged estimator can track a sufficiently excited synthetic V path

Probable interpretation
→ the baseline negative r is strongly influenced by weak excitation / metric context

Still undefined
→ how much excitation is sufficient in every possible regime
```

If tracking remains poor or reversed:

```text
Observed
→ the focused synthetic stress test still shows mismatch

Next step
→ open a narrow observation-model / estimator issue
```

Do not tune coefficients inside this bench.

## Epistemic boundary 🧭

```text
Observed
→ metrics from one declared synthetic recipe

Probable
→ explanation for why baseline tracking looked awkward

Assumed
→ the current observation coefficients and the deliberate V clamp

Undefined
→ broader human relationships not specified by this model

Not-yet-decided
→ whether any core-model change is warranted after the result
```

The bench exists to reduce uncertainty before making that last decision. ☕🌿
