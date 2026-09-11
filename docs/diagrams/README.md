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

Reproducible source:

```text
csrdm-from-routine-to-posterior.dataflow.json
```

Static SVG export:

```text
../assets/csrdm-from-routine-to-posterior.svg
```

Full interactive map:

```text
https://cctsao1008.github.io/coffee-routine-model/csrdm-from-routine-to-posterior.html
```

The three artifacts have deliberately different roles:

```text
JSON IR → reproducible source of the authored topology
SVG     → compact static export
HTML    → full-size interactive reading target
```

The SVG remains a compact static snapshot derived from the validated Archify export. The checked-in JSON IR remains the reproducible diagram source. The interactive HTML is generated and published by GitHub Actions after the same source passes Archify validation and delivery checks.

The README now links directly to the interactive map instead of embedding the static SVG, because the full node labels, route annotations, and legend are more legible at interactive scale. The SVG is retained as a companion export, not as a second source of truth.

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

The experiment is pinned to **Archify v2.16.0** rather than a moving `main` branch.

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

The Pages publication workflow repeats this validated delivery before publishing the interactive target. The published HTML is therefore a delivery artifact, not a separate hand-maintained source.

## Scope boundary

Archify is a **documentation tool only** here.

Do not add it to the Python package runtime dependencies. Do not let the diagram invent components, behavior, relationships, or epistemic claims that are absent from the current architecture/docs/code.

```text
Diagram != architecture authority
Generated artifact != new model claim
```

The initial experiment and README promotion are tracked in GitHub Issue #66. Interactive publication is tracked in GitHub Issue #70.
