#!/usr/bin/env python3
"""D2-GEO-01: dimension-constrained three-way test baffle geometry.

Grounded in original Wavecor factory PDF outline drawings, NOT a final
enclosure/CAD tool or measured acoustic-directivity solution.

The acoustic toy model assumes three ideal omnidirectional monopoles with
flat, equal response, individually distance/phase-calibrated to one
reference listening point, correct LR4 phase bridging, 1/r propagation
and frequency-dependent acoustic propagation phase. It omits real driver
polar responses, finite-baffle diffraction, cone breakup, acoustic-center
offsets, enclosure/loading, room reflections, microphone/clock/DSP/amp
phase, excursion, THD and actual SPL. Score is ONLY geometry sensitivity
within this explicit model and cannot approve a component or final shell.
"""
from __future__ import annotations

import cmath
import json
import math
from dataclasses import asdict, dataclass

from threeway_acoustic_geometry import lr4_pair

SPEED_SOUND_M_S = 343.0
REF_EAR_M = (0.0, 0.0, 0.7)
CROSSOVER_LOW_MID_HZ = 450.0
CROSSOVER_MID_HIGH_HZ = 2500.0

@dataclass(frozen=True)
class Driver:
    name: str
    outer_diameter_mm: float
    rear_max_diameter_mm: float
    mounting_circle_diameter_mm: float
    nominal_mounting_depth_mm: float
    drawing: str
    note: str = ""

DRIVERS = {
    "LOW": Driver(
        "Wavecor WF168WA06-01", 168, 143, 159, 73,
        "https://www.wavecor.com/Driver%20specifications%20PDF/WF168WA05_06_specifications.pdf",
        "rear max Ø143 is not yet a machining cutout tolerance"),
    "MID": Driver(
        "Wavecor MR120BD02-01", 120, 98, 110, 64,
        "https://www.wavecor.com/Driver%20specifications%20PDF/MR120BD01_02_03_04_specifications.pdf",
        "dedicated separate airtight MID chamber, initial comparison fixture 2 L NET"),
    "HIGH": Driver(
        "Wavecor TW030WA22-01", 104, 80, 92, 30,
        "https://www.wavecor.com/Driver%20specifications%20PDF/TW030WA21_22_specifications.pdf",
        "Ø80 is largest housing behind flange; depth 30 mm max"),
}

ORDER = ("LOW", "MID", "HIGH")

@dataclass(frozen=True)
class Layout:
    name: str
    # Positions in millimeters, x=0 at mid/low vertical axis,
    # y=0 halfway between MID and HIGH (desired ear-height reference).
    positions_mm: dict[str, tuple[float, float]]
    description: str

def vertical_layout(name: str, gap_lm_mm: float, gap_mh_mm: float,
                    hf_x_mm: float = 0) -> Layout:
    d_lm = (DRIVERS["LOW"].outer_diameter_mm +
            DRIVERS["MID"].outer_diameter_mm) / 2 + gap_lm_mm
    total_mh = (DRIVERS["MID"].outer_diameter_mm +
                DRIVERS["HIGH"].outer_diameter_mm) / 2 + gap_mh_mm
    if abs(hf_x_mm) >= total_mh:
        raise ValueError("tweeter horizontal offset exceeds available M/H distance")
    vertical_mh = math.sqrt(total_mh**2 - hf_x_mm**2)
    p = {
        "LOW": (0.0, -d_lm-vertical_mh/2),
        "MID": (0.0, -vertical_mh/2),
        "HIGH": (hf_x_mm, vertical_mh/2),
    }
    return Layout(name,p,
      f"LOW-MID rim gap {gap_lm_mm:g}mm, MID-HIGH rim gap {gap_mh_mm:g}mm, HF x offset {hf_x_mm:g}mm")

def clearance_mm(layout: Layout, a: str, b: str) -> float:
    ax,ay=layout.positions_mm[a]
    bx,by=layout.positions_mm[b]
    return math.hypot(ax-bx,ay-by) - (
        DRIVERS[a].outer_diameter_mm+DRIVERS[b].outer_diameter_mm)/2

def validate_layout(layout: Layout, min_rim_gap_mm: float = 5.0) -> None:
    if set(layout.positions_mm) != set(ORDER):
        raise ValueError("exactly LOW MID HIGH required")
    if min_rim_gap_mm < 0:
        raise ValueError("invalid gap limit")
    for i,a in enumerate(ORDER):
        for b in ORDER[i+1:]:
            if clearance_mm(layout,a,b) < min_rim_gap_mm-1e-7:
                raise ValueError(f"{layout.name}: {a}/{b} flanges overlap or clearance insufficient")

def panel_dimensions(layout: Layout, edge_margin_mm: float=18.0,
                     grid_mm: float=5.0) -> dict:
    if edge_margin_mm < 0 or grid_mm <= 0:
        raise ValueError("invalid fixture panel parameters")
    validate_layout(layout)
    lo_x=min(layout.positions_mm[k][0] - DRIVERS[k].outer_diameter_mm/2 for k in ORDER)
    hi_x=max(layout.positions_mm[k][0] + DRIVERS[k].outer_diameter_mm/2 for k in ORDER)
    lo_y=min(layout.positions_mm[k][1] - DRIVERS[k].outer_diameter_mm/2 for k in ORDER)
    hi_y=max(layout.positions_mm[k][1] + DRIVERS[k].outer_diameter_mm/2 for k in ORDER)
    width=grid_mm*math.ceil((hi_x-lo_x+2*edge_margin_mm)/grid_mm)
    height=grid_mm*math.ceil((hi_y-lo_y+2*edge_margin_mm)/grid_mm)
    shift_x=(width-(hi_x-lo_x))/2-lo_x
    shift_y=(height-(hi_y-lo_y))/2-lo_y
    center_positions={k:[round(x+shift_x,3),round(y+shift_y,3)]
                      for k,(x,y) in layout.positions_mm.items()}
    ear_reference_mm=[round(shift_x,3),round(shift_y,3)]
    return {
       "required_flat_panel_width_mm":round(width,3),
       "required_flat_panel_height_mm":round(height,3),
       "nominal_edge_clearance_mm":edge_margin_mm,
       "center_xy_from_lower_left_mm":center_positions,
       "nominal_ear_projection_from_lower_left_mm":ear_reference_mm,
       "min_frame_clearance_mm":round(
           min(clearance_mm(layout,a,b) for i,a in enumerate(ORDER)
               for b in ORDER[i+1:]),3),
       "drawing_is_tooling_only":True,
       "cutouts_and_screw_template_production_ready":False,
    }

def distance_to_source_m(ear_xyz_m: tuple[float,float,float],
                         driver_xy_mm: tuple[float,float]) -> float:
    ex,ey,ez=ear_xyz_m
    if ez <= 0:
        raise ValueError("listening distance must be positive")
    sx,sy=driver_xy_mm
    return math.sqrt((ex-sx*.001)**2+(ey-sy*.001)**2+ez**2)

def ideal_filters(f: float, fc1: float = CROSSOVER_LOW_MID_HZ,
                  fc2: float = CROSSOVER_MID_HIGH_HZ) -> dict[str,complex]:
    lo,hi=lr4_pair(f,fc1)
    lo2,hi2=lr4_pair(f,fc2)
    return {
       "LOW":lo*(lo2+hi2),
       "MID":hi*lo2,
       "HIGH":hi*hi2
    }

def hypothetical_complex_pressure(layout: Layout, f_hz: float,
         ear_xyz_m: tuple[float,float,float],
         reference_ear_m: tuple[float,float,float]=REF_EAR_M) -> complex:
    # Trims and per-driver propagation delay exactly align ALL paths at
    # one calibrated reference ear location (idealized best-case).
    # Once ear moves, calibration stays fixed.
    if f_hz <= 0:
        raise ValueError("frequency must be positive")
    filtered=ideal_filters(f_hz)
    amplitude=0j
    for k in ORDER:
        r=distance_to_source_m(ear_xyz_m,layout.positions_mm[k])
        r0=distance_to_source_m(reference_ear_m,layout.positions_mm[k])
        delta=r-r0
        amplitude += filtered[k]*(r0/r)*cmath.exp(
            -2j*math.pi*f_hz*delta/SPEED_SOUND_M_S)
    return amplitude

def relative_db(layout: Layout, f_hz: float,
                ear_xyz_m: tuple[float,float,float]) -> float:
    # Compare head motion at a chosen distance to staying centered at
    # that SAME distance, excluding ordinary inverse-distance gain.
    _,_,distance=ear_xyz_m
    p=hypothetical_complex_pressure(layout,f_hz,ear_xyz_m)
    p_center=hypothetical_complex_pressure(layout,f_hz,(0.,0.,distance))
    if abs(p) < 1e-12 or abs(p_center) < 1e-12:
        raise ValueError("pressure node too close to zero for stable dB comparison")
    return 20*math.log10(abs(p)/abs(p_center))

TEST_FREQUENCIES_HZ=(300,400,450,600,1000,1700,2000,2250,2500,2750,3000,3500,4000)
TEST_DISTANCES_M=(.6,.7,.8)
HEAD_Y_M=(-.1,-.05,0,.05,.1)
HEAD_X_M=(-.08,0,.08)

def layout_score(layout: Layout) -> dict:
    validate_layout(layout)
    values=[]
    worst=None
    for z in TEST_DISTANCES_M:
        for y in HEAD_Y_M:
            for x in HEAD_X_M:
                for f in TEST_FREQUENCIES_HZ:
                    delta=relative_db(layout,f,(x,y,z))
                    a=abs(delta)
                    values.append(a)
                    if worst is None or a>worst["abs_delta_db"]:
                        worst={
                          "abs_delta_db":round(a,4),
                          "signed_delta_db":round(delta,4),
                          "head_xy_m":[x,y],"distance_m":z,
                          "frequency_hz":f
                        }
    values.sort()
    return {
      "worst_case":worst,
      "percentile_95_abs_db":round(values[math.ceil(.95*len(values))-1],4),
      "rms_abs_db":round(math.sqrt(sum(v*v for v in values)/len(values)),4),
      "frequency_samples":len(TEST_FREQUENCIES_HZ),
      "grid_positions":len(TEST_DISTANCES_M)*len(HEAD_Y_M)*len(HEAD_X_M),
      "total_checked_points":len(values),
      "mid_high_2500hz_ear_up_10cm_70cm_db":
        round(relative_db(layout,2500,(0.,.1,.7)),4),
    }

def default_layouts() -> list[Layout]:
    return [
      vertical_layout("A_minimum_practical_vertical",5,5,0),
      vertical_layout("B_ventilation_gaps_vertical",15,20,0),
      vertical_layout("C_offset_HF_40mm",5,5,40),
      vertical_layout("D_compact_but_too_tight",2,2,0),
      vertical_layout("E_wide_gaps_vertical",35,40,0),
    ]

def report() -> dict:
    layouts=[]
    for l in default_layouts():
        try:
            panel=panel_dimensions(l)
            score=layout_score(l)
            layouts.append({"id":l.name,"description":l.description,
                            "positions_mm_relative_to_mid_hf_midpoint":l.positions_mm,
                            "tooling_panel":panel,"ideal_model_head_window":score,
                            "physical_rim_clearance_pass":True})
        except ValueError as e:
            layouts.append({"id":l.name,"description":l.description,
                            "physical_rim_clearance_pass":False,
                            "reason":str(e)})
    valid=sorted((r for r in layouts if r["physical_rim_clearance_pass"]),
                 key=lambda v:(v["ideal_model_head_window"]["worst_case"]["abs_delta_db"],
                               v["ideal_model_head_window"]["rms_abs_db"]))
    return {
      "study":"D2-GEO-01",
      "measured_acoustic_head_window":False,
      "model":"ideal point-source/flat-response LR4 with LF upper-split allpass, calibrated at one 0.7m reference; 1/r and geometric phase only",
      "angular_directivity_measured_or_modeled":False,
      "baffle_diffraction_measured_or_modeled":False,
      "common_manufacturer_phase_time_zero_proven":False,
      "real_speaker_crossover_qualified":False,
      "driver_nominal_dimensions":{k:asdict(v) for k,v in DRIVERS.items()},
      "reference_listener_m":list(REF_EAR_M),
      "crossover_trial_hz":{"low_mid":CROSSOVER_LOW_MID_HZ,
                            "mid_high":CROSSOVER_MID_HIGH_HZ},
      "window":{"distances_m":TEST_DISTANCES_M,
                "head_vertical_m":HEAD_Y_M,"head_horizontal_m":HEAD_X_M,
                "sample_frequencies_hz":TEST_FREQUENCIES_HZ},
      "layouts":layouts,
      "conditionally_most_robust_layout_id":valid[0]["id"],
      "physical_build_decision":"removable test baffle only; no finalized enclosure",
      "warnings":[
        "Ranking is conditional on ideal omnidirectional point drivers, NOT actual Wavecor measured off-axis.",
        "No final cabinet shape, front panel diffraction/step, recessed mounting or acoustical volumes solved.",
        "Nominal factory outer flange bounds, not verified cutout toolpaths or screw clearance.",
        "The MID 2L chamber is an isolated TEST volume; driver displacement and bracing must be subtracted.",
        "Fixed reference per-driver phase calibration is not reproduced by independent actual DACs until measured.",
        "Real room, desk reflections and vertical listening window may reverse any conditional ranking.",
        "Changing tweeter, waveguide or manufacturer requires a new dimensional/acoustic audit."
      ]
    }

if __name__=="__main__":
    print(json.dumps(report(),indent=2,ensure_ascii=False))
