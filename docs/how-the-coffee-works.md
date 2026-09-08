# How the Coffee Works ☕✨

This project started with a very small question:

> What happens when two people keep a tiny voluntary routine going for a long time?

No grand theory required. Just coffee. XD

## 1. The observable layer 👀

The model only gets behavior-level observations, for example:

```text
+1?
+
pass
👍
late reply
resume
```

It does **not** get direct access to anyone's internal state.

That distinction matters:

```text
Observed behavior != internal truth
```

## 2. The six soft states ☕🧠

We keep six slowly changing variables:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = State Sharing
F = Friction
```

They are not labels for a person.

They are just a compact way to describe how the **routine itself** appears to be behaving over time.

## 3. Why `pass` is important 🌿

A routine is more interesting when it remains voluntary.

If either side can still say:

```text
pass
```

and the routine can later return naturally, that tells us something different from a routine that continues only because it became an obligation.

So this project keeps this little rule close:

```text
Continuity != obligation
```

## 4. Disturbance is allowed 🌧️➡️🌱

People get busy.

People take leave.

People reply late.

Plans fail.

The model therefore does not treat every interruption as a collapse.

Instead, it watches whether the routine can recover:

```text
Disturbance != rupture
```

The current modes are:

```text
Normal
Busy
Leave
Special
Recovery
```

## 5. Why particles? 🐣🐣🐣

Because uncertainty is the honest answer.

Instead of keeping exactly one hidden-state guess, the model keeps thousands of little guesses.

Each particle carries a possible:

```text
[P, M, V, C, E, F]
```

New observations change the weights of those guesses.

Plausible ones survive.

Unlikely ones fade away.

That is the basic idea behind the Particle Filter used here.

## 6. What this project is *not* 🚫🔮

It is not a mind reader.

It is not a relationship-score machine.

It is not a deterministic predictor of human behavior.

It is not allowed to say:

```text
"This number proves what somebody truly feels."
```

The model is a structured way to track uncertainty in a repeated interaction.

That's all. ☕

## 7. The first reference protocol 🐾

The companion project [`coffee-routine-protocol`](https://github.com/cctsao1008/coffee-routine-protocol) describes the tiny interaction protocol itself.

This repo starts one layer later:

```text
Coffee Routine Protocol
        ↓
Observable events
        ↓
Coffee Routine Model
        ↓
Particle Filter
        ↓
Soft state distribution
```

Tiny protocol. Tiny model. Suspiciously serious math. XD
