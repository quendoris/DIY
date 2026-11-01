#!/usr/bin/env python3
"""Inverse small-signal sealed-box sizing to compare candidate woofer volumes.

Not a final box design: ignores finite cone excursion, real response,
cabinet displacement, damping/leakage, nearfield desk effects and DSP.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from acoustic_baseline import SealedBox

ROOT = Path(__file__).resolve().parent


def volume_for_qtc(qts: float, vas_l: float, target_qtc: float) -> float:
    """Vb = Vas / ((Qtc/Qts)^2 - 1), ideal sealed-box relation."""
    if min(qts, vas_l, target_qtc) <= 0:
        raise ValueError("parameters must be positive")
    if target_qtc <= qts:
        raise ValueError("finite positive sealed volume requires target Qtc > Qts")
    return vas_l / ((target_qtc / qts) ** 2 - 1)


def compare(catalog: dict, qtc: float = 1 / 2**0.5) -> dict:
    result = {"assumption": "ideal second-order sealed box, fixed Qtc",
              "target_qtc": qtc, "midwoofers": [], "subwoofers": []}
    for category in ("midwoofers", "subwoofers"):
        for v in catalog[category]:
            try:
                liters = volume_for_qtc(v["qts"], v["vas_l"], qtc)
            except ValueError:
                row = {"id": v["id"], "status": "NO_FINITE_POSITIVE_BOX"}
            else:
                box = SealedBox(v["fs_hz"], v["qts"], v["vas_l"], liters)
                row = {"id": v["id"], "status": "IDEAL_SEALED_QTC",
                       "net_box_l": round(liters, 3),
                       "fc_hz": round(box.fc_hz, 3),
                       "f3_hz": round(box.f3_hz(), 3)}
            row["source"] = v["source"]
            result[category].append(row)
    result["limits"] = [
        "Qtc alone is not a listening-quality objective",
        "No driver measured and no SPL, excursion, vent, room, baffle or DSP modeled",
        "Net internal volume excludes real driver/bracing/electronics displacements",
        "Manufacturer T/S and sensitivity can vary with drive level and tolerance",
    ]
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--qtc", type=float, default=1 / 2**0.5)
    args = p.parse_args()
    catalog = json.loads((ROOT / "candidates.json").read_text(encoding="utf8"))
    print(json.dumps(compare(catalog, args.qtc), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
