# Controlled Action-Aware Reference 🎮☕🐣

The original `examples/365-cute-days/` basket stays an **observation-only baseline**.

This reference exists for a different question:

> What happens when one declared generic action schedule is supplied to both the synthetic truth dynamics and the Particle Filter using the architecture's existing temporal contract?

## Scope

```text
separate controlled synthetic reference
truth actions supplied                  = true
particle-filter actions supplied        = true
controlled state-transition path        = exercised
Shared Context action accumulation      = exercised
observation-only baseline mutated       = false
person-specific ontology                = false
human-validation claim                  = false
```

This is validation coverage, not a new model feature.

## Action grammar

The reference repeats a small generic cycle:

```text
ordinary-opt-in
callback-opt-in
voluntary-pass
coordinated-exception
recovery-return
quiet
```

The concrete control fields remain the architecture's existing generic actions:

```text
a_invite
a_deliver
a_notify
a_callback
a_boundary_preserving
b_opt_in
b_pass_choice
b_acknowledge
b_exception_sync
b_closure
```

The schedule deliberately exercises invitation, delivery/acknowledgment, boundary-preserving pass, exception synchronization, callback/context memory, closure, and quiet steps.

`Action != intention` still applies.

## Temporal invariant ⏱️

The architecture already defines:

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

The current day's scheduled event may appear in the current observation basket, but it becomes a control only for the **next** hidden-state transition.

This avoids the easy but subtle off-by-one error where a reproducible test would exercise the wrong semantics.

## Shared Context path 🧠🌱

The same declared action schedule is passed to `generate_truth(..., actions=...)` and to the action-aware filter with the one-step temporal alignment above.

Therefore the reference exercises the existing reservoir law:

```text
C[t+1] = C[t]
       + eta * I(action[t]) * (1 - C[t])
       - lambda * C[t]
       + noise
```

No `eta`, `lambda`, process noise, observation coefficient, or production prior is tuned here.

## Two filter views

The same synthetic truth and observations are replayed through:

```text
action-aware
→ receives the known previous-step controls

action-blind
→ receives the same observations but no controls
```

The action-blind replay is a diagnostic comparator. A performance difference demonstrates that the known-control path matters in this declared synthetic world; it does **not** prove causal truth about humans.

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

The scorecard reports per-state bias, RMSE, MAE, Pearson correlation, and 95% interval coverage for both filter views.

The state-excitation audit reports truth range/std/span so a strong or weak score cannot quietly hide behind an unexcited state.

The recipe records architecture version, scenario, seed, particle count, environment, action grammar version, temporal contract, and the source revision that generated the basket.

## Reproduce it

```bash
python -m tiny_tools.controlled_reference \
  --days 96 \
  --particles 1200 \
  --seed 20260908 \
  --scenario cozy-normal-year \
  --out examples/controlled-cute-days
```

CI runs the same recipe into a scratch basket and checks the receipts.

## Epistemic boundary

```text
Known control != internal intention
Controlled reference != observation-only baseline
Synthetic truth != human truth
More path coverage != empirical validation
Better score != automatic parameter change
```

Architecture `0.3` remains unchanged. ☕🧠
