# Tiny Change-Point Result ✂️🐣☕

This file is a **reproducible synthetic result snapshot**, not an architecture definition.

The reference boundary check uses:

```text
before world : cozy-normal-year
after world  : sleepy-reply-season
days         : 180
true boundary: day 91
min segment  : 24
seed         : 20260908
change prior : 0.20
```

Recorded CI result for this recipe:

```text
true boundary             = day 91
best detected boundary    = day 93
absolute timing error     = 2 days
P(change | clues)         = 0.968
stable-control P(change)  = 0.395
```

With the detection threshold of `0.80` used by that recipe:

```text
known persistent shift → DETECTED
stable control         → NOT DETECTED
```

Interpretation is intentionally narrow:

```text
The detector distinguished the injected synthetic shift from the paired stable control in this recipe.
```

It does **not** imply universal detector performance and it is not evidence about any real person or real routine.

For the detector design and limitations, see [`change-point-garden.md`](change-point-garden.md).
