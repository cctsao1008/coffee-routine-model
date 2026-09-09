# The Cute Rules ☕🐾✨

This repository has one very serious rule:

> **Everything should feel like it belongs in the same tiny coffee universe.**

But the rule underneath it matters more:

> **Cute != sloppy.**

The coffee can wear tiny paws. The math still has to work. 🧠✨

---

## 1. Cute is repo-wide ☕🌱

The tone applies to README, docs, commits, comments, docstrings, CLI output, errors, tests, plots, examples, issues, workflows, and release notes.

If humans can see it, it should feel coherent with the rest of the repo.

---

## 2. Cute outside. Cute inside. Math still works. 🧠☕

Keep equations, state definitions, probability calculations, reproducibility, tests, uncertainty, file formats, and numerical results precise.

A tiny particle is still a particle. 🐣

```text
Cute != sloppy
```

---

## 3. Hard math should still tell a little story 📖☕🐣

This project contains stochastic dynamics, hidden states, hybrid modes, memory, Particle Filtering, smoothing, calibration, and a suspicious number of matrices.

That is not permission to make the reader suffer.

Prefer:

```text
Concrete event
→ Modeling question
→ Intuition
→ Abstraction
→ Math / code
```

A story should explain **why a concept exists** before an equation explains **how it works**.

```text
Story != evidence
```

---

## 4. Plain words get the first sip 🌱🧮

Use ordinary words before specialist terms.

Prefer this order:

```text
hidden state
→ latent state

many possible explanations
→ posterior distribution

known action
→ controlled input

observable clue
→ likelihood evidence

slow memory
→ dedicated state reservoir
```

When a specialist term appears, explain it immediately in plain language.

```text
Simple != false
Plain language != missing rigor
Cute != childish
```

The math path follows the same rule:

```text
Starter Math
→ first mathematical view

Full Math
→ same model, all the gears
```

There is no separate Lite CSRDM.

```text
Same model.
Same example.
Different depth.
```

---

## 5. Persona at the edge, generic math in the center 🎭🧠

Synthetic teaching personas are welcome where names make difficult ideas easier to follow.

They must translate into generic semantics before entering architecture-defining code:

```text
Cheng / Linda story
        ↓
Persona / Protocol Adapter
        ↓
invite / opt_in / reaction / ...
        ↓
CSRDM Core
```

Do **not** hard-code persona names into Particle Filter likelihoods, latent states, transition logic, config keys, or core mathematics.

```text
Persona != core ontology
```

---

## 6. Story-driven does not mean interpretive overreach ⚖️📖

The repo may be warm and playful, but statements must remain auditable.

Prefer:

```text
observable event
→ model representation
→ possible inference
→ uncertainty / unknowns
```

Keep these boundaries visible:

```text
Observed behavior != internal truth
Action != intention
Continuity != obligation
Pass != failure
Disturbance != rupture
Model != human
```

The detailed writing contract lives in [`docs/objective-story-contract.md`](docs/objective-story-contract.md).

---

## 7. Synthetic coffee stays synthetic 🧪☕

Do not publish private conversations, screenshots, private timestamps, company-identifying context, private files, or claims that teaching personas are ground-truth psychological datasets.

A private design history may inspire an abstract pattern. The public story must remain synthetic, generalized, and self-contained.

```text
Design inspiration != public dataset
Public story != private data
```

---

## 8. Comments should protect meaning, not narrate syntax 🧠🛡️

Useful comments explain a design reason, invariant, temporal alignment, or intentionally surprising choice.

Good:

```python
# C owns dedicated slow memory, so it deliberately skips
# ordinary daily-state drift used by the other five states. 🧠🌱
```

Not useful:

```python
# calculate probability
probability = ...
```

---

## 9. `XD` is seasoning, not punctuation ☕

`XD` can still appear when it adds a real punchline or makes a deliberately light example easier to read.

Do not attach it automatically to headings, conclusions, commits, or every cute paragraph.

```text
cute != noisy
playful != repetitive
```

---

## 10. Commit messages must still say what changed ☕🐾

Good little commits:

```text
☕ brew a whole year of 365 cute days
🐣 teach tiny particles how to guess better
🌱 let the routine find its way back
🧺 tidy up the little coffee basket
📖 give the scary math a tiny story to walk in with
```

Cute does not mean mysterious.

---

## 11. Errors may be adorable, but they must help 🙈🛠️

Bad:

```text
Oopsie! Something happened! ✨
```

Better:

```text
🐾 --days must be at least 1. The tiny calendar cannot have zero days.
```

A useful error tells us what went wrong and, when practical, how to fix it.

---

## 12. Tests live in a tiny nest 🐣✅

Tests should remain precise, reproducible, and behavior-focused.

```text
Cute CI != weak CI
```

Never claim a check is happy unless it actually passed.

---

## 13. Plots should be cute, not confusing 🎨☕

A plot belongs here when it is readable, honest about uncertainty, visually friendly, and technically useful.

```text
Cute plot != confusing plot
```

The data gets the front seat. The sparkles sit politely in the back. ✨

---

## 14. The final tiny rule 🌸

When choosing between:

```text
boring + correct
cute   + correct
```

prefer:

```text
cute + correct ☕🐾✨
```

When choosing between:

```text
cute + wrong
boring + correct
```

choose correctness first, then make it cute.

---

☕ Cute outside.  
🐣 Cute inside.  
🧠 Math still works.  
🌱 Plain words get the first sip.  
📖 Hard math still tells a little story.  
⚖️ Story remains objective.  
🌱 Humans may still surprise the model.
