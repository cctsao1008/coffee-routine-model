from __future__ import annotations

import argparse
import json

from coffee_brain.observation_model import (
    BINARY_CHANNEL_NAMES,
    DEFAULT_OBSERVATION_MODEL,
    STATE_ORDER,
)


MODE_ORDER = ("Normal", "Busy", "Leave", "Special", "Recovery")


def _edge_status(value: float) -> tuple[str, str]:
    if abs(float(value)) > 0.0:
        return "present", "Assumed"
    return "no-direct-edge", "Undefined beyond the current direct specification"


def build_inventory() -> list[dict[str, object]]:
    """Read the default observation recipe without inventing a second source of truth. 🎛️☕"""

    config = DEFAULT_OBSERVATION_MODEL
    rows: list[dict[str, object]] = []

    for name in BINARY_CHANNEL_NAMES:
        channel = getattr(config, name)
        rows.append(
            {
                "channel": name,
                "parameter_kind": "intercept",
                "target": "baseline",
                "value": float(channel.intercept),
                "model_edge": "baseline",
                "epistemic_status": "Assumed",
            }
        )
        for state, value in zip(STATE_ORDER, channel.state_coefficients):
            edge, status = _edge_status(value)
            rows.append(
                {
                    "channel": name,
                    "parameter_kind": "state_coefficient",
                    "target": state,
                    "value": float(value),
                    "model_edge": edge,
                    "epistemic_status": status,
                }
            )
        for mode, value in zip(MODE_ORDER, channel.mode_offsets):
            edge, status = _edge_status(value)
            rows.append(
                {
                    "channel": name,
                    "parameter_kind": "mode_offset",
                    "target": mode,
                    "value": float(value),
                    "model_edge": edge,
                    "epistemic_status": status,
                }
            )

    warmth = config.tone_warmth
    rows.append(
        {
            "channel": "tone_warmth",
            "parameter_kind": "intercept",
            "target": "baseline",
            "value": float(warmth.intercept),
            "model_edge": "baseline",
            "epistemic_status": "Assumed",
        }
    )
    for state, value in zip(STATE_ORDER, warmth.state_coefficients):
        edge, status = _edge_status(value)
        rows.append(
            {
                "channel": "tone_warmth",
                "parameter_kind": "state_coefficient",
                "target": state,
                "value": float(value),
                "model_edge": edge,
                "epistemic_status": status,
            }
        )
    for mode, value in zip(MODE_ORDER, warmth.mode_offsets):
        edge, status = _edge_status(value)
        rows.append(
            {
                "channel": "tone_warmth",
                "parameter_kind": "mode_offset",
                "target": mode,
                "value": float(value),
                "model_edge": edge,
                "epistemic_status": status,
            }
        )
    rows.append(
        {
            "channel": "tone_warmth",
            "parameter_kind": "noise_scale",
            "target": "sigma",
            "value": float(warmth.sigma),
            "model_edge": "noise",
            "epistemic_status": "Assumed",
        }
    )

    delay = config.response_delay
    delay_parameters = (
        ("base_minutes", "baseline", delay.base_minutes, "baseline"),
        ("state_gap", "P", delay.predictability_gap_minutes, "present"),
        ("state_gap", "M", delay.mutuality_gap_minutes, "present"),
        ("noise_scale", "sigma_log", delay.sigma_log, "noise"),
        ("floor", "minimum_mean_minutes", delay.minimum_mean_minutes, "floor"),
    )
    for kind, target, value, edge in delay_parameters:
        rows.append(
            {
                "channel": "response_delay",
                "parameter_kind": kind,
                "target": target,
                "value": float(value),
                "model_edge": edge,
                "epistemic_status": "Assumed",
            }
        )
    for mode, value in zip(MODE_ORDER, delay.mode_add_minutes):
        edge, status = _edge_status(value)
        rows.append(
            {
                "channel": "response_delay",
                "parameter_kind": "mode_add_minutes",
                "target": mode,
                "value": float(value),
                "model_edge": edge,
                "epistemic_status": status,
            }
        )

    return rows


def _markdown_table(rows: list[dict[str, object]]) -> str:
    lines = [
        "| channel | kind | target | value | model edge | epistemic status |",
        "|---|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {channel} | {parameter_kind} | {target} | {value:g} | {model_edge} | {epistemic_status} |".format(
                **row
            )
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect the default observation-model provenance without changing the model. 🎛️🧭☕"
    )
    parser.add_argument("--json", action="store_true", help="Print the inventory as JSON instead of a Markdown table.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_inventory()
    if args.json:
        print(json.dumps(rows, indent=2))
        return
    print("🎛️🧭 Default observation-model provenance inventory")
    print("Assumed direct edge != discovered law")
    print("No direct edge != proven independence\n")
    print(_markdown_table(rows))


if __name__ == "__main__":
    main()
