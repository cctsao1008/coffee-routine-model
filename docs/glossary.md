# Glossary 📚☕

> **Document role:** Terminology index · **Authority:** Index only · **Audience:** Anyone looking up a recurring project term

A compact vocabulary map for Coffee Routine Model.

This page aligns wording and points to canonical sources. It is **not** a second specification.
If wording here conflicts with a specialist source, the specialist source wins.

```text
Glossary
= shared wording + pointers
!= new ontology
!= new architecture
!= mini textbook
```

For recurring misreadings rather than definitions, use [`common-confusions.md`](common-confusions.md).

## Quick index 🧭

- [Core model](#core-model-terms-) — CSRDM, routine, event, action, observation, latent state, mode, context
- [Six soft states](#the-six-soft-states-) — P, M, V, C, E, F
- [Inference](#inference-terms-) — Particle Filter, posterior, filtering, smoothing, ESS
- [Dynamics / memory](#dynamics-and-memory-terms-) — transition, action-aware dynamics, Shared Context memory
- [Validation](#validation-and-diagnostics-terms-) — observability, identifiability, calibration, sensitivity
- [Epistemics](#epistemic-status-terms-) — Observed, Probable, Assumed, Undefined, Not-yet-decided
- [Public / reproducibility](#public-surface-and-reproducibility-terms-) — API, baskets, ExperimentSpec, versions, release snapshot

## Naming aliases 🏷️

The project intentionally uses three naming layers for the six states:

| Conceptual name | Math shorthand | Public named-result key |
|---|---|---|
| Predictability | `P` | `predictability` |
| Mutuality | `M` | `mutuality` |
| Voluntariness | `V` | `voluntariness` |
| Shared Context | `C` | `shared_context` |
| Everyday State Sharing | `E` | `state_sharing` |
| Friction | `F` | `friction` |

```text
conceptual name → human-readable meaning
math shorthand  → equations / state vector
result key      → public API named view
```

These are aliases for the same six model dimensions, not three different ontologies.

See: [`public-api.md`](public-api.md), [`math/full-math.md`](math/full-math.md), [`architecture.md`](architecture.md)

## Source-of-truth rule 🧭

```text
architecture behavior → architecture.md
mathematics           → math/full-math.md
public calling rules  → public-api.md
epistemic categories  → epistemic-status.md
glossary              → concise lookup + canonical pointers
```

---

## Core model terms ☕🧠

### CSRDM

**Coupled Shared Routine Dynamics Model.** A stochastic model of a shared routine whose hidden condition changes over time and is inferred from observable events.

```text
shared-routine model != one person's personality model
model != ground-truth psychology meter
```

See: [`architecture.md`](architecture.md), [`math/full-math.md`](math/full-math.md)

### Routine

The repeated shared interaction pattern that CSRDM treats as its modeling object.

```text
Continuity != obligation
Pass != failure
```

See: [`how-the-coffee-works.md`](how-the-coffee-works.md), [`design-principles.md`](design-principles.md)

### Observable event

A behavior-level event explicitly supplied to the model or synthetic record, such as invite, opt-in, pass, reaction, maintenance, or resume.

```text
Observed event != internal truth
```

See: [`tiny-protocol-bridge.md`](tiny-protocol-bridge.md), [`epistemic-status.md`](epistemic-status.md)

### Protocol adapter

The boundary that translates story/protocol vocabulary into generic actions and observations before the mathematical core.

```text
story vocabulary → adapter → generic model fields
```

See: [`tiny-protocol-bridge.md`](tiny-protocol-bridge.md), [`architecture.md`](architecture.md)

### Action (`a_t`)

A known observable input that may affect the hidden-state transition.

```text
Action != intention
```

See: [`action-aware-dynamics.md`](action-aware-dynamics.md), [`public-api.md`](public-api.md)

### Observation / clue (`z_t`)

An observable value used to update uncertainty about hidden state and mode. A clue may be binary, continuous, or missing.

```text
Observation != latent state
Missing clue != zero
```

See: [`public-api.md`](public-api.md), [`observation-provenance.md`](observation-provenance.md)

### Latent state

A hidden model variable inferred probabilistically rather than directly measured.

```text
Model variable != measured human trait
```

See: [`math/starter-math.md`](math/starter-math.md), [`architecture.md`](architecture.md)

### Hidden state vector (`x_t`)

The six continuous latent states at time `t`:

```text
x_t = [P, M, V, C, E, F]
```

See: [`math/full-math.md`](math/full-math.md)

### Mode (`m_t`)

The latent discrete routine operating mode carried alongside `x_t`.

```text
Normal · Busy · Leave · Special · Recovery
Mode != regime
```

See: [`architecture.md`](architecture.md), [`math/full-math.md`](math/full-math.md)

### Context / disturbance (`d_t`)

Explicit known context or disturbance supplied to the transition process when available.

```text
Context input != intention
```

See: [`transition-weather.md`](transition-weather.md), [`architecture.md`](architecture.md)

---

## The six soft states 🧺

### Predictability (`P`, `predictability`)

How regular or expectable the shared routine currently appears under the model.

```text
Predictability != commitment
```

See: [`math/starter-math.md`](math/starter-math.md)

### Mutuality (`M`, `mutuality`)

Shared participation or contribution within the routine; exact symmetry is not required.

```text
Mutuality != 50/50 symmetry
```

See: [`design-principles.md`](design-principles.md)

### Voluntariness (`V`, `voluntariness`)

How much room the routine preserves for participation to remain optional rather than obligatory.

```text
Voluntariness != compliance
Voluntariness != liking
Voluntariness != future commitment
```

See: [`voluntariness-excitation.md`](voluntariness-excitation.md), [`v-dynamics-prior-result.md`](v-dynamics-prior-result.md)

### Shared Context (`C`, `shared_context`)

Slowly accumulated shared context derived from observable coordination. `C` uses its own memory path rather than ordinary daily drift.

```text
one quiet day != all shared context disappeared
```

See: [`memory-garden.md`](memory-garden.md), [`architecture.md`](architecture.md)

### Everyday State Sharing (`E`, `state_sharing`)

Ordinary state-sharing signals that become part of the routine's observable interaction pattern.

It is not a direct measure of emotional intimacy or private disclosure.

See: [`observation-provenance.md`](observation-provenance.md)

### Friction (`F`, `friction`)

Coordination difficulty or resistance within the routine.

```text
Friction != rupture
Friction != failure
```

See: [`architecture.md`](architecture.md)

---

## Inference terms 🐣📐

### Particle Filter

The sequential Monte Carlo estimator used to approximate the posterior with many weighted candidate states and modes.

```text
predict → score → normalize → resample when needed
```

See: [`tutorial/08-why-particles.md`](tutorial/08-why-particles.md), [`math/full-math.md`](math/full-math.md)

### Particle

One candidate hidden state + mode carried by the Particle Filter.

```text
particle != observed fact
```

### Posterior

The probability distribution over hidden state and mode after conditioning on available evidence under current model assumptions.

```text
Posterior probability != observed truth
Narrow posterior != automatically correct
```

See: [`epistemic-status.md`](epistemic-status.md)

### Filtering

Inference at time `t` using evidence available through time `t`.

```text
p(x_t, m_t | z_1:t)
```

### Smoothing

Using later observations to refine earlier posterior uncertainty.

```text
Smoothing != rewriting observed history
```

See: [`smoothing-garden.md`](smoothing-garden.md)

### Process noise

Uncertainty in how hidden state evolves between steps. It is transition uncertainty, not new evidence.

### Observation likelihood

The model-specified probability of seeing a clue under a candidate hidden state and mode.

```text
Assumed coefficient != discovered law
```

See: [`observation-provenance.md`](observation-provenance.md)

### Effective sample size (`ESS`)

A computational diagnostic for particle-weight degeneracy.

```text
high ESS → weight mass broadly distributed
low ESS  → few particles carry most weight
```

### Resampling

Refreshing the particle cloud by drawing more often from high-weight candidates when needed.

```text
Resampling != new evidence
```

See inference details: [`math/full-math.md`](math/full-math.md)

---

## Dynamics and memory terms 🌦️🧠

### Transition

Probabilistic evolution from one hidden state/mode to the next. Known actions and explicit context may influence it.

### Fixed transition baseline

The estimator's default five-mode transition matrix when context-aware transitions are disabled.

```text
Synthetic World != Estimator Assumptions
```

### Context-aware transition

An explicit opt-in mechanism that nudges mode-transition probabilities using declared state/action/context information.

It does not deterministically choose the next mode.

See: [`transition-weather.md`](transition-weather.md), [`public-api.md`](public-api.md)

### Shared Context memory

The dedicated bounded accumulation / decay / saturation mechanism for `C`.

See: [`memory-garden.md`](memory-garden.md)

### Action-aware dynamics

Transition behavior in which known observable actions may affect hidden-state evolution.

```text
Action-aware dynamics != causal identification
```

See: [`action-aware-dynamics.md`](action-aware-dynamics.md)

---

## Validation and diagnostics terms 🔬🧪

### Synthetic world

A simulator or scenario that generates actions/observations for testing.

```text
Synthetic World != Estimator Assumptions
```

### Synthetic reference

A reproducible synthetic run with its own recipe, environment, source revision, inputs, outputs, metrics, and plots.

```text
Synthetic reference != real-human validation
```

See: [`../examples/365-cute-days/`](../examples/365-cute-days/)

### Controlled reference

A separate synthetic reference that supplies known actions explicitly so action-aware behavior can be evaluated without mutating the observation-only baseline.

See: [`controlled-reference-result.md`](controlled-reference-result.md)

### Observability

Whether the available clues contain enough information to distinguish or constrain hidden states under the model.

```text
observable in principle != accurately estimated in every dataset
```

### Identifiability

Whether distinct parameter/state explanations can be uniquely distinguished from available evidence.

```text
Estimable != identifiable
Sensitivity != identifiability
```

See: [`state-chair-test.md`](state-chair-test.md), parked issue `#51`

### Calibration

Whether probability outputs keep their statistical promises across repeated evaluated cases.

```text
Calibration != ontology discovery
```

See: [`calibration-bench.md`](calibration-bench.md)

### Sensitivity

How much outputs change when assumptions or parameters are perturbed.

```text
Sensitivity != causality
```

See: [`sensitivity-map.md`](sensitivity-map.md)

### Change point

A possible persistent generating-process change rather than a one-step anomaly.

See: [`change-point-garden.md`](change-point-garden.md)

---

## Epistemic-status terms 🧭⚖️

### Epistemic status

The kind of basis supporting a claim, relation, or future event in this repository.

```text
Observed · Probable · Assumed · Undefined · Not-yet-decided
```

These are claim statuses, not latent states.

### Observed

Directly present in the declared input or synthetic record.

### Probable

A probabilistic statement conditioned on observations and model assumptions.

```text
Probability != fact
```

### Assumed

A structural hypothesis, prior, coefficient, transition rule, or synthetic recipe specified by the model/project.

```text
Assumption != evidence
```

### Undefined

A relationship the project intentionally does not claim or specify.

```text
Undefined relationship != zero relationship
```

### Not-yet-decided

A future action or choice that has not occurred yet, even if one outcome is historically very probable.

```text
High historical probability != future commitment
```

Canonical source for all five: [`epistemic-status.md`](epistemic-status.md)

---

## Public-surface and reproducibility terms 🚪🛂

### Public API

The stable caller-facing surface centered on `CSRDM`, `CSRDMConfig`, `CSRDMResult`, experiment recipe helpers, and declared configuration objects.

See: [`public-api.md`](public-api.md)

### Observation basket

The mapping of generic observation fields supplied to `CSRDM.update(...)`.

### Action basket

The mapping of known generic actions supplied with an update and associated with the preceding transition into the current state.

```text
first update → actions may be recorded, but no preceding transition exists
```

See baskets and timing: [`public-api.md`](public-api.md)

### Experiment specification (`ExperimentSpec`)

The reproducible run recipe: scenario, duration, seed, particle count, dataset identity, config snapshot, and architecture version.

### Recipe fingerprint

A deterministic identifier derived from the experiment recipe rather than display names, timestamps, or output filenames.

```text
Same recipe → same fingerprint
Metric without recipe → mystery bean
```

### Architecture version

The version of CSRDM's structural / mathematical model contract.

Current baseline:

```text
architecture 0.3
```

### Package version

The software distribution / release version.

Current formal package release:

```text
package 0.3.1
```

```text
package version != architecture version
```

### Release snapshot

The intentionally selected commit that a formal release tag points to.

For `v0.3.1`:

```text
808efbbab0b976eab507fb9272155c1cdb13c1b9
```

See: [`release-notes-0.3.1.md`](release-notes-0.3.1.md)

---

## One-page memory card ☕

```text
CSRDM             → model of the shared routine
x_t               → six soft latent states
m_t               → latent discrete mode
a_t               → known observable action
z_t               → observation clue
d_t               → explicit known context / disturbance
Particle Filter   → online posterior approximation
Smoothing         → later evidence refining earlier uncertainty
C memory          → slow dedicated Shared Context path
Observed          → directly in the declared record
Probable          → probability under model + evidence
Assumed           → structural model choice
Undefined         → intentionally not claimed
Not-yet-decided   → future choice has not occurred
architecture 0.3  → structural model version
package 0.3.1     → software release version
```

```text
Shared wording != duplicated authority
Compact glossary != mini textbook
```
