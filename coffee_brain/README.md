# Coffee Brain Core 🧠☕🐣

This folder contains the generic model implementation.

If you are using the project as an application, start with the public door instead of opening every drawer:

```python
from coffee_brain import CSRDM, CSRDMConfig

brain = CSRDM(CSRDMConfig())
result = brain.step(["+1?", "要", "☕", "👍"])
```

> **Public API first. Specialist internals only when the question actually needs them.**

## The little map 🗺️

```text
protocol / observable events
        ↓
protocol_adapter.py
        ↓
actions.py + observation basket
        ↓
api.py  →  CSRDM public facade
        ↓
config.py
        ↓
model dynamics / memory / mode transitions
        ↓
particles.py + observation_model.py
        ↓
posterior
```

The exact architecture contract lives in [`../docs/architecture.md`](../docs/architecture.md).

## Stable public door 🏛️

Normal callers should prefer the objects exported from `coffee_brain.__init__`:

```text
CSRDM
CSRDMConfig
CSRDMResult
ExperimentSpec
ExperimentResult
```

`CSRDM.particle_filter` exists as an explicit diagnostic escape hatch, not as the default application interface.

## Core drawers 🧺

| Drawer | Responsibility |
|---|---|
| `api.py` | stable `CSRDM` facade and online step contract |
| `config.py` | unified architecture/configuration tree |
| `protocol_adapter.py` | observable protocol events → generic actions / clues |
| `actions.py` | explicit controlled action basket and action effects |
| `model.py` | state names, modes, fixed transition baseline, compact synthetic demo index |
| `memory.py` | dedicated slow Shared Context memory law |
| `transitions.py` | optional context-aware stochastic mode transitions |
| `observation_model.py` | estimator-side observation probability assumptions |
| `particles.py` | Sequential Monte Carlo / Particle Filter inference |
| `smoothing.py` | optional genealogical hindsight without rewriting observed facts |
| `experiment.py` | reproducible experiment recipe and result contract |

## Specialist drawers 🔬

These exist to challenge or compare the model rather than define ordinary application flow:

```text
calibration.py
diagnostics.py
change_points.py
learning.py
arena.py
recovery.py
sensitivity.py
redundancy.py
```

The runnable fronts for those labs live in [`../tiny_tools/`](../tiny_tools/).

## Boundary rules ⚖️

The core stays generic on purpose.

```text
Persona != core ontology
Observation != latent state
Action != intention
Missing clue != zero
Pass != failure
Continuity != obligation
Disturbance != rupture
Model != human
```

Persona-shaped fields belong in examples or adapters at the edge, not inside Particle Filter likelihoods or state definitions.

Synthetic diagnostics may know synthetic truth. Production-facing inference does not get that privilege.

```text
Synthetic World != Estimator Assumptions
```

## Before changing the skeleton ❄️

Architecture `0.3` is the architecture-complete baseline.

Good reasons to edit the core:

```text
bug
broken invariant
clear calibration / validation evidence
adapter need that cannot be solved cleanly at the edge
measured limitation in an existing layer
```

Weak reason:

```text
"this algorithm looks cool"  → tiny coffee brain says no thanks ☕🐾
```

For the story of **why** these drawers exist, follow [`../docs/tutorial/README.md`](../docs/tutorial/README.md).

Cute outside. Generic inside. The math still has to behave. ☕🧠
