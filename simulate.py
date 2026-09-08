from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np

from model import MODE_NAMES, RoutineMode, relationship_index
from particles import CoffeeParticleFilter


DEFAULT_SEED = 20260908
DEFAULT_DAYS = 365
DEFAULT_PARTICLES = 6000
STATE_KEYS = ("P", "M", "V", "C", "E", "F")
STATE_METRIC_NAMES = (
    "P_predictability",
    "M_mutuality",
    "V_voluntariness",
    "C_shared_context",
    "E_state_sharing",
    "F_friction",
)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def generate_truth(days: int, rng: np.random.Generator):
    states = np.zeros((days, 6))
    modes = np.zeros(days, dtype=int)
    states[0] = [0.78, 0.68, 0.88, 0.70, 0.36, 0.14]

    transition = CoffeeParticleFilter.transition
    target = CoffeeParticleFilter.target

    for t in range(1, days):
        modes[t] = rng.choice(5, p=transition[modes[t - 1]])
        mode_effect = np.zeros(6)

        if modes[t] == RoutineMode.BUSY:
            mode_effect = [-0.005, -0.008, 0.000, -0.002, -0.002, 0.008]
        elif modes[t] == RoutineMode.LEAVE:
            mode_effect = [-0.008, -0.010, 0.000, -0.005, -0.005, 0.005]
        elif modes[t] == RoutineMode.SPECIAL:
            mode_effect = [0.010, 0.012, 0.005, 0.015, 0.020, -0.004]
        elif modes[t] == RoutineMode.RECOVERY:
            mode_effect = [0.006, 0.006, 0.003, 0.008, 0.005, -0.005]

        states[t] = np.clip(
            states[t - 1]
            + 0.035 * (target - states[t - 1])
            + mode_effect
            + rng.normal(0, [0.012, 0.014, 0.009, 0.012, 0.018, 0.009]),
            0.02,
            0.98,
        )

    return states, modes


def observe(x, mode, rng):
    p, m, v, c, e, f = x
    invite = int(mode != RoutineMode.LEAVE and rng.random() < 0.92)

    mode_opt = {0: 0.0, 1: -0.7, 2: -2.5, 3: 0.2, 4: 0.15}[int(mode)]
    opt_in = int(invite and rng.random() < sigmoid(-1.2 + 1.7*m + 1.2*v + 0.8*p - 1.8*f + mode_opt))
    text_reply = int(rng.random() < sigmoid(-0.7 + 1.1*m + 0.6*c + 0.3*e - 0.8*f + 0.2*(mode == 3) - 0.2*(mode == 1)))
    reaction = int(rng.random() < sigmoid(-0.6 + 0.9*m + 0.5*p + 0.4*v - 0.5*f))
    state_share = int(rng.random() < sigmoid(-2.2 + 2.0*e + 0.8*c + 0.3*m - 0.3*(mode == 1)))
    proactive_update = int(rng.random() < sigmoid(-1.8 + 1.3*m + 0.8*c + 0.5*e - 0.6*f + 0.45*(mode in (1, 2))))

    mode_maint = {0: 0.0, 1: -0.3, 2: -1.4, 3: 0.3, 4: 0.6}[int(mode)]
    routine_maintenance = int(rng.random() < sigmoid(-1.1 + 1.5*p + 1.4*m + 0.9*v + 0.7*c - 1.4*f + mode_maint))

    mode_pass = {0: -0.5, 1: 1.2, 2: 2.7, 3: -0.5, 4: -1.0}[int(mode)]
    pass_event = int(invite and rng.random() < sigmoid(-2.5 - 1.0*m + 1.0*f + mode_pass))

    mode_resume = {0: -0.8, 1: -0.5, 2: -1.0, 3: 0.0, 4: 2.8}[int(mode)]
    resume_signal = int(rng.random() < sigmoid(-3.0 + 1.0*p + 0.6*m + mode_resume))

    tone_warmth = float(np.clip(0.15 + 0.28*m + 0.18*v + 0.16*c + 0.12*e - 0.20*f + rng.normal(0, 0.07), 0, 1))
    delay_base = 8 + 45*(1-p) + 30*(1-m) + 75*(mode == 1) + 110*(mode == 2)
    response_delay_min = float(np.clip(rng.lognormal(math.log(max(1.0, delay_base)), 0.45), 0.2, 360))

    return {
        "cheng_invite": invite,
        "linda_opt_in": opt_in,
        "text_reply": text_reply,
        "reaction": reaction,
        "state_share": state_share,
        "proactive_update": proactive_update,
        "routine_maintenance": routine_maintenance,
        "pass_event": pass_event,
        "resume_signal": resume_signal,
        "tone_warmth": tone_warmth,
        "response_delay_min": response_delay_min,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Simulate a tiny coffee routine. ☕🐣")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="number of synthetic days (default: 365)")
    parser.add_argument("--particles", type=int, default=DEFAULT_PARTICLES, help="particle count (default: 6000)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="random seed")
    parser.add_argument("--out", type=Path, default=None, help="output directory")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 2:
        raise SystemExit("☕ --days must be at least 2")
    if args.particles < 100:
        raise SystemExit("🐣 --particles must be at least 100")

    out = args.out or Path(f"examples/{args.days}-cute-days")
    rng = np.random.default_rng(args.seed)
    truth, true_modes = generate_truth(args.days, rng)
    observations = [observe(truth[t], true_modes[t], rng) for t in range(args.days)]

    pf = CoffeeParticleFilter(particle_count=args.particles, seed=args.seed)
    estimates = []
    estimated_modes = []
    ci95_low = []
    ci95_high = []
    ess = []

    for obs in observations:
        posterior = pf.update(obs)
        estimates.append(posterior.mean)
        estimated_modes.append(posterior.mode)
        ci95_low.append(posterior.ci95_low)
        ci95_high.append(posterior.ci95_high)
        ess.append(posterior.ess)

    estimates = np.asarray(estimates)
    ci95_low = np.asarray(ci95_low)
    ci95_high = np.asarray(ci95_high)
    ess = np.asarray(ess)

    true_r = relationship_index(truth)
    est_r = relationship_index(estimates)

    rmse = np.sqrt(np.mean((estimates - truth)**2, axis=0))
    mae = np.mean(np.abs(estimates - truth), axis=0)
    correlation = np.array([
        np.corrcoef(estimates[:, i], truth[:, i])[0, 1]
        for i in range(6)
    ])
    coverage = np.mean((truth >= ci95_low) & (truth <= ci95_high), axis=0)

    r_rmse = float(np.sqrt(np.mean((est_r - true_r)**2)))
    r_mae = float(np.mean(np.abs(est_r - true_r)))
    r_corr = float(np.corrcoef(est_r, true_r)[0, 1])
    mode_accuracy = float(np.mean([
        estimated_modes[t] == MODE_NAMES[RoutineMode(int(true_modes[t]))]
        for t in range(args.days)
    ]))

    out.mkdir(parents=True, exist_ok=True)

    with (out / "input.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sample_id", *observations[0].keys()])
        writer.writeheader()
        for i, obs in enumerate(observations, 1):
            writer.writerow({"sample_id": i, **obs})

    with (out / "output.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["sample_id", "true_mode", "estimated_mode", "ESS"]
        for name in STATE_KEYS:
            fieldnames += [f"true_{name}", f"est_{name}", f"ci95_low_{name}", f"ci95_high_{name}"]
        fieldnames += ["true_R", "est_R"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for t in range(args.days):
            row = {
                "sample_id": t + 1,
                "true_mode": MODE_NAMES[RoutineMode(int(true_modes[t]))],
                "estimated_mode": estimated_modes[t],
                "ESS": ess[t],
                "true_R": true_r[t],
                "est_R": est_r[t],
            }
            for j, name in enumerate(STATE_KEYS):
                row[f"true_{name}"] = truth[t, j]
                row[f"est_{name}"] = estimates[t, j]
                row[f"ci95_low_{name}"] = ci95_low[t, j]
                row[f"ci95_high_{name}"] = ci95_high[t, j]
            writer.writerow(row)

    with (out / "metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric_scope", "RMSE", "MAE", "Pearson_r", "CI95_coverage"])
        for name, state_rmse, state_mae, state_r, state_coverage in zip(
            STATE_METRIC_NAMES, rmse, mae, correlation, coverage
        ):
            writer.writerow([name, state_rmse, state_mae, state_r, state_coverage])
        writer.writerow(["relationship_index_R", r_rmse, r_mae, r_corr, ""])
        writer.writerow(["mode_classification_accuracy", "", "", mode_accuracy, ""])

    print(f"☕ {args.days} cute synthetic days generated")
    print(f"🐣 particles               : {args.particles}")
    print(f"🌱 relationship-index RMSE : {r_rmse:.4f}")
    print(f"✨ relationship-index MAE  : {r_mae:.4f}")
    print(f"🧭 relationship-index r    : {r_corr:.3f}")
    print(f"🎯 mode accuracy           : {mode_accuracy:.2%}")
    print(f"🧺 output                  : {out}")


if __name__ == "__main__":
    main()
