# Documentation Map 🗺️☕

The repository has several kinds of documents. They answer different questions on purpose.

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

## 🏛️ Look up the architecture

Use these when you already know the ideas and want the current design contract:

- [`architecture.md`](architecture.md) — architecture `0.3`
- [`tiny-protocol-bridge.md`](tiny-protocol-bridge.md) — protocol / adapter boundary
- [`action-aware-dynamics.md`](action-aware-dynamics.md) — controlled transition semantics
- [`memory-garden.md`](memory-garden.md) — Shared Context memory mechanism
- [`smoothing-garden.md`](smoothing-garden.md) — fixed-lag smoothing

## 🧪 Challenge one modeling assumption

These are labs, not required reading for the first journey:

- [`observability-garden.md`](observability-garden.md) — can the clues distinguish the states?
- [`calibration-bench.md`](calibration-bench.md) — do predicted probabilities behave as promised?
- [`sensitivity-map.md`](sensitivity-map.md) — which assumptions matter most?
- [`change-point-garden.md`](change-point-garden.md) — anomaly vs persistent generating change
- [`recovery-garden.md`](recovery-garden.md) — interruption and return toward the nominal set
- [`learning-spoon.md`](learning-spoon.md) — bounded observation-parameter learning
- [`model-arena.md`](model-arena.md) — compare variants without one combined winner score

## ☕ Run examples

The runnable story and synthetic baskets live in [`../examples/`](../examples/).

Useful starting points:

- [`../examples/cheng_linda_story.py`](../examples/cheng_linda_story.py) — synthetic persona → generic model semantics
- [`../examples/365-cute-days/`](../examples/365-cute-days/) — committed synthetic reference basket

## ⚖️ Writing and evidence boundaries

- [`../CUTE_RULES.md`](../CUTE_RULES.md) — repository tone and engineering rules
- [`objective-story-contract.md`](objective-story-contract.md) — how to keep story-driven teaching objective
- [`../COFFEELOG.md`](../COFFEELOG.md) — project history

## The short version 🌱

```text
First visit      → README.md
Want to learn    → docs/tutorial/
Want the spec    → docs/architecture.md
Want experiments → docs/*garden.md / *bench.md / model-arena.md
Want to run      → examples/ and tiny_tools/
```

Same model. Different questions. Different doors.
