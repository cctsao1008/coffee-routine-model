# Tiny Observation Calibration Bench 🎛️☕🐣

## Why this exists

The observation model contains hand-set probability assumptions. That is acceptable for a structural prototype only if those assumptions stay visible and testable.

This bench asks:

> **When the model predicts a probability, does that probability behave like the number it claims to be in the synthetic test world?**

This is the lab behind tutorial chapter [`tutorial/09-challenge-the-model.md`](tutorial/09-challenge-the-model.md).

Before calibration, the observation relationship provenance is documented separately in [`observation-provenance.md`](observation-provenance.md). Calibration can challenge an assumed probability family; it does not upgrade an assumed edge into a discovered law.

```text
Calibration first
Optimization later
```

Calibration does not prove the ontology is correct. It checks whether probabilistic predictions keep their stated promises under a defined synthetic experiment.

## The tiny knob tray 🧺

Estimator-side observation parameters live in:

```text
coffee_brain/observation_model.py
```

The default hand-set baseline is:

```python
DEFAULT_OBSERVATION_MODEL
```

It contains explicit recipes for:

```text
opt_in
text_reply
reaction
state_share
proactive_update
routine_maintenance
pass_event
resume_signal
tone_warmth
response_delay
```

The baseline is a **structural prototype assumption**. It is not a learned psychological scale and it is not fitted from private human data.

## Bernoulli clues ☕

Each binary clue uses a logistic recipe:

```text
logit p = intercept + beta · x + mode_offset
```

where:

```text
x = [P, M, V, C, E, F]
```

The bench reports:

```text
Brier score
log loss
mean predicted probability
observed synthetic frequency
calibration gap
expected calibration error (ECE)
reliability bins
```

For `opt_in` and `pass_event`, only days with an invitation are scored. A closed response door is not silently counted as a zero.

## Continuous clues 📏

`tone_warmth` uses residuals on its native scale.

`response_delay` uses residuals in log-minutes because its likelihood is log-normal.

The bench reports:

```text
RMSE
mean residual
residual standard deviation
expected sigma
normalized residual mean
normalized residual standard deviation
```

A normalized residual standard deviation near `1` is evidence that the assumed noise scale is not wildly inconsistent with that synthetic sample. It is not proof that the full model is correct.

## Scenario weather matters 🌦️

The synthetic generator deliberately contains weather-specific biases and noise that the estimator baseline does not automatically know.

```text
Synthetic World != Estimator Assumptions
```

A matched synthetic world may look well calibrated while a noisy or special-day world can expose overconfidence, bias, or a missing context term.

Run every public weather world:

```bash
python -m tiny_tools.calibrate_observations --scenario all --days 365
```

The basket contains:

```text
channel-summary.csv
reliability.csv
continuous-summary.csv
scenario-summary.csv
baseline-config.json
```

## Calibration and learning are separate questions 🎚️🥄

The observation config is immutable and replaceable:

```python
better_guess = DEFAULT_OBSERVATION_MODEL.with_binary_channel(
    "opt_in",
    intercept=-1.0,
)
```

The repository now also contains a deliberately narrow bounded learner in [`learning-spoon.md`](learning-spoon.md). That learner adjusts only a small parameter family, then returns to held-out calibration for evaluation.

```text
Learning a knob != validating the ontology
Better train fit != better model
```

The hand-set default remains preserved for reproducibility and comparison.

## Epistemic boundary 🧠✨

```text
Assumed coefficient != discovered law
Zero coefficient != proven independence
well optimized != well specified
well calibrated != causally true
synthetic calibration != real-human validation
```

The purpose of this bench is to expose probability behavior, not to manufacture confidence.

Tiny knobs. Visible assumptions. Measurable promises. 🎛️☕
