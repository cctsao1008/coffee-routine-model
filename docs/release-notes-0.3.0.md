# v0.3.0 Release Candidate ☕📦🐣

This snapshot packages the first architecture-complete CSRDM baseline without pretending that packaging is a new mathematical model.

```text
Package / release version → 0.3.0
CSRDM architecture        → 0.3
```

```text
Release hygiene != model growth
Packaging != API redesign
```

## 🧠 Architecture baseline

Architecture `0.3` remains the model baseline.

The six soft hidden states stay:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = Everyday State Sharing
F = Friction
```

This release-candidate work does **not** change latent-state meanings, Particle Filter equations, observation coefficients, transition laws, Shared Context memory law, or default inference behavior.

## 📖 Teaching and documentation

The public reading path now separates depth instead of splitting the model:

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

The stable `CSRDM` facade now fails earlier on confirmed caller mistakes, including:

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

The repository now has a minimal `pyproject.toml` package boundary.

Ordinary installation from a checkout is:

```bash
python -m pip install .
```

The installed distribution includes the two runtime drawers used by public examples and tooling:

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

## ⚖️ License gate

No license is being chosen silently.

The formal GitHub Release remains blocked until the repository owner makes an explicit license decision and package / README metadata can be made consistent with it.

```text
No explicit license choice
→ no invented legal terms
→ no formal release yet
```

## 🚪 Release gate

Before `v0.3.0` becomes a formal GitHub Release:

- installed-package smoke CI must pass from outside the source tree;
- normal project CI must remain green;
- the final snapshot commit must be intentionally selected;
- the owner must make the license decision.

Until those gates close, this document describes a **release candidate**, not a published release. ☕📦🐣
