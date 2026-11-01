#!/usr/bin/env python3
"""D2-WAVE-02 conditional three-way+desktop image-source superposition.

The source is the ideal per-driver piston/phase-bridged LR4 transfer, with
independent propagation, and a hypothetical single table reflection.
Specular image source is valid ONLY as infinite rigid-plane approximation,
with a crude finite-desk *ray existence* flag. No BEM, GTD, multiple
reflection, real off-axis FRD, finite-rectangle acoustic field or THD.
"""
from __future__ import annotations
import cmath
import json
import math

from threeway_baffle_geometry import (
    ORDER, REF_EAR_M, SPEED_SOUND_M_S, default_layouts,
    ideal_filters, panel_dimensions
)
from threeway_wave_desk_model import (
    HEAD_HEIGHT_ABOVE_DESK_M, piston_directivity,
    placement_for_ear_height
)


def integrated_pressure(layout,f_hz,ear_x_offset_m,ear_y_offset_m,
                        axial_distance_m,
                        reflection_coefficient=0.,
                        desk_forward_extent_from_speaker_m=None,
                        use_ideal_pistons=True):
    """Returns complex relative pressure with calibrated DIRECT reference.

    Per-band direct point/piston waves are coherent by assumption at reference
    ear position for the CHOSEN crossover. A separate image source is added
    with positive *pressure* coefficient Gamma for the same band.
    """
    if f_hz<=0 or axial_distance_m<=0 or not (0<=reflection_coefficient<=1):
        raise ValueError("invalid frequency, range or reflection")
    if desk_forward_extent_from_speaker_m is not None and desk_forward_extent_from_speaker_m<0:
        raise ValueError("desk depth must be nonnegative")
    ear_height=HEAD_HEIGHT_ABOVE_DESK_M+ear_y_offset_m
    if ear_height<=0:
        raise ValueError("ear must be above desk")
    panel=panel_dimensions(layout)
    placement=placement_for_ear_height(layout)
    if not placement["panel_bottom_is_above_table"]:
        raise ValueError("hypothetical cabinet intersects table at configured ear height")
    px,py=panel["nominal_ear_projection_from_lower_left_mm"]
    transfer=ideal_filters(f_hz)
    out=0j
    for name in ORDER:
        x_mm,y_mm=panel["center_xy_from_lower_left_mm"][name]
        sx_m=(x_mm-px)/1000
        src_height=(y_mm+placement["panel_bottom_height_above_table_mm"])/1000
        lateral=ear_x_offset_m-sx_m
        direct=math.sqrt(lateral*lateral+(ear_height-src_height)**2+axial_distance_m**2)
        direct0=math.sqrt(sx_m*sx_m+(HEAD_HEIGHT_ABOVE_DESK_M-src_height)**2+REF_EAR_M[2]**2)
        if use_ideal_pistons:
            angle=math.degrees(math.atan2(math.hypot(lateral,ear_height-src_height),
                                              axial_distance_m))
            angle0=math.degrees(math.atan2(
                math.hypot(sx_m,HEAD_HEIGHT_ABOVE_DESK_M-src_height),REF_EAR_M[2]))
            numerator=piston_directivity(name,f_hz,angle)
            denominator=piston_directivity(name,f_hz,angle0)
            if abs(denominator)<.05:
                raise ValueError("attempt to calibrate near directivity null")
            angular=numerator/denominator
        else:
            angular=1.
        direct_ratio=(direct0/direct)*angular*cmath.exp(
            -2j*math.pi*f_hz*(direct-direct0)/SPEED_SOUND_M_S)
        reflection=0j
        if reflection_coefficient:
            # crude finite-table existence rule: longitudinal specular point
            # must be between speaker and FRONT edge. Later ray tracing
            # must check physical desk width and finite panel boundaries.
            specular_x=axial_distance_m*src_height/(src_height+ear_height)
            reflected_allowed=(desk_forward_extent_from_speaker_m is None or
                               specular_x<=desk_forward_extent_from_speaker_m)
            if reflected_allowed:
                image_distance=math.sqrt(lateral*lateral+
                    (ear_height+src_height)**2+axial_distance_m**2)
                reflection=reflection_coefficient*direct/image_distance*cmath.exp(
                    -2j*math.pi*f_hz*(image_distance-direct)/SPEED_SOUND_M_S)
        out+=transfer[name]*direct_ratio*(1+reflection)
    return out


def reference_relative_db(layout,f_hz,reflection_coefficient,desk_extent=None,
                          ear_offset_xy=(0.,0.),distance_m=.7,
                          use_ideal_pistons=True):
    base=integrated_pressure(layout,f_hz,*ear_offset_xy,distance_m,0.,
                             None,use_ideal_pistons)
    altered=integrated_pressure(layout,f_hz,*ear_offset_xy,distance_m,
                             reflection_coefficient,desk_extent,use_ideal_pistons)
    if abs(base)<1e-12:
        raise ValueError("ill-defined zero direct pressure")
    return 20*math.log10(abs(altered)/abs(base))


def scenarios():
    layouts={x.name:x for x in default_layouts()}
    selected=("A_minimum_practical_vertical","F_side_LOW_left",
              "G_side_LOW_right")
    freq=(350,450,700,1000,2000,2500,3000,4000)
    rows=[]
    for name in selected:
        layout=layouts[name]
        tests=[]
        for coeff in (0.,.3,.6):
            for extent in (None,.2,.3,.45):
                tests.append({
                    "reflection_pressure_coefficient":coeff,
                    "forward_desk_length_from_speaker_m":extent,
                    "composite_level_change_from_direct_only_db":{
                        str(f):round(reference_relative_db(layout,f,coeff,extent),4)
                        for f in freq},
                    "composite_change_head_up_10cm_db":{
                        str(f):round(reference_relative_db(layout,f,coeff,extent,
                                          ear_offset_xy=(0.,.1)),4)
                        for f in (450,2500,3000)}
                })
        rows.append({
            "layout_id":name,
            "panel_bottom_above_desk_mm":
              placement_for_ear_height(layout)["panel_bottom_height_above_table_mm"],
            "assumed_ear_height_mm":HEAD_HEIGHT_ABOVE_DESK_M*1000,
            "scenarios":tests
        })
    return {
      "study":"D2-WAVE-02",
      "component_phase_time_zero_verified":False,
      "real_desktop_dimensions_known":False,
      "real_reflection_coefficient_known":False,
      "actual_output_Spl_measured":False,
      "combined_model_type":"single specular image source + ideal rigid piston with 3-way phase bridge",
      "calibration":"direct/free-field path of each driver set in phase at 0.7m reference; reflected pressure is NOT individually calibrated",
      "reflection_coefficients":[0,.3,.6],
      "reference_ear_height_m":HEAD_HEIGHT_ABOVE_DESK_M,
      "reference_distance_m":.7,
      "desk_forward_extents_m":[None,.2,.3,.45],
      "assumptions":[
        "A source behind a finite panel is NOT the same as a monopole plus one ideal desk reflection.",
        "A specular reflection point within a finite table is necessary but not sufficient for a real reflected ray.",
        "The table's width/absorption/edge diffraction/monitor obstructions and real reflection phase are unknown.",
        "Rigidbody piston farfield directivity differs from actual Wavecor angular FRDs.",
        "Individual source phases/delays assumed calibrated at one reference, NOT hardware validated.",
        "Results are illustrative change relative to a coherent direct-only model, NOT full system SPL or acoustic quality."
      ],
      "results":rows,
    }


if __name__=="__main__":
    print(json.dumps(scenarios(),ensure_ascii=False,indent=2))
