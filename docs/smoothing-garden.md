# Tiny Smoothing Garden 🔭🐣☕

## Why this exists

Filtering and smoothing answer different questions:

```text
filtered posterior = what the model could infer using clues available up to that time
smoothed posterior = what the model can infer about that hidden state after later clues arrive
```

The observed event itself never changes. Only uncertainty about the hidden state may be updated by later evidence.

This is the deeper lab behind the hindsight part of [`tutorial/08-why-particles.md`](tutorial/08-why-particles.md).

## Tiny equations 🧠✨

Filtering:

```math
p(x_t,m_t\mid z_{1:t})
```

Smoothing:

```math
p(x_t,m_t\mid z_{1:T})
```

The implementation uses recorded particle ancestry and a **fixed-lag genealogical smoother** by default.

For each day `t`, descendants are followed forward to roughly `t + lag`, then their later filtering weights are projected backward through the particle genealogy.

## Why fixed lag? 🌱

A long ancestry trace is possible, but Sequential Monte Carlo family trees eventually become thin: many later descendants may share only a few old ancestors.

That is particle path degeneracy.

So the default is:

```text
lag = 30 days
```

and full-history mode remains available for experiments.

```text
Fixed lag != incomplete reasoning
```

It is a deliberate trade between hindsight horizon and genealogy quality.

## History memory is opt-in 🧺

```python
pf = CoffeeParticleFilter(
    particle_count=6000,
    record_history=True,
)
```

Each recorded day keeps compact arrays:

```text
particles  → float32
weights    → float32
modes      → int8
parents    → int32
```

Normal filtering does not pay this history-memory cost unless smoothing is requested.

## Tiny comparison tool 🎩

```bash
python -m tiny_tools.compare_smoothing \
  --scenario slow-recovery \
  --days 120 \
  --particles 800 \
  --lag 30
```

It produces:

```text
comparison.csv
metrics.csv
hindsight.png
```

The scorecard compares filtered and smoothed state RMSE plus mode accuracy on synthetic worlds.

A better smoothed score is welcome, but it is **not guaranteed on every run**. Genealogical smoothing can become noisy when ancestry collapses, and synthetic model mismatch still matters.

## Epistemic boundary 🌟

```text
Later evidence may update uncertainty
Later evidence does not rewrite observed facts
Smoothing improvement != model truth
```

No time machine. Just Bayesian hindsight with an explicit boundary. 🔭🐣
