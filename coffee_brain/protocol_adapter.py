from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .actions import RoutineActions


@dataclass(frozen=True)
class CoffeeEvent:
    """One tiny observable event. No mind reading allowed. ☕🐾"""

    kind: str
    token: str | None = None


@dataclass(frozen=True)
class CoffeeStep:
    """One tiny state-space step with actions and clues kept in separate baskets. 🧺✨"""

    actions: RoutineActions
    observation: dict


YES_TOKENS = {"+", "+1", "要", "對"}
INVITE_TOKENS = {"+1?", "+?", "coffee?", "咖啡?", "咖啡？"}
PASS_TOKENS = {"pass"}
DELIVERY_TOKENS = {"☕", "delivered", "coffee delivered"}
RESUME_TOKENS = {"resume"}
PAUSE_TOKENS = {"pause"}
REACTION_TOKENS = {"👍", "❤️", "❤", "😂"}


def _empty_observation() -> dict:
    """A little basket with only things we actually observed. 🧺"""

    return {
        "invite": None,
        "opt_in": None,
        "text_reply": None,
        "reaction": None,
        "state_share": None,
        "proactive_update": None,
        "routine_maintenance": None,
        "pass_event": None,
        "resume_signal": None,
        "tone_warmth": None,
        "response_delay_min": None,
        "pause_event": None,
        "payment_event": None,
        "unknown_events": [],
    }


def _normalize_token(token: str) -> str:
    return token.strip()


def _event_from_token(token: str, *, invited: bool, delivered: bool) -> CoffeeEvent:
    """Turn tiny protocol text into an event without inventing feelings. 🐣"""

    raw = _normalize_token(token)
    lowered = raw.lower()

    if raw in INVITE_TOKENS or lowered in INVITE_TOKENS:
        return CoffeeEvent("invite", raw)
    if raw in YES_TOKENS:
        return CoffeeEvent("opt_in", raw)
    if lowered in PASS_TOKENS:
        return CoffeeEvent("pass", raw)
    if raw in DELIVERY_TOKENS or lowered in DELIVERY_TOKENS:
        return CoffeeEvent("delivered", raw)
    if lowered in RESUME_TOKENS:
        return CoffeeEvent("resume", raw)
    if lowered in PAUSE_TOKENS:
        return CoffeeEvent("pause", raw)

    # 👍 is deliberately contextual: the protocol allows it as yes,
    # but after delivery it is usually just a reaction. Cute != overconfident. ☕
    if raw == "👍":
        if invited and not delivered:
            return CoffeeEvent("opt_in", raw)
        if delivered:
            return CoffeeEvent("reaction", raw)
        return CoffeeEvent("ambiguous", raw)

    if raw in REACTION_TOKENS:
        return CoffeeEvent("reaction", raw)

    if lowered in {"text", "reply", "text_reply"}:
        return CoffeeEvent("text_reply", raw)
    if lowered in {"state", "state_share", "state-sharing"}:
        return CoffeeEvent("state_share", raw)
    if lowered in {"update", "proactive_update", "leave notice", "exception"}:
        return CoffeeEvent("proactive_update", raw)
    if lowered in {"payment", "paid", "water fee", "水費"}:
        return CoffeeEvent("payment", raw)

    # Explicit action-only words for the controlled state-space layer. 🎮☕
    if lowered in {"notify", "notification"}:
        return CoffeeEvent("notify", raw)
    if lowered in {"callback", "remember", "remembered callback"}:
        return CoffeeEvent("callback", raw)
    if lowered in {"boundary", "boundary-preserving", "boundary_preserving"}:
        return CoffeeEvent("boundary_preserving", raw)
    if lowered in {"ack", "acknowledge", "acknowledgement"}:
        return CoffeeEvent("acknowledge", raw)
    if lowered in {"exception_sync", "exception sync"}:
        return CoffeeEvent("exception_sync", raw)
    if lowered in {"closure", "close loop", "loop closure"}:
        return CoffeeEvent("closure", raw)

    return CoffeeEvent("unknown", raw)


def _parse_events(events: Iterable[str | CoffeeEvent]) -> list[CoffeeEvent]:
    """Parse once so action and observation baskets see the same tiny facts. ☕👀"""

    parsed: list[CoffeeEvent] = []
    invited = False
    delivered = False

    for item in events:
        event = item if isinstance(item, CoffeeEvent) else _event_from_token(
            item, invited=invited, delivered=delivered
        )
        parsed.append(event)
        kind = event.kind.strip().lower()
        if kind == "invite":
            invited = True
        elif kind == "delivered":
            delivered = True

    return parsed


def coffee_to_actions(events: Iterable[str | CoffeeEvent]) -> RoutineActions:
    """Put observable actions into their own controlled-dynamics basket. ☕🎮🧺"""

    values = {name: 0.0 for name in RoutineActions.__dataclass_fields__}
    for event in _parse_events(events):
        kind = event.kind.strip().lower()
        if kind == "invite":
            values["a_invite"] = 1.0
        elif kind == "delivered":
            values["a_deliver"] = 1.0
        elif kind == "notify":
            values["a_notify"] = 1.0
        elif kind == "callback":
            values["a_callback"] = 1.0
        elif kind == "boundary_preserving":
            values["a_boundary_preserving"] = 1.0
        elif kind == "opt_in":
            values["b_opt_in"] = 1.0
        elif kind == "pass":
            values["b_pass_choice"] = 1.0
        elif kind in {"reaction", "acknowledge"}:
            values["b_acknowledge"] = 1.0
        elif kind in {"proactive_update", "exception_sync"}:
            values["b_exception_sync"] = 1.0
        elif kind in {"payment", "closure"}:
            values["b_closure"] = 1.0

    return RoutineActions(**values)


def coffee_to_observation(
    events: Iterable[str | CoffeeEvent],
    *,
    tone_warmth: float | None = None,
    response_delay_min: float | None = None,
) -> dict:
    """Convert protocol-level events into a PF-ready observation basket. ☕➡️🐣

    Only observable facts are encoded. Missing facts stay ``None`` so the
    estimator can remain uncertain instead of receiving made-up neutral data.
    """

    obs = _empty_observation()
    invited = False
    delivered = False

    for event in _parse_events(events):
        kind = event.kind.strip().lower()

        if kind == "invite":
            obs["invite"] = 1
            invited = True
        elif kind == "opt_in":
            obs["opt_in"] = 1
            if obs["text_reply"] is None:
                obs["text_reply"] = 1
        elif kind == "pass":
            obs["pass_event"] = 1
            if invited:
                obs["opt_in"] = 0
            if obs["text_reply"] is None:
                obs["text_reply"] = 1
        elif kind == "delivered":
            obs["routine_maintenance"] = 1
            delivered = True
        elif kind in {"reaction", "acknowledge"}:
            obs["reaction"] = 1
        elif kind == "text_reply":
            obs["text_reply"] = 1
        elif kind == "state_share":
            obs["state_share"] = 1
        elif kind in {"proactive_update", "exception_sync"}:
            obs["proactive_update"] = 1
        elif kind == "resume":
            obs["resume_signal"] = 1
        elif kind == "pause":
            obs["pause_event"] = 1
        elif kind == "payment":
            obs["payment_event"] = 1
        elif kind in {"notify", "callback", "boundary_preserving", "closure"}:
            # These belong to the explicit action basket in the controlled model.
            pass
        else:
            obs["unknown_events"].append(event.token or event.kind)

    if obs["invite"] == 1 and obs["opt_in"] is None and obs["pass_event"] is None:
        # Silence is not automatically yes or no. 🌱
        pass

    if tone_warmth is not None:
        if not 0.0 <= tone_warmth <= 1.0:
            raise ValueError("🌡️ Tiny warmth must stay between 0 and 1.")
        obs["tone_warmth"] = float(tone_warmth)

    if response_delay_min is not None:
        if response_delay_min < 0.0:
            raise ValueError("⏰ Tiny reply delay cannot travel backward in time XD")
        obs["response_delay_min"] = float(response_delay_min)

    return obs


def coffee_to_step(
    events: Iterable[str | CoffeeEvent],
    *,
    tone_warmth: float | None = None,
    response_delay_min: float | None = None,
) -> CoffeeStep:
    """Split one protocol moment into controlled actions and observed clues. ☕🎮👀"""

    parsed = _parse_events(events)
    return CoffeeStep(
        actions=coffee_to_actions(parsed),
        observation=coffee_to_observation(
            parsed,
            tone_warmth=tone_warmth,
            response_delay_min=response_delay_min,
        ),
    )
