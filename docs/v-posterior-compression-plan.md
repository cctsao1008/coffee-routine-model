# V Posterior Compression — Diagnostic Boundary 🌿🔬

This note exists because the deliberate Voluntariness excitation bench changed the question.

The baseline problem was:

```text
Why is V Pearson r negative?
```

The focused bench showed:

```text
negative sign disappears
but
posterior amplitude remains strongly compressed
```

So the next question is narrower:

> **Does the compression come mainly from observation information, the state-dynamics prior, cross-state aliasing, or mode uncertainty?**

This note is not a model change and does not choose an answer in advance.

## Candidate diagnostic layers

```text
1. Likelihood-only V slice
   hold P/M/C/E/F + mode fixed
   ask whether current observations distinguish low V from high V

2. Dynamics-prior comparison
   keep the same observation basket
   compare default V transition pressure with diagnostic-only relaxed dynamics

3. Cross-state aliasing check
   compare V-only inference against full six-state inference

4. Mode uncertainty check
   compare Normal-mode-fixed diagnostic against ordinary hidden-mode inference
```

Each layer should preserve the #30 epistemic contract:

```text
Observed metric != cause
Probable explanation != fact
Diagnostic perturbation != proposed production setting
Undefined cause != zero cause
```

No architecture `0.3` change is justified by this note alone.
