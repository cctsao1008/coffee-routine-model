# Observation-Model Provenance Map 🎛️🧭☕

This page answers a narrower question than calibration:

> **What kind of claim is each observation-model relationship?**

The observation model turns observable clues into likelihoods over the hidden CSRDM state. That does **not** mean the coefficients were discovered from people.

For the default architecture `0.3` model:

```text
observable clue itself
→ Observed when it is actually present in the input

clue → latent-state / mode relationship
→ Assumed structural prototype

likelihood value produced by that relationship
→ Probable under the current model

broader real-world relationship not represented by an edge
→ Undefined by this repository
```

```text
Assumed coefficient != discovered law
Zero coefficient != proven independence
Undefined relationship != zero relationship
Calibration != ontology discovery
```

The repo-wide status vocabulary lives in [`epistemic-status.md`](epistemic-status.md).

## 1. Three layers that should not be collapsed 🧺

Suppose the input contains:

```text
pass_event = 1
```

Three different statements are possible:

```text
Observed
→ a pass event was recorded

Assumed
→ the current likelihood recipe gives pass_event direct coefficients on M and F plus mode offsets

Probable
→ after the likelihood update, some hidden-state / mode explanations receive more posterior mass than others
```

A fourth statement stays intentionally separate:

```text
Undefined
→ why a real person chose pass is not specified here
```

The event can be observed while the mapping remains assumed.

## 2. Where the current numeric recipe comes from 🎛️

The authoritative runtime values live in:

```text
coffee_brain/observation_model.py
→ DEFAULT_OBSERVATION_MODEL
```

They are explicitly described by the config as:

```text
hand-set structural baseline; not learned from real humans
```

The numeric magnitudes serve a **synthetic structural prototype**. They are inspectable, calibratable, and challengeable. They are not a recovered psychological scale.

Run the complete current coefficient / mode-offset inventory with:

```bash
python -m tiny_tools.inspect_observation_provenance
```

The inspector reads the runtime config directly, so the numeric source of truth stays in one place.

## 3. Why each clue channel exists 🌱

The table below records the public-safe modeling motivation. A motivation is not a fitted coefficient.

| Channel | Observable role | Why it exists in the prototype | Mapping status |
|---|---|---|---|
| `opt_in` | explicit participation choice | keeps participation observable and keeps continuity separate from obligation | Assumed mapping; design-history motivated |
| `text_reply` | reply present / absent | represents a basic coordination clue while preserving `missing != zero` | Assumed mapping |
| `reaction` | acknowledgement / reaction observed | gives a small explicit acknowledgement clue without turning a reaction into a hidden-state fact | Assumed mapping; design-history motivated |
| `state_share` | explicit everyday-state sharing | represents observable state-sharing events without inferring private motive | Assumed mapping; design-history motivated |
| `proactive_update` | proactive exception / status update | represents observable coordination updates around busy / leave / exceptions | Assumed mapping; design-history motivated |
| `routine_maintenance` | observable continuation / closure | represents repeated maintenance of the routine grammar | Assumed mapping; design-history motivated |
| `pass_event` | explicit decline branch | keeps pass as a valid observable branch rather than a failure code | Assumed mapping; design-history motivated |
| `resume_signal` | explicit return / resume clue | represents ordinary return after pause or disturbance | Assumed mapping; design-history motivated |
| `tone_warmth` | synthetic continuous tone proxy | provides a continuous teaching / calibration clue; it is not an emotion measurement | Assumed mapping; synthetic convenience |
| `response_delay` | measured reply delay when a reply exists | provides a timing clue while keeping `delay != disengagement` | Assumed mapping; synthetic convenience |

The private design history motivated some **questions and observable pattern classes**. It did not provide the numeric slopes, intercepts, sigmas, or mode offsets.

## 4. Current direct state-edge map 🧠

For binary channels and `tone_warmth`, a nonzero direct coefficient means only:

> the current prototype includes a direct likelihood edge from that latent state to that clue.

It does not mean the relationship is causal or empirically identified.

```text
opt_in              ← P, M, V, F
text_reply           ← M, C, E, F
reaction             ← P, M, V, F
state_share          ← M, C, E
proactive_update     ← M, C, E, F
routine_maintenance ← P, M, V, C, F
pass_event           ← M, F
resume_signal        ← P, M
tone_warmth          ← M, V, C, E, F
response_delay       ← P, M + mode additions
```

Every arrow above is **Assumed** in architecture `0.3`.

The absence of an arrow means:

```text
coefficient = 0 in this specification
```

not:

```text
real relationship = proven absent
```

For example, `pass_event` currently has no direct V likelihood coefficient. That does not prove pass and Voluntariness are unrelated. In architecture `0.3`, the boundary-preserving role of a voluntary pass is represented primarily on the **action-aware transition side**, not by forcing a direct pass→V observation edge.

## 5. Mode offsets are assumptions too 🌦️

Binary channels may also carry offsets for:

```text
Normal / Busy / Leave / Special / Recovery
```

and reply delay has mode-specific added minutes.

Those values are structural prototype assumptions that let the likelihood family express context-sensitive clue rates in synthetic experiments.

```text
mode offset != discovered behavioral law
zero mode offset != proof that a mode has no effect
```

A zero simply means the current likelihood recipe applies no **direct** adjustment for that channel / mode pair.

## 6. Intercepts and noise scales do not get a stronger status 📏

The Bernoulli intercepts, warmth `sigma`, delay `sigma_log`, base delay, and minimum delay floor are also hand-set prototype parameters.

They are useful for:

```text
reproducible synthetic worlds
calibration exercises
sensitivity analysis
bounded learning experiments
```

They are not privileged just because they are scalar numbers.

```text
numeric precision != epistemic certainty
```

## 7. Calibration and learning do not rewrite provenance 🎚️

Calibration asks whether the probabilities produced by the current assumed family keep their probabilistic promises in a declared synthetic experiment.

Bounded learning currently changes only:

```text
8 Bernoulli intercepts
warmth sigma
delay sigma
```

while state slopes and mode offsets remain fixed.

Even when a learned knob improves held-out likelihood:

```text
learned probability knob
!= discovered ontology
!= discovered intention
!= proof that a zero edge should become nonzero
```

See [`calibration-bench.md`](calibration-bench.md) and [`learning-spoon.md`](learning-spoon.md).

## 8. Why provenance stays outside runtime config 🧭

This audit considered embedding per-edge provenance metadata into `ObservationModelConfig`.

The decision is **not to add it** in architecture `0.3`.

Reasons:

```text
runtime config should describe executable likelihood behavior
provenance is explanatory metadata, not a numerical model input
adding prose metadata to serialized config can perturb experiment fingerprints
one sidecar inspector can read the authoritative config without duplicating values
```

So the split is:

```text
coffee_brain/observation_model.py
→ executable numeric source of truth

tiny_tools.inspect_observation_provenance
→ exact runtime inventory

docs/observation-provenance.md
→ epistemic interpretation and design rationale
```

This keeps traceability without making epistemic prose part of the estimator state.

## 9. Safe wording for future docs 📖

Prefer:

> The current prototype gives `opt_in` direct likelihood dependence on P, M, V, and F.

Avoid:

> Opt-in proves P, M, V, and F.

Prefer:

> `tone_warmth` is a synthetic continuous clue whose mapping is hand-set for the prototype.

Avoid:

> Tone warmth measures internal emotion.

Prefer:

> The current direct coefficient is zero.

Avoid:

> The variables are independent.

## 10. Compact status receipt ☕🧾

```text
Observed
→ clue/event values actually present in a declared input

Probable
→ likelihoods and posterior claims conditional on the current model

Assumed
→ all default clue→state slopes, mode offsets, intercepts, and noise scales

Undefined
→ broader real-world relations not established by the prototype, including zero direct edges

Not-yet-decided
→ future choices remain open; observation coefficients do not commit them
```

The observation model is allowed to be useful before every relationship is empirically identified. It is not allowed to forget which parts are assumptions. ☕🎛️🧭
