# Documentation Map 🗺️☕

The repository has several kinds of documents. They answer different questions on purpose.

> **Tutorial teaches the path. Reference defines the contract. Labs challenge assumptions. Results record one recipe.**

## 📖 Learn the model-design story

Start here if you want to understand **why the model gradually became this shape**:

- [`tutorial/README.md`](tutorial/README.md) — guided ten-step tutorial
- [`how-the-coffee-works.md`](how-the-coffee-works.md) — shorter gentle explanation

The tutorial follows:

```text
story
→ observable events
→ modeling problems
→ abstractions
→ uncertainty
→ diagnostics
```

## 🏛️ Look up the current architecture

Use these when you already know the ideas and want the present design contract:

- [`architecture.md`](architecture.md) — architecture `0.3`
- [`adapter-little-contract.md`](adapter-little-contract.md) — minimum adapter invariant
- [`tiny-protocol-bridge.md`](tiny-protocol-bridge.md) — protocol / adapter semantics
- [`action-aware-dynamics.md`](action-aware-dynamics.md) — controlled transition semantics
- [`memory-garden.md`](memory-garden.md) — Shared Context memory mechanism
- [`transition-weather.md`](transition-weather.md) — optional context-aware mode transitions
- [`smoothing-garden.md`](smoothing-garden.md) — fixed-lag smoothing
- [`epistemic-status.md`](epistemic-status.md) — Observed / Probable / Assumed / Undefined / Not-yet-decided claim status

These documents describe the current mechanism or interpretation contract. Development-era roadmap language does not belong here once the feature already exists.

## 🧪 Challenge one modeling assumption

These are labs, not required reading for the first journey:

- [`observability-garden.md`](observability-garden.md) — can the clues distinguish the states?
- [`voluntariness-excitation.md`](voluntariness-excitation.md) — does V track when the synthetic truth is deliberately given enough dynamic range?
- [`calibration-bench.md`](calibration-bench.md) — do predicted probabilities behave as promised?
- [`sensitivity-map.md`](sensitivity-map.md) — which assumptions matter most?
- [`state-chair-test.md`](state-chair-test.md) — does every latent state earn a separate chair?
- [`change-point-garden.md`](change-point-garden.md) — anomaly vs persistent generating change
- [`recovery-garden.md`](recovery-garden.md) — interruption and return toward the nominal set
- [`learning-spoon.md`](learning-spoon.md) — bounded observation-parameter learning
- [`model-arena.md`](model-arena.md) — compare variants without one combined winner score

The common lab pattern is:

```text
one modeling doubt
→ one explicit experiment
→ multiple visible metrics
→ limited conclusion
```

A focused excitation lab may deliberately move one synthetic latent variable more than ordinary dynamics would. That makes it a diagnostic stress test, not a claim that real trajectories behave that way.

## 📏 Result snapshots

Small result documents such as [`change-point-result.md`](change-point-result.md) record a particular reproducible synthetic recipe or smoke result.

They are **not** architecture definitions and should not be read as universal model performance.

```text
Result snapshot != design contract
Synthetic metric != human validation
```

## ☕ Run examples

The runnable story and synthetic baskets live in [`../examples/`](../examples/).

Useful starting points:

- [`../examples/cheng_linda_story.py`](../examples/cheng_linda_story.py) — synthetic persona → generic model semantics
- [`../examples/365-cute-days/`](../examples/365-cute-days/) — committed synthetic reference basket

Runnable diagnostic helpers live in [`../tiny_tools/`](../tiny_tools/).

## ⚖️ Writing and epistemic boundaries

- [`../CUTE_RULES.md`](../CUTE_RULES.md) — repository tone and engineering rules
- [`epistemic-status.md`](epistemic-status.md) — Observed / Probable / Assumed / Undefined / Not-yet-decided contract
- [`objective-story-contract.md`](objective-story-contract.md) — objective story-writing contract
- [`source-notes.md`](source-notes.md) — public boundary around design inspiration
- [`../COFFEELOG.md`](../COFFEELOG.md) — project history

These documents keep several distinctions explicit:

```text
Probability != fact
Assumption != evidence
Undefined relationship != zero relationship
High historical probability != future commitment
```

## The short version 🌱

```text
First visit      → README.md
Want to learn    → docs/tutorial/
Want the spec    → docs/architecture.md
Want claim status→ docs/epistemic-status.md
Want experiments → docs/*garden.md / *bench.md / *test.md / focused labs / model-arena.md
Want to run      → examples/ and tiny_tools/
Want history     → COFFEELOG.md
```

Same model. Different questions. Different doors. ☕
