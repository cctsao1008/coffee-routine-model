# Tiny Smoothing Garden 🔭🐣☕

Filtering and smoothing answer two different questions.

```text
filtered posterior  = what the tiny brain knew then
smoothed posterior  = what the tiny brain can infer after later clues arrive
```

The observed event itself never changes.
Only the uncertainty about the hidden state is allowed to learn from later evidence.

## Tiny equations 🧠✨

Filtering:

```text
p(x[t], m[t] | z[1:t])
```

Smoothing:

```text
p(x[t], m[t] | z[1:T])
```

The implementation uses recorded particle ancestry and a **fixed-lag genealogical smoother** by default.

For each day `t`, the tiny descendants are followed forward to roughly `t + lag`, then their later filtering weights are projected backward through the family tree.

## Why fixed lag? 🌱

A full 365-day ancestry trace is possible, but Sequential Monte Carlo family trees eventually become very skinny. Many descendants may share only a few old ancestors.

That is particle path degeneracy.

So the comfy default is:

```text
lag = 30 tiny days
```

and full-history mode stays available for experiments.

```text
Fixed lag != incomplete thinking.
It is a deliberate trade between hindsight and particle genealogy quality. 🐣
```

## Memory basket 🧺

History recording is opt-in:

```python
pf = CoffeeParticleFilter(
    particle_count=6000,
    record_history=True,
)
```

Each recorded day keeps compact arrays:

```text
particles  -> float32
weights    -> float32
modes      -> int8
parents    -> int32
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

A better smoothed score is welcome, but it is **not guaranteed on every tiny run**. Genealogical smoothing can become noisy when ancestry collapses, and synthetic model mismatch still matters.

## Tiny law 🌟

```text
Later evidence may update uncertainty.
Later evidence does not rewrite observed facts.
```

No time machine. Just Bayesian hindsight wearing a tiny hat. 🎩🐣✨
