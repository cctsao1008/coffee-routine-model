# 365 Cute Days 🗓️☕🌱

One tiny coffee routine.  
One whole synthetic year.  
Quite a lot of tiny particle friends.

## What's in this basket? 🧺

```text
input.csv
output.csv
metrics.csv
state-excitation.csv
recipe.json
source-revision.txt
environment.txt
README.md
*.png
```

- `input.csv` — synthetic behavior-level clues only 👀
- `output.csv` — synthetic hidden truth + Particle Filter estimates 🐣
- `metrics.csv` — compact estimator scorecard; this is the metric source of truth ✨
- `state-excitation.csv` — how much each synthetic truth state actually moved, plus simple estimate-offset context 🔍
- `recipe.json` — scenario / seed / days / particle count / architecture + runtime versions + declared reference scope
- `source-revision.txt` — source commit that generated this committed basket
- `environment.txt` — exact Python package environment used by the packing workflow
- `*.png` — gallery rendered from the committed `output.csv`

`state-excitation.csv` is intentionally **not** a second scorecard. Root mean squared error (RMSE), correlation, and interval coverage remain owned by `metrics.csv`.

## Tiny recipe ☕

The intended reference recipe is:

```text
scenario  = cozy-normal-year
seed      = 20260908
days      = 365
particles = 6000
```

`recipe.json` is the machine-readable receipt for the current committed run.

Regenerate the same logical basket with:

```bash
python -m tiny_tools.simulate \
  --scenario cozy-normal-year \
  --days 365 \
  --particles 6000 \
  --seed 20260908
```

The packing workflow also runs:

```bash
python -m tiny_tools.audit_reference examples/365-cute-days/output.csv
```

so the committed basket carries an excitation receipt beside the estimator scorecard.

The baseline output directory is automatically:

```text
examples/365-cute-days/
```

For byte-level investigation, also inspect `source-revision.txt` and `environment.txt` before comparing outputs.

## What this reference actually exercises 🔍🌱

This baseline is intentionally recorded as:

```text
reference_scope                          = observation-only baseline
action_schedule                          = none
particle_filter_actions_supplied          = false
controlled_transition_path_exercised      = false
shared_context_action_accumulation_exercised = false
```

Those fields are written into `recipe.json` by the pack workflow.

That means this 365-day basket is useful for checking:

```text
synthetic observation generation
protocol-semantic coherence
Particle Filter observation updates
latent-state / mode estimation under one declared synthetic world
uncertainty behavior
reference reproducibility
```

It is **not** the evidence source for claiming that the action-aware controlled transition path has been validated over a full synthetic year.

Likewise, Shared Context in this baseline is not being driven by a supplied action schedule, so this basket does not exercise action-driven `C` accumulation.

```text
Reference exists != every architecture path is exercised
```

If Phase 6 later earns a controlled/action-aware reference, it should be a separate declared experiment rather than a silent change to this baseline.

## Protocol grammar inside the synthetic world 🧭☕

The synthetic generator may disagree with the estimator assumptions on purpose, but the generated observable basket should still be semantically possible.

The reference packer checks invariants such as:

```text
opt_in and pass_event are not both true
opt_in / pass_event imply an observed reply
delivered-coffee maintenance requires opt-in
no observed reply means no invented finite reply delay
```

This is a generator constraint, not a claim that the Particle Filter likelihood must factor the channels in the same way.

```text
Synthetic World != Estimator Assumptions
Protocol grammar != estimator factorization
```

## Important tiny honesty rule 🌿

```text
Synthetic reference != real human truth
```

Nothing in this folder is a private conversation export.
Nothing here is a screenshot.
Nothing here contains real names or raw messages.

It is a reproducible synthetic coffee world used to check whether the model behaves sensibly under one declared recipe and one declared scope. ☕🐾

## Why keep the full year? 🐣

A 365-day reference makes it easier to notice:

- slow drift 🌱
- busy patches 🌧️
- leave / interruption 💤
- recovery-mode behavior 🌿
- special moments 🎂
- estimator uncertainty 🐣🐣🐣
- weakly excited states that make some metrics hard to interpret 🔍

The exact scorecard belongs in `metrics.csv`, not copied into several documents where it can quietly go stale.
The excitation receipt belongs in `state-excitation.csv`, so an awkward correlation can be inspected before anyone reaches for a tuning knob.

```text
Awkward metric != bug
Low excitation != permission to tune
```
