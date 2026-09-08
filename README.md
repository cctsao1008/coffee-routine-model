# Coffee Routine Model ☕🐾✨

A tiny little model for a long-running coffee routine.

Somehow it has **states, memory, recovery, uncertainty, and a particle filter**.

Oops. XD

> **Humans are not state machines.**  
> Coffee routines are not either.

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

Cute outside. Probabilistic inside. ✨

## A tiny but important rule 🌿

```text
Disturbance != Rupture
```

A missed day, a `pass`, a busy morning, or a late reply does not automatically mean the routine is broken.

The interesting question is whether the system can naturally recover.

## 100 cute days 🗓️☕

The first demo contains 100 synthetic days:

```text
examples/100-cute-days/
├── input.csv
├── output.csv
└── metrics.csv
```

The current baseline uses **6,000 particles** and estimates the six hidden states from behavior-level observations only.

Synthetic baseline highlights:

- Relationship-index RMSE: `0.0213`
- Relationship-index MAE: `0.0164`
- Mode classification accuracy: `82%`

These numbers only tell us that the estimator can work on a synthetic world we understand. They do **not** prove that a real human relationship follows the same equations.

## Files 🧺

```text
coffee-routine-model/
├── README.md
├── model.py
├── particles.py
├── simulate.py
├── requirements.txt
├── docs/
│   └── how-the-coffee-works.md
└── examples/
    └── 100-cute-days/
        ├── input.csv
        ├── output.csv
        └── metrics.csv
```

## Run it ☕➡️🐣

```bash
python -m pip install -r requirements.txt
python simulate.py
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
Model != human
```

The model is allowed to be uncertain.

Humans are allowed to surprise it. XD
