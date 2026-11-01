#!/usr/bin/env python3
"""Comparison of user-proposed HiVi driver offers.

The catalog separates conflicting F6N parameter scenarios; results are only
illustrative second-order small-signal SEALED-box electrical-mechanical models.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from acoustic_baseline import SealedBox

DATA = Path(__file__).with_name("hivi_offers_2026-11-01.json")
Q_BUTTERWORTH = 1 / math.sqrt(2)


def volume_at_qtc(qts: float, vas_l: float, desired_qtc: float = Q_BUTTERWORTH) -> float:
    if min(qts, vas_l, desired_qtc) <= 0 or desired_qtc <= qts:
        raise ValueError("finite positive sealed box requires Qtc > Qts > 0 and Vas > 0")
    return vas_l / ((desired_qtc / qts) ** 2 - 1)


def compare(catalog: dict, fixture_l: float = 8.0) -> dict:
    if fixture_l <= 0:
        raise ValueError("fixture volume must be positive")
    rows = []
    for candidate in catalog["candidates"]:
        scenarios = candidate["scenarios"]
        if not scenarios:
            raise ValueError("candidate must have at least one sourced scenario")
        for s in scenarios:
            box = SealedBox(s["fs_hz"], s["qts"], s["vas_l"], fixture_l)
            target_l = volume_at_qtc(s["qts"], s["vas_l"])
            target_box = SealedBox(s["fs_hz"], s["qts"], s["vas_l"], target_l)
            qts_from_components = 1 / (1 / s["qms"] + 1 / s["qes"])
            rows.append({
                "model": candidate["model"],
                "scenario_id": s["id"],
                "source_type": s["provenance"],
                "source": s.get("source", "user-supplied seller description"),
                "seller_observed_price_rub_each": candidate["unit_price_rub_user_observed"],
                "seller_observed_price_rub_pair": 2 * candidate["unit_price_rub_user_observed"],
                "fixture_net_volume_l": fixture_l,
                "fixture_fc_hz": round(box.fc_hz, 2),
                "fixture_qtc": round(box.qtc, 3),
                "fixture_f3_hz": round(box.f3_hz(), 2),
                "butterworth_qtc": Q_BUTTERWORTH,
                "butterworth_box_net_l": round(target_l, 2),
                "butterworth_f3_hz": round(target_box.f3_hz(), 2),
                "qts_from_qms_and_qes": round(qts_from_components, 4),
                "qts_source_value": s["qts"],
                "source_internal_qts_difference": round(abs(s["qts"] - qts_from_components), 4),
                "rated_power_w": candidate["rated_w"],
                "max_power_w": candidate["max_w"],
                "notes": "Not a measured cabinet, not a loudness or midrange distortion prediction",
            })
    return {
        "status": "HYPOTHETICAL small-signal, not a purchasing recommendation",
        "speaker_distance_m": [0.60, 0.80],
        "comparison": rows,
        "known_source_disagreement": [
            "F6N seller vs independent database differ in Fs, Qts, Vas and Xmax",
            "D6G Qts/Vas absent from user listing; third-party data only",
            "M6N seller moving mass unit typo; exact part/revision still to verify",
        ],
        "limitations": [
            "8L is a fixture example, not a cabinet recommendation",
            "No complex drive voltage/excursion, driver polar response, breakup, distortion or thermal behavior",
            "No impedance Le, bafflestep, room, desktop reflection, filter phase, tweeter or sub integration",
            "Seller prices not independently verified and actual shipping/revision may differ",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(compare(json.loads(DATA.read_text(encoding="utf-8"))),
                     ensure_ascii=False, indent=2, sort_keys=True))
