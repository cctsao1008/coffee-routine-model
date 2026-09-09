# Tiny Change-Point Garden ✂️🐣☕

## Why this exists

Sometimes one day is unusual.

Sometimes the process generating the observable routine really changes in a more persistent way.

Those are **not** the same modeling question.

```text
Mode != regime
Anomaly != change point
Change point != story conclusion
```

This lab answers the tutorial question: **when should a persistent shift be treated differently from one strange day?**

## What the tiny scissors do 🧠

`coffee_brain/change_points.py` implements a conservative **offline single-change-point detector** over observable clues.

The observation basket currently contains:

```text
invite
opt_in
text_reply
reaction
state_share
proactive_update
routine_maintenance
pass_event
resume_signal
tone_warmth
log(response_delay_min)
```

Missing values are temporarily imputed with the full-timeline feature mean during standardization, making a missing clue neutral in standardized space instead of silently turning it into zero.

## Candidate boundary score ✂️

For each candidate boundary `tau`, the detector compares:

```text
H0: one mean regime for the whole timeline
H1: one mean before tau + another mean after tau
```

Each active clue receives a BIC-like gain:

```text
gain_j(tau)
    = 0.5 * [SSE_j(H0) - SSE_j(H1) - log(T)]
```

where `j` is one observable clue and `T` is the number of days.

Then:

```text
score(tau) = sum of positive gain_j(tau)
```

If no clue earns a positive gain, the least-negative clue carries the score so `no change` can still retain stronger evidence.

The detector is sparse across clue channels:

```text
one persistent delay shift
    → pays one complexity penalty

one persistent delay shift
    → does not pay eleven penalties
      for ten clues that stayed ordinary
```

The score is **not** exact physical truth. It is an approximate log-evidence score for this detector family.

## Approximate boundary posterior 🐣

The model carries explicit prior mass for:

```text
no change
one change somewhere
```

The one-change prior is divided across all admissible candidate boundaries before scores are normalized.

That prevents a long search window from receiving many free chances to declare a change.

Outputs include:

```text
P(no change | clues)
P(one change | clues)
P(tau | one change, clues)
```

plus a 90% conditional boundary interval.

## Why one weird day usually does not win 🌧️

A one-day spike may improve one split slightly, but it usually cannot overcome:

```text
minimum segment length
+ per-clue complexity penalty
+ prior spread across candidate days
```

A persistent before/after shift accumulates more evidence.

```text
one weird day != new world
persistent generating shift → maybe a new regime
```

The word `maybe` matters: the detector identifies statistical structure, not a narrative explanation for why the structure changed.

## Synthetic known-boundary garden 🌱

Run:

```bash
python -m tiny_tools.detect_change_points \
  --days 240 \
  --change-day 121 \
  --before cozy-normal-year \
  --after sleepy-reply-season
```

The helper grows one continuous hidden synthetic timeline and switches the **observation-generating weather** at the known boundary. It also creates a stable control timeline with no switch.

It writes:

```text
boundary-score.csv
summary.csv
change-point.png
```

Both changed and stable controls are reported because a useful detector should not announce a boundary everywhere.

## Current scope 🧺

The detector is intentionally narrow:

- offline, not online;
- one persistent change point at a time;
- mainly sensitive to persistent mean shifts in observable features;
- sparse across clue channels;
- does not explain *why* the generating process changed.

Context-aware mode-transition dynamics already live elsewhere in the architecture. This detector remains a separate observable-regime diagnostic rather than silently becoming the controller for hybrid modes.

That separation preserves the current contract:

```text
Mode != regime
Detector != story generator
```
