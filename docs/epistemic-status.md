# Epistemic Status Contract 🧭☕

This document answers a question that sits underneath the whole repository:

> **What kind of thing is this statement?**

Coffee Routine Model should not collapse everything into `evidence / no evidence` or `true / false`.
Some things are observed. Some are probabilistic. Some are structural assumptions. Some relationships are intentionally left undefined. Some future actions are simply not decided yet.

The contract is:

```text
Observed
Probable
Assumed
Undefined
Not-yet-decided
```

These labels are not new latent states. They describe the **epistemic status of a claim, relation, or future event**.

```text
Probability != fact
Assumption != evidence
Undefined relationship != zero relationship
Missing clue != zero
High historical probability != future commitment
```

## 1. Observed 👀

**Observed** means the event or value is directly present in the declared input / synthetic record.

Synthetic example:

```text
Cheng: +1?
Linda: pass
```

The adapter may record:

```text
invite = 1
pass_event = 1
```

Those event fields are observed for that step.

What is **not** observed:

```text
private motive
private emotion
future choice
latent V
```

A recorded event can support inference, but the event itself should not be silently upgraded into an internal-state fact.

```text
Observation != latent state
```

## 2. Probable 🐣

**Probable** means the statement comes from a probability distribution conditioned on observations and model assumptions.

For example, a Particle Filter may produce:

```text
P(Busy at t | observations so far) = 0.37
```

or a posterior over `V = Voluntariness`.

That means:

> under the current model and current clues, some hidden explanations are more plausible than others.

It does **not** mean:

```text
Busy is an observed fact
V is directly measured
posterior confidence proves model correctness
```

```text
Posterior probability != observed truth
Narrow posterior != automatically correct
```

## 3. Assumed 🎛️

**Assumed** means the relation exists because the current model deliberately specifies it as a structural hypothesis, prior, coefficient, transition rule, or synthetic-world recipe.

Example:

```text
b_pass_choice
→ small boundary-preserving action effect on V
```

That is an inspectable model choice. It is not a discovered universal human law.

Likewise, hand-set observation coefficients describe the current prototype's likelihood structure.

```text
Assumed coefficient != discovered law
Structural prior != empirical fact
```

An assumption may later be calibrated, challenged, replaced, or left as a transparent modeling choice.

## 4. Undefined 🌫️

**Undefined** means the project intentionally does not claim a relationship yet.

This is different from zero.

Suppose the current prototype gives one observation channel a coefficient of `0` for state `P`.
Inside that particular mathematical specification, the direct coefficient is zero.
But the broader real-world relationship may still be **undefined** by this repository.

So keep two levels separate:

```text
model coefficient = 0
        !=
real relationship proven absent
```

Other useful distinctions:

```text
missing observation != observed zero
undefined relation  != negative relation
not modeled directly != impossible
```

Leaving a relation undefined is a valid design decision when specifying it would create false precision.

## 5. Not-yet-decided 🌱

**Not-yet-decided** is slightly different from the other four statuses.
It is primarily a status for a **future action or choice**, not a truth claim about the current hidden state.

A long history can make one next event highly probable:

```math
P(a_{t+1}=\text{opt-in}\mid H_t) \rightarrow 1
```

but until the next observable choice occurs:

```text
a[t+1] is still not-yet-decided
```

High predictive probability does not create commitment.

That distinction is especially important for a voluntary routine:

```text
stable history
+ high next-step probability
!= default entitlement
```

A new `+1?` still leaves room for `opt_in` or `pass`.

```text
Continuity != obligation
High historical probability != future commitment
```

## One synthetic example, five statuses ☕🧺

Suppose the history contains many ordinary opt-ins, then today:

```text
+1?
pass
```

A careful description can be:

```text
Observed
→ invite=1, pass_event=1

Probable
→ the posterior over V / mode changes under the current model

Assumed
→ CSRDM treats a clean voluntary pass as boundary-preserving rather than automatic failure

Undefined
→ the private motive for the pass is not specified by the model

Not-yet-decided
→ tomorrow's choice remains open even if historical opt-in frequency is high
```

Nothing needs to be forced into a stronger status than it has earned or been defined to have.

## Status can change over time 🔄

The categories are not permanent labels.

Examples:

```text
Not-yet-decided
→ Observed
when the future choice actually occurs

Undefined
→ Assumed
when a new model version explicitly introduces a structural relation

Assumed
→ challenged / recalibrated assumption
when diagnostics provide new information

Probable
→ different probability
when new observations arrive
```

But one transition is never automatic:

```text
Probable
→ Observed
```

A probability becoming large does not transform an unobserved event into an observed fact.

## Writing rule 📖⚖️

Before making a claim, ask:

```text
Is this...
Observed?
Probable under the model?
Assumed by the model?
Undefined by the project?
Not-yet-decided because it is a future choice?
```

Then choose language that matches.

| Status | Prefer | Avoid |
|---|---|---|
| Observed | `the event occurred` | adding an unobserved motive |
| Probable | `the posterior favors...` | `this proves...` |
| Assumed | `the model specifies...` | `the data discovered...` |
| Undefined | `the relation is not defined here` | treating it as zero / false |
| Not-yet-decided | `the next choice remains open` | treating historical probability as commitment |

## Model-change rule 🔧

Phase 6 does not require empirical proof before every model relationship can exist.
It requires clarity about what kind of basis currently supports the relationship.

```text
Observed result
      ↓
probabilistic interpretation
      ↓
structural assumptions + undefined parts
      ↓
is the proposed relation sufficiently specified?
      ↓
smallest justified change — or no change
```

Sometimes the correct result is a code fix.
Sometimes it is a narrower probability statement.
Sometimes the correct result is to keep a relation undefined.

```text
Not everything needs an answer.
Some things only need a probability.
Some things should remain undefined.
```

Architecture `0.3` is unchanged by this contract. The contract describes how claims about the architecture, experiments, and future choices should be interpreted. ☕🧭
