# v0.3.0 Architecture Tag Note 🏛️☕

`v0.3.0` is an existing annotated historical tag for the architecture-complete CSRDM `0.3` baseline.

```text
Tag      → v0.3.0
Commit   → 6449ed385fdcfb47f7bbb05c171a2d8e62d4d449
Meaning  → architecture-complete CSRDM 0.3 baseline
```

The tag predates the later Phase 6 public-API, packaging, license, and release-hygiene work. It is intentionally **not moved** to a newer commit.

```text
Historical tag != movable release pointer
Architecture version != package patch version
```

## What stays true

Architecture `0.3` remains the model baseline:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = Everyday State Sharing
F = Friction
```

The later Phase 6 work did not relabel that mathematical architecture.

## Why the formal release moves to v0.3.1

After the `v0.3.0` tag, the repository added substantial project-surface work around:

- progressive documentation and teaching depth;
- targeted diagnostics and epistemic provenance;
- stricter public API guardrails;
- clean package installation through `pyproject.toml`;
- installed-package smoke CI;
- MIT license alignment;
- release and reproducibility hygiene.

Those changes justify a package-level patch release without claiming a new CSRDM architecture.

```text
v0.3.0 → preserve historical architecture marker
v0.3.1 → formal release-ready package snapshot
CSRDM   → architecture 0.3 throughout
```

For the current formal release candidate, see [`release-notes-0.3.1.md`](release-notes-0.3.1.md).
