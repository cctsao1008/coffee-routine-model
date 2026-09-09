# Documentation Map 🗺️☕

Different documents answer different questions on purpose.

> **Story welcomes. Tutorial teaches. Starter Math bridges. Full Math formalizes. Public API guides. Architecture defines. Labs challenge. Results record.**

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

Use [`release-notes-0.3.1.md`](release-notes-0.3.1.md) when the question is **what belongs in the current formal release candidate?**

The earlier [`release-notes-0.3.0.md`](release-notes-0.3.0.md) records why the existing `v0.3.0` tag is kept as an immutable architecture-baseline marker instead of being moved forward.

```text
Package 0.3.1 → current release candidate
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
