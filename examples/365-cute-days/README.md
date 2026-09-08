# 365 Cute Days 🗓️☕🌱

One tiny coffee routine.  
One whole synthetic year.  
Quite a lot of tiny particle friends. XD

## What's in this basket? 🧺

```text
input.csv
output.csv
metrics.csv
README.md
```

- `input.csv` — synthetic behavior-level clues only 👀
- `output.csv` — synthetic hidden truth + Particle Filter estimates 🐣
- `metrics.csv` — compact estimator scorecard ✨
- `README.md` — this tiny picnic map

## Tiny recipe ☕

```text
scenario  = cozy-normal-year
seed      = 20260908
days      = 365
particles = 6000
```

Regenerate the same basket with:

```bash
python simulate.py \
  --scenario cozy-normal-year \
  --days 365 \
  --particles 6000 \
  --seed 20260908
```

The baseline output directory is automatically:

```text
examples/365-cute-days/
```

## Important tiny honesty rule 🌿

```text
Synthetic reference != real human truth
```

Nothing in this folder is a private conversation export.
Nothing here is a screenshot.
Nothing here contains real names or raw messages.

It is a reproducible synthetic coffee world used to check whether the model behaves sensibly. ☕🐾

## Why keep the full year? 🐣

A 365-day reference makes it easier to notice:

- slow drift 🌱
- busy patches 🌧️
- leave / interruption 💤
- recovery behavior 🌿
- special moments 🎂
- estimator uncertainty 🐣🐣🐣

A hundred days is a nice coffee break.
A whole year is a tiny life. XD
