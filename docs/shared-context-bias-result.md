# Shared Context Bias Decomposition 🧠🌱🔬

`C = Shared Context` has an odd-looking observation-only baseline signature:

```text
shape tracking looks strong
absolute offset stays negative
```

Those are different questions.

This diagnostic separates them **before anyone touches the slow-memory law**.

> **Shape tracking != unbiased estimation.**

## Reproducible recipe 🧺

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

CI recipe:

```text
synthetic days = 365
particles      = 6000
seed           = 20260908
truth C[0]     = 0.7000
```

## Error decomposition 📏

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

## Main result 🔍

`☕ Tiny Coffee Checks` run #149 reports:

```text
candidate              mean bias   RMSE    centered RMSE   Pearson r   CI95 coverage
default                   -0.099    0.104      0.033          0.901        57.8%
matched-truth-start       -0.045    0.063      0.044          0.890        92.6%
mirror-high               -0.021    0.063      0.060          0.882       100.0%
```

The default prior mean is:

```text
estimated initial C center ≈ 0.5809
synthetic truth C[0]       = 0.7000
initial prior offset       ≈ -0.1191
```

For the default replay:

```text
mean bias                 ≈ -0.0990
offset MSE fraction       ≈ 0.8976
quiet-law predicted bias  ≈ -0.0918
observed - quiet prediction≈ -0.0072
```

So about 90% of the default MSE is the squared mean-offset term, and the no-input slow-memory law predicts most of the observed mean bias magnitude from the initial mismatch alone.

That is strong evidence that the baseline problem is **bias dominated**, not primarily a failure to follow the shape.

## What matching the start changes 🌱

Moving only the diagnostic prior center near `C[0]` changes:

```text
mean bias   -0.099 → -0.045
RMSE         0.104 →  0.063
coverage     57.8% → 92.6%
```

That removes a large part of the baseline mismatch without changing:

```text
eta
lambda
C process noise
observation coefficients
mode transition model
public API
```

But it does **not** remove all negative bias. The matched replay becomes negative again later in the year.

Therefore:

```text
initial prior mismatch
→ dominant contributor to the default offset

initial prior mismatch
!=
complete explanation of every later C error
```

## Time decomposition ⏳

Default replay:

```text
window       mean bias   centered RMSE
day 001-030    -0.044       0.018
day 031-090    -0.080       0.020
day 091-180    -0.132       0.015
day 181-365    -0.098       0.028
```

Matched-start replay:

```text
window       mean bias   centered RMSE
day 001-030    +0.054       0.019
day 031-090    -0.004       0.024
day 091-180    -0.075       0.023
day 181-365    -0.059       0.024
```

The later negative tendency survives the matched initialization. That residual can come from observation/filter interaction, synthetic-world versus estimator assumptions, or other coupled effects. This diagnostic does not identify one of those as fact.

## Mode decomposition 🌦️

Default mean bias by true synthetic mode:

```text
Normal     -0.098
Busy       -0.100
Leave      -0.100
Special    -0.097
Recovery   -0.111
```

The values are close across modes. Recovery is slightly more negative, but no single mode carries the overall effect.

This makes a mode-specific Shared Context defect a weak explanation for the baseline-wide offset.

## Quiet-memory receipt 🍂

The observation-only reference gives Shared Context no action-driven accumulation input.

For two nearby no-input trajectories using the same memory law:

```text
delta[t+1] = (1 - lambda) * delta[t]
```

With `lambda = 0.0015`, the unclipped offset-retention ratio is:

```text
day 1      1.0000
day 30     0.9574
day 90     0.8749
day 180    0.7644
day 365    0.5790
```

So even after a synthetic year, about 58% of a small initial offset remains under pure quiet decay.

That is consistent with the intended role of `C` as slow memory.

> A slow reservoir preserves both useful history and initialization mistakes. 🧠🍂

## What #32 can conclude 🧭

```text
Observed
→ default C error is strongly offset dominated
→ default initial C prior is about 0.119 below synthetic truth C[0]
→ quiet no-input propagation predicts most of the default mean bias
→ matched initialization materially reduces bias/RMSE and restores coverage
→ a smaller later negative tendency remains after matching the start
→ mean bias is broadly similar across modes

Probable
→ initial prior mismatch + slow no-input memory explain most of the default baseline bias
→ the remaining late tendency comes from observation/filter interaction and/or synthetic-estimator mismatch

Assumed
→ the committed 365-day observation-only basket is a useful diagnostic reference
→ matched and mirror-high priors are diagnostic comparators, not production settings

Undefined
→ the correct universal initial C prior for real applications
→ the contribution of action-driven accumulation until the controlled #33 reference is evaluated

Not-yet-decided
→ whether future evidence warrants public initial-prior configurability
```

## Production decision ⚖️

No model change is justified by this result.

```text
SharedContextMemoryConfig.eta           → unchanged
SharedContextMemoryConfig.lambda        → unchanged
SharedContextMemoryConfig.process_noise → unchanged
C observation mapping                   → unchanged
production initial C prior              → unchanged
public API                               → unchanged
architecture 0.3                        → unchanged
```

Changing the production initial prior from `0.58` to the simulator's `0.70` merely because that improves this synthetic basket would let the estimator peek at the answer key.

The correct conclusion is narrower:

```text
the observation-only baseline carries an initialization mismatch
and the slow C reservoir preserves much of it
```

The action-aware comparison is deliberately left to #33, where action-driven Shared Context accumulation can be exercised without mutating this observation-only reference.

## Result basket ☕

```text
prior-summary.csv
error-track.csv
time-bias.csv
mode-bias.csv
quiet-memory.csv
shared-context-bias.png
recipe.json
```

## Validation ✅

- `15e74d42183da79ef61901fdc0ec53913bc4152d` — `🧠🌱 separate Shared Context shape from offset`
- `ad1e86c7f3a6cae40c502e74307af525b1f894b0` — `🧾🧠 keep the C-bias receipts visible in CI`
- `c0f6dd3fa0f995780f152024e14b86462ff5f78b` — `🍂📏 stop clipping the quiet C-memory receipt`
- `☕ Tiny Coffee Checks` run #149 — completed successfully
- pytest in run #149 — `134 passed`

## Boundaries

```text
Bias evidence != automatic tuning request
Shape tracking != unbiased estimation
Prior mismatch != broken memory law
Observation-only baseline != controlled routine
Synthetic result != human truth
```

The tiny coffee brain gets to keep its slow memory. It just has to admit when the first memory started from a different shelf. ☕🧠🐣
