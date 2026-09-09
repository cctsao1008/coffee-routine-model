# Tiny Parameter Learning Spoon 🎚️🥄🐣

## Why this exists

Calibration can reveal that a probability family is biased or overconfident. The next temptation is to let an optimizer rewrite everything.

This repo deliberately does **not** do that.

The learning spoon asks one narrow question:

> **If the structural observation model stays fixed, can a few bounded calibration knobs adapt to a shifted synthetic world without rewriting CSRDM's ontology?**

This is one of the final labs linked from [`tutorial/10-let-the-model-lose.md`](tutorial/10-let-the-model-lose.md).

```text
Explicit parameters
    ↓
Calibration
    ↓
Bounded learning
    ↓
Held-out calibration again
```

## What learns 🌱

The current learner adjusts only:

```text
8 Bernoulli intercepts
warmth sigma
delay sigma
```

Everything structural stays frozen:

```text
state slopes
mode offsets
state dynamics
mode transitions
memory constants
process noise
state definitions
```

So the experiment changes probability calibration, not the meaning of `P / M / V / C / E / F`.

## Tiny optimizer 🐣🎚️

Each Bernoulli intercept is fitted with a bounded one-dimensional Newton update while all slopes remain fixed.

For one clue channel:

```text
logit(p[t]) = fixed_offset[t] + b
```

and only `b` is learned.

The continuous sigmas use residual RMS, which is the Gaussian / log-normal scale MLE under the fixed mean model.

Hard bounds keep the knobs inside the declared experiment family:

```text
binary intercept : [-6, 6]
warmth sigma     : [0.02, 0.50]
delay sigma_log  : [0.10, 1.50]
```

Approximate standard errors and 95% intervals are reported for every learned knob.

```text
Parameter uncertainty != posterior state uncertainty
```

They answer different questions.

## Train is not validation ☕📚

The timeline is split chronologically:

```text
first 60%  → synthetic training
last 40%   → held-out validation
```

Before and after learning, both splits report:

```text
mean Bernoulli Brier score
mean Bernoulli log loss
mean ECE
warmth RMSE / normalized residual std
delay-log RMSE / normalized residual std
```

Run:

```bash
python -m tiny_tools.learn_parameters \
  --scenario special-day-sparkle \
  --days 480 \
  --seed 20260908
```

Outputs:

```text
parameters.csv
metrics.csv
baseline-config.json
learned-config.json
```

`learned-config.json` has the normal `ObservationModelConfig` shape. Optimization does not create a secret second model format.

## Why the boundary is intentionally small 🧠✨

A learner that can freely change dynamics, state definitions, transition semantics, and observation semantics at once could improve a loss while making the model harder to interpret.

So this experiment keeps the hypothesis narrow enough to inspect:

```text
Can a few observation-calibration parameters adapt?
```

not:

```text
Can an optimizer invent a new ontology for us?
```

## Epistemic boundary

```text
Better train fit != better model
Better validation likelihood != better ontology
Synthetic adaptation != real-human truth
Learning a knob != discovering an intention
```

The learner may improve probability calibration. It may not redefine the meaning of the model because one loss function prefers a different shape.
