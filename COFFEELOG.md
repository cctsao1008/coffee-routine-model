# COFFEELOG 📖☕🐾

A changelog, but make it smell like coffee.

This little book remembers meaningful changes so nobody has to excavate every commit like an archaeologist looking for a lost espresso shot. XD

> Cute notes. Real changes. No corporate release-note soup.

---

## ☕ Fresh Brew

### Tiny first brew — 2026-09-08

- created the six-soft-state coffee routine model: `P / M / V / C / E / F` 🧠☕
- invited thousands of tiny Particle Filter friends to keep uncertain guesses instead of pretending there is one perfect answer 🐣🐣🐣
- grew the main demo from 100 cute days into a full **365-day synthetic coffee year** 🗓️🌱
- added seven tiny weather worlds: cozy, busy, leave-and-return, sleepy replies, special sparkle, chaos, and slow recovery 🌦️
- connected `coffee-routine-protocol` events to generic observation clues through `coffee_brain/protocol_adapter.py` ☕➡️🧠
- packed the full reproducible 365-day picnic basket with `input.csv`, `output.csv`, `metrics.csv`, and its own tiny map 🧺
- taught `tiny_tools/visualize.py` to paint the coffee year into a little gallery wall 🎨🖼️
- planted a tiny observability garden that hides one clue family at a time and checks which soft states can actually still be seen 🐣🔍
- gave the hidden-state transition an explicit action basket so known actions can move the tiny world instead of hiding inside observation likelihoods ☕🎮

## 🐣 Tiny Fixes

- missing clues now stay missing instead of quietly turning into fake zeroes 🌱
- ambiguous clues can stay ambiguous instead of being forced into a story 🙈
- `👍` learned context: after `+1?` it may be an opt-in; after `☕` it may be a reaction; alone it may simply shrug XD
- opt-in / pass likelihood is only scored when the tiny response door was actually open 🚪☕
- story-specific observation names became generic `invite` / `opt_in`, while old synthetic baskets still get a polite compatibility hug 🧺
- protocol moments can now be split into a `RoutineActions` basket and an observation basket without asking the model to guess intention 🧺🎮👀

## 🌱 Recovery Improvements

- made `pass` a normal voluntary event instead of a failure state
- added explicit pause / resume semantics
- added `Busy`, `Leave`, and `Recovery` modes so an interruption does not automatically become a rupture
- added a slow-recovery synthetic world because tiny routines are allowed to come back at their own pace 🐌🌱
- made voluntary pass actions preserve `V` instead of secretly subtracting `M` just because coffee did not happen that day 🌿

## ✨ Sparkles

- adopted the extremely serious repository law: **Everything must be cute.** ☕🐾✨
- added [`CUTE_RULES.md`](CUTE_RULES.md) so the cuteness survives future maintenance
- made README, docs, commits, CLI messages, tests, workflows, issues, and plots live in the same tiny coffee universe
- added the 365-day summary picture to the README front porch
- gave GitHub Actions tiny coffee robot names because CI deserves a personality too 🤖☕

## 🧺 Tidying

- separated the public synthetic model from private real-world source material
- added generic source notes without names, screenshots, timestamps, or raw messages 🌿
- added tiny protocol bridge docs and adapter contract notes
- added reproducible scenario / seed / particle-count metadata
- added tests for model math, particles, scenarios, simulator, protocol adapter, tiny painter, observability diagnostics, and action-aware dynamics ✅
- taught little robots to repack the reference CSV basket and repaint the gallery reproducibly
- tucked model internals into `coffee_brain/` and runnable helpers into `tiny_tools/` so the root can breathe 🧺☕

---

## How future tiny entries should look 🐾

Keep them short enough to sip:

```md
## ☕ Fresh Brew
- added a new thing

## 🐣 Tiny Fixes
- fixed a tiny wobble

## 🌱 Recovery Improvements
- made interruptions kinder

## ✨ Sparkles
- made something nicer to look at

## 🧺 Tidying
- put the beans back where they belong
```

The wording can be adorable.

The technical meaning still has to be true. 🧠✨
