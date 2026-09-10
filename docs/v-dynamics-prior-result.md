# V Dynamics-Prior Scan Result 🌿🎛️

This result follows [`v-compression-result.md`](v-compression-result.md).

Here `V` means **Voluntariness**.

The previous diagnostic showed that the current V observation likelihood contains directional information, while the sequential posterior remains compressed. A relaxed V dynamics prior helped strongly in one focused stress path.

The next question was therefore narrower:

> **Is there one bounded V dynamics prior that improves deliberately excited tracking without degrading the ordinary observation-only baseline enough to make the trade-off ambiguous?**

No production setting was changed during this scan.

## Scan recipe 🧪

The diagnostic used three deliberately different V paths:

```text
ramp
step
triangle
```

with three seeds:

```text
20260908
20260909
20260910
```

Each stress run used:

```text
low V     = 0.58
high V    = 0.94
180 days
800 particles
```

The committed `examples/365-cute-days/` observation-only basket was also replayed as a regression guard.

To isolate the V prior itself, `P / M / C / E / F` and mode were supplied from synthetic truth in this diagnostic filter. Only V remained uncertain.

```text
Diagnostic isolator != public CSRDM inference path
```

The result tables use these short metric names:

```text
RMSE = root mean squared error
r    = Pearson correlation
```

## Candidate family 🌱

| Candidate | Mean reversion | Process sigma | Role |
|---|---:|---:|---|
| `default` | 0.0350 | 0.0110 | current baseline |
| `half-reversion` | 0.0175 | 0.0110 | bounded comparator |
| `double-noise` | 0.0350 | 0.0220 | bounded comparator |
| `half-reversion-1.5x-noise` | 0.0175 | 0.0165 | bounded comparator |
| `half-reversion-double-noise` | 0.0175 | 0.0220 | bounded comparator |
| `quarter-reversion-double-noise` | 0.00875 | 0.0220 | bounded comparator |
| `zero-reversion-high-noise` | 0.0 | 0.0350 | stress extreme |

The extreme comparator exists to reveal sensitivity. It is not a proposed default.

## Aggregate result 📏

Continuous-integration (CI) run #145 reported:

| Candidate | Stress RMSE | Stress r | Amp ratio | Stress coverage | Baseline RMSE |
|---|---:|---:|---:|---:|---:|
| `default` | 0.151 | 0.491 | 0.200 | 48.3% | **0.033** |
| `half-reversion` | 0.132 | 0.479 | 0.374 | 49.1% | 0.045 |
| `double-noise` | 0.112 | 0.691 | 0.475 | 72.5% | 0.045 |
| `half-reversion-1.5x-noise` | 0.115 | 0.600 | 0.557 | 69.4% | 0.054 |
| `half-reversion-double-noise` | **0.106** | 0.672 | 0.675 | 85.5% | 0.061 |
| `quarter-reversion-double-noise` | 0.112 | 0.669 | 0.810 | 87.3% | 0.071 |
| `zero-reversion-high-noise` | 0.117 | **0.751** | **1.038** | **92.8%** | 0.089 |

The table reveals a real trade-off rather than one obvious winner.

## What changed as the prior became more permissive? 🔍

The deliberately excited stress paths generally improved when the prior was loosened:

```text
more posterior amplitude
higher interval coverage
usually lower stress RMSE
```

But the ordinary committed baseline moved in the opposite direction:

```text
default baseline RMSE       ≈ 0.033
double-noise baseline RMSE  ≈ 0.045
half-rev + double-noise     ≈ 0.061
zero-rev + high-noise       ≈ 0.089
```

Using the rounded CI values, even the comparatively moderate `double-noise` option raises baseline RMSE by roughly one third while reducing stress RMSE by roughly one quarter.

The candidate with the lowest stress RMSE, `half-reversion-double-noise`, nearly doubles the baseline RMSE relative to the default.

The stress extreme recovers nearly full amplitude and high coverage, but its baseline RMSE is roughly 2.7× the default.

## No candidate dominates both objectives ⚖️

The current default is best on the ordinary baseline guard.

Every alternative that improves deliberately excited tracking makes that baseline guard worse.

So the decision is not:

```text
which candidate is numerically best?
```

It is:

```text
how much ordinary-baseline degradation
are we willing to trade
for stronger response to large V excursions?
```

That weighting is currently **Undefined**.

Choosing one candidate anyway would silently turn an unspecified design preference into a model default.

```text
Trade-off != winner
Undefined utility weighting != zero importance
```

## Should the production default change now? 🚪

**No.**

The scan strengthens the conclusion that V tracking is sensitive to its dynamics prior, but it does not identify a robust production replacement.

The current epistemic status is:

```text
Observed
→ permissive V priors improve deliberate-excitation tracking
→ the same priors degrade the ordinary observation-only baseline guard
→ no scanned candidate dominates both objectives

Probable
→ V posterior compression is materially controlled by prior stiffness
→ process noise and mean reversion create a genuine bias/variance trade-off

Assumed
→ the chosen stress shapes and baseline basket are useful diagnostic regimes
→ the current candidate grid covers meaningful bounded perturbations

Undefined
→ the correct weighting between excursion responsiveness and ordinary-baseline accuracy
→ the correct production V prior across all possible regimes

Not-yet-decided
→ whether future evidence should justify regime-dependent or per-state V dynamics
```

## Should per-state dynamics configuration enter the public API now? 🏛️

**Not yet.**

A public per-state V dynamics knob would expose a tuning decision that this scan has not resolved. The diagnostic layer can already vary these assumptions without expanding the stable application API.

That keeps architecture `0.3` honest:

```text
Diagnostic flexibility
!=
public configuration obligation
```

A future controlled/action-aware reference or another independently motivated regime may change that conclusion. If so, the new basis should be explicit before the API grows.

## Decision 🌿

```text
Production V prior        → unchanged
Observation coefficients → unchanged
Architecture 0.3         → unchanged
Public config surface    → unchanged
```

The result is not “the default prior is correct.”

It is:

> **The current diagnostics reveal a real trade-off, but they do not yet define the utility function needed to choose a new default.**

So the correct Phase 6 action is to document the sensitivity and stop rather than manufacture precision.
