# Tiny Change-Point Garden ✂️🐣☕

Sometimes one day is unusual.

Sometimes the little process that generates the routine really changes.

Those are **not** the same thing.

```text
Mode != regime.
Anomaly != change point.
Change point != story conclusion.
```

## What the tiny scissors currently do 🧠

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

Missing values are temporarily imputed with the full-timeline feature mean during standardization, which makes a missing clue neutral in standardized space instead of secretly becoming zero.

## Candidate boundary score ✂️

For each candidate boundary `tau`, the detector compares:

```text
H0: one mean regime for the whole timeline
H1: one mean before tau + another mean after tau
```

The evidence score is deliberately simple and inspectable. Each active clue first gets its own BIC-like gain:

```text
gain_j(tau)
    = 0.5 * [SSE_j(H0) - SSE_j(H1) - log(T)]
```

where `j` is one observable clue and `T` is the number of days.

Then:

```text
score(tau) = sum of positive gain_j(tau)
```

If no clue earns a positive gain, the least-negative clue carries the score so `no change` still receives stronger evidence.

This makes the detector **sparse across clue channels**:

```text
one persistent delay shift
    -> pays one complexity penalty

one persistent delay shift
    -> does NOT pay eleven penalties
       for ten clues that stayed ordinary XD
```

The score is **not** treated as exact physical truth. It is an approximate log-evidence score for this detector family.

## Approximate boundary posterior 🐣

The model carries an explicit prior mass for:

```text
no change
one change somewhere
```

The one-change prior is divided across all admissible candidate boundaries before scores are normalized.

That matters because searching 300 possible days should not get 300 free lottery tickets. XD

Outputs include:

```text
P(no change | clues)
P(one change | clues)
P(tau | one change, clues)
```

plus a 90% conditional boundary interval.

## Why one weird day usually does not win 🌧️

A one-day spike may improve one split a little, but it usually cannot overcome:

```text
minimum segment length
+ per-clue complexity penalty
+ prior spread across many candidate days
```

A persistent before/after shift has much more accumulated evidence.

So:

```text
one weird day != new world
persistent generating shift -> maybe new regime
```

## Synthetic known-boundary garden 🌱

Run:

```bash
python -m tiny_tools.detect_change_points \
  --days 240 \
  --change-day 121 \
  --before cozy-normal-year \
  --after sleepy-reply-season
```

The helper grows one continuous hidden synthetic timeline and switches the **observation-generating weather** at the known boundary. It also grows a stable control timeline with no switch.

It writes:

```text
boundary-score.csv
summary.csv
change-point.png
```

The changed basket and stable control are both reported because a detector that finds a boundary everywhere is just a dramatic little pair of scissors. XD

## Current scope 🧺

This first detector is intentionally narrow:

- offline, not online
- one persistent change point at a time
- mainly sensitive to persistent mean shifts in observable features
- sparse across clue channels
- does not explain *why* the generating process changed
- does not yet make mode-transition dynamics regime-dependent

Later P2 work can extend this into multiple boundaries, richer likelihoods, and context-aware transition regimes.

Tiny scissors first. Chainsaw later. ✂️🐣
