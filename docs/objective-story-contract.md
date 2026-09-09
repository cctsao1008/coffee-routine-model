# Objective Story Contract 📖⚖️☕

This repository uses stories to make a difficult model easier to learn.

That creates one responsibility:

> **Readable like a story. Reviewable like engineering.**

The story may be warm, playful, and concrete. The claims still need clear evidence boundaries.

## 1. Observable event first

Prefer:

```text
Cheng asks +1?
Linda says pass
The adapter records invite=1 and pass_event=1.
```

Then explain what the model does with those clues.

Do not jump directly to an internal-state claim.

```text
Observed event
    ↓
model mapping
    ↓
possible interpretation
    ↓
uncertainty remains visible
```

## 2. Say what the model does — not what a person "is"

Prefer:

> The model maps repeated clear coordination to evidence related to Predictability.

Avoid:

> This proves the person is predictable.

Prefer:

> A clean pass preserves the model's Voluntariness boundary.

Avoid:

> The pass reveals what somebody secretly wanted.

```text
Observation != latent state
Action != intention
```

## 3. Persona names are teaching costumes

`Cheng` and `Linda` are synthetic teaching personas in the public repository.

They may appear in:

```text
README stories
examples/
tutorials
small explanatory snippets
```

They must translate into generic semantics before entering architecture-defining code:

```text
persona vocabulary
      ↓
adapter
      ↓
invite / opt_in / pass_event / reaction / ...
      ↓
CSRDM core
```

```text
Persona != core ontology
```

## 4. Public story != private source material

Do not publish:

- private transcripts;
- timestamps from private conversations;
- company or workplace-identifying facts;
- screenshots from private interactions;
- private files or exports;
- claims that the synthetic story is a verbatim historical record.

The design history may inspire a pattern. The public example must be distilled, synthetic, and self-contained.

```text
Design inspiration != public dataset
Story != evidence
```

## 5. Distinguish four layers

When useful, keep these layers explicit:

```text
1. Observable fact
2. Model representation
3. Inference / hypothesis
4. Unknown
```

Example:

```text
Observable fact:
  a pass token occurred

Model representation:
  pass_event=1; pass action is available

Inference:
  under CSRDM, this may help preserve Voluntariness rather than count as failure

Unknown:
  private motive for the pass
```

That structure prevents the narrative layer from becoming mind reading.

## 6. One anomaly is not a pattern

A single unusual event should usually remain a single unusual event unless the model has enough evidence to support something stronger.

```text
one slow reply != persistent shift
one leave day != rupture
one unusual reaction != new regime
```

The repository has separate tools for local modes, change points, recovery, and uncertainty because those questions should not be collapsed into one dramatic interpretation.

## 7. Ordinary can remain ordinary

Not every event needs a lesson about hidden meaning.

```text
ordinary coffee day = ordinary coffee day
ordinary resume     = ordinary resume
```

Use a story beat when it teaches a modeling distinction. Do not manufacture significance merely to make the prose more dramatic.

## 8. Warm tone, restrained conclusions

Cute language and small metaphors are welcome when they improve comprehension.

But the conclusion should remain precise.

Good:

> The tiny brain keeps several hypotheses alive because the clues do not determine one hidden state.

Also good:

> The posterior is narrow in this synthetic run, but narrow uncertainty does not prove the model is correct.

Avoid decorative certainty.

## 9. `XD` is seasoning, not punctuation

The repository can still use `XD` when it adds a real punchline or makes a deliberately light example easier to read.

Do not attach it automatically to headings, conclusions, commits, or every cute paragraph.

```text
cute != noisy
playful != repetitive
```

## 10. Final review checklist 🌱

Before merging a story-driven document, ask:

- [ ] Is the example clearly synthetic or illustrative?
- [ ] Are observable events separated from latent-state claims?
- [ ] Are names confined to the story / persona layer?
- [ ] Does every psychological-sounding statement have an evidence-safe rewrite?
- [ ] Are uncertainty and unknowns visible where needed?
- [ ] Did one anomaly accidentally become a pattern claim?
- [ ] Did the prose invent significance for an ordinary event?
- [ ] Is the story teaching a modeling decision rather than decorating the page?
- [ ] Could a skeptical engineer tell which statements are facts, model assumptions, and inferences?
- [ ] Is `XD` present only where it genuinely helps?

The target is simple:

```text
Narrative richness != interpretive overreach
Cute != sloppy
Story != evidence
Model != human
```
