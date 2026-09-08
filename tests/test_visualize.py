import csv

from visualize import STATE_KEYS, paint_coffee_year


def test_tiny_painter_makes_every_promised_picture(tmp_path):
    output_csv = tmp_path / "output.csv"
    fieldnames = ["sample_id", "true_mode", "estimated_mode", "ESS"]
    for state in STATE_KEYS:
        fieldnames += [f"true_{state}", f"est_{state}", f"ci95_low_{state}", f"ci95_high_{state}"]
    fieldnames += ["true_R", "est_R"]

    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for day, mode in enumerate(("Normal", "Busy", "Recovery", "Special"), 1):
            row = {
                "sample_id": day,
                "true_mode": mode,
                "estimated_mode": mode,
                "ESS": 250.0 + day,
                "true_R": 0.70 + day * 0.01,
                "est_R": 0.69 + day * 0.01,
            }
            for state in STATE_KEYS:
                row[f"true_{state}"] = 0.7
                row[f"est_{state}"] = 0.68
                row[f"ci95_low_{state}"] = 0.60
                row[f"ci95_high_{state}"] = 0.76
            writer.writerow(row)

    pictures = paint_coffee_year(output_csv, tmp_path / "gallery")
    names = {path.name for path in pictures}

    assert names == {
        "state-P.png",
        "state-M.png",
        "state-V.png",
        "state-C.png",
        "state-E.png",
        "state-F.png",
        "modes.png",
        "ess.png",
        "tiny-year-summary.png",
    }
    assert all(path.exists() and path.stat().st_size > 0 for path in pictures)
