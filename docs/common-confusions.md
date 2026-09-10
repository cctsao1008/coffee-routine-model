# Common Confusions ❓☕

> **Document role:** Explanatory correction · **Authority:** Pointer, not source of truth · **Audience:** Any reader who is about to over-interpret the model

This page answers recurring **category mistakes** quickly.
It does not replace the specialist documents linked under each answer.

```text
Glossary → what does this term mean?
Common Confusions → what is this term commonly mistaken for?
```

## Are `P / M / V / C / E / F` human personality traits?

**No.** They are latent variables in a model of the **shared routine**.

```text
Model variable != measured human trait
Model != human
```

See: [`architecture.md`](architecture.md), [`math/starter-math.md`](math/starter-math.md)

## Is Mutuality (`M`) the same as 50/50 symmetry?

**No.** Mutuality does not require equal contribution on every step.

```text
Mutuality != 50/50 symmetry
```

See: [`glossary.md`](glossary.md), [`design-principles.md`](design-principles.md)

## Does `pass` mean failure or rejection?

**No.** In this model, a clean voluntary pass can preserve Voluntariness rather than count as automatic failure.

```text
Pass != failure
Continuity != obligation
```

See: [`tutorial/03-pass-is-not-failure.md`](tutorial/03-pass-is-not-failure.md), [`epistemic-status.md`](epistemic-status.md)

## Does a narrow posterior mean the model is correct?

**No.** A narrow posterior means uncertainty is narrow **under the current model and supplied evidence**.
It does not validate the ontology or assumptions that produced it.

```text
Posterior certainty != model correctness
Probability != fact
```

See: [`math/full-math.md`](math/full-math.md), [`epistemic-status.md`](epistemic-status.md)

## Does `Missing` mean zero?

**No.** Missing means the clue was not observed for that step.

```text
Missing clue != zero
```

See: [`public-api.md`](public-api.md)

## Does an undefined relationship mean there is no relationship?

**No.** `Undefined` means the repository intentionally does not claim the relationship.
It is not the same as zero, false, negative, or impossible.

```text
Undefined relationship != zero relationship
```

See: [`epistemic-status.md`](epistemic-status.md)

## Does action-aware dynamics mean CSRDM can give causal advice?

**No.** Known actions can enter the transition model, but that does not by itself identify intervention effects or counterfactual truth.

```text
Action-aware dynamics != causal identification
Prediction != intervention effect
```

See: [`action-aware-dynamics.md`](action-aware-dynamics.md), parked issue `#53`

## Is a synthetic reference validation on real people?

**No.** Synthetic references are reproducible model tests generated under declared recipes.

```text
Synthetic reference != real-human validation
Synthetic World != Estimator Assumptions
```

See: [`../examples/365-cute-days/`](../examples/365-cute-days/), [`controlled-reference-result.md`](controlled-reference-result.md)

## Why is architecture `0.3` while the package is `0.3.1`?

They version **different boundaries**.

```text
architecture 0.3 → mathematical / structural model baseline
package 0.3.1    → formal software/package release
```

A packaging patch does not silently relabel the model architecture.

See: [`architecture.md`](architecture.md), [`release-notes-0.3.1.md`](release-notes-0.3.1.md)

## Does a high historical probability decide the next voluntary action?

**No.** A future choice can be highly probable and still remain not-yet-decided until it occurs.

```text
High historical probability != future commitment
```

See: [`epistemic-status.md`](epistemic-status.md)

## Does better fit mean a better ontology?

**No.** A benchmark can improve because of assumptions, flexibility, or tuning without demonstrating that the model's conceptual decomposition is more truthful.

```text
Better fit != better ontology
Winner != truth
```

See: [`model-arena.md`](model-arena.md), [`observation-provenance.md`](observation-provenance.md)

## The short version 🌱

```text
latent state      != human trait
Mutuality         != 50/50 symmetry
pass              != failure
posterior narrow  != model proven correct
missing           != zero
undefined         != absent
known action      != causal identification
synthetic success != real-human validation
package version   != architecture version
high probability  != future commitment
```

If you need the meaning of a term rather than a correction to a misconception, use [`glossary.md`](glossary.md). ☕📚
