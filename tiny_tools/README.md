# Tiny Tools Map 🧰☕🐣

`tiny_tools/` contains runnable helpers for generating synthetic worlds, painting outputs, and challenging model assumptions.

These scripts are **diagnostic doors**, not extra ontology hiding beside CSRDM.

```text
model question
    ↓
one explicit helper
    ↓
reproducible synthetic run
    ↓
metrics / plots / limited conclusion
```

> **A tool should answer a question, not merely exist because we can write one.**

## Start here 🌱

### Generate one synthetic routine

```bash
python -m tiny_tools.simulate --scenario slow-recovery --days 365
```

`simulate.py` creates behavior-level clues, synthetic hidden truth, Particle Filter estimates, uncertainty bands, and metrics.

### Paint an existing simulator basket

```bash
python -m tiny_tools.visualize examples/365-cute-days/output.csv
```

`visualize.py` turns the CSV output into state, mode, ESS, and synthetic summary plots.

## Pick the modeling doubt you want to test 🧪

| Question | Helper | Deeper note |
|---|---|---|
| Can the clues distinguish the states? | `diagnose_observability.py` | [`../docs/observability-garden.md`](../docs/observability-garden.md) |
| Does V track when the synthetic truth is deliberately excited? | `excite_voluntariness.py` | [`../docs/voluntariness-excitation.md`](../docs/voluntariness-excitation.md) |
| Why does the excited V posterior stay compressed? | `diagnose_v_compression.py` | [`../docs/v-compression-result.md`](../docs/v-compression-result.md) |
| Do observation probabilities keep their promises? | `calibrate_observations.py` | [`../docs/calibration-bench.md`](../docs/calibration-bench.md) |
| Which assumptions move the answer most? | `map_sensitivity.py` | [`../docs/sensitivity-map.md`](../docs/sensitivity-map.md) |
| Does Shared Context accumulate and decay slowly? | `inspect_memory.py` | [`../docs/memory-garden.md`](../docs/memory-garden.md) |
| Does every state earn a separate chair? | `inspect_redundancy.py` | [`../docs/state-chair-test.md`](../docs/state-chair-test.md) |
| Does hindsight help without rewriting observed history? | `compare_smoothing.py` | [`../docs/smoothing-garden.md`](../docs/smoothing-garden.md) |
| Do known contexts improve mode-transition predictions? | `compare_transitions.py` | [`../docs/transition-weather.md`](../docs/transition-weather.md) |
| When does one odd day become evidence of a persistent shift? | `detect_change_points.py` | [`../docs/change-point-garden.md`](../docs/change-point-garden.md) |
| How does the synthetic routine return after disturbance? | `measure_recovery.py` | [`../docs/recovery-garden.md`](../docs/recovery-garden.md) |
| Can bounded observation knobs learn without rewriting the model? | `learn_parameters.py` | [`../docs/learning-spoon.md`](../docs/learning-spoon.md) |
| Can simpler / altered variants compete on the same basket? | `run_model_arena.py` | [`../docs/model-arena.md`](../docs/model-arena.md) |

## A useful order for experimenting 🧭

```text
simulate
   ↓
visualize
   ↓
observability + focused excitation + compression diagnosis + calibration
   ↓
sensitivity
   ↓
memory / smoothing / transitions / recovery
   ↓
redundancy / bounded learning / model arena
```

This is a learning order, not a mandatory pipeline.

## What these tools are allowed to conclude ⚖️

They can test code behavior and model assumptions inside explicit synthetic experiments.

They cannot turn synthetic success into claims about a real person's hidden state.

```text
Synthetic metric != human validation
Sensitivity != causality
Better fit != better ontology
Winner != truth
Model != human
```

Focused excitation and diagnostic perturbations add two more boundaries:

```text
Deliberately excited synthetic truth
!=
ordinary real-world trajectory

Diagnostic comparator
!=
production recommendation
```

## Where the stable API lives 🏛️

Applications should normally use:

```python
from coffee_brain import CSRDM, CSRDMConfig
```

The helpers in this folder may open specialist drawers because their job is diagnosis and experimentation. They are not the preferred application interface.

- [`../docs/architecture.md`](../docs/architecture.md) — stable architecture `0.3`
- [`../docs/tutorial/README.md`](../docs/tutorial/README.md) — why the model became this shape
- [`../examples/`](../examples/) — runnable story examples and reference baskets

Tiny tools make the model argue with itself. Nobody gets a crown for simply producing more CSVs. ☕🧠🐣
