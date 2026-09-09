# v0.3.1 Release Candidate ☕📦🐣

This is the first formal release-ready package snapshot built on the architecture-complete CSRDM `0.3` baseline.

```text
Package / release version → 0.3.1
CSRDM architecture        → 0.3
Historical architecture tag → v0.3.0
```

The existing `v0.3.0` annotated tag is intentionally preserved as the earlier architecture-complete baseline. It points to commit `6449ed385fdcfb47f7bbb05c171a2d8e62d4d449` and is not moved.

```text
Historical tag != movable release pointer
Packaging patch version != architecture relabel
Release hygiene != model growth
```

## 🧠 Architecture baseline

Architecture `0.3` remains unchanged.

The six soft hidden states stay:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = Everyday State Sharing
F = Friction
```

This release work does **not** change latent-state meanings, Particle Filter equations, observation coefficients, transition laws, Shared Context memory law, or default inference behavior.

## 📖 Teaching and documentation

The public reading path separates depth instead of splitting the model:

```text
story
→ tutorial
→ Starter Math
→ Full Math
→ public API
→ architecture / diagnostics
```

The README remains the front door, while specialist material stays in `docs/`.

```text
Same model.
Same example.
Different depth.
```

## 🔬 Diagnostics and epistemic hygiene

Phase 6 diagnostics added explicit receipts for questions around:

- Voluntariness excitation and posterior compression;
- bounded dynamics-prior sensitivity;
- Shared Context bias decomposition;
- a separate known-action controlled reference;
- observation-model provenance and epistemic status.

The governing rule remains:

```text
Observed != Assumed
Assumed != Probable
Undefined != zero
Better fit != better ontology
```

Result snapshots stay at their dedicated scorecard / result sources instead of being copied into release prose and allowed to drift.

## 🛠️ Public API fixes

The stable `CSRDM` facade fails earlier on confirmed caller mistakes, including:

- unknown observation keys;
- invalid binary or continuous clue values;
- contradictory reply-delay semantics;
- impossible protocol baskets;
- context-transition inputs when context-aware transitions are not enabled;
- hidden online-learning expectations that the facade does not perform.

Readable named posterior views and first-step transition visibility were added without removing raw posterior access.

```text
Public guardrail != new ontology
Input validation != model inference
```

See [`public-api.md`](public-api.md) for the calling contract.

## 📦 Packaging and installation

The repository has a minimal `pyproject.toml` package boundary.

Ordinary installation from a checkout is:

```bash
python -m pip install .
```

The installed distribution includes:

```text
coffee_brain
tiny_tools
```

`requirements.txt` remains a readable runtime-dependency mirror for repo-local tooling and CI, while package installers use `pyproject.toml` metadata.

Supported Python is intentionally declared as:

```text
Python >= 3.12
```

because Python 3.12 is the version exercised by the main CI and reproducibility receipts. Broader support should be claimed only after it is tested.

## 🧺 Reproducibility receipts

The committed 365-day observation-only reference keeps its own reproducibility basket under:

```text
examples/365-cute-days/
```

That basket owns its recipe, environment, source revision, inputs, outputs, metrics, and plots.

The known-action controlled reference remains separately generated so observation-only and action-aware claims do not get mixed together.

```text
Synthetic reference != real-human validation
Synthetic World != Estimator Assumptions
```

## ⚖️ License

The repository uses the **MIT License**.

The authoritative legal text lives at:

```text
LICENSE
```

The package metadata declares the same MIT license and points packaging tools at that root license file. The README carries only a human-facing pointer back to the authoritative text.

```text
LICENSE           → legal source of truth
README            → human-facing pointer
pyproject.toml     → package metadata
```

## 🚪 Release gate

Before `v0.3.1` becomes a formal GitHub Release:

- package version must be `0.3.1` while architecture remains `0.3`;
- installed-package smoke CI must pass from outside the source tree;
- normal project CI must remain green;
- the final snapshot commit must be intentionally selected;
- a **new** `v0.3.1` tag must point at that selected snapshot.

The existing `v0.3.0` tag stays untouched as historical architecture provenance.

Until those gates close, this document describes the `v0.3.1` release candidate. ☕📦🐣
