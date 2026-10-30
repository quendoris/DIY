#!/usr/bin/env python3
"""Compare manufacturer T/S data using a deliberately simple closed-box model.

No real loudspeaker, baffle, crossover, port, excursion or room acoustics are
simulated. Inputs retain provenance in candidates.json.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from acoustic_baseline import SealedBox

BASE = Path(__file__).resolve().parent


def compare_catalog(catalog: dict) -> dict:
    groups = {}
    for key in ("midwoofers", "subwoofers"):
        rows = []
        for candidate in catalog[key]:
            box = SealedBox(
                candidate["fs_hz"],
                candidate["qts"],
                candidate["vas_l"],
                candidate["illustrative_box_l"],
            )
            sd = candidate.get("sd_cm2")
            xmax = candidate.get("xmax_mm")
            vd_cm3 = round(sd * xmax / 10, 2) if sd is not None and xmax is not None else None
            rows.append({
                "id": candidate["id"],
                "maker": candidate["maker"],
                "diameter_in": candidate["diameter_in"],
                "illustrative_box_l": candidate["illustrative_box_l"],
                "sealed_fc_hz": round(box.fc_hz, 2),
                "sealed_qtc": round(box.qtc, 3),
                "sealed_f3_hz": round(box.f3_hz(), 2),
                "vd_cm3_if_xmax_defined": vd_cm3,
                "source": candidate["source"],
                "disclaimer": "Illustrative small-signal sealed box, no real in-room SPL",
            })
        groups[key] = rows
    return {
        "status": "MODEL ONLY, NOT PURCHASE RECOMMENDATIONS",
        "schema_version": 1,
        "groups": groups,
        "tweeters": [
            {"id": t["id"], "kind": t["kind"], "fs_hz": t["fs_hz"],
             "sensitivity_2v83_1m_db": t["sensitivity_2v83_1m_db"],
             "source": t["source"]}
            for t in catalog["tweeters"]
        ],
        "limitations": [
            "Sealed small-signal only; f3 is free-field small-signal response",
            "Not a vented, bandpass or passive-radiator comparison",
            "No actual measurements, SPL, distortion, thermal budget, maximum excursion or DSP EQ",
            "No off-axis response, nearfield summation, desk/room effects, port airspeed or acoustic crossover",
            "Displacement is estimated as Sd(cm²)*Xmax(mm)/10 only for comparable reported Xmax"
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=BASE / "candidates.json")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    report = compare_catalog(catalog)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return
    for group in ("midwoofers", "subwoofers"):
        print(f"## {group}")
        print("| Driver | Demo closed box, L | Fc, Hz | Qtc | F3, Hz | Vd if Xmax known, cm³ |")
        print("|---|---:|---:|---:|---:|---:|")
        for v in report["groups"][group]:
            displacement = f"{v['vd_cm3_if_xmax_defined']:.1f}" if v["vd_cm3_if_xmax_defined"] is not None else "n/a"
            print(f"| {v['id']} | {v['illustrative_box_l']} | {v['sealed_fc_hz']} | "
                  f"{v['sealed_qtc']} | {v['sealed_f3_hz']} | {displacement} |")
        print()
    print("All calculated values are model demonstrations; no actual drive-level SPL or physical response prediction.")


if __name__ == "__main__":
    main()
