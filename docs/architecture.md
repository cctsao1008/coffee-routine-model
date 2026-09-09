# Tiny Coffee Brain Architecture 🗺️🏛️☕🐣

Architecture version: **`0.3`**

The model has enough features now.

This document defines the shape we intend to keep stable: the public boundary, the configuration tree, the experiment contract, and the internal model layers.

> **Feature growth is no longer the default. Architecture clarity is.**

```text
Cute outside.
Cute inside.
Math still works.
Architecture stays put. XD
```

## Story door before the math door 📖☕

A difficult model is easier to enter when the reader first sees a tiny observable story.
The story layer is optional and deliberately outside the core:

```text
Synthetic Persona Story
   Cheng / Linda example
            │
            ▼
      Persona / Protocol Adapter
            │
            ├──────────────┐
            ▼              ▼
      Observable Actions  Observations
            a_t              z_t
            │                │
            └───────┬────────┘
                    ▼
                CSRDM Core
```

The names are example costumes. They disappear before model semantics begin.

```text
Story != evidence
Persona != core ontology
```

## One tiny front door 🏛️☕

Normal callers should start here:

```python
from coffee_brain import CSRDM, CSRDMConfig

brain = CSRDM(CSRDMConfig())
result = brain.step(["+1?", "要", "☕", "👍"])

print(result.posterior.mean)
```

The public facade owns the plumbing between protocol events, action extraction, observations, filtering, and optional smoothing.

## Full vertical stack 🧠🌱

```text
               Optional Story / Persona Layer
                         │
                         ▼
                 ☕ Observable Events
                         │
                         ▼
              ┌──────────────────────┐
              │   Protocol Adapter   │
              └──────────┬───────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Observable Actions       Observations
             a_t                    z_t
              │                     │
              ▼                     │
    ┌──────────────────────┐        │
    │      CSRDM Core      │        │
    │ x_t = [P M V C E F] │        │
    │ hybrid mode m_t      │        │
    │ action dynamics      │        │
    │ context transitions  │        │
    │ C memory reservoir   │        │
    └──────────┬───────────┘        │
               │                    │
               └─────────┬──────────┘
                         ▼
              ┌──────────────────────┐
              │   Particle Filter    │
              │ p(x_t,m_t | z_1:t)  │
              └──────────┬───────────┘
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
          Posterior             History
               │                   │
               │                   ▼
               │            Particle Smoother
               │            p(x_t,m_t | z_1:T)
               │
    ┌──────────┴────────────────────────────┐
    ▼                                       ▼
Diagnostics                              Evaluation
observability                            model arena
calibration                              trade-offs
sensitivity
redundancy
recovery
change-point
    │
    ▼
Learning
bounded observation
parameter learning
```

## State contract 🧺🧠

```text
x_t = [P, M, V, C, E, F]
```

| State | Meaning |
|---|---|
| `P` | Predictability |
| `M` | Mutuality |
| `V` | Voluntariness |
| `C` | Shared Context |
| `E` | Everyday State Sharing |
| `F` | Friction |

The discrete routine mode remains:

```text
Normal · Busy · Leave · Special · Recovery
```

`C` is structurally special: it has a slow accumulation / decay / saturation memory law instead of ordinary daily-state drift.
That means ordinary target pull, mode drift, and generic process noise deliberately leave `C` alone.

The six-state definition is the architecture baseline, not an ontological claim.

## Controlled state-space contract 🎮👀

\[
x_{t+1} \sim p(x_{t+1}\mid x_t,m_t,a_t,d_t)
\]

\[
z_t \sim p(z_t\mid x_t,m_t)
\]

```text
a_t = observable actions
z_t = observable clues
d_t = explicit known disturbance / regime context
x_t = latent continuous state
m_t = latent discrete mode
```

Temporal alignment matters: the action basket supplied with update `t` drives the transition from the previous hidden state into the current hidden state. The first update has no preceding transition.

Actions and observations stay in separate baskets on purpose.

## One transition baseline, many synthetic worlds 🎲🌦️

The fixed estimator transition table has one structural source of truth in the core model.
Synthetic scenarios may copy or perturb that baseline, but the estimator does not import scenario definitions.

```text
Synthetic World != Estimator Assumptions
```

This keeps synthetic validation from becoming an exam where the estimator secretly owns the answer key.

## Unified configuration tree 🧺🎛️

```text
CSRDMConfig
├── dynamics
│   ├── process_noise_scale
│   └── optional fixed_transition override
├── memory
│   └── SharedContextMemoryConfig
├── observation
│   └── ObservationModelConfig
├── transition
│   └── optional ContextTransitionConfig
├── inference
│   ├── particle_count
│   ├── seed
│   └── record_history
├── smoothing
│   ├── enabled
│   ├── lag
│   └── full_history
├── learning
│   ├── enabled
│   ├── train_fraction
│   └── bounded_parameters_only
└── architecture_version
```

Architecture-defining numpy config tables are made physically read-only where practical; `frozen=True` alone is not enough to freeze array storage.

Default transition behavior remains the fixed stochastic matrix. Context-aware transitions stay **opt-in**.

```text
Model definition = code + config.
```

## Experiment contract 🛂🧪

Every serious future run should be describable by one `ExperimentSpec`:

```text
ExperimentSpec
├── scenario
├── days
├── seed
├── particle_count
├── dataset_identity
├── CSRDMConfig snapshot
└── architecture_version
```

The spec generates a deterministic recipe fingerprint.
Display names, timestamps, and output filenames do **not** enter that fingerprint.

```text
Same recipe -> same fingerprint.
Metric without recipe -> mystery bean. XD
```

## Public boundary vs internal drawers 🚪🧺

### Stable public surface

```text
coffee_brain.CSRDM
coffee_brain.CSRDMConfig
coffee_brain.CSRDMResult
coffee_brain.ExperimentSpec
coffee_brain.ExperimentResult
```

### Optional story surface

```text
examples/cheng_linda_story.py
```

### Internal / specialist surfaces

```text
CoffeeParticleFilter
particle genealogy / smoother internals
observation calibration helpers
change-point detector
sensitivity / redundancy benches
model arena runners
synthetic scenario generators
```

`CSRDM.particle_filter` exists as an explicit diagnostic escape hatch, not as the preferred application interface.

## Architecture invariants 🧠✨

```text
Story != Evidence
Persona != Core Ontology
Observation != Latent State
Action != Intention
Missing clue != zero
Ambiguous clue != forced story
Pass != Failure
Continuity != Obligation
Disturbance != Rupture
Sensitivity != Causality
Smoothing != rewriting history
Better fit != better model
Synthetic learning != real-human truth
Winner != truth
Model != Human
```

## What is deliberately outside the core 🙈☕

```text
persona-specific field names
deep neural networks
transformers
end-to-end learned latent semantics
unbounded parameter learning
online adaptation of every structural constant
one universal scalar relationship score
real-person ground-truth labels
```

Any future addition needs evidence that an existing layer cannot answer the problem cleanly.

```text
New algorithm because it exists                     -> no thanks 🐾
New algorithm because a measured limit requires it -> maybe ☕
```

## Freeze policy ❄️🏛️

Architecture `0.3` is the first **architecture-complete baseline**.

From here:

1. fix bugs,
2. improve tests,
3. improve calibration and validation,
4. improve story / documentation clarity,
5. add adapters or experiments when useful,
6. change the core shape only when evidence justifies it.

The tiny coffee brain is allowed to learn.

Its skeleton does not need to rearrange itself every morning. XDDD ☕🐣🧠
