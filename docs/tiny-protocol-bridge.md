# Tiny Protocol Bridge ☕➡️🧠➡️🐣

The coffee world starts with very small observable things:

```text
+1?
+
要
對
👍
pass
☕
pause
resume
水費
```

Those events are useful because they describe **what happened**.

They do not magically reveal **why it happened**.

```text
Protocol event != latent state
```

## Tiny translation table 🧺

| Little event | Observation clue |
|---|---|
| `+1?` | `invite = 1` |
| `+`, `要`, `對` | `opt_in = 1` |
| `pass` | `pass_event = 1`, and `opt_in = 0` when an invite is present |
| `☕` | `routine_maintenance = 1` |
| `resume` | `resume_signal = 1` |
| explicit state-sharing event | `state_share = 1` |
| explicit leave / exception update | `proactive_update = 1` |
| `水費` / payment | `payment_event = 1` |

`pause_event` and `payment_event` are preserved as observable metadata even though the current Particle Filter does not score them directly yet. Tiny clues are allowed to wait patiently for a future model. 🌱

## The little `👍` problem XD

The protocol accepts `👍` as a yes.

But the same symbol can also be a reaction after coffee arrives.

So context matters:

```text
+1? → 👍     = opt-in
☕  → 👍     = reaction
👍 by itself  = ambiguous
```

A lonely thumb is not forced into a story. 🐾

## Silence gets its own chair 🌿

If we only see:

```text
+1?
```

then the adapter returns:

```text
invite = 1
opt_in = None
pass_event = None
```

No hidden yes.
No hidden no.
No imaginary mood.

Just missing information.

## Tiny explicit events 🐣

When raw text is too ambiguous, callers can use an explicit `CoffeeEvent`:

```python
from protocol_adapter import CoffeeEvent, coffee_to_observation

obs = coffee_to_observation([
    CoffeeEvent("proactive_update", "leave notice"),
    CoffeeEvent("pause", "leave"),
    CoffeeEvent("resume", "back tomorrow"),
])
```

This keeps the adapter small and honest:

```text
Observable facts in.
Soft probabilistic guesses later.
Humans remain humans. ☕✨
```
