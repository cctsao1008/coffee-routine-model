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
- added opt-in particle ancestry plus a fixed-lag genealogical smoother so later clues can refine earlier latent-state uncertainty 🔭🐣
- gave `C = Shared Context` its own accumulation / decay / saturation memory reservoir instead of treating it like an ordinary daily state 🧠🌱
- gathered every estimator-side observation probability knob into one explicit immutable configuration tray 🎛️☕
- added a scenario-wise calibration bench with Brier score, log loss, reliability bins, ECE, and continuous residual diagnostics 🐣📏
- gave the tiny coffee brain an offline change-point detector that can compare `no change` with one persistent regime boundary ✂️🐣
- added optional context-aware mode transitions so the same previous mode can roll different stochastic dice under different known weather 🌦️🎲
- built a 21-poke sensitivity map covering clue ablations, observation scales/offsets, memory decay, process noise, and transition temperature 🧪🗺️
- added a six-state chair test with posterior correlation, held-out leave-one-state-out reconstruction, five-dimensional projections, observation NLL/Brier, and Recovery-mode fidelity 🪑🐣
- gave ten observation knobs a bounded synthetic learning spoon with held-out calibration checks and approximate parameter uncertainty 🎚️🥄
- opened a model arena where six tiny competitors share one synthetic track and keep RMSE, calibration, mode, recovery, runtime, and memory trade-offs separate 🗺️🏁
- added one stable `CSRDM` public facade so ordinary callers can use protocol events without opening every internal drawer 🏛️☕
- gathered dynamics, memory, observation, transition, inference, smoothing, and learning policy into one `CSRDMConfig` tree 🧺🧠
- gave experiments a deterministic `ExperimentSpec` fingerprint and portable `ExperimentResult` receipt 🛂🧪
- declared architecture `0.3` as the first architecture-complete baseline and drew its contract in `docs/architecture.md` 🗺️🏛️

## 🐣 Tiny Fixes

- missing clues now stay missing instead of quietly turning into fake zeroes 🌱
- ambiguous clues can stay ambiguous instead of being forced into a story 🙈
- `👍` learned context: after `+1?` it may be an opt-in; after `☕` it may be a reaction; alone it may simply shrug XD
- opt-in / pass likelihood is only scored when the tiny response door was actually open 🚪☕
- story-specific observation names became generic `invite` / `opt_in`, while old synthetic baskets still get a polite compatibility hug 🧺
- protocol moments can now be split into a `RoutineActions` basket and an observation basket without asking the model to guess intention 🧺🎮👀
- smoothing keeps filtered and hindsight posteriors separate, because learning later is not the same thing as rewriting yesterday 🎩
- direct action drift no longer sneaks into `C`; memory-building actions enter through `shared_context_input()` instead 🧠🧺
- scattered estimator likelihood constants no longer hide inside the Particle Filter; the filter now reads `ObservationModelConfig` explicitly 🎛️🐣
- change-point evidence pays a complexity penalty and spreads prior mass across candidate days so one loud afternoon does not automatically become a whole new universe ✂️🌧️
- voluntary `pass` no longer doubles as hidden Leave evidence, ordinary delivery + acknowledgment no longer masquerades as Recovery, and Special needs explicit special-event context 🌿🎲
- exposed fixed-transition and process-noise knobs explicitly so sensitivity tests can perturb assumptions without monkey-patching the tiny brain 🧪🔧
- parameter learning freezes structural slopes, state dynamics, transitions, memory constants, and state meanings instead of letting one optimizer quietly rewrite the ontology 🎚️🔒
- arena metrics leave non-comparable quantities as `N/A` instead of punishing simpler models with fake zeros 🗺️🙈
- architecture cleanup preserves the fixed-transition baseline and keeps context-aware transitions opt-in instead of quietly changing old reference baskets 🏛️🎲

## 🌱 Recovery Improvements

- made `pass` a normal voluntary event instead of a failure state
- added explicit pause / resume semantics
- added `Busy`, `Leave`, and `Recovery` modes so an interruption does not automatically become a rupture
- added a slow-recovery synthetic world because tiny routines are allowed to come back at their own pace 🐌🌱
- made voluntary pass actions preserve `V` instead of secretly subtracting `M` just because coffee did not happen that day 🌿
- added a nominal routine **set**, post-disturbance recovery time, repair-cost proxy, natural-resume flag, and resilience score so recovery is measurable without grading either person 🌱🩹
- kept disturbance duration separate from recovery lag so a long coordinated leave is not automatically called fragile XD
- made state-reduction candidates report Recovery-mode relationship-index error instead of hiding recovery behavior inside an all-days average 🌱🪑

## ✨ Sparkles

- adopted the extremely serious repository law: **Everything must be cute.** ☕🐾✨
- added [`CUTE_RULES.md`](CUTE_RULES.md) so the cuteness survives future maintenance
- made README, docs, commits, CLI messages, tests, workflows, issues, and plots live in the same tiny coffee universe
- added the 365-day summary picture to the README front porch
- gave GitHub Actions tiny coffee robot names because CI deserves a personality too 🤖☕
- taught the tiny robot to compare filtering with hindsight and paint a little `hindsight.png` 🔭🖼️
- added a tiny memory inspector that paints build / quiet / long-pause phases without turning silence into amnesia 🧠🖼️
- taught the tiny robot to ask whether probabilities keep their promises across every coffee-weather world 🎛️🌦️
- added a little `change-point.png` where the scissors can show which boundary they currently believe in ✂️🖼️
- built a tiny transition weather race where fixed dice and context-aware dice are judged by NLL, Brier score, and top-1 accuracy instead of one fake victory number 🌦️🏁
- added a sensitivity heatmap plus a posterior-correlation chair map so invisible model coupling can finally show its face 🗺️🪑
- added a separate **Deep Coffee Diagnostics** workflow for longer 120-day / 800-particle sensitivity and seven-world chair exams 🔬☕
- taught the deep-exam robot to learn a few bounded probability knobs and run a six-model comparison arena without awarding a fake universal crown 🎚️🗺️👑🙅
- put the architecture version and public-door example on the README front porch so callers know where to knock 🏛️🚪🐣

## 🧺 Tidying

- separated the public synthetic model from private real-world source material
- added generic source notes without names, screenshots, timestamps, or raw messages 🌿
- added tiny protocol bridge docs and adapter contract notes
- added reproducible scenario / seed / particle-count metadata
- added tests for model math, particles, scenarios, simulator, protocol adapter, tiny painter, observability diagnostics, action-aware dynamics, recovery dynamics, particle smoothing, shared-context memory, observation calibration, change-point detection, context-aware mode transitions, sensitivity mapping, state redundancy, bounded parameter learning, model-arena comparison, and the public architecture contract ✅
- taught little robots to repack the reference CSV basket and repaint the gallery reproducibly
- tucked model internals into `coffee_brain/` and runnable helpers into `tiny_tools/` so the root can breathe 🧺☕
- preserved the original hand-set observation baseline as an inspectable config plus JSON export for reproducible future learning experiments 🎛️🧺
- kept the first change-point detector deliberately offline and single-boundary so the little scissors stay inspectable before they grow more blades ✂️🧺
- preserved the original fixed transition matrix as the default Particle Filter baseline; context-aware transitions are explicit opt-in instead of silently changing old baskets 🎲🧺
- kept reduced-state experiments labeled as projection/reconstruction diagnostics instead of pretending they are already fully retrained five-state filters 🪑🧺
- kept learned configs in the normal `ObservationModelConfig` shape so optimization does not create a secret second model format 🎚️🧺
- made the arena report synthetic-truth training flags, latent dimensions, hybrid/smoothing flags, learned parameter count, runtime, and memory proxy beside prediction metrics 🗺️📏
- separated the stable public API from specialist internals so future refactors can move drawers without moving the front door 🚪🧺
- made complete config snapshots JSON-shaped and experiment fingerprints independent of clocks, filenames, and display labels 📸🛂

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
