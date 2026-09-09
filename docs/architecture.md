# Tiny Coffee Brain Architecture 🗺️🏛️☕🐣

Architecture version: **`0.3`**

This document is the formal design contract for the current baseline. It defines the public boundary, configuration tree, experiment contract, and internal model layers.

> **Feature growth is not the default. Architecture clarity is.**

For the progressive learning path, start with [`tutorial/README.md`](tutorial/README.md). This file assumes the reader already understands why the main pieces exist.
For safe public calling behavior, use [`public-api.md`](public-api.md).

## Story door before the math door 📖☕

The optional story layer stays outside the core:

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

The names are teaching costumes. They disappear before architecture-defining model semantics begin.

```text
Story != evidence
Persona != core ontology
```

## One stable public door 🏛️☕

Normal callers should start here:

```python
from coffee_brain import CSRDM, CSRDMConfig

brain = CSRDM(CSRDMConfig())
result = brain.step(["+1?", "要", "☕", "👍"])

print(result.mean_by_state)
```

The public facade owns the plumbing between protocol events, action extraction, observations, filtering, and optional smoothing.
It also validates the public observation basket so typos and contradictory protocol values do not silently become different evidence.

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
                                   │
                                   ▼
                            Particle Smoother
                            p(x_t,m_t | z_1:T)

Diagnostics / Evaluation
├── observability
├── calibration
├── sensitivity
├── redundancy
├── recovery
├── change-point detection
├── bounded parameter learning
└── model arena / trade-offs
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

The discrete routine mode is:

```text
Normal · Busy · Leave · Special · Recovery
```

`C` is structurally special. It uses a dedicated slow accumulation / decay / saturation memory law rather than the ordinary daily-state drift used by `P / M / V / E / F`.

Therefore ordinary target pull, mode drift, and generic process noise deliberately leave `C` alone.

The six-state definition is the architecture baseline, not an ontological claim about people.

## Controlled state-space contract 🎮👀

```math
x_{t+1}\sim p(x_{t+1}\mid x_t,m_t,a_t,d_t)
```

```math
z_t\sim p(z_t\mid x_t,m_t)
```

```text
a_t = observable actions
z_t = observable clues
d_t = explicit known disturbance / context when available
x_t = latent continuous state
m_t = latent discrete mode
```

Temporal alignment matters: the action basket supplied with update `t` is associated with the transition from the previous hidden state into the current hidden state. The first update has no preceding transition.

`CSRDMResult.transition_applied` exposes that first-step boundary to public callers instead of leaving it implicit.

Actions and observations stay in separate baskets on purpose.

## One transition baseline, many synthetic worlds 🎲🌦️

The fixed estimator transition table has one structural source of truth in the core model.

Synthetic scenarios may copy or perturb that baseline, but the estimator does not import scenario definitions.

```text
Synthetic World != Estimator Assumptions
```

This keeps synthetic validation from becoming an exam where the estimator quietly owns the answer key.

The fixed transition matrix remains the default. Context-aware transitions are explicit opt-in behavior; see [`transition-weather.md`](transition-weather.md).

Public callers can opt into the current default context-aware transition recipe with `coffee_brain.DEFAULT_CONTEXT_TRANSITIONS`. Passing `transition_context` while context-aware transitions are disabled is rejected rather than silently ignored.

## Shared Context memory 🧠🌱

`C` owns one dedicated memory path:

```math
C_{t+1}=C_t+\eta I_t(1-C_t)-\lambda C_t+w_t^C
```

`I_t` is bounded shared-context input derived from observable coordination actions. The implementation keeps this path separate from ordinary state drift so two mechanisms do not compete to update the same state.

See [`memory-garden.md`](memory-garden.md).

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

Architecture-defining numpy tables are made physically read-only where practical; `frozen=True` alone does not freeze array storage.

```text
Model definition = code + config
```

`LearningConfig` is part of the architecture recipe, but the online `CSRDM` facade does not perform hidden online parameter learning. Bounded learning remains an explicit specialist bench.

## Experiment contract 🛂🧪

A reproducible run should be describable by one `ExperimentSpec`:

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

The spec generates a deterministic recipe fingerprint. Display names, timestamps, and output filenames do **not** enter that fingerprint.

```text
Same recipe → same fingerprint
Metric without recipe → mystery bean
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

### Public configuration / recipe helpers

```text
coffee_brain.DynamicsConfig
coffee_brain.InferenceConfig
coffee_brain.SmoothingConfig
coffee_brain.LearningConfig
coffee_brain.DEFAULT_CONTEXT_TRANSITIONS
coffee_brain.config_snapshot
```

These helpers do not expose Particle Filter internals. They make declared public configuration paths reachable without hidden repository imports.

### Optional story surface

```text
examples/cheng_linda_story.py
```

### Internal / specialist surfaces

```text
CoffeeParticleFilter
particle genealogy / smoother internals
observation calibration helpers
custom observation / memory / transition model internals
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
Mode != regime
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

A core change needs evidence that the existing layers cannot answer the problem cleanly.

```text
New algorithm because it exists                     → no
New algorithm because a measured limit requires it → evaluate
```

## Freeze policy ❄️🏛️

Architecture `0.3` is the first **architecture-complete baseline**.

From here:

1. fix bugs;
2. improve tests;
3. improve calibration and validation;
4. improve story / documentation clarity;
5. add adapters or experiments when useful;
6. change the core shape only when evidence justifies it.

The tiny coffee brain may learn. Its skeleton does not need to rearrange itself every morning. ☕🐣🧠
