# Tiny Routine → Model 📖☕🧠

This is the guided model-design tutorial for **Coffee Routine Model**.

The goal is not to prove that a coffee routine needs complicated math. The goal is to show, step by step, how a small repeated interaction can raise modeling questions — and how those questions can gradually produce a stochastic state-space model.

> **Observation first. Question second. Abstraction third. Math when it earns its place.**

The story layer uses **Cheng** and **Linda** as clearly synthetic teaching personas. The names make the examples easier to follow; the model itself remains generic.

```text
Synthetic story
    ↓
Observable events
    ↓
Modeling question
    ↓
Generic abstraction
    ↓
Math / code
    ↓
Diagnostics that challenge the abstraction
```

This tutorial does **not** publish private transcripts, timestamps, company facts, screenshots, or ground-truth claims about real people.

```text
Story != evidence
Persona != core ontology
Observation != latent state
Action != intention
Model != human
```

## A compact design-principle map first 🗺️🌱

If you want to see the recurring modeling problems before walking through all ten chapters, read [`../design-principles.md`](../design-principles.md).

It distills private design inspiration into public-safe principles such as:

```text
stable routine != entitlement
pass != failure
mutuality != 50/50 symmetry
disturbance != rupture
missing clue != zero
one anomaly != a new regime
high historical probability != future commitment
```

The document also marks what came later as **modeling interpretation** — for example the exact `P/M/V/C/E/F` ontology, Shared Context equation, Particle Filter, and diagnostic machinery.

```text
Recurring design problem can motivate an abstraction.
It does not prove the abstraction is true. ☕🧭
```

## The reading path 🌱

| Step | Question | Chapter |
|---:|---|---|
| 01 | What can we actually observe? | [`01-a-tiny-routine.md`](01-a-tiny-routine.md) |
| 02 | When does a tiny exchange become a protocol? | [`02-event-not-meaning.md`](02-event-not-meaning.md) |
| 03 | Why is `pass` not failure? | [`03-pass-is-not-failure.md`](03-pass-is-not-failure.md) |
| 04 | What should the hidden state describe? | [`04-six-soft-states.md`](04-six-soft-states.md) |
| 05 | Why separate actions from observations? | [`05-actions-vs-observations.md`](05-actions-vs-observations.md) |
| 06 | Why should Shared Context remember slowly? | [`06-shared-context-memory.md`](06-shared-context-memory.md) |
| 07 | Why do Busy, Leave, Special, and Recovery need modes? | [`07-weather-and-recovery.md`](07-weather-and-recovery.md) |
| 08 | Why does a Particle Filter appear naturally? | [`08-why-particles.md`](08-why-particles.md) |
| 09 | How do we challenge the assumptions we invented? | [`09-challenge-the-model.md`](09-challenge-the-model.md) |
| 10 | How do we let simpler or learned variants compete? | [`10-let-the-model-lose.md`](10-let-the-model-lose.md) |

Each chapter follows roughly the same rhythm:

```text
concrete situation
    ↓
modeling problem
    ↓
why the simpler idea is insufficient
    ↓
new abstraction
    ↓
code / equation
    ↓
next natural question
```

The compact principle map links each distilled lesson back to the chapters where the engineering response is taught, so the tutorial does not need to duplicate the source-inspired story in every chapter.

## Three doors, one model 🚪

This tutorial is the **learning path**.

For other kinds of reading:

```text
📖 Learn the design progressively
   → docs/tutorial/

📚 See the distilled design problems
   → docs/design-principles.md

🏛️ Look up the formal architecture contract
   → docs/architecture.md

🧪 Challenge specific assumptions
   → observability / calibration / sensitivity / recovery / arena docs

☕ Run synthetic stories
   → examples/
```

The tutorial intentionally does not duplicate every technical detail. When a question becomes deep enough, it links to the relevant lab or reference document.

## What you should know at the end 🎯

After these ten chapters, you should be able to explain:

- why observable events come before interpretation;
- why a simple coffee counter is not enough for this modeling exercise;
- why `P / M / V / C / E / F` exist;
- why `pass` protects Voluntariness instead of counting as failure;
- why actions and observations are separate;
- why Shared Context gets slow memory;
- why temporary modes differ from persistent regime change;
- why latent-state uncertainty leads naturally to Particle Filtering;
- why observability, calibration, sensitivity, and model comparison are needed to challenge the design;
- why synthetic success is still not evidence that real people follow the equations;
- why the history can explain **which modeling questions mattered** without becoming a public dataset or answer key.

If those ideas make sense, the scary-looking math has already lost most of its teeth. ☕🐣
