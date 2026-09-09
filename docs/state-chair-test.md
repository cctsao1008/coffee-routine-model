# Tiny State Chair Test 🪑🐣☕

## Why this exists

Six latent states are useful only if six distinct dimensions are buying the model something measurable.

The chair test asks:

> **Can one state be reconstructed or merged without much measurable loss?**

This is a redundancy diagnostic linked from [`tutorial/09-challenge-the-model.md`](tutorial/09-challenge-the-model.md) and the model arena.

```text
More states != better model
Fewer states != simpler truth
Redundancy != permission to erase semantics
```

## Three little diagnostics 🧭

### 1. Posterior estimate correlation

The tool measures correlation among filtered estimates of:

```text
P / M / V / C / E / F
```

High correlation is a warning light, not proof of redundancy.

### 2. Leave-one-state-out reconstruction

For each target state, a small ridge model uses the other five filtered estimates to reconstruct that target on a held-out synthetic validation segment.

It compares:

```text
direct filter RMSE
vs
reconstructed RMSE
vs
mean-only baseline RMSE
```

A small reconstruction penalty means the current representation may not be using that state very independently.

### 3. Five-dimensional projection variants

The current candidates are:

```text
full-6
merge-C-E
reconstruct-C-from-other-5
reconstruct-E-from-other-5
reconstruct-F-from-other-5
```

Each candidate is scored on the same held-out synthetic segment for:

```text
mean / max state RMSE
relationship-index RMSE
Recovery-mode relationship-index RMSE
binary observation NLL
binary observation Brier score
warmth RMSE
log reply-delay RMSE
```

The Brier score checks probability calibration instead of judging reduced representations only by latent RMSE. Recovery-mode error asks whether a reduction keeps its shape specifically during synthetic recovery periods.

These are **projection/reconstruction diagnostics**, not fully retrained five-state Particle Filters.

That distinction is part of the experiment contract.

## Across tiny weather worlds 🌦️

By default the CLI repeats the chair audition across every public synthetic scenario:

```bash
python -m tiny_tools.inspect_redundancy \
  --scenario all \
  --days 120 \
  --particles 800 \
  --seed 20260908
```

Outputs:

```text
posterior-correlation.csv
posterior-correlation.png
reconstruction-scorecard.csv
variant-scorecard.csv
chair-summary.csv
```

## Reading the result carefully 🌱

If `C` and `E` are highly correlated but `merge-C-E` noticeably damages observation NLL, Brier score, held-out RMSE, or recovery fidelity, that is evidence to keep them separate under the current architecture.

If `F` can be reconstructed cheaply and removing its independent chair barely changes those metrics, that is evidence that a proper reduced-model experiment may be worth building.

It is not yet evidence that the ontology should be changed.

```text
Chair test → evidence for a model experiment
Chair test != final ontology verdict
```

Tiny chairs. Real diagnostics. No symmetry tax. 🪑☕
