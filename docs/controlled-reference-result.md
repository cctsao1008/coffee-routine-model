# Controlled Action-Aware Reference 🎮☕🐣

The original `examples/365-cute-days/` basket stays an **observation-only baseline**.

This reference asks a different question:

> What happens when one declared generic action schedule is supplied to both the synthetic truth dynamics and the Particle Filter using the architecture's existing temporal contract?

## Scope

```text
separate controlled synthetic reference
truth actions supplied                  = true
particle-filter actions supplied        = true
controlled soft-state transition path   = exercised
Shared Context action accumulation      = exercised
context-aware mode-transition model     = not enabled in this recipe
observation-only baseline mutated       = false
person-specific ontology                = false
human-validation claim                  = false
```

That distinction matters: `actions=` moves the six soft states and the Shared Context reservoir. This recipe deliberately leaves the optional `ContextTransitionConfig` off, so it is **not** a test of action-conditioned mode dice.

This is validation coverage, not a new model feature.

## Recipe

`☕ Tiny Coffee Checks` run **#151** used:

```text
days       = 96
particles  = 1200
seed       = 20260908
scenario   = cozy-normal-year
```

The generic action cycle repeats:

```text
ordinary-opt-in
ordinary-opt-in
callback-opt-in
voluntary-pass
quiet
coordinated-exception
quiet
recovery-return
ordinary-opt-in
callback-opt-in
quiet
ordinary-opt-in
```

Across 96 synthetic days:

```text
nonzero action days       = 72
mean Shared Context input = 0.458
```

The action grammar exercises:

```text
a_invite
a_deliver / b_acknowledge
a_notify
a_callback
a_boundary_preserving / b_pass_choice
b_exception_sync
b_closure
quiet steps
```

No person-specific ontology is used.

## Temporal invariant ⏱️

The implementation keeps the architecture contract:

```text
action[t-1]
    ↓
transition from hidden state[t-1]
    ↓
hidden state[t]
    ↓
observation[t]
    ↓
pf.update(observation[t], actions=action[t-1])
```

The first filter update receives no action because no previous transition exists.

Tests explicitly verify both sides of this timing rule:

- `generate_truth(...)` uses day `t` action for the transition into day `t+1`;
- the Particle Filter ignores a supplied action on its first update and applies it on the following transition.

## Shared Context result 🧠🌱

This is the strongest result from the reference.

Truth excitation:

```text
C truth min   = 0.7000
C truth max   = 0.8865
C truth std   = 0.0525
C truth span  = 0.1865
```

Same truth + same observations, two filter views:

```text
                    bias      RMSE      r        CI95
action-aware       -0.0373    0.0393   +0.9733   100.0%
action-blind       -0.1104    0.1284   -0.4544    31.3%
```

The action-aware estimator tracks the controlled `C` trajectory much more closely when it receives the same known controls that generated the synthetic Shared Context accumulation.

This directly sharpens the #32 conclusion:

```text
observation-only C bias
!= evidence that the slow-memory law is broken

known action accumulation restored
→ C shape tracking becomes strongly positive
→ absolute error drops materially
→ a smaller negative offset still remains
```

The remaining `-0.037` bias is not tuned away here.

## Whole-state scorecard

```text
state   aware RMSE   aware r    blind RMSE   blind r
P         0.0274      0.913       0.0776       0.854
M         0.0224      0.973       0.0601       0.913
V         0.0274      0.683       0.0616       0.410
C         0.0393      0.973       0.1284      -0.454
E         0.0915     -0.153       0.1720       0.232
F         0.0134      0.959       0.1102       0.499
```

The known-control path reduces RMSE for all six states in this recipe.

But the result is not uniformly strong in every sense:

- `E` has lower RMSE but weak/negative shape correlation;
- `V` has only `0.10` truth span and remains comparatively lightly excited;
- 95% coverage is very high for the action-aware run, so narrowness/calibration is not established by this reference.

Therefore the useful claim is **path validity under this synthetic recipe**, not universal state-estimation quality.

## Compact summary

```text
                     demo-index RMSE   demo-index r   mode accuracy
action-aware              0.00848         0.9826        84.38%
action-blind              0.04828         0.9396        84.38%
```

Mode accuracy is identical by design in this recipe. Known actions move the soft-state dynamics and Shared Context memory, while the optional context-aware mode-transition layer is not enabled.

That is a useful negative control: the reference exercises exactly the path it claims to exercise instead of quietly claiming more.

## Result basket

Running the reference produces:

```text
action-schedule.csv
input.csv
output.csv
scorecard.csv
state-excitation.csv
summary.csv
scope.csv
recipe.json
```

The recipe records architecture version, scenario, seed, particle count, environment, action grammar version, temporal contract, and source revision.

Reproduce it with:

```bash
python -m tiny_tools.controlled_reference \
  --days 96 \
  --particles 1200 \
  --seed 20260908 \
  --scenario cozy-normal-year \
  --out examples/controlled-cute-days
```

## Epistemic conclusion 🧭

```text
Observed
→ the known-action path runs end-to-end with correct one-step timing
→ Shared Context receives nonzero action-driven accumulation
→ controlled C truth is materially excited
→ action-aware C RMSE is far lower than action-blind C RMSE
→ action-aware C correlation is strongly positive
→ action-aware RMSE is lower for all six states in this recipe
→ mode accuracy is unchanged because context-aware mode transitions are not enabled

Probable
→ missing action-driven accumulation explains a substantial part of the observation-only C mismatch seen in #32
→ the remaining controlled C offset is smaller and should not be tuned away from this one reference

Assumed
→ this deterministic generic action cycle is a useful path-coverage recipe
→ the cozy synthetic world is an adequate integration-test environment

Undefined
→ correct action schedule distribution for real applications
→ real-world coefficient validity
→ whether action-aware mode-transition context improves a separate declared use case

Not-yet-decided
→ whether a future empirical dataset justifies any parameter change
```

## Validation

- `3c72bf3adb07311e7edc3e61e9f1a1e5fe15bea8` — `🎮☕ give known actions their own tiny reference basket`
- `☕ Tiny Coffee Checks` run #151 — **success**
- `138 passed`
- controlled-reference generation, receipt printing, and artifact-presence checks all succeeded

## Boundary preserved

```text
Known control != internal intention
Controlled reference != observation-only baseline
Synthetic truth != human truth
More path coverage != empirical validation
Better score != automatic parameter change
```

Architecture `0.3`, observation coefficients, action coefficients, memory law, and production priors remain unchanged. ☕🧠
