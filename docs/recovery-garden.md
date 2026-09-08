# Tiny Recovery Meter 🌱🩹☕

The model already knows that tiny routines can wobble:

```text
Busy
Leave
pass
late reply
Recovery
```

But a wobble should not automatically become a failure score.

So recovery is measured separately.

## Nominal routine set 🌿

The routine does **not** have to return to one magical exact equilibrium point.

Instead, recovery uses a small acceptable region:

```text
E = nominal routine set
```

Each soft state gets a center and a tolerance.
If the state lands comfortably inside that box, its normalized distance is zero.

```text
dist(x, E) = 0  -> comfortably inside

dist(x, E) > 0  -> outside the little routine neighborhood
```

## Disturbance windows 🌧️

The first recovery meter treats `Busy` and `Leave` modes as explicit disturbance windows.

A disturbance window has:

```text
start
end
duration
```

Then recovery begins **after the disturbance itself ends**.

That distinction matters.

A three-day planned leave should not automatically look less resilient than a one-day busy morning just because the leave lasted longer. XD

## Recovery time 🌱

For one disturbance ending at time `t_end`:

```text
T_r = first k >= 0 such that x[t_end + k] is back inside E
```

So:

```text
recovery_time = 0
```

means the first post-disturbance state was already back inside the nominal routine set.

## Repair cost 🩹

Recovery can happen naturally, or it can require explicit repair / coordination effort.

The current tiny proxy counts only action channels that look like repair work:

```text
notify
callback
boundary-preserving action
exception sync
closure
```

If explicit action baskets are unavailable, the model can fall back to a smaller observable proxy using:

```text
proactive_update
resume_signal
```

Ordinary coffee delivery is **not** billed as repair work.
Neither is ordinary opt-in.

## Natural resume ☕🌱

```text
natural_resume = recovered with repair_cost == 0
```

This captures the small but important pattern:

```text
interruption
    ↓
ordinary return
    ↓
no repair drama required
```

## Resilience score 🧠✨

For recovered disturbances:

```text
R = 1 / (1 + T_r + lambda * C_r)
```

where:

```text
T_r = post-disturbance recovery time
C_r = repair-cost proxy
```

If the routine never returns inside the nominal set during the available timeline:

```text
R = 0
```

No imaginary happy ending is inserted. 🐾

## Tiny recovery basket 🧺

Run:

```bash
python -m tiny_tools.measure_recovery
```

The tool writes:

```text
examples/recovery-garden/
├── events.csv
├── summary.csv
└── recovery-story.png
```

The picture shows one disturbance window and the normalized distance back toward the nominal set.

## Important tiny rules 🌿

```text
Disturbance != rupture.
Long leave != slow recovery.
Fast recovery != mandatory recovery.
Repair cost != blame.
```

The meter describes how the **routine dynamics** recover.
It does not grade either person. ☕🐾✨
