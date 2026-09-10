# How the Coffee Works ☕✨

> **Document role:** Gentle explanation · **Authority:** Explanatory · **Audience:** First-time readers

This is the short, gentle explanation of the project.

For the full step-by-step model-design story, start at [`tutorial/README.md`](tutorial/README.md).

## 1. Begin with observable events 👀

A tiny synthetic routine may contain:

```text
+1?
要
pass
☕
👍
busy
leave
resume
```

The model starts from events like these.

It does **not** get direct access to intention, private emotion, or hidden meaning.

```text
Observed behavior != internal truth
```

## 2. Simple counting is not enough 🧩

A coffee counter cannot distinguish:

```text
voluntary pass
busy interruption
leave
ordinary resume
broken coordination
```

So the project asks a different question:

> How might the **shared routine itself** be changing over time, given only observable clues and explicit known actions?

That is the purpose of the **Coupled Shared Routine Dynamics Model (CSRDM)**.

## 3. Six soft states describe the routine 🌱

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = Everyday State Sharing
F = Friction
```

They are latent model variables, not labels attached to a person.

```text
x_t = [P, M, V, C, E, F]
```

Read `x_t` as the hidden routine-state vector at time `t`.

A few important boundaries:

```text
Mutuality != 50/50 symmetry
Continuity != obligation
Pass != failure
```

## 4. Some days are different kinds of weather 🌦️

The model also carries a discrete routine mode:

```text
Normal
Busy
Leave
Special
Recovery
```

This lets a temporary interruption remain different from permanent structural failure.

```text
Disturbance != rupture
Mode != regime
```

## 5. Shared Context remembers slowly 🧠🌱

Accumulated conventions and recurring context should not disappear because one day is quiet.

So `C = Shared Context` uses a dedicated slow memory path rather than ordinary daily drift.

```text
one quiet day != no shared history
```

The detailed mechanism lives in [`memory-garden.md`](memory-garden.md).

## 6. Why particles? 🐣🐣🐣

The six states and five modes are hidden.

One quiet day may fit several explanations:

```text
ordinary noise
Busy mode
slightly higher Friction
missing clues with little state change
```

Instead of forcing one answer too early, the Particle Filter keeps many candidate hidden states and reweights them when new observations arrive.

```text
posterior = uncertainty under the current model
```

A narrow posterior is not proof that the model is correct.

## 7. The model also challenges itself 🔍🧪

The repository includes small labs for questions such as:

```text
Can the clues distinguish the six states?
Are the observation probabilities calibrated?
Which assumptions matter most?
Is one weird day really a change point?
Can a simpler model compete?
```

That is why observability, calibration, sensitivity, change-point, recovery, learning, and model-arena documents exist.

## 8. What this project is not 🚫🔮

It is not:

```text
a mind reader
a relationship-score machine
a deterministic human predictor
a ground-truth psychology dataset
```

It is a small teaching project about how a repeated observable routine can be turned into a stochastic model while keeping uncertainty and design boundaries visible.

## 9. Where to go next 📚

```text
Need terminology?
→ glossary.md

Common confusion?
→ common-confusions.md

Want the full learning path?
→ tutorial/README.md

Want the formal contract?
→ architecture.md

Want the documentation map?
→ README.md inside docs/

Want runnable examples?
→ ../examples/
```

Tiny story. Explicit assumptions. Serious enough math. ☕🐣🧠
