# Documentation Map 🗺️☕

Different documents answer different questions on purpose.

> **Story welcomes. Glossary aligns. Tutorial teaches. Starter Math bridges. Full Math formalizes. Public API guides. Architecture defines. Labs challenge. Results record.**

## 🏷️ Role / authority at a glance

Use this before treating two documents as if they have the same job.

| Surface | Role | Authority for its scope |
|---|---|---|
| [`glossary.md`](glossary.md) | terminology index | **Index only** — specialist sources win |
| [`how-the-coffee-works.md`](how-the-coffee-works.md) | gentle explanation | **Explanatory** |
| [`tutorial/README.md`](tutorial/README.md) | guided learning path | **Explanatory** |
| [`math/starter-math.md`](math/starter-math.md) | first mathematical projection | **Explanatory** — same CSRDM, fewer symbols |
| [`math/full-math.md`](math/full-math.md) | complete mathematical view | **Canonical mathematical reference** for architecture `0.3` |
| [`public-api.md`](public-api.md) | caller contract | **Canonical public-calling reference** |
| [`architecture.md`](architecture.md) | software / architecture contract | **Canonical architecture reference** |
| [`epistemic-status.md`](epistemic-status.md) | claim-status contract | **Canonical epistemic reference** |
| lab documents | focused experiment | **Experiment**, not architecture contract |
| `*-result.md` documents | reproducible result snapshot | **Snapshot**, not design contract |
| `release-notes-*` | release record | **Release / historical context** |

```text
Canonical    → owns a contract for its declared scope
Explanatory  → teaches or interprets that contract
Index        → helps you find shared wording
Experiment   → challenges one assumption
Snapshot     → records one reproducible result
Historical   → preserves past release / design context
```

This table is navigation metadata, not another specification.

## 📚 Terminology / glossary

Use [`glossary.md`](glossary.md) when the question is **what does this recurring term mean in this project?**

The glossary keeps definitions short and points back to specialist sources instead of becoming a second specification.

```text
Glossary
= shared wording + pointers
!= new ontology
!= second source of truth
```

If the question is instead **“does this term imply X?”**, use [`common-confusions.md`](common-confusions.md).

```text
Glossary          → meaning
Common Confusions → recurring misreading
```

## ☕ Story / gentle explanation

Start here when you want the idea before the machinery:

- [`how-the-coffee-works.md`](how-the-coffee-works.md) — short gentle explanation
- [`design-principles.md`](design-principles.md) — compact map of recurring design lessons

## 📖 Tutorial path

Use [`tutorial/README.md`](tutorial/README.md) when you want to learn **why the model gradually became this shape**.

The tutorial moves through:

```text
story
→ observable events
→ modeling questions
→ abstractions
→ uncertainty
→ diagnostics
```

## 🧮 Math path

Use [`math/README.md`](math/README.md) when the main question is **how much math do I want right now?**

```text
🌱 Starter Math
→ math/starter-math.md
→ first mathematical view
→ fewer symbols, same CSRDM

📐 Full Math
→ math/full-math.md
→ complete architecture 0.3 mathematical view
```

```text
Starter Math != Lite model
Full Math != separate model
Same model. Different depth.
```

## 🛠️ Public API path

Use [`public-api.md`](public-api.md) when the question is **how do I call this safely without knowing the internal drawers?**

It covers:

```text
CSRDM.step(...)
CSRDM.update(...)
missing clues
strict public observation validation
action timing
context-aware transition opt-in
smoothing
named posterior summaries
reproducible recipe cards
```

## 🏛️ Architecture / mechanism reference

Use these when you already understand the ideas and want the current implementation contract:

- [`architecture.md`](architecture.md) — architecture `0.3`
- [`tiny-protocol-bridge.md`](tiny-protocol-bridge.md) — protocol / adapter semantics
- [`action-aware-dynamics.md`](action-aware-dynamics.md) — controlled transition semantics
- [`memory-garden.md`](memory-garden.md) — Shared Context memory mechanism
- [`transition-weather.md`](transition-weather.md) — optional context-aware mode transitions
- [`smoothing-garden.md`](smoothing-garden.md) — fixed-lag smoothing
- [`observation-provenance.md`](observation-provenance.md) — which clue relationships are observed, probable, assumed, or still undefined

Math pages explain equations. Public API pages explain safe calling behavior. Architecture pages define software behavior and boundaries. Provenance pages explain what kind of claim a relationship is.

## 🧪 Labs — challenge one assumption

These are focused experiments, not required reading for the first journey:

- [`observability-garden.md`](observability-garden.md) — can the clues distinguish the states?
- [`voluntariness-excitation.md`](voluntariness-excitation.md) — what happens when V gets enough room to move?
- [`v-compression-result.md`](v-compression-result.md) — why did the V posterior stay compressed?
- [`v-dynamics-prior-result.md`](v-dynamics-prior-result.md) — responsiveness vs ordinary-baseline trade-off
- [`shared-context-bias-result.md`](shared-context-bias-result.md) — shape error vs slow offset in C
- [`controlled-reference-result.md`](controlled-reference-result.md) — known-action path end-to-end
- [`calibration-bench.md`](calibration-bench.md) — do predicted probabilities keep their promises?
- [`sensitivity-map.md`](sensitivity-map.md) — which assumptions matter most?
- [`state-chair-test.md`](state-chair-test.md) — does every latent state earn a separate chair?
- [`change-point-garden.md`](change-point-garden.md) — anomaly vs persistent generating change
- [`recovery-garden.md`](recovery-garden.md) — interruption and return
- [`learning-spoon.md`](learning-spoon.md) — bounded observation-parameter learning
- [`model-arena.md`](model-arena.md) — compare variants without one winner score

Common lab rhythm:

```text
one modeling doubt
→ one explicit experiment
→ multiple visible metrics
→ limited conclusion
```

## 📏 Result snapshots

Result files such as:

- [`change-point-result.md`](change-point-result.md)
- [`v-compression-result.md`](v-compression-result.md)
- [`v-dynamics-prior-result.md`](v-dynamics-prior-result.md)
- [`shared-context-bias-result.md`](shared-context-bias-result.md)
- [`controlled-reference-result.md`](controlled-reference-result.md)

record one reproducible synthetic recipe or diagnostic result.

```text
Result snapshot != design contract
Synthetic metric != human validation
```

## 📦 Release / packaging snapshot

Use [`release-notes-0.3.1.md`](release-notes-0.3.1.md) when the question is **what belongs in the current formal release?**

The earlier [`release-notes-0.3.0.md`](release-notes-0.3.0.md) records why the existing `v0.3.0` tag is kept as an immutable architecture-baseline marker instead of being moved forward.

```text
Package 0.3.1 → current formal release
Architecture 0.3 → unchanged model baseline
v0.3.0 → historical architecture tag
```

```text
Packaging patch version != architecture relabel
Release hygiene != model growth
```

## ☕ Runnable examples

See [`../examples/`](../examples/):

- [`../examples/cheng_linda_story.py`](../examples/cheng_linda_story.py) — synthetic persona → generic semantics
- [`../examples/365-cute-days/`](../examples/365-cute-days/) — observation-only synthetic reference

The separate action-aware reference is generated on demand by [`../tiny_tools/controlled_reference.py`](../tiny_tools/controlled_reference.py):

```bash
python -m tiny_tools.controlled_reference
```

Its committed result summary lives in [`controlled-reference-result.md`](controlled-reference-result.md).

Diagnostic helpers live in [`../tiny_tools/`](../tiny_tools/).

## ⚖️ Writing / source / epistemic boundaries

- [`epistemic-status.md`](epistemic-status.md) — Observed / Probable / Assumed / Undefined / Not-yet-decided
- [`observation-provenance.md`](observation-provenance.md) — provenance map for clue→state / mode relationships
- [`common-confusions.md`](common-confusions.md) — compact corrections to recurring category mistakes
- [`objective-story-contract.md`](objective-story-contract.md) — objective story-writing contract
- [`design-principles.md`](design-principles.md) — distilled principle map and public boundary around private design inspiration
- [`../CUTE_RULES.md`](../CUTE_RULES.md) — tone and engineering rules
- [`../COFFEELOG.md`](../COFFEELOG.md) — project history

Keep these distinctions visible:

```text
Probability != fact
Assumption != evidence
Assumed coefficient != discovered law
Zero coefficient != proven independence
Undefined relationship != zero relationship
High historical probability != future commitment
Design inspiration != public dataset
```

## The short version 🌱

```text
First visit          → README.md
Need terminology     → docs/glossary.md
Common confusion?    → docs/common-confusions.md
Want the story       → docs/how-the-coffee-works.md
Want to learn        → docs/tutorial/
Want Starter Math    → docs/math/starter-math.md
Want Full Math       → docs/math/full-math.md
Want to call the API → docs/public-api.md
Want the spec        → docs/architecture.md
Want claim status    → docs/epistemic-status.md
Want clue provenance → docs/observation-provenance.md
Want experiments     → labs / result docs
Want release status  → docs/release-notes-0.3.1.md
Want to run          → examples/ and tiny_tools/
Want history         → COFFEELOG.md
```

Same model. Different questions. Different depth. Different doors. ☕🌱📐🐣
