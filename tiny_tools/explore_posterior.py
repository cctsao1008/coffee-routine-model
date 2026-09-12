from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable


STATE_KEYS = ("P", "M", "V", "C", "E", "F")
STATE_TITLES = {
    "P": "Predictability",
    "M": "Mutuality",
    "V": "Voluntariness",
    "C": "Shared Context",
    "E": "Everyday State Sharing",
    "F": "Friction",
}
EVENT_KEYS = (
    "opt_in",
    "reaction",
    "state_share",
    "proactive_update",
    "routine_maintenance",
    "pass_event",
    "resume_signal",
)
MODE_ORDER = ("Normal", "Busy", "Leave", "Special", "Recovery")
MODE_COLORS = {
    "Normal": "#8ecae6",
    "Busy": "#ffb703",
    "Leave": "#adb5bd",
    "Special": "#fb8500",
    "Recovery": "#90be6d",
}
STATE_COLORS = {
    "P": "#3a86ff",
    "M": "#ff006e",
    "V": "#8338ec",
    "C": "#2a9d8f",
    "E": "#f4a261",
    "F": "#6c757d",
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _required_output_columns() -> set[str]:
    required = {"sample_id", "scenario", "estimated_mode", "ESS"}
    for state in STATE_KEYS:
        required.update({f"est_{state}", f"ci95_low_{state}", f"ci95_high_{state}"})
    return required


def _active_events(row: dict[str, str]) -> list[str]:
    events: list[str] = []
    for key in EVENT_KEYS:
        raw = row.get(key, "")
        try:
            active = float(raw) > 0.0
        except ValueError:
            active = False
        if active:
            events.append(key)
    return events


def load_explorer_rows(
    output_csv: Path,
    events_csv: Path | None = None,
) -> list[dict[str, object]]:
    """Load one synthetic run without turning observations into private meaning. ☕🔎"""

    output_rows = _read_csv(output_csv)
    if not output_rows:
        raise ValueError("🙈 Posterior explorer found an empty output CSV.")

    missing = _required_output_columns() - set(output_rows[0])
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"🙈 Posterior explorer is missing required output columns: {names}")

    event_map: dict[str, list[str]] = {}
    if events_csv is not None:
        event_rows = _read_csv(events_csv)
        if event_rows and "sample_id" not in event_rows[0]:
            raise ValueError("🙈 Event CSV needs a sample_id column so tiny days can line up.")
        for row in event_rows:
            sample_id = row["sample_id"]
            if sample_id in event_map:
                raise ValueError(f"🙈 Duplicate event sample_id: {sample_id}")
            event_map[sample_id] = _active_events(row)

    rows: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for raw in output_rows:
        sample_id = raw["sample_id"]
        if sample_id in seen_ids:
            raise ValueError(f"🙈 Duplicate output sample_id: {sample_id}")
        seen_ids.add(sample_id)

        states: dict[str, dict[str, float]] = {}
        for state in STATE_KEYS:
            states[state] = {
                "estimate": float(raw[f"est_{state}"]),
                "low": float(raw[f"ci95_low_{state}"]),
                "high": float(raw[f"ci95_high_{state}"]),
            }

        rows.append(
            {
                "sample_id": int(float(sample_id)),
                "scenario": raw["scenario"],
                "estimated_mode": raw["estimated_mode"],
                "true_mode": raw.get("true_mode", ""),
                "ess": float(raw["ESS"]),
                "states": states,
                "events": event_map.get(sample_id, []),
            }
        )

    return rows


def _rgba(hex_color: str, alpha: float) -> str:
    value = hex_color.lstrip("#")
    red, green, blue = (int(value[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({red},{green},{blue},{alpha})"


def _day_detail(row: dict[str, object]) -> str:
    states = row["states"]
    assert isinstance(states, dict)
    events = row["events"]
    assert isinstance(events, list)

    lines = [
        f"<b>Day {row['sample_id']}</b>",
        f"Scenario: {row['scenario']}",
        f"Estimated mode: {row['estimated_mode']}",
        f"ESS: {row['ess']:.1f}",
        f"Observed events: {', '.join(events) if events else 'none of the highlighted clues'}",
        "<br><b>Posterior summary</b>",
    ]
    for state in STATE_KEYS:
        values = states[state]
        lines.append(
            f"{state} {values['estimate']:.3f} "
            f"[{values['low']:.3f}, {values['high']:.3f}]"
        )
    lines.append("<br>Posterior != human truth")
    return "<br>".join(lines)


def _mode_points(rows: list[dict[str, object]], field: str, y: float) -> tuple[list[int], list[float], list[str], list[str]]:
    x: list[int] = []
    ys: list[float] = []
    colors: list[str] = []
    hover: list[str] = []
    for row in rows:
        mode = str(row.get(field, ""))
        if mode not in MODE_COLORS:
            continue
        x.append(int(row["sample_id"]))
        ys.append(y)
        colors.append(MODE_COLORS[mode])
        label = "Estimated" if field == "estimated_mode" else "Synthetic truth"
        hover.append(f"Day {row['sample_id']}<br>{label} mode: {mode}")
    return x, ys, colors, hover


def _event_points(rows: list[dict[str, object]]) -> tuple[list[int], list[float], list[str]]:
    x: list[int] = []
    y: list[float] = []
    hover: list[str] = []
    for row in rows:
        events = row["events"]
        assert isinstance(events, list)
        if not events:
            continue
        x.append(int(row["sample_id"]))
        y.append(0.0)
        hover.append(
            f"Day {row['sample_id']}<br>Observed clues: {', '.join(events)}"
            "<br>Observation != intention"
        )
    return x, y, hover


def build_posterior_explorer(rows: list[dict[str, object]]):
    """Build one interactive view. Plotly stays an optional presentation dependency. 📈☕"""

    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Plotly is optional. Install the visualization extra with: "
            "python -m pip install '.[viz]'"
        ) from exc

    if not rows:
        raise ValueError("🙈 Posterior explorer needs at least one synthetic day.")

    days = [int(row["sample_id"]) for row in rows]
    details = [_day_detail(row) for row in rows]

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.70, 0.16, 0.14],
        subplot_titles=(
            "Latent routine-state posterior",
            "Routine mode",
            "Highlighted observable events",
        ),
    )

    state_trace_indices: dict[str, tuple[int, int, int]] = {}
    for state in STATE_KEYS:
        values = [row["states"][state] for row in rows]
        low = [item["low"] for item in values]
        high = [item["high"] for item in values]
        estimate = [item["estimate"] for item in values]
        color = STATE_COLORS[state]
        visible = state == "P"

        low_index = len(fig.data)
        fig.add_trace(
            go.Scatter(
                x=days,
                y=low,
                mode="lines",
                line={"width": 0},
                hoverinfo="skip",
                showlegend=False,
                visible=visible,
                legendgroup=state,
            ),
            row=1,
            col=1,
        )
        high_index = len(fig.data)
        fig.add_trace(
            go.Scatter(
                x=days,
                y=high,
                mode="lines",
                line={"width": 0},
                fill="tonexty",
                fillcolor=_rgba(color, 0.16),
                name=f"{state} 95% interval",
                hoverinfo="skip",
                showlegend=False,
                visible=visible,
                legendgroup=state,
            ),
            row=1,
            col=1,
        )
        mean_index = len(fig.data)
        fig.add_trace(
            go.Scatter(
                x=days,
                y=estimate,
                mode="lines",
                line={"color": color, "width": 2.4},
                name=f"{state} — {STATE_TITLES[state]}",
                text=details,
                hovertemplate="%{text}<extra></extra>",
                visible=visible,
                legendgroup=state,
            ),
            row=1,
            col=1,
        )
        state_trace_indices[state] = (low_index, high_index, mean_index)

    estimated_x, estimated_y, estimated_colors, estimated_hover = _mode_points(
        rows, "estimated_mode", 0.0
    )
    fig.add_trace(
        go.Scatter(
            x=estimated_x,
            y=estimated_y,
            mode="markers",
            marker={"symbol": "square", "size": 11, "color": estimated_colors},
            name="estimated mode",
            text=estimated_hover,
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    true_x, true_y, true_colors, true_hover = _mode_points(rows, "true_mode", 1.0)
    if true_x:
        fig.add_trace(
            go.Scatter(
                x=true_x,
                y=true_y,
                mode="markers",
                marker={
                    "symbol": "square-open",
                    "size": 9,
                    "color": true_colors,
                    "line": {"width": 1.4},
                },
                name="synthetic truth mode",
                text=true_hover,
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
            ),
            row=2,
            col=1,
        )

    event_x, event_y, event_hover = _event_points(rows)
    fig.add_trace(
        go.Scatter(
            x=event_x,
            y=event_y,
            mode="markers",
            marker={"symbol": "diamond", "size": 9},
            name="observed clue basket",
            text=event_hover,
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        ),
        row=3,
        col=1,
    )

    buttons = []
    total_traces = len(fig.data)
    fixed_indices = set(range(3 * len(STATE_KEYS), total_traces))
    for state in STATE_KEYS:
        visible = [False] * total_traces
        for index in state_trace_indices[state]:
            visible[index] = True
        for index in fixed_indices:
            visible[index] = True
        buttons.append(
            {
                "label": f"{state} — {STATE_TITLES[state]}",
                "method": "update",
                "args": [
                    {"visible": visible},
                    {"yaxis.title.text": f"{state} posterior value"},
                ],
            }
        )

    fig.update_layout(
        title={
            "text": "CSRDM Posterior Explorer ☕🐾<br>"
            "<sup>Hover a day for the full six-state posterior summary. "
            "Observed clues remain observations, not inferred intentions.</sup>",
            "x": 0.02,
        },
        template="plotly_white",
        height=900,
        hovermode="x unified",
        margin={"l": 72, "r": 32, "t": 110, "b": 60},
        updatemenus=[
            {
                "type": "dropdown",
                "direction": "down",
                "x": 1.0,
                "xanchor": "right",
                "y": 1.12,
                "yanchor": "top",
                "buttons": buttons,
                "active": 0,
            }
        ],
        annotations=list(fig.layout.annotations)
        + [
            {
                "text": "Posterior != human truth · Observation != intention",
                "xref": "paper",
                "yref": "paper",
                "x": 0.0,
                "y": -0.10,
                "showarrow": False,
                "font": {"size": 12},
            }
        ],
    )
    fig.update_yaxes(range=[0.0, 1.0], title_text="P posterior value", row=1, col=1)
    fig.update_yaxes(
        range=[-0.5, 1.5],
        tickvals=[0.0, 1.0] if true_x else [0.0],
        ticktext=["estimated", "synthetic truth"] if true_x else ["estimated"],
        row=2,
        col=1,
    )
    fig.update_yaxes(range=[-0.5, 0.5], tickvals=[], row=3, col=1)
    fig.update_xaxes(title_text="Synthetic day", row=3, col=1)
    return fig


def write_posterior_explorer(
    output_csv: Path,
    events_csv: Path | None,
    out_html: Path,
) -> Path:
    rows = load_explorer_rows(output_csv, events_csv)
    fig = build_posterior_explorer(rows)
    out_html.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out_html,
        include_plotlyjs=True,
        full_html=True,
        config={"displaylogo": False, "responsive": True},
    )
    return out_html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open one tiny CSRDM posterior in an interactive browser window. 📈☕"
    )
    parser.add_argument(
        "output_csv",
        nargs="?",
        type=Path,
        default=Path("examples/365-cute-days/output.csv"),
        help="simulator output.csv",
    )
    parser.add_argument(
        "--events",
        type=Path,
        default=None,
        help="matching input.csv with observable clues; defaults to output.csv sibling when present",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="standalone HTML output path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.output_csv.exists():
        raise SystemExit(f"🙈 Posterior explorer cannot find: {args.output_csv}")

    events = args.events
    if events is None:
        sibling = args.output_csv.with_name("input.csv")
        events = sibling if sibling.exists() else None
    if events is not None and not events.exists():
        raise SystemExit(f"🙈 Posterior explorer cannot find event basket: {events}")

    out_html = args.out or args.output_csv.with_name("posterior-explorer.html")
    try:
        result = write_posterior_explorer(args.output_csv, events, out_html)
    except (ValueError, RuntimeError) as exc:
        raise SystemExit(str(exc)) from exc

    print(f"📈☕ Tiny posterior explorer ready: {result}")


if __name__ == "__main__":
    main()
