# 03 — Why `pass` Is Not Failure 🌿☕

Suppose the protocol is working perfectly:

```text
Cheng: +1?
Linda: pass
```

Nothing is ambiguous. No coffee is delivered.

A naïve score might record:

```text
coffee = 0
therefore routine quality -= 1
```

That creates the wrong model.

## The modeling problem

A repeated routine can be stable **and** remain voluntary.

If participation is meaningful only when every invitation must become coffee, the model has accidentally turned continuity into obligation.

So CSRDM keeps a structural rule close:

```text
Continuity != obligation
Pass != failure
```

A clean `pass` is observable evidence that a choice was expressed. It is not automatically evidence that the routine broke.

## Voluntariness appears because counting is insufficient

This is where one latent dimension earns its place:

```text
V = Voluntariness
```

`V` asks whether the modeled routine still preserves room for choice.

The important part is not the exact numeric value. The important part is the design requirement:

> A model of a voluntary routine should not reward continuity so strongly that saying `pass` becomes mathematically equivalent to damage.

This is why the action model can represent a pass choice as boundary-preserving rather than as a secret penalty to Mutuality.

See [`../action-aware-dynamics.md`](../action-aware-dynamics.md) for the controlled transition details.

## Explicit opt-in matters too

The same logic applies to positive participation.

```text
invite
→ explicit opt-in
→ delivery
```

is different from assuming participation by default.

That distinction gives us a better conceptual pair:

```text
continuity + choice
```

instead of:

```text
continuity at any cost
```

## A useful correction

Initial intuition:

```text
more coffee days = stronger routine
```

Correction:

```text
frequency alone does not tell us whether participation remained voluntary
```

That does not mean frequency is useless. It means frequency needs context.

## Pass also teaches us something about Mutuality

Mutuality does not require both sides to perform identical actions.

One side may invite or deliver more often. The other may contribute through:

```text
opt-in
acknowledgment
exception updates
continuation
closure
```

So:

```text
Mutuality != 50/50 symmetry
```

This matters because a perfectly symmetric model would misread complementary participation as imbalance.

## The next question

We now have at least two useful ideas:

```text
Voluntariness
Mutuality
```

But the routine also raises questions about predictability, accumulated context, everyday state sharing, and friction.

Rather than adding variables because they sound nice, we should ask:

> **What problems does each hidden state actually solve?**

Continue to [`04-six-soft-states.md`](04-six-soft-states.md).
