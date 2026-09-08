# Coffee Routine Model ☕🐾✨

A tiny little model for a long-running coffee routine.

Somehow it has **states, memory, recovery, uncertainty, and a particle filter**.

Oops. XD

> **Humans are not state machines.**  
> Coffee routines are not either.

## House rule: everything must be cute ☕🌸

Yes, this is an actual repository rule. XD

README, docs, commits, tests, plots, CLI messages, issues, PRs... all of it.

The full tiny constitution lives in [`CUTE_RULES.md`](CUTE_RULES.md).  
The little history book lives in [`COFFEELOG.md`](COFFEELOG.md). 📖☕

```text
Cute != sloppy.
Cute math is still math. 🧠✨
```

## What's going on here? ☕💭

Someone asks:

```text
+1?
```

Someone replies:

```text
+
```

Coffee appears. ☕

Sometimes:

```text
pass
```

Sometimes people are busy.  
Sometimes replies are late.  
Sometimes the routine gets interrupted.

And somehow...

**it comes back tomorrow. 🌱**

This repo tries to model that little rhythm without pretending people are deterministic machines.

## Tiny protocol bridge ☕➡️🧠➡️🐣

The companion [`coffee-routine-protocol`](https://github.com/cctsao1008/coffee-routine-protocol) speaks tiny coffee language:

```text
+1?
+
要
對
👍
pass
☕
resume
```

`protocol_adapter.py` turns those observable events into behavior-level clues:

```python
from protocol_adapter import coffee_to_observation

obs = coffee_to_observation(["+1?", "+", "☕", "👍"])
```

which gives the model a little basket like:

```text
invite              = 1
opt_in              = 1
routine_maintenance = 1
reaction            = 1
```

The important bit:

```text
Protocol event != latent state
```

If a clue is missing, it stays `None`.  
If a token is ambiguous, it stays ambiguous.  
Silence is not secretly converted into yes or no. 🌱

Even `👍` is contextual: after `+1?` it can be an opt-in; after `☕` it can be a reaction. A lonely `👍` is allowed to remain mysterious. XD

Tiny bridge details live in [`docs/tiny-protocol-bridge.md`](docs/tiny-protocol-bridge.md).

## The tiny brain inside 🧠✨

The model watches six soft states:

| Symbol | Tiny meaning |
|---|---|
| `P` | Predictability — does the routine feel steady? |
| `M` | Mutuality — are both sides still participating? |
| `V` | Voluntariness — can either side still freely say `pass`? |
| `C` | Shared Context — is the little shared language/history growing? |
| `E` | State Sharing — are everyday states entering the interaction? |
| `F` | Friction — is coordination becoming annoying or costly? |

So the little state vector is:

```text
x(t) = [P, M, V, C, E, F]
```

There are also a few routine modes:

```text
Normal · Busy · Leave · Special · Recovery
```

## Tiny particle friends 🐣🐣🐣

We do **not** know the true hidden state.

So instead of making one confident guess, the model keeps many possible guesses at the same time.

Each particle says:

> Maybe the routine looks like this! ☕

Then new observations arrive:

```text
+
pass
👍
resume
late reply
```

The particles update their beliefs, unlikely guesses fade away, and plausible guesses survive.

That's the **Particle Filter**.

Missing clues are simply skipped instead of being filled with made-up neutral values.

**Cute outside. Probabilistic inside. ✨**

## A tiny but important rule 🌿

```text
Disturbance != Rupture
```

A missed day, a `pass`, a busy morning, or a late reply does not automatically mean the routine is broken.

The interesting question is whether the system can naturally recover.

## 365 cute days 🗓️☕🌱

The main demo runs **365 synthetic days** and the complete reference basket is committed in the repo.

One tiny coffee routine.  
One whole simulated year.  
Quite a lot of particles. XD

```text
examples/365-cute-days/
├── README.md       # tiny picnic map
├── input.csv       # 365 behavior-level synthetic observations
├── output.csv      # truth + posterior estimates + uncertainty
└── metrics.csv     # reference baseline scorecard
```

The baseline uses **6,000 tiny particle friends 🐣** and estimates the six hidden states from behavior-level observations only.

365-day baseline highlights:

- Relationship-index RMSE: `0.0185`
- Relationship-index MAE: `0.0135`
- Relationship-index correlation: `0.805`
- Mode classification accuracy: `82.2%`

These numbers only tell us that the estimator can work on a synthetic world we understand. They do **not** prove that a real human relationship follows the same equations.

The exact recipe is tucked into [`examples/365-cute-days/README.md`](examples/365-cute-days/README.md), and a tiny robot can repack it reproducibly. 🧺🤖

## Tiny coffee gallery 🎨☕🖼️

CSV is useful. CSV is not very cuddly. XD

`visualize.py` paints the full synthetic year into separate, readable little pictures. Every soft state gets its own plot with synthetic truth, Particle Filter estimate, and the 95% uncertainty blanket.

![One tiny coffee routine across one synthetic year](examples/365-cute-days/tiny-year-summary.png)

The gallery also contains:

```text
state-P.png   state-M.png   state-V.png
state-C.png   state-E.png   state-F.png
modes.png     ess.png       tiny-year-summary.png
```

The mode picture lets Busy, Leave, Special, and Recovery moments show up without pretending every interruption is a disaster. 🌧️💤🎂🌱

Paint it again with:

```bash
python visualize.py examples/365-cute-days/output.csv
```

```text
Cute plot != confusing plot.
Uncertainty is allowed to be visible. 🐣
```

### 100 cute days = quick coffee break ☕⚡

The old 100-day demo stays around as a quick smoke test:

```bash
python simulate.py --days 100
```

The main one-year demo is simply:

```bash
python simulate.py
```

or explicitly:

```bash
python simulate.py --days 365
```

Different lengths automatically go to their own tiny basket:

```text
examples/<days>-cute-days/
```

## Pick your coffee weather 🌦️☕

The synthetic world can now have different moods without teaching the Particle Filter the answer key.

```text
Synthetic World != Estimator Assumptions
```

Available tiny weather:

```text
🌤️ cozy-normal-year
🌧️ super-busy-month
🏖️ long-leave-and-return
💤 sleepy-reply-season
🎂 special-day-sparkle
🌪️ noisy-chaos-week
🌱 slow-recovery
```

For example:

```bash
python simulate.py --scenario slow-recovery --days 365
```

Alternate worlds get their own little cubby so they do not overwrite the cozy baseline:

```text
examples/365-cute-days/slow-recovery/
```

Same seed + same scenario + same settings = same tiny adventure. 🐾✨

## Tiny test nest 🐣✅

The particles are cute. They are still not allowed to misbehave. XD

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The nest checks state math, Particle Filter invariants, protocol adaptation, ambiguous events, missing clues, reproducible seeds, every little weather card, the painter, and small end-to-end scenario picnics.

When the command is green:

```text
☕✨ All tiny tests are happy.
```

## Run it ☕➡️🐣

```bash
python -m pip install -r requirements.txt
python simulate.py
python visualize.py
```

Want a shorter coffee break?

```bash
python simulate.py --days 100
```

Want to invite even more tiny particle friends?

```bash
python simulate.py --particles 10000
```

Want different weather?

```bash
python simulate.py --scenario noisy-chaos-week
```

## Related little project 🐾

[`coffee-routine-protocol`](https://github.com/cctsao1008/coffee-routine-protocol) defines the tiny interaction protocol:

```text
+1?  ->  + / pass
```

This repo looks at what might happen **over time** when those tiny interactions keep repeating.

## Philosophy ☕

```text
Observed behavior != internal truth
Continuity != obligation
Disturbance != rupture
Protocol event != latent state
Model != human
```

The model is allowed to be uncertain.

Humans are allowed to surprise it. XD
