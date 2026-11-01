#!/usr/bin/env python3
"""Audit a full 3-way stereo+sub parts shortlist against a 2-way+sub baseline.

Only manufacturer/seller metadata and arithmetic. This is NOT an acoustic
response, distortion, excursion-at-drive, room, phase, or cooling simulation.
"""
from __future__ import annotations
import json
from pathlib import Path

CATALOG = Path(__file__).with_name("threeway_system_candidates_2026-11.json")
PART_GROUPS = ("midranges", "tweeters", "bass_satellites", "subwoofers")


def evaluate(data: dict) -> dict:
    parts = {}
    for name in PART_GROUPS:
        for entry in data[name]:
            if entry["id"] in parts:
                raise ValueError("duplicate part id")
            parts[entry["id"]] = entry
    out = []
    for candidate in data["sample_systems"]:
        drivers = candidate["per_satellite"]
        active_channels = 2 * len(drivers) + 1
        if active_channels != candidate["speaker_channels"]:
            raise ValueError(f"{candidate['id']}: inconsistent amplifier channel count")
        sub = parts[candidate["sub"]]
        per_satellite_cost = sum(parts[id]["price_rub_unit"] for id in drivers)
        predicted_driver_cost = 2*per_satellite_cost + sub["price_rub_unit"]
        if predicted_driver_cost != candidate["estimated_drivers_rub"]:
            raise ValueError(f"{candidate['id']}: inconsistent item cost")
        out.append({
            "system_id": candidate["id"],
            "satellite_driver_count_each": len(drivers),
            "digital_amp_output_channels": active_channels,
            "satellite_drivers": drivers,
            "satellite_ohm_each": [parts[id]["ohm"] for id in drivers],
            "sub_driver": candidate["sub"],
            "sub_ohm": sub["ohm"],
            "drivers_only_rub": predicted_driver_cost,
            "excluded":"amps, DSP/DAC, MCU, fiber, PSUs, final cabinet, shipping, taxes, tools",
            "status":"USER/RETAILER PRICE OBSERVATIONS, ACOUSTIC PERFORMANCE NOT EVALUATED",
        })
    subs=[]
    for p in data["subwoofers"]:
        theoretical = p["sd_cm2"]*p["xmax_oneway_mm"]/10
        if abs(theoretical-p["vd_cm3"])>0.11:
            raise ValueError(f"{p['id']}: displacement inconsistent")
        subs.append({"id":p["id"],"vd_cm3":round(theoretical,1),
                     "unit_price_rub":p["price_rub_unit"],
                     "measured_bass_at_25hz":None})
    return {"system_comparisons":out,"subwoofer_displacement_comparison":subs,
            "important":"Output displacement is a geometric estimate, not proof of SPL/THD at any frequency."}


if __name__ == "__main__":
    data=json.loads(CATALOG.read_text(encoding="utf-8"))
    print(json.dumps(evaluate(data),ensure_ascii=False,indent=2))
