from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CoffeeEvent:
    """One tiny observable event. No mind reading allowed. ☕🐾"""

    kind: str
    token: str | None = None


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

    return CoffeeEvent("unknown", raw)


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

    for item in events:
        event = item if isinstance(item, CoffeeEvent) else _event_from_token(
            item, invited=invited, delivered=delivered
        )
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
        elif kind == "reaction":
            obs["reaction"] = 1
        elif kind == "text_reply":
            obs["text_reply"] = 1
        elif kind == "state_share":
            obs["state_share"] = 1
        elif kind == "proactive_update":
            obs["proactive_update"] = 1
        elif kind == "resume":
            obs["resume_signal"] = 1
        elif kind == "pause":
            obs["pause_event"] = 1
        elif kind == "payment":
            obs["payment_event"] = 1
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
