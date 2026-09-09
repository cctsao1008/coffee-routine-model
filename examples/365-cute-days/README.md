# 365 Cute Days 🗓️☕🌱

One tiny coffee routine.  
One whole synthetic year.  
Quite a lot of tiny particle friends.

## What's in this basket? 🧺

```text
input.csv
output.csv
metrics.csv
recipe.json
source-revision.txt
environment.txt
README.md
*.png
```

- `input.csv` — synthetic behavior-level clues only 👀
- `output.csv` — synthetic hidden truth + Particle Filter estimates 🐣
- `metrics.csv` — compact estimator scorecard; this is the metric source of truth ✨
- `recipe.json` — scenario / seed / days / particle count / architecture + runtime versions
- `source-revision.txt` — source commit that generated this committed basket
- `environment.txt` — exact Python package environment used by the packing workflow
- `*.png` — gallery rendered from the committed `output.csv`

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

The baseline output directory is automatically:

```text
examples/365-cute-days/
```

For byte-level investigation, also inspect `source-revision.txt` and `environment.txt` before comparing outputs.

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

It is a reproducible synthetic coffee world used to check whether the model behaves sensibly under one declared recipe. ☕🐾

## Why keep the full year? 🐣

A 365-day reference makes it easier to notice:

- slow drift 🌱
- busy patches 🌧️
- leave / interruption 💤
- recovery behavior 🌿
- special moments 🎂
- estimator uncertainty 🐣🐣🐣

The exact scorecard belongs in `metrics.csv`, not copied into several documents where it can quietly go stale.
