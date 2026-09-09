# Math, One Sip at a Time ☕🧮

This folder has one job:

> **Let readers choose how much mathematics they want right now.**

There is still only **one CSRDM**.

```text
Starter Math
= the first mathematical view

Full Math
= the complete mathematical view

Architecture
= the software / implementation contract
```

```text
Same model.
Same example.
Different depth.
```

## Pick a door 🚪

### 🌱 Starter Math — [`starter-math.md`](starter-math.md)

Choose this if you understand variables and basic probability, but do not want the whole stochastic machinery yet.

You will meet:

```text
x_t  → the hidden routine state
z_t  → what we can observe
a_t  → known actions
w_t  → small uncertainty / disturbance
```

and only the equations needed to understand the model's main shape.

### 📐 Full Math — [`full-math.md`](full-math.md)

Choose this when you want the complete architecture `0.3` mathematical view:

```text
continuous hidden state
+ discrete mode
+ known actions
+ explicit context
+ observation likelihood
+ Shared Context memory
+ Particle Filtering
+ smoothing
```

### 🐣 Estimator / inference

If the main question is **how hidden state is estimated**, continue to:

- [`../tutorial/08-why-particles.md`](../tutorial/08-why-particles.md)
- [`../smoothing-garden.md`](../smoothing-garden.md)

### 🔬 Diagnostics

If the main question is **why we should trust any of this**, continue to:

- [`../observability-garden.md`](../observability-garden.md)
- [`../calibration-bench.md`](../calibration-bench.md)
- [`../sensitivity-map.md`](../sensitivity-map.md)
- [`../model-arena.md`](../model-arena.md)

## The little depth ladder 🪜

```text
☕ Story
   What happened?
        ↓
🌱 Intuition
   Why is counting not enough?
        ↓
🧮 Starter Math
   What are the variables and basic relationships?
        ↓
📐 Full Math
   What is the complete stochastic model?
        ↓
🐣 Inference
   How do we estimate hidden state?
        ↓
🔬 Diagnostics
   How do we challenge the assumptions?
```

This ladder is about **desired depth**, not educational credentials.

A reader can stop anywhere and still keep the same story and the same model.

```text
Simple != false
Plain language != missing rigor
Cute != childish
```
