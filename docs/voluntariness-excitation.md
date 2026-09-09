# Voluntariness Excitation Bench 🌿☕

## Why this exists

The observation-only 365-day reference gives `V = Voluntariness` relatively little truth variation and an awkward negative Pearson correlation.

That result is **Observed** for that synthetic recipe. The explanation was still **Probable / Undefined**, so #31 created a focused test that gives synthetic `V` much more room to move without changing CSRDM architecture `0.3`.

```text
Awkward metric != bug
Low excitation != zero information
Probability != fact
```

## What is deliberately controlled 🧪

The truth path is a focused diagnostic clamp:

```text
high V hold
    ↓
ramp down
    ↓
low V hold
    ↓
ramp up
    ↓
high V return
```

During this test:

```text
P / M / E / F → held at nominal estimator targets
C             → follows ordinary quiet-memory decay
mode          → Normal
V             → deliberately excited
```

This path is **Assumed synthetic test structure**, not ordinary CSRDM truth dynamics and not a claim about how real people change.

```text
Synthetic clamp != human law
Focused diagnostic != new model feature
```

## Which clues directly carry V? 🎛️

Under the current observation model, direct V coefficients exist only in a subset of channels:

```text
opt_in               +1.20
reaction             +0.40
routine_maintenance  +0.90
tone_warmth          +0.18
```

The remaining current direct coefficients are zero.

That statement means:

> the **current model specification** gives those channels no direct V term.

It does **not** mean a broader real-world relationship has been proven absent.

```text
model coefficient = 0
!=
real relationship proven absent
```

`pass_event` is especially important here: in the observation-only likelihood it has no direct V coefficient. A voluntary pass can preserve V through the **action-aware transition path**, but that is a different architecture path and belongs to the separate controlled-reference work in #33.

The diagnostic writes `channel-sensitivity.csv` directly from `DEFAULT_OBSERVATION_MODEL` so this map does not need to be maintained by hand.

## Reproducible bench 🌱

```bash
python -m tiny_tools.excite_voluntariness \
  --days 180 \
  --particles 1200 \
  --low-v 0.58 \
  --high-v 0.94 \
  --seed 20260908 \
  --out .tiny-v-excitation
```

Outputs:

```text
summary.csv
v-track.csv
channel-sensitivity.csv
recipe.json
v-excitation.png
```

`summary.csv` includes both the deliberate excitation result and, when available, the committed observation-only 365-day baseline for context.

## Observed result 🔍

The CI reference run used the exact command above.

```text
truth V std               = 0.1498
truth V span              = 0.3600
estimate V std            = 0.0143
V RMSE                    = 0.1699
V MAE                     = 0.1352
V Pearson r               = +0.1802
V 95% interval coverage   = 55.56%
excitation std / baseline = 6.29x
baseline V Pearson r      = -0.1688
```

So the negative sign **did not persist** once V received much stronger excitation.

But the stronger conclusion is not “V is fine.” The posterior still moved far too little:

```text
truth std    ≈ 0.1498
estimate std ≈ 0.0143
```

The estimate carried only about one tenth of the truth variation, RMSE increased substantially under the stress test, and interval coverage fell well below the nominal 95% target.

## What this does and does not justify 🧭

### Observed

```text
baseline r was negative under weak V excitation
focused-excitation r became positive
focused estimate amplitude remained strongly compressed
focused CI coverage was poor
```

### Probable

```text
weak baseline excitation contributed to sign instability
```

This is a reasonable interpretation because the sign changed when truth excitation increased by about `6.29x`.

### Still undefined

The bench does **not** isolate why the estimate amplitude stayed compressed.

Possible contributors include:

```text
strong V mean-reversion / narrow process dynamics
cross-state aliasing in shared observation channels
mode uncertainty
limited direct V information in the likelihood
protocol reconciliation changing effective clue information
some combination of the above
```

Those possibilities are not equivalent and should not be collapsed into one “V coefficient bug.”

## Decision gate outcome 🚪

The #31 decision gate lands in the middle:

```text
negative tracking did not persist
        +
adequate directional tracking did not emerge either
```

Therefore:

```text
Do not tune V coefficients here.
Do not declare the baseline negative r meaningless.
Open a narrower diagnostic issue for posterior compression.
```

The next diagnostic should separate **observation information** from **state-dynamics prior / cross-state aliasing** before any model change is proposed.

## Epistemic boundary 🧭

```text
Observed
→ metrics from one declared synthetic recipe

Probable
→ weak excitation contributed to the baseline sign instability

Assumed
→ current observation coefficients + deliberate V clamp

Undefined
→ exact cause of posterior compression and broader human relationships

Not-yet-decided
→ whether any core-model change is warranted
```

The bench reduced uncertainty, but it did not manufacture a final answer. That is the intended Phase 6 behavior. ☕🌿
