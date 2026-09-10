# Glossary 📚☕

A compact vocabulary map for Coffee Routine Model.

This page helps readers find a shared meaning quickly. It is **not** a second specification.
When a specialist document owns a definition or behavior, that document remains authoritative.

```text
Glossary
= shared wording + pointers
!= new ontology
!= new architecture
!= mini textbook
```

## Source-of-truth rule 🧭

```text
architecture behavior → architecture.md
mathematics           → math/full-math.md
public calling rules  → public-api.md
epistemic categories  → epistemic-status.md
glossary              → concise lookup + canonical pointers
```

If wording here ever conflicts with a specialist source, follow the specialist source.

---

## Core model terms ☕🧠

### CSRDM

**Coupled Shared Routine Dynamics Model.** The repository's stochastic model of a shared routine whose hidden condition changes over time and is inferred from observable events.

Not the same as:

```text
one person's personality model
a deterministic relationship score
a ground-truth psychology meter
```

See: [`architecture.md`](architecture.md), [`math/full-math.md`](math/full-math.md)

### Routine

The repeated shared interaction pattern that CSRDM treats as its modeling object.

A routine can continue, pause, recover, become easier or harder to coordinate, or contain voluntary passes without implying obligation.

```text
Continuity != obligation
Pass != failure
```

See: [`how-the-coffee-works.md`](how-the-coffee-works.md), [`design-principles.md`](design-principles.md)

### Observable event

A behavior-level event explicitly supplied to the model or synthetic record, such as an invite, opt-in, pass, reaction, routine maintenance event, or resume signal.

```text
Observed event != internal truth
```

See: [`tiny-protocol-bridge.md`](tiny-protocol-bridge.md), [`epistemic-status.md`](epistemic-status.md)

### Protocol adapter

The boundary that translates story/protocol vocabulary into generic model fields before the mathematical core begins.

```text
Persona / story vocabulary
→ protocol adapter
→ generic actions + observations
→ CSRDM core
```

See: [`tiny-protocol-bridge.md`](tiny-protocol-bridge.md), [`architecture.md`](architecture.md)

### Action (`a_t`)

A known observable input that may affect the hidden-state transition.

Actions are kept separate from observation clues on purpose.

```text
Action != intention
```

See: [`action-aware-dynamics.md`](action-aware-dynamics.md), [`public-api.md`](public-api.md), [`math/full-math.md`](math/full-math.md)

### Observation / clue (`z_t`)

An observable value used to score or update uncertainty about the hidden state and mode.

Observations may be binary, continuous, or missing.

```text
Observation != latent state
Missing clue != zero
```

See: [`public-api.md`](public-api.md), [`observation-provenance.md`](observation-provenance.md), [`math/full-math.md`](math/full-math.md)

### Latent state

A hidden model variable inferred probabilistically rather than directly measured.

CSRDM uses six soft latent states.

```text
Model variable != measured human trait
```

See: [`math/starter-math.md`](math/starter-math.md), [`architecture.md`](architecture.md)

### Hidden state vector (`x_t`)

The six continuous latent states collected into one vector at time `t`:

```text
x_t = [P, M, V, C, E, F]
```

See: [`math/starter-math.md`](math/starter-math.md), [`math/full-math.md`](math/full-math.md)

### Mode (`m_t`)

The discrete routine operating mode carried alongside the continuous state vector.

Current architecture `0.3` uses:

```text
Normal · Busy · Leave · Special · Recovery
```

Mode is latent and probabilistic; it is not an observed label unless an external input explicitly provides related evidence.

```text
Mode != regime
```

See: [`architecture.md`](architecture.md), [`math/full-math.md`](math/full-math.md)

### Context / disturbance (`d_t`)

Explicit known context or disturbance supplied to the transition process when available.

It is known input, not a hidden private story inferred by the model.

```text
Context input != intention
```

See: [`architecture.md`](architecture.md), [`transition-weather.md`](transition-weather.md)

---

## The six soft states 🧺

### Predictability (`P`)

A soft latent state representing how regular or expectable the shared routine currently appears under the model.

It is not a guarantee that the next event will occur.

```text
Predictability != commitment
High probability != future obligation
```

See: [`math/starter-math.md`](math/starter-math.md), [`architecture.md`](architecture.md)

### Mutuality (`M`)

A soft latent state representing shared participation or contribution within the routine.

It does not require exact symmetry or equal contribution on every step.

```text
Mutuality != 50/50 symmetry
```

See: [`README.md`](../README.md), [`architecture.md`](architecture.md)

### Voluntariness (`V`)

A soft latent state representing how much room the routine preserves for participation to remain optional rather than obligatory.

A clean pass can therefore be modeled as boundary-preserving rather than automatic failure.

Not the same as:

```text
compliance
liking
commitment
future willingness
```

See: [`epistemic-status.md`](epistemic-status.md), [`voluntariness-excitation.md`](voluntariness-excitation.md), [`v-dynamics-prior-result.md`](v-dynamics-prior-result.md)

### Shared Context (`C`)

A soft latent state representing slowly accumulated shared context from observable coordination.

`C` is structurally special: it uses a dedicated accumulation / decay / saturation memory path rather than the ordinary drift path used by the other five soft states.

```text
one quiet day
!=
all shared context disappeared
```

See: [`memory-garden.md`](memory-garden.md), [`architecture.md`](architecture.md), [`math/full-math.md`](math/full-math.md)

### Everyday State Sharing (`E`)

A soft latent state representing ordinary state-sharing signals that become part of the routine's observable interaction pattern.

It is a model variable, not a direct measure of emotional intimacy or private disclosure.

See: [`architecture.md`](architecture.md), [`observation-provenance.md`](observation-provenance.md)

### Friction (`F`)

A soft latent state representing coordination difficulty or resistance within the routine.

Friction may change over time; it is not the same as rupture, conflict, or a verdict about the relationship.

```text
Disturbance != rupture
Friction != failure
```

See: [`README.md`](../README.md), [`architecture.md`](architecture.md)

---

## Inference terms 🐣📐

### Particle Filter

The sequential Monte Carlo estimator used by CSRDM to approximate the posterior over continuous hidden state and discrete mode with many weighted candidate states.

Typical cycle:

```text
predict
→ score observations
→ normalize weights
→ resample when needed
```

See: [`tutorial/08-why-particles.md`](tutorial/08-why-particles.md), [`math/full-math.md`](math/full-math.md)

### Particle

One candidate hidden state + mode carried by the Particle Filter.

A particle is a computational hypothesis, not a separate observed fact.

See: [`math/full-math.md`](math/full-math.md)

### Posterior

The probability distribution over hidden state and mode after conditioning on available observations under the current model assumptions.

```text
Posterior probability != observed truth
Narrow posterior != automatically correct
```

See: [`epistemic-status.md`](epistemic-status.md), [`math/full-math.md`](math/full-math.md)

### Filtering

Inference about the hidden condition at time `t` using evidence available through time `t`.

Conceptually:

```text
p(x_t, m_t | z_1:t)
```

See: [`math/full-math.md`](math/full-math.md)

### Smoothing

Re-estimating earlier posterior uncertainty using later observations as well as earlier evidence.

```text
Later evidence may update uncertainty.
Later evidence does not rewrite observed facts.
Smoothing != rewriting history
```

See: [`smoothing-garden.md`](smoothing-garden.md), [`public-api.md`](public-api.md)

### Process noise

Model uncertainty in how hidden state evolves from one step to the next.

It represents uncertainty in the transition model; it is not new observation evidence.

See: [`math/starter-math.md`](math/starter-math.md), [`math/full-math.md`](math/full-math.md)

### Observation likelihood

The model-specified probability of seeing an observation clue given a candidate hidden state and mode.

Current clue-to-state relationships are structural prototype assumptions unless separately supported.

```text
Assumed coefficient != discovered law
```

See: [`observation-provenance.md`](observation-provenance.md), [`math/full-math.md`](math/full-math.md)

### Effective sample size (`ESS`)

A diagnostic for particle-weight degeneracy:

```text
high ESS → weight mass is broadly distributed
low ESS  → a small number of particles carry most weight
```

It is a computational diagnostic, not a model-validity score.

See: [`math/full-math.md`](math/full-math.md)

### Resampling

A Particle Filter computation that refreshes the particle cloud by drawing more often from high-weight candidates when weights become too concentrated.

```text
Resampling != new evidence
```

See: [`math/full-math.md`](math/full-math.md)

---

## Dynamics and memory terms 🌦️🧠

### Transition

The probabilistic evolution from the previous hidden state/mode into the current or next hidden state/mode.

Known actions and explicit context may influence this process.

See: [`action-aware-dynamics.md`](action-aware-dynamics.md), [`math/full-math.md`](math/full-math.md)

### Fixed transition baseline

The default five-mode transition matrix used by the estimator when context-aware mode transitions are not enabled.

Synthetic scenarios may use different generating behavior; the estimator does not import the simulator's answer key.

```text
Synthetic World != Estimator Assumptions
```

See: [`architecture.md`](architecture.md), [`transition-weather.md`](transition-weather.md)

### Context-aware transition

An explicit opt-in mode-transition mechanism that can adjust transition probabilities using declared state/action/context information.

It does not deterministically select the next mode.

See: [`transition-weather.md`](transition-weather.md), [`public-api.md`](public-api.md)

### Shared Context memory

The dedicated memory mechanism for `C` that allows bounded accumulation, slow decay, saturation, and dedicated process uncertainty.

This path is kept separate from ordinary drift so two mechanisms do not compete to update `C`.

See: [`memory-garden.md`](memory-garden.md), [`architecture.md`](architecture.md)

### Action-aware dynamics

Transition behavior in which known observable actions can affect the hidden-state evolution.

```text
Action-aware dynamics != causal identification
```

See: [`action-aware-dynamics.md`](action-aware-dynamics.md)

---

## Validation and diagnostics terms 🔬🧪

### Synthetic world

A simulator or scenario that generates observations/actions for testing the estimator.

The synthetic generator and the estimator must remain conceptually separate.

```text
Synthetic World != Estimator Assumptions
```

See: [`architecture.md`](architecture.md)

### Synthetic reference

A reproducible synthetic dataset/run used as a committed project reference with its own recipe, environment, source revision, inputs, outputs, metrics, and plots.

```text
Synthetic reference != real-human validation
```

See: [`../examples/365-cute-days/`](../examples/365-cute-days/), [`release-notes-0.3.1.md`](release-notes-0.3.1.md)

### Controlled reference

A separate synthetic reference in which known action paths are supplied explicitly so action-aware behavior can be evaluated without mutating the observation-only baseline.

See: [`controlled-reference-result.md`](controlled-reference-result.md)

### Observability

Whether available observation channels contain enough information to distinguish or constrain hidden states under the current model.

```text
Observable in principle != accurately estimated in every dataset
```

See: [`observability-garden.md`](observability-garden.md)

### Identifiability

Whether distinct parameter/state explanations can be uniquely distinguished from available evidence, structurally or in finite data.

```text
Estimable != identifiable
Sensitivity != identifiability
```

See: [`state-chair-test.md`](state-chair-test.md), parked issue `#51`

### Calibration

Whether probability outputs behave like probabilities across repeated cases — for example, whether events assigned a probability near `0.7` occur at roughly that rate under the evaluated setup.

Calibration does not prove that the ontology is correct.

```text
Calibration != ontology discovery
```

See: [`calibration-bench.md`](calibration-bench.md)

### Sensitivity

How much outputs change when assumptions or parameters are perturbed.

Sensitivity can reveal fragile assumptions but does not establish causality.

```text
Sensitivity != causality
```

See: [`sensitivity-map.md`](sensitivity-map.md)

### Change point

A possible persistent change in the generating process rather than a one-step anomaly.

A detected change point is still a model/diagnostic result, not automatic proof of a real-world cause.

See: [`change-point-garden.md`](change-point-garden.md)

---

## Epistemic-status terms 🧭⚖️

### Epistemic status

The category describing what kind of basis supports a claim, relation, or future event in this repository.

The five statuses are:

```text
Observed
Probable
Assumed
Undefined
Not-yet-decided
```

These are not latent states.

See: [`epistemic-status.md`](epistemic-status.md)

### Observed

Directly present in the declared input or synthetic record.

Observed behavior can support inference but should not be silently upgraded into a private-state fact.

See: [`epistemic-status.md`](epistemic-status.md)

### Probable

A statement produced from a probability distribution conditioned on observations and model assumptions.

```text
Probability != fact
```

See: [`epistemic-status.md`](epistemic-status.md)

### Assumed

A relation that exists because the current model explicitly specifies it as a structural hypothesis, prior, coefficient, transition rule, or synthetic recipe.

```text
Assumption != evidence
```

See: [`epistemic-status.md`](epistemic-status.md)

### Undefined

A relationship the project intentionally does not claim or specify.

Undefined is not the same as zero, false, negative, or impossible.

```text
Undefined relationship != zero relationship
```

See: [`epistemic-status.md`](epistemic-status.md)

### Not-yet-decided

A status mainly for a future action or choice that has not occurred yet, even when history makes one outcome highly probable.

```text
High historical probability != future commitment
```

See: [`epistemic-status.md`](epistemic-status.md)

---

## Public-surface and reproducibility terms 🚪🛂

### Public API

The stable caller-facing surface centered on `CSRDM`, `CSRDMConfig`, `CSRDMResult`, experiment recipe helpers, and declared configuration objects.

Internal Particle Filter drawers are not the preferred application interface.

See: [`public-api.md`](public-api.md), [`architecture.md`](architecture.md)

### Observation basket

The mapping of generic observation fields supplied to `CSRDM.update(...)`.

Public observation baskets are validated so typos or contradictory protocol values do not silently become different evidence.

See: [`public-api.md`](public-api.md)

### Action basket

The mapping of known generic actions supplied with an update and associated with the preceding hidden-state transition into the current state.

The first update has no preceding transition, even if actions are recorded.

See: [`public-api.md`](public-api.md)

### Experiment specification (`ExperimentSpec`)

The reproducible recipe describing a run's scenario, duration, seed, particle count, dataset identity, configuration snapshot, and architecture version.

See: [`architecture.md`](architecture.md)

### Recipe fingerprint

A deterministic identifier derived from the experiment recipe rather than display names, timestamps, or output filenames.

```text
Same recipe → same fingerprint
Metric without recipe → mystery bean
```

See: [`architecture.md`](architecture.md), [`public-api.md`](public-api.md)

### Architecture version

The version of the CSRDM model/contract itself.

Current baseline:

```text
architecture = 0.3
```

Changing package metadata or documentation does not automatically change the architecture version.

See: [`architecture.md`](architecture.md)

### Package version

The software distribution version declared in `pyproject.toml`.

Current formal release:

```text
package = 0.3.1
architecture = 0.3
```

```text
Packaging patch version != architecture relabel
```

See: [`release-notes-0.3.1.md`](release-notes-0.3.1.md)

### Release snapshot

The intentionally selected commit used as the target of a formal GitHub Release.

For `v0.3.1`, the selected release snapshot is recorded in the release notes / release-hygiene issue history.

A later documentation commit does not move an already published release tag.

See: [`release-notes-0.3.1.md`](release-notes-0.3.1.md)

---

## Tiny distinction table ☕🧾

| Do not collapse | Into |
|---|---|
| observation | latent state |
| action | intention |
| missing clue | zero |
| probability | fact |
| assumption | evidence |
| undefined relation | zero relation |
| mutuality | 50/50 symmetry |
| continuity | obligation |
| pass | failure |
| disturbance | rupture |
| mode | regime |
| sensitivity | causality |
| smoothing | rewriting history |
| calibration | ontology discovery |
| synthetic success | real-human truth |
| package version | architecture version |
| glossary | second specification |

## Short route back to the sources 🗺️

```text
Need terminology      → glossary.md
Need story            → how-the-coffee-works.md
Need first math       → math/starter-math.md
Need full equations   → math/full-math.md
Need calling rules    → public-api.md
Need architecture     → architecture.md
Need claim status     → epistemic-status.md
Need docs map         → README.md
```

One vocabulary map. Many specialist sources. Same tiny coffee brain. ☕📚🐣
