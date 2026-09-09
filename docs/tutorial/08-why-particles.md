# 08 — Why Particle Filtering Appears Naturally 🐣🐣🐣

At this point CSRDM has enough structure to create a new problem:

```text
x[t] = six hidden continuous states
m[t] = one hidden discrete mode
```

The model cannot observe either of them directly.

## One quiet day, several plausible explanations

Suppose the observed interaction is quieter than usual.

Several hypotheses may still fit:

```text
🐣 #1 ordinary noise
🐣 #2 Busy mode
🐣 #3 slightly higher Friction
🐣 #4 fewer observable clues, with little real state change
```

Choosing one immediately would create false certainty.

So the estimator should carry a distribution of possible hidden states instead of a single hard guess.

## Tiny particles as hypotheses

A particle carries one possible combination of:

```text
[P, M, V, C, E, F]
+
routine mode
```

Many particles together approximate the posterior distribution.

The cycle is conceptually:

```text
previous particles
      ↓
predict using dynamics + known actions
      ↓
compare with current observations
      ↓
reweight
      ↓
resample when needed
      ↓
current posterior
```

Filtering asks:

```math
p(x_t,m_t\mid z_{1:t})
```

The output is therefore not “the true state.”

It is a probability distribution under the current model assumptions and observed clues.

```text
Posterior certainty != model correctness
```

A narrow posterior can still be confidently wrong if the model is misspecified.

## Why not just use one deterministic state estimate?

A deterministic estimate can be useful, but it tends to hide multimodal uncertainty.

For example:

```text
50% Busy
50% Normal with slightly higher Friction
```

can collapse into a synthetic average that corresponds to neither explanation very well.

Particle Filtering keeps those alternatives available longer.

## Later evidence and smoothing

Suppose a normal resume event appears a few days later.

That later clue may change how plausible earlier hidden-state hypotheses look.

Smoothing asks:

```math
p(x_t,m_t\mid z_{1:T})
```

But it changes only the **inference about hidden state**.

It does not change the earlier observed event.

```text
Later evidence may update uncertainty.
Later evidence does not rewrite observed facts.
```

The implementation uses particle ancestry and fixed-lag genealogical smoothing. See [`../smoothing-garden.md`](../smoothing-garden.md).

## The public API stays small

The underlying estimator is not tiny, but the stable public door is:

```python
from coffee_brain import CSRDM, CSRDMConfig

brain = CSRDM(CSRDMConfig())
result = brain.step(["+1?", "要", "☕", "👍"])

print(result.posterior.mean)
```

The API returns posterior state estimates without asking callers to manage the Particle Filter internals directly.

## A useful correction

Initial intuition:

```text
we have an estimator
→ therefore we know the hidden state
```

Correction:

```text
we have an estimator
→ therefore we have a model-conditioned uncertainty distribution
```

That difference is central to the whole project.

## The next question

Now the estimator can produce plausible posteriors.

But that creates a harder question:

> **Can the observable clues actually distinguish the six states we invented, or are we only producing precise-looking numbers?**

Continue to [`09-challenge-the-model.md`](09-challenge-the-model.md).
