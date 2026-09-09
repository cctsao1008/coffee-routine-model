# Controlled Cute Days 🎮☕🐣

This folder is the declared home for the **separate controlled action-aware synthetic reference**.

It does **not** replace or reinterpret `../365-cute-days/`.

```text
365-cute-days/
→ observation-only historical reference basket

controlled-cute-days/
→ known-action path coverage for architecture 0.3
```

Generate the basket with:

```bash
python -m tiny_tools.controlled_reference \
  --days 96 \
  --particles 1200 \
  --seed 20260908 \
  --scenario cozy-normal-year \
  --out examples/controlled-cute-days
```

Expected receipts:

```text
action-schedule.csv
input.csv
output.csv
scorecard.csv
state-excitation.csv
summary.csv
scope.csv
recipe.json
```

The action grammar is generic. No person-specific ontology belongs in this reference.

> **Separate experiment != silent baseline drift.** ☕🌱
