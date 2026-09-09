# Tiny Recovery Meter 🌱🩹☕

## Why this exists

Busy days, leave, pauses, and delayed replies can disturb a routine without proving that the routine has failed.

So recovery is measured separately from disturbance.

The question is:

> **After a disturbance ends, how quickly and with how much explicit repair does the modeled routine return toward its nominal set?**

This is the deeper lab for [`tutorial/07-weather-and-recovery.md`](tutorial/07-weather-and-recovery.md).

```text
Disturbance != rupture
```

## Nominal routine set 🌿

The routine does **not** have to return to one exact equilibrium point.

Instead, recovery uses an acceptable region:

```text
E = nominal routine set
```

Each soft state has a center and a tolerance. If the state lies comfortably inside that region, its normalized distance is zero.

```text
dist(x, E) = 0  → inside the nominal region

dist(x, E) > 0  → outside the nominal region
```

This makes stability set-based rather than point-based.

## Disturbance windows 🌧️

The current recovery meter treats `Busy` and `Leave` modes as explicit disturbance windows.

A disturbance window has:

```text
start
end
duration
```

Recovery begins **after the disturbance itself ends**.

That distinction prevents a coordinated three-day leave from automatically looking less resilient than a one-day busy period merely because the disturbance lasted longer.

## Recovery time 🌱

For a disturbance ending at `t_end`:

```text
T_r = first k >= 0 such that x[t_end + k] is back inside E
```

Therefore:

```text
recovery_time = 0
```

means the first post-disturbance state is already back inside the nominal routine set.

## Repair cost 🩹

Recovery can happen naturally or require explicit coordination effort.

The current proxy counts action channels that look like repair or exception handling:

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

Ordinary coffee delivery is **not** billed as repair work. Neither is ordinary opt-in.

## Natural resume ☕🌱

```text
natural_resume = recovered with repair_cost == 0
```

This captures a simple observable pattern:

```text
interruption
    ↓
ordinary return
    ↓
no explicit repair proxy required
```

It does not assign hidden meaning to the return.

## Resilience score 🧠✨

For recovered disturbances:

```math
R_{resilience}=\frac{1}{1+T_r+\lambda C_r}
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

No unobserved recovery is invented.

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

## Important boundaries 🌿

```text
Disturbance != rupture
Long leave != slow recovery
Fast recovery != mandatory recovery
Repair cost != blame
```

The meter describes how the **routine dynamics** recover. It does not grade either person. ☕🐾
