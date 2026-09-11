# Diagram Sources 🗺️☕

This directory holds reproducible **documentation diagram sources**.

They are not CSRDM model definitions and they do not participate in Python runtime behavior.

```text
README     → explains the system
Archify    → shows the system
Math docs  → defines the model
Issues     → explain the journey
Code       → proves the current state
```

## CSRDM — From Tiny Routine to Posterior

Source:

```text
csrdm-from-routine-to-posterior.dataflow.json
```

The source uses Archify's typed `dataflow` JSON IR. Its job is to visualize the already-documented architecture path:

```text
synthetic Cheng / Linda story
        ↓
observable events
        ↓
protocol adapter
   ↙             ↘
actions      observations
   ↘             ↙
      CSRDM dynamics
            ↓
      particle filter
            ↓
 posterior + uncertainty
       ↙           ↘
diagnostics     public API
```

The map intentionally keeps these boundaries visible:

```text
Observation != intention
Posterior != human truth
Model the routine, not the person
```

## Reproduce with Archify

The initial experiment is pinned to **Archify v2.16.0** rather than a moving `main` branch.

Release asset integrity used for this experiment:

```text
archify.zip
sha256: 4c59fa6557a2385beaaef8c7219cc414573acc9f0c30a932d5053b0b20689a46
```

After extracting the Archify release package so that its CLI is available at `<archify>/bin/archify.mjs`:

```bash
node <archify>/bin/archify.mjs validate \
  dataflow \
  docs/diagrams/csrdm-from-routine-to-posterior.dataflow.json \
  --json \
  --quality showcase
```

Then use verified delivery:

```bash
node <archify>/bin/archify.mjs deliver \
  dataflow \
  docs/diagrams/csrdm-from-routine-to-posterior.dataflow.json \
  docs/diagrams/csrdm-from-routine-to-posterior.html \
  --json \
  --quality showcase
```

The generated HTML should only be promoted into README/docs after it passes Archify's validation and is visually clearer than the existing text diagram.

## Scope boundary

Archify is a **documentation tool only** here.

Do not add it to the Python package runtime dependencies. Do not let the diagram invent components, behavior, relationships, or epistemic claims that are absent from the current architecture/docs/code.

```text
Diagram != architecture authority
Generated artifact != new model claim
```

The experiment and its conclusions are tracked in GitHub Issue #66.
