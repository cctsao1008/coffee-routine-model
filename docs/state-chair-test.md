# Tiny State Chair Test 🪑🐣☕

Six latent states are useful only if six distinct soft-state dimensions are actually buying us something.

The chair test asks:

> **Can one state be reconstructed or merged without much measurable loss?**

```text
More states != better model.
Fewer states != simpler truth.
Redundancy != permission to erase semantics.
```

## Three little diagnostics 🧭

### 1. Posterior estimate correlation

The tool measures correlation among filtered estimates of:

```text
P / M / V / C / E / F
```

High correlation is a warning light, not proof of redundancy.

### 2. Leave-one-state-out reconstruction

For each target state, a tiny ridge model uses the other five filtered estimates to reconstruct that target on a held-out synthetic validation segment.

It compares:

```text
direct filter RMSE
vs
reconstructed RMSE
vs
mean-only baseline RMSE
```

A small reconstruction penalty means the current model may not be using that state very independently.

### 3. Five-dimensional projection variants

The first candidates are:

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
binary observation NLL
warmth RMSE
log reply-delay RMSE
```

These are **projection/reconstruction diagnostics**, not fully retrained five-state Particle Filters. That distinction matters.

The test can tell us that a reduced representation looks competitive enough to investigate next. It cannot by itself prove that a smaller latent model is the final answer.

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

If `C` and `E` are highly correlated but `merge-C-E` noticeably damages observation NLL or held-out RMSE, that is evidence to keep them separate for now.

If `F` can be reconstructed cheaply and removing its independent chair barely changes predictive metrics, that would justify a proper reduced-model experiment later.

```text
Chair test -> evidence for the next model experiment.
Chair test != final ontology verdict.
```

Tiny chairs. Real diagnostics. No aesthetic symmetry tax. XD
