# Tiny Observation Calibration Bench 🎛️☕🐣

The coffee brain is allowed to have hand-set probability knobs.

It is **not** allowed to hide them under the rug forever. XD

This little bench makes the observation model inspectable and asks whether its probabilities keep their promises before any optimizer is invited into the kitchen.

> **Calibration first. Optimization later.**

## The tiny knob tray 🧺

All estimator-side observation parameters now live in:

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

Each binary clue has a logistic recipe:

```text
logit p = intercept + beta · x + mode_offset
```

where:

```text
x = [P, M, V, C, E, F]
```

The calibration bench reports:

```text
Brier score
log loss
mean predicted probability
observed synthetic frequency
calibration gap
expected calibration error (ECE)
reliability bins
```

For `opt_in` and `pass_event`, only days with an invitation are scored. A closed response door is not silently counted as a zero. 🚪☕

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

A normalized residual standard deviation near `1` is one clue that the assumed noise scale is not wildly wrong. It is not proof that the whole model is correct. 🐣

## Scenario weather matters 🌦️

The synthetic generator deliberately has weather-specific biases and noise that the estimator baseline does not automatically know.

That is useful.

```text
Synthetic World != Estimator Assumptions
```

So a cozy matched world may look well calibrated while a noisy or special-day world can expose overconfidence, bias, or a missing context term.

Run every weather world:

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

## A clean hook for later learning 🔧🐣

The observation config is immutable and replaceable:

```python
better_guess = DEFAULT_OBSERVATION_MODEL.with_binary_channel(
    "opt_in",
    intercept=-1.0,
)
```

That gives a future EM, Bayesian, gradient-based, or other parameter learner a clean parameter surface without forcing the current repo to pretend learning is already solved.

The hand-set default remains preserved for reproducibility.

## Tiny epistemology rule 🧠✨

A prettier loss is not enough.

```text
well optimized != well specified
well calibrated != causally true
synthetic calibration != real-human validation
```

The purpose of this bench is to reveal which probability families deserve learning next, not to manufacture confidence.

Tiny knobs. Visible assumptions. Measurable promises. 🎛️☕✨
