# Tiny Parameter Learning Spoon 🎚️🥄🐣

The observation model already keeps every probability knob in one visible tray.

Now a **small** subset is allowed to learn from synthetic hidden-state data.

```text
Explicit parameters
    ↓
Calibration
    ↓
Tiny bounded learning spoon
    ↓
Held-out calibration again
```

No giant parameter buffet. XD

## What learns 🌱

The first learner adjusts only:

```text
8 Bernoulli intercepts
warmth sigma
delay sigma
```

Everything else stays frozen:

```text
state slopes
mode offsets
state dynamics
mode transitions
memory constants
process noise
state definitions
```

So the experiment asks a narrow question:

> If the structural observation model is already reasonable, can a few calibration knobs adapt to a shifted synthetic world without destabilizing the rest of CSRDM?

## Tiny optimizer 🐣🎚️

Each Bernoulli intercept is fitted with a bounded one-dimensional Newton update while all slopes remain fixed.

For one clue channel:

```text
logit(p[t]) = fixed_offset[t] + b
```

and only `b` is learned.

The continuous sigmas use residual RMS, which is the Gaussian / log-normal scale MLE under the fixed mean model.

Hard bounds keep the knobs from wandering into nonsense:

```text
binary intercept : [-6, 6]
warmth sigma     : [0.02, 0.50]
delay sigma_log  : [0.10, 1.50]
```

Approximate standard errors and 95% intervals are reported for every learned knob.

```text
Parameter uncertainty != posterior state uncertainty.
```

They are separate little creatures. 🐣🐣

## Train is not validation ☕📚

The timeline is split chronologically:

```text
first 60%  -> synthetic training
last 40%   -> held-out validation
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

`learned-config.json` has the same normal `ObservationModelConfig` shape as the hand-set baseline, so later experiments do not need a secret optimizer-only format.

## Important tiny rule 🧠✨

```text
Better train fit != better model.
Better validation likelihood != better ontology.
Synthetic adaptation != real-human truth.
Learning a knob != discovering an intention.
```

The learner is allowed to improve probability calibration.

It is not allowed to rewrite what `P / M / V / C / E / F` mean just because one loss function asked nicely. XD
