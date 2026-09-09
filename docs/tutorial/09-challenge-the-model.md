# 09 — Challenge the Model Before Trusting the Numbers 🔍🧪

A Particle Filter can produce smooth posterior curves even when the model is poorly designed.

So the next stage is not “celebrate the graph.”

It is:

> **Try to make the model fail in informative ways.**

## Question 1: can the clues distinguish the states?

We invented six latent dimensions:

```text
P / M / V / C / E / F
```

That does not guarantee the observation model can identify them separately.

The observability diagnostics ask whether small changes in each hidden direction create distinguishable observation signatures.

See [`../observability-garden.md`](../observability-garden.md).

The rule is:

```text
Estimable != identifiable
Narrow posterior != automatically correct
```

## Question 2: do the probabilities keep their promises?

The observation model contains hand-set structural prototype parameters.

If a clue is predicted with probability `0.8`, does that kind of prediction behave like `0.8` across synthetic cases?

That is a calibration question.

See [`../calibration-bench.md`](../calibration-bench.md).

```text
Calibration first
Optimization later
```

## Question 3: which assumptions matter most?

A model can look stable simply because nobody has moved the knobs.

Sensitivity experiments perturb structural assumptions and measure what changes.

See [`../sensitivity-map.md`](../sensitivity-map.md).

```text
Sensitivity != causality
```

If changing one coefficient strongly changes the output, we learn that the model depends on that assumption. We do not learn that the coefficient is a real-world causal law.

## Question 4: is one weird day a new regime?

A slow reply or unusual day is tempting to overinterpret.

The change-point garden asks for persistent evidence before declaring a shift in the observation-generating regime.

See [`../change-point-garden.md`](../change-point-garden.md).

```text
Mode != regime
Anomaly != change point
Change point != story conclusion
```

## Question 5: does interruption recovery behave as designed?

Recovery experiments introduce disturbances and measure return toward a nominal routine set.

See [`../recovery-garden.md`](../recovery-garden.md).

The useful question is not:

```text
Did anything unusual happen?
```

but:

```text
How did the modeled routine behave after the disturbance?
```

## Useful modeling corrections

The diagnostics preserve several lessons that are easy to forget:

```text
slow reply = bad state
    ↓ correction
reply delay is one noisy clue; context matters

one interruption = structural failure
    ↓ correction
disturbance != rupture

continued routine = automatically strong
    ↓ correction
voluntariness must remain explicit

six estimated numbers = six independent truths
    ↓ correction
estimable != identifiable

better fit = better ontology
    ↓ correction
fit, calibration, ontology, and causality are different questions
```

These are modeling corrections, not claims about real people.

## Synthetic validation has a boundary

The repository can test whether CSRDM behaves coherently in synthetic worlds where hidden truth is known because the simulator created it.

That supports statements like:

```text
this estimator recovered this synthetic state reasonably well
this diagnostic detected this injected change
this calibration metric improved on held-out synthetic data
```

It does **not** support:

```text
real people have exactly these six states
these parameter values are universal
this posterior reveals private human truth
```

```text
Synthetic success != real-human truth
```

## The next question

Even if CSRDM passes its own diagnostics, it should not win simply by comparing against itself.

So the final teaching step asks:

> **Can simpler or slightly learned alternatives compete on the same synthetic exam?**

Continue to [`10-let-the-model-lose.md`](10-let-the-model-lose.md).
