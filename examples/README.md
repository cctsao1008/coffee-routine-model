# Runnable Coffee Stories ☕📖🐣

This folder is the **hands-on door** into the project.

The examples here are intentionally smaller and more concrete than the architecture docs:

```text
story / protocol moment
        ↓
generic observable events
        ↓
action + observation baskets
        ↓
CSRDM or a reproducible synthetic basket
```

> **Readable first. Generic before the core. Synthetic when truth is needed.**

## Pick a tiny door 🚪

### `cheng_linda_story.py` — persona costume at the edge 🎭☕

A short synthetic teaching story that demonstrates the persona boundary.

```text
Cheng / Linda-shaped fields
        ↓
CoffeeEvent / CoffeeStep
        ↓
generic CSRDM semantics
```

The names are illustrative teaching personas. This file is **not** a private transcript, behavioral ground truth, or evidence about real people.

Run it with:

```bash
python -m examples.cheng_linda_story
```

Useful lesson:

```text
Persona != core ontology
Story != evidence
```

### `protocol_snacks.py` — tiny adapter edge cases 🥨☕

A handful of small protocol examples:

- ordinary `+1? → + → ☕ → 👍`
- voluntary `pass`
- an ambiguous lonely `👍`
- explicit update / pause / resume events

Run it with:

```bash
python -m examples.protocol_snacks
```

Useful lesson:

```text
Observed event != interpretation
Missing clue != zero
Ambiguous clue != forced story
Pass != failure
```

### `365-cute-days/` — committed synthetic reference basket 🗓️🌱

A reproducible synthetic year containing generated clues, hidden synthetic truth, Particle Filter estimates, metrics, and plots.

Start with [`365-cute-days/README.md`](365-cute-days/README.md).

Useful lesson:

```text
Synthetic reference != real-human validation
```

## What does not belong here? 🙈

```text
private transcripts
company data
screenshots of real conversations
real-person ground-truth labels
persona-specific dependencies inside coffee_brain/
```

If a story-specific name is useful for teaching, it should lose its costume before entering the generic model.

## Want the model-design journey instead? 📚

- [`../docs/tutorial/README.md`](../docs/tutorial/README.md) — ten-step teaching path
- [`../docs/architecture.md`](../docs/architecture.md) — formal architecture `0.3` contract
- [`../docs/README.md`](../docs/README.md) — full documentation map
- [`../tiny_tools/`](../tiny_tools/) — runnable diagnostic labs

Examples are the coffee samples on the counter. The architecture still lives in the kitchen. ☕🐣
