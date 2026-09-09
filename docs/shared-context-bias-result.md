# Shared Context Bias Decomposition 🧠🌱🔬

`C = Shared Context` has an odd-looking observation-only baseline signature:

```text
shape tracking looks strong
absolute offset stays negative
```

Those are different questions.

This diagnostic exists to separate them **before anyone touches the slow-memory law**.

> **Shape tracking != unbiased estimation.**

## What is being tested

The committed `examples/365-cute-days/` basket is replayed three times with the same observations, same estimator, same seed, and same memory law.

Only the initial `C` particle cloud is shifted:

```text
default
→ current production initialization

matched-truth-start
→ diagnostic-only shift so the C prior center starts near synthetic truth C[0]

mirror-high
→ diagnostic-only shift to the opposite side of truth
```

The shift preserves the existing particle offsets as much as clipping allows. No public API is added.

## Error decomposition

For each replay:

```text
error_t = estimated_C_t - true_C_t
bias    = mean(error_t)
```

Total squared error is separated into:

```text
RMSE² = bias² + centered_RMSE²
```

`centered_RMSE` answers the shape/residual question after the constant offset is removed.

`offset_MSE_fraction` reports how much of total MSE is explained by the mean offset term.

## Quiet-memory comparison 🍂

The observation-only reference gives the Shared Context reservoir no action-driven accumulation input.

The same memory law used by `inspect_memory.py` therefore predicts that an initialization offset should decay only slowly:

```text
C[t+1] = C[t] - lambda * C[t] + noise
```

for the no-input comparison.

The diagnostic records the deterministic offset-retention curve from the current `decay_rate` and compares it with the observed posterior error.

This matters because:

```text
slow decay of an initial mismatch
!=
proof that the memory law is wrong
```

## Time and mode views

The result basket contains:

```text
prior-summary.csv
error-track.csv
time-bias.csv
mode-bias.csv
quiet-memory.csv
shared-context-bias.png
recipe.json
```

`time-bias.csv` asks whether the offset decays, stays flat, or changes character over the year.

`mode-bias.csv` checks whether one routine mode is carrying the effect.

## Decision rules ⚖️

```text
matched prior removes most offset
→ initialization semantics are the main suspect
→ do not tune eta/lambda just to repair this baseline

matched prior still leaves similar offset
→ initialization alone is insufficient
→ inspect observation information / slow-memory convergence more deeply

mode-specific error dominates
→ inspect mode-conditioned evidence before touching the memory reservoir

action-aware reference later changes the picture
→ document observation-only scope rather than retrofitting the baseline
```

The action-aware comparison belongs with the separate controlled reference from #33 once that reference exists.

## Boundaries

```text
Bias evidence != automatic tuning request
Shape tracking != unbiased estimation
Prior mismatch != broken memory law
Observation-only baseline != controlled routine
Synthetic result != human truth
```

Architecture `0.3`, observation coefficients, `eta`, `lambda`, and Shared Context process noise remain unchanged by this diagnostic. ☕🐣
