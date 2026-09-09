# 10 — Let the Model Lose Sometimes 🗺️☕

A model comparison is useful only if the favorite model is allowed to lose.

CSRDM therefore includes a small arena where several variants see the same synthetic timeline and are scored with the same held-out rules.

```text
Winner != truth
Simpler != worse
One metric != model quality
```

## Why compare at all?

By this point CSRDM contains:

```text
six latent states
hybrid modes
Shared Context memory
Particle Filtering
optional smoothing
calibrated observation probabilities
```

That machinery has a cost.

A simpler model may be:

```text
faster
more interpretable
less memory-hungry
nearly as accurate on a particular task
```

If so, the simpler result is informative.

The purpose of the arena is not to defend CSRDM. It is to expose trade-offs.

## The first competitors

The current arena includes variants such as:

```text
CSRDM-6 hand-set Particle Filter
CSRDM-6 learned observation parameters
CSRDM-6 fixed-lag smoother
CSRDM-6 frozen Shared Context memory
CSRDM-5 reconstruct C diagnostic
static-prior non-hybrid baseline
```

Each competitor receives the same synthetic exam conditions where applicable.

See [`../model-arena.md`](../model-arena.md) for the detailed contract.

## Why bounded learning is intentionally small

The parameter learner does not rewrite the ontology.

It only adjusts a narrow family of observation-model parameters:

```text
selected Bernoulli intercepts
warmth scale
delay scale
```

while keeping the structural state definitions, transition architecture, and memory mechanism fixed.

See [`../learning-spoon.md`](../learning-spoon.md).

The boundary is deliberate:

```text
Learning a probability knob != discovering an intention
Better train fit != better model
Better validation likelihood != better ontology
```

## One score would hide the interesting part

A model can have:

```text
lower state RMSE
worse calibration
better mode accuracy
higher runtime
larger memory use
more learned parameters
```

Compressing those into one winner score would hide the trade-off.

So the arena leaves multiple metrics visible.

That is a general model-design lesson:

> **Evaluation should preserve the dimensions of the decision you actually care about.**

## What the whole tutorial was really teaching

We began with:

```text
+1?
要
pass
☕
👍
busy
leave
resume
```

Then each modeling problem created a new abstraction:

```text
observable events
    ↓
protocol semantics
    ↓
Voluntariness and complementary Mutuality
    ↓
P / M / V / C / E / F
    ↓
actions vs observations
    ↓
slow Shared Context memory
    ↓
hybrid modes and Recovery
    ↓
Particle Filtering and smoothing
    ↓
observability / calibration / sensitivity
    ↓
model comparison
```

That sequence is more important than any single equation.

The project is a small example of a broader engineering habit:

```text
observe carefully
→ define the boundary
→ build the smallest useful abstraction
→ expose uncertainty
→ challenge the abstraction
→ keep the model replaceable
```

## The final boundary

The synthetic story makes the design easier to learn.

The synthetic experiments make the software easier to test.

Neither turns the model into ground truth about people.

```text
Narrative richness != interpretive overreach
Story != evidence
Synthetic validation != human validation
Model != human
```

## Where to go next 📚

- Return to the project [`README`](../../README.md) for the runnable overview.
- Read [`../architecture.md`](../architecture.md) for the formal architecture `0.3` contract.
- Browse the diagnostic gardens and benches for one specific modeling question at a time.
- Run the synthetic examples in [`../../examples/`](../../examples/).

If you can now explain **why each piece exists**, the tutorial has done its job. ☕🐣
