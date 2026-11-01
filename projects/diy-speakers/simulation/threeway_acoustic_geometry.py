#!/usr/bin/env python3
"""Strict early three-way acoustic-integration geometry and LR4 math.

This is an IDEALIZED COMPLEX-FREQUENCY RESPONSE mathematical demonstration,
NOT measured loudspeaker output. It deliberately refuses to sum driver
responses lacking phase.
"""
from __future__ import annotations

import cmath
import json
import math
from dataclasses import dataclass
from pathlib import Path


def lr4_pair(f_hz: float, fc_hz: float) -> tuple[complex, complex]:
    """Matched 4th-order Linkwitz-Riley electrical HP and LP, ideal stages."""
    if f_hz <= 0 or fc_hz <= 0:
        raise ValueError("positive frequencies required")
    x = f_hz / fc_hz
    d = complex(1 - x*x, math.sqrt(2)*x)
    low = (1/d)**2
    high = (complex(-x*x, 0)/d)**2
    return low, high


def db20(amplitude: float) -> float:
    if amplitude <= 0:
        raise ValueError("amplitude must be positive")
    return 20*math.log10(amplitude)


def delayed_pair_sum_db(fc_hz: float, relative_delay_us: float) -> float:
    """At the electrical crossover only: difference in acoustical delay."""
    if relative_delay_us < 0:
        raise ValueError("delay nonnegative")
    lo, hi = lr4_pair(fc_hz, fc_hz)
    phase = cmath.exp(-2j*math.pi*fc_hz*relative_delay_us/1e6)
    return db20(abs(lo + hi*phase))


def propagation_distance_m(
    listener_distance_m: float,
    listener_height_m: float,
    driver_height_m: float,
) -> float:
    if listener_distance_m <= 0:
        raise ValueError("listener distance must be positive")
    return math.hypot(listener_distance_m, listener_height_m-driver_height_m)


def pair_path_difference_us(
    separation_m: float, listening_distance_m: float, head_height_offset_m: float,
    sound_speed_m_s: float=343.
) -> float:
    if separation_m <= 0 or sound_speed_m_s <= 0:
        raise ValueError("invalid geometry")
    d_low = propagation_distance_m(listening_distance_m,head_height_offset_m,-separation_m/2)
    d_high = propagation_distance_m(listening_distance_m,head_height_offset_m,separation_m/2)
    return abs(d_low-d_high)/sound_speed_m_s*1e6


@dataclass(frozen=True)
class ResponsePoint:
    frequency_hz: float
    magnitude_db: float
    phase_deg: float


def parse_phase_frd(text: str) -> list[ResponsePoint]:
    """Simple frequency[Hz] magnitude[dB] phase[deg] FRD, with #/; comments.

    REQUIRES phase, no guarantee that vendor phases share reference plane,
    acoustic origin, time window or enclosure. Do not assert measured
    crossovers from this parser alone.
    """
    out=[]
    for lineno, raw in enumerate(text.splitlines(),1):
        line=raw.strip()
        if not line or line.startswith(("#",";","*")):
            continue
        parts=line.replace(","," ").split()
        if len(parts)!=3:
            raise ValueError(f"line {lineno}: three columns F Hz / magnitude dB / phase degrees required")
        try:
            f,mag,phase=map(float,parts)
        except ValueError as exc:
            raise ValueError(f"line {lineno}: nonnumeric FRD") from exc
        if not all(math.isfinite(v) for v in (f,mag,phase)) or f <= 0:
            raise ValueError(f"line {lineno}: invalid FRD values")
        if out and f <= out[-1].frequency_hz:
            raise ValueError(f"line {lineno}: FRD frequencies must increase")
        out.append(ResponsePoint(f,mag,phase))
    if len(out)<2:
        raise ValueError("need at least two phase-bearing FRD samples")
    return out


def complex_from_point(point: ResponsePoint) -> complex:
    return 10**(point.magnitude_db/20) * cmath.exp(1j*math.radians(point.phase_deg))


def projected_mid_high_geometry() -> dict:
    fc=2500.
    separation=0.115 # illustrative, NOT a driver dimension
    rows=[]
    for distance in (.6,.7,.8):
        for head in (0,.10,.15):
            path_us=pair_path_difference_us(separation,distance,head)
            rows.append({
              "distance_m":distance,
              "head_vertical_offset_m":head,
              "path_delay_difference_us":round(path_us,3),
              "ideal_lr4_loss_if_no_geometric_compensation_db":
                  round(delayed_pair_sum_db(fc,path_us),3),
            })
    return {
      "scope":"geometry + ideal LR4 only; not actual Wavecor crossover/acoustic prediction",
      "candidate_driver_pair":"Wavecor MR120BD02 / TW030WA22",
      "mid_high_fc_hz":fc,
      "illustrative_driver_center_spacing_m":separation,
      "assumed_speed_of_sound_m_s":343,
      "head_movement_window":rows,
      "separate_digital_delay_examples_us":[0,50,100],
      "same_pair_crossover_amplitude_db":[
         round(delayed_pair_sum_db(fc,v),3) for v in (0,50,100)
      ],
      "manufacturer_source_urls":[
        "https://www.wavecor.com/html/mr120bd01_02_03_04.html",
        "https://www.wavecor.com/html/tw030wa21_22.html",
        "https://www.wavecor.com/html/wf168wa05_06.html"
      ],
      "measured_driver_phase_imported":False,
      "baffle_and_reflection_modeled":False,
      "derived_production_crossover":False,
      "notes":[
        "Real total group delay includes separate DAC, amplifier, DSP and acoustic centers",
        "Equalization of one listening point does not guarantee broad vertical window",
        "Real FRD magnitude without phase cannot be coherently summed",
        "Manufacturer infinite-baffle data are not final enclosure measurements",
      ],
    }


if __name__=="__main__":
    print(json.dumps(projected_mid_high_geometry(),indent=2,sort_keys=True))
