# V Posterior Compression Result 🌿🔬

This result follows the deliberate **Voluntariness (`V`)** excitation bench in [`voluntariness-excitation.md`](voluntariness-excitation.md).

The focused question was:

> **Why does the V posterior stay compressed even when synthetic truth V is deliberately given a wide dynamic range?**

Architecture `0.3`, the observation model, and production coefficients were not changed for this diagnostic.

## Diagnostic recipe 🧪

The same 180-day focused V path was used:

```text
high V hold
→ ramp down
→ low V hold
→ ramp up
→ high V return
```

with:

```text
low V      = 0.58
high V     = 0.94
truth span = 0.36
particles  = 1200
seed       = 20260908
```

The diagnostic separated four possible compression mechanisms:

```text
observation information
state-dynamics prior
cross-state aliasing
mode uncertainty
```

The scorecards below use these short names:

```text
PF   = Particle Filter
std  = standard deviation
r    = Pearson correlation
RMSE = root mean squared error
```

## 1. The likelihood itself can distinguish low and high V 🎛️

With `P / M / C / E / F` and mode held fixed, the current observation likelihood was evaluated over a one-dimensional V grid.

Observed peaks:

```text
low-V clue basket  → peak V ≈ 0.561
true low V         →          0.580

high-V clue basket → peak V ≈ 0.949
true high V        →          0.940
```

Peak separation:

```text
≈ 0.387
```

So the current likelihood contains substantial directional information about V in this synthetic test.

```text
Likelihood information exists
!=
Sequential estimator must track perfectly
```

This makes `observation likelihood has almost no V information` an unlikely primary explanation for the compression seen in this recipe.

## 2. Locking the mode does not remove the compression 🌤️🔒

Two full six-state filters were compared on the same clue basket:

| Variant | Estimate/truth std ratio | Pearson r | RMSE | 95% coverage |
|---|---:|---:|---:|---:|
| Full PF, hidden mode | 0.096 | 0.180 | 0.170 | 55.6% |
| Full PF, Normal mode effectively locked | 0.078 | 0.230 | 0.166 | 55.6% |

Mode locking improves correlation slightly but does not recover V amplitude or interval coverage.

So, for this focused recipe:

```text
mode uncertainty
→ not the dominant compression mechanism
```

That is a result about this diagnostic, not a universal claim about every CSRDM regime.

## 3. Fixing the other five states helps, but not enough 🪑🌿

A diagnostic-only one-dimensional V filter was then run with `P / M / C / E / F` supplied from synthetic truth and mode fixed to Normal.

It kept the **same V dynamics prior** as the production filter:

```text
V target         = 0.90
mean reversion   = 0.035
process sigma    = 0.011
```

Result:

| Variant | Estimate/truth std ratio | Pearson r | RMSE | 95% coverage |
|---|---:|---:|---:|---:|
| Full PF, Normal locked | 0.078 | 0.230 | 0.166 | 55.6% |
| V-only, default prior | 0.201 | 0.493 | 0.151 | 47.2% |

Removing cross-state uncertainty more than doubles the recovered V amplitude and materially improves correlation.

So cross-state aliasing is a **real contributor** in this synthetic test.

But the estimate is still strongly compressed:

```text
amplitude ratio = 0.201
```

Therefore aliasing alone does not explain the result.

## 4. Relaxing only the V dynamics prior changes the picture strongly 🌿🎛️

A second one-dimensional comparator kept the same observation likelihood and clue basket, but used a deliberately permissive diagnostic prior:

```text
mean reversion = 0.0
process sigma  = 0.035
```

This is **not** a production recommendation.

Result:

| Variant | Estimate/truth std ratio | Pearson r | RMSE | 95% coverage |
|---|---:|---:|---:|---:|
| V-only, default prior | 0.201 | 0.493 | 0.151 | 47.2% |
| V-only, relaxed diagnostic prior | 0.900 | 0.771 | 0.113 | 95.6% |

The amplitude ratio moves from about `0.20` to `0.90`, while coverage rises from `47.2%` to `95.6%`.

This is the largest change among the isolated diagnostic layers.

## 5. Why the default prior can be restrictive 📏

The production-side V prior currently shares the common continuous-state mean-reversion coefficient:

```text
V target       = 0.90
mean reversion = 0.035
process sigma  = 0.011
```

At the low clamp `V = 0.58`, the deterministic restoring drift is:

```text
0.035 × (0.90 - 0.58)
≈ +0.0112 per day
```

That is approximately one default V process-noise sigma per day and is also comparable to the day-to-day slope of the deliberate ramp.

So during a low-V hold or downward movement, the sequential prior continually pushes probability mass back toward `0.90` while the observations must repeatedly overcome that pressure.

This does not prove that the production prior is wrong. It explains why the prior is a strong candidate limiter under this stress path.

## Epistemic conclusion 🧭

```text
Observed
→ low/high clue baskets produce well-separated V likelihood peaks
→ mode locking does not recover the compressed amplitude
→ fixing other states helps materially but leaves strong compression
→ a relaxed V prior changes amplitude and coverage dramatically

Probable
→ the default V dynamics prior is the strongest identified limiter in this synthetic experiment
→ cross-state aliasing is a secondary contributor
→ mode uncertainty is not a major contributor here

Assumed
→ current observation coefficients
→ focused synthetic V path
→ diagnostic comparator settings

Undefined
→ the correct production V mean reversion / process noise
→ whether one V prior should apply across all regimes

Not-yet-decided
→ whether architecture/config defaults should change
```

## Decision gate 🚪

The result is specific enough to justify a narrower next issue, but not specific enough to choose production parameters.

Created:

- **#42 — Decide whether V needs a less restrictive dynamics prior**

That issue must test multiple seeds / excitation shapes and keep the ordinary baseline as a regression guard before any production change is considered.

```text
Diagnostic improvement != production recommendation
Observed mismatch != universal law
Better tracking != better human model
```

The current architecture remains `0.3`.
