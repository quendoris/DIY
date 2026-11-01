#!/usr/bin/env python3
"""D2-WAVE-01: first-order piston, finite-rectangle edge paths and desk study.

Evidence strictly separated:
  * PISTON: canonical far-field, rigid circular piston in INFINITE baffle.
    NOT a manufacturer's angular measurement, real cone breakup or lobing.
  * EDGE: purely geometric path-lag catalogue from speaker to FOUR baffle edges
    and thence to the listener. NOT a diffraction transfer-function or SPL.
  * DESK: specular infinite rigid plane image-source pressure approximation.
    NOT finite furniture geometry or actual measured room response.
  * ARRAY: ideal 3-way LR4 phase-bridged point-source with optional piston
    direction factors. Calibration at ONE reference cannot correct full field.

No production cabinet, crossover, DSP, IMD, THD, SPL or certification is approved.
"""
from __future__ import annotations

import cmath
import json
import math
from dataclasses import asdict

from threeway_baffle_geometry import (
    DRIVERS, ORDER, REF_EAR_M, TEST_DISTANCES_M, TEST_FREQUENCIES_HZ,
    HEAD_Y_M, HEAD_X_M, SPEED_SOUND_M_S,
    default_layouts, distance_to_source_m, ideal_filters, panel_dimensions,
    validate_layout,
)

# Manufacturer Sd quoted for these TWO physical cone drivers (not frame area).
# Effective dome piston size is only its nominal 30mm diameter, NOT a factory Sd.
PISTON={
    "LOW": {"effective_sd_cm2":131.0, "basis":"manufacturer Sd, uniform-rigid-piston hypothesis"},
    "MID": {"effective_sd_cm2":50.0, "basis":"manufacturer Sd, uniform-rigid-piston hypothesis"},
    "HIGH":{"effective_diameter_mm":30.0,"basis":"nominal 30mm dome, effective piston aperture unmeasured"},
}
HEAD_HEIGHT_ABOVE_DESK_M=0.35  # hypothetical, not user measured
DESK_REFLECTION_COEFFICIENTS=(0.0,0.3,0.6) # positive pressure coefficients, hypothetically constant


def jinc2(x: float) -> float:
    """Stable-enough power series 2*J1(x)/x over x in [0,15].

    sum(-1)^m * (x*x/4)^m / (m!*(m+1)!)
    Use no external dependencies. Guard high-frequency extrapolation.
    """
    if not math.isfinite(x) or x < 0 or x > 15:
        raise ValueError("outside validated series interval [0,15]")
    if x == 0:
        return 1.
    t=1.
    total=1.
    for m in range(1,80):
        t*= -(x*x/4)/(m*(m+1))
        total+=t
        if abs(t) < 1e-15:
            break
    return total


def piston_radius_m(name: str) -> float:
    if name not in PISTON:
        raise ValueError("unknown driver")
    p=PISTON[name]
    if "effective_sd_cm2" in p:
        return math.sqrt(p["effective_sd_cm2"]*1e-4/math.pi)
    return p["effective_diameter_mm"]/2000


def piston_directivity(name: str, f_hz: float, angle_deg: float) -> float:
    if not 0<=angle_deg<=90 or f_hz<=0:
        raise ValueError("invalid angle or frequency")
    x=2*math.pi*f_hz/SPEED_SOUND_M_S*piston_radius_m(name)*math.sin(math.radians(angle_deg))
    return jinc2(x)


def source_angle_deg(ear,driver_xy_mm) -> float:
    ex,ey,ez=ear
    if ez<=0:
        raise ValueError("positive source-to-listener axial distance required")
    sx,sy=driver_xy_mm
    transverse=math.hypot(ex-sx*.001,ey-sy*.001)
    return math.degrees(math.atan2(transverse,ez))


def pressure(layout, f_hz, ear, piston=True) -> complex:
    """Amplitude/phase calibrate each ideal path at one 70cm center reference.

    Piston option includes a far-field on-axis normalized ideal circular piston
    factor, not actual finite baffle angular directivity.
    """
    if f_hz<=0:
        raise ValueError("positive frequency")
    transfer=ideal_filters(f_hz)
    out=0j
    for name in ORDER:
        loc=layout.positions_mm[name]
        d=distance_to_source_m(ear,loc)
        d0=distance_to_source_m(REF_EAR_M,loc)
        if piston:
            direct=piston_directivity(name,f_hz,source_angle_deg(ear,loc))
            reference=piston_directivity(name,f_hz,source_angle_deg(REF_EAR_M,loc))
            if abs(reference)<.05:
                raise ValueError("calibration near angular null, invalid ideal piston assumption")
            shape=direct/reference
        else:
            shape=1.
        out+=transfer[name]*(d0/d)*shape*cmath.exp(
            -2j*math.pi*f_hz*(d-d0)/SPEED_SOUND_M_S)
    return out


def relative_window_db(layout, f_hz, ear, piston=True) -> float:
    ex,ey,ez=ear
    a=abs(pressure(layout,f_hz,ear,piston))
    b=abs(pressure(layout,f_hz,(0.,0.,ez),piston))
    if min(a,b)<=1e-12:
        raise ValueError("near cancellation null invalid for logarithmic score")
    return 20*math.log10(a/b)


def window_score(layout,piston=True):
    errs=[]
    worst=None
    for z in TEST_DISTANCES_M:
        for y in HEAD_Y_M:
            for x in HEAD_X_M:
                for f in TEST_FREQUENCIES_HZ:
                    d=relative_window_db(layout,f,(x,y,z),piston)
                    err=abs(d)
                    errs.append(err)
                    if worst is None or err>worst["abs_delta_db"]:
                        worst={"abs_delta_db":round(err,4),"signed_delta_db":round(d,4),
                               "x_m":x,"y_m":y,"z_m":z,"frequency_hz":f}
    errs.sort()
    return {"n_points":len(errs),"p95_abs_db":round(errs[math.ceil(.95*len(errs))-1],4),
            "rms_abs_db":round(math.sqrt(sum(t*t for t in errs)/len(errs)),4),
            "worst":worst,
            "source_model":"IDEAL_FARFIELD_CIRCULAR_PISTON" if piston else "IDEAL_MONOPOLE"}


def edge_path_proxies(layout, ref_listener=REF_EAR_M):
    """Distances via nearest cardinal edge locations; NOT edge diffraction response."""
    panel=panel_dimensions(layout)
    W,H=panel["required_flat_panel_width_mm"],panel["required_flat_panel_height_mm"]
    ear_axis=panel["nominal_ear_projection_from_lower_left_mm"]
    ex,ey,ez=ref_listener
    listener=(ex*1000+ear_axis[0],ey*1000+ear_axis[1],ez*1000)
    out={}
    for name,source in panel["center_xy_from_lower_left_mm"].items():
        x,y=source
        edges={
          "left":(0.,y),"right":(W,y),
          "bottom":(x,0.),"top":(x,H)
        }
        direct=math.sqrt((listener[0]-x)**2+(listener[1]-y)**2+listener[2]**2)
        rows=[]
        for edge,(a,b) in edges.items():
            ds=math.hypot(x-a,y-b)
            de=math.sqrt((listener[0]-a)**2+(listener[1]-b)**2+listener[2]**2)
            delta=(ds+de-direct)/1000.
            if delta < -1e-9:
                raise ValueError("edge path shorter than straight path, error")
            rows.append({"edge":edge,"speaker_to_nearest_edge_mm":round(ds,3),
                         "extra_via_edge_path_mm":round(delta*1000,3),
                         "extra_via_edge_delay_us":round(delta/SPEED_SOUND_M_S*1e6,3),
                         "geometric_half_cycle_hz_if_scattering_existed":
                             round(SPEED_SOUND_M_S/(2*delta),1) if delta>1e-9 else None})
        out[name]=rows
    return out


def placement_for_ear_height(layout,ear_height_m=HEAD_HEIGHT_ABOVE_DESK_M):
    """Ideal vertical positioning if reference MID/HF ear projection is kept at ear height."""
    if ear_height_m<=0:
        raise ValueError("ear must be above the assumed tabletop")
    p=panel_dimensions(layout)
    ear_project_y=p["nominal_ear_projection_from_lower_left_mm"][1]/1000.
    base_height=ear_height_m-ear_project_y
    return {
      "assumed_ear_height_above_table_mm":round(ear_height_m*1000,3),
      "panel_bottom_height_above_table_mm":round(base_height*1000,3),
      "panel_bottom_is_above_table":base_height>=0.,
      "driver_acoustic_center_heights_above_table_mm":{
        name:round(base_height*1000+coord[1],3)
        for name,coord in p["center_xy_from_lower_left_mm"].items()},
      "reference_ear_projection_y_mm":p["nominal_ear_projection_from_lower_left_mm"][1]
    }


def desk_reflection_geometry(source_height_m:float,ear_height_m:float,depth_m:float):
    if min(source_height_m,ear_height_m,depth_m)<=0:
        raise ValueError("plane must be below speaker, listener and depth must be positive")
    direct=math.hypot(depth_m,ear_height_m-source_height_m)
    reflected=math.hypot(depth_m,ear_height_m+source_height_m)
    delay=reflected-direct
    # Specular reflection point horizontal distance from speaker.
    reflection_x=depth_m*source_height_m/(source_height_m+ear_height_m)
    return {
      "direct_path_m":direct,"image_reflected_path_m":reflected,
      "extra_path_m":delay,"extra_delay_us":delay/SPEED_SOUND_M_S*1e6,
      "reflection_point_from_speaker_m":reflection_x,
      "first_halfcycle_interference_hz":SPEED_SOUND_M_S/(2*delay),
    }


def desk_comb_db(f_hz:float, source_height_m:float, ear_height_m:float,
                 depth_m:float, reflection_coefficient:float) -> float:
    if f_hz<=0 or not 0<=reflection_coefficient<=1:
        raise ValueError("invalid f / hypothetical pressure reflection coefficient")
    g=desk_reflection_geometry(source_height_m,ear_height_m,depth_m)
    r0,r1=g["direct_path_m"],g["image_reflected_path_m"]
    complex_ratio=1+reflection_coefficient*(r0/r1)*cmath.exp(
        -2j*math.pi*f_hz*g["extra_path_m"]/SPEED_SOUND_M_S)
    return 20*math.log10(abs(complex_ratio))


def report() -> dict:
    out=[]
    for l in default_layouts():
        try:
            validate_layout(l)
            fixture=panel_dimensions(l)
        except ValueError:
            continue
        placement=placement_for_ear_height(l)
        desk={}
        if placement["panel_bottom_is_above_table"]:
            for k,height in placement["driver_acoustic_center_heights_above_table_mm"].items():
                geom=desk_reflection_geometry(height*.001,HEAD_HEIGHT_ABOVE_DESK_M,.7)
                desk[k]={
                  "extra_path_mm":round(1000*geom["extra_path_m"],2),
                  "reflection_point_from_speaker_mm":
                      round(1000*geom["reflection_point_from_speaker_m"],2),
                  "first_halfcycle_hz":round(geom["first_halfcycle_interference_hz"],1),
                  "conditional_levels_db_at_450_2500hz":{
                    str(reflection):{
                        str(f):round(desk_comb_db(f,height*.001,HEAD_HEIGHT_ABOVE_DESK_M,
                                                    .7,reflection),3)
                        for f in (450,2500)}
                    for reflection in DESK_REFLECTION_COEFFICIENTS
                  },
                }
        out.append({
            "layout":l.name,
            "panel_mm":[fixture["required_flat_panel_width_mm"],
                        fixture["required_flat_panel_height_mm"]],
            "nominal_ear_height_table_setup":placement,
            "monopole_head_window":window_score(l,False),
            "ideal_piston_head_window":window_score(l,True),
            "edge_path_geometry_no_diffraction_transfer":edge_path_proxies(l),
            "ideal_infinite_table_image_source_examples":desk,
        })
    directivity={}
    for k in ORDER:
        points={"0":0.}
        passbands={"LOW":(450,600),"MID":(1000,2500,3500),
                   "HIGH":(2500,5000,10000)}[k]
        for f in passbands:
            for a in (15,30,45,60):
                factor=abs(piston_directivity(k,f,a))
                points[f"{f}Hz_{a}deg"]=round(20*math.log10(max(factor,1e-12)),3)
        directivity[k]={
            "assumed_piston_radius_mm":round(1000*piston_radius_m(k),3),
            "data_basis":PISTON[k]["basis"],
            "ideal_infinite_baffle_farfield_directivity_db":points,
        }
    return {
      "study":"D2-WAVE-01",
      "actual_speaker_measurements":False,
      "wave_eq_finite_baffle_diffraction_solved":False,
      "desk_reflection_measured":False,
      "manufacturer_angular_response_measured":False,
      "piston_model_does_not_use_manufacturer_angular_data":True,
      "sound_speed_m_s":SPEED_SOUND_M_S,
      "assumed_ear_height_above_desk_m":HEAD_HEIGHT_ABOVE_DESK_M,
      "assumed_nominal_acoustic_split_hz":[450,2500],
      "ideal_farfield_piston_examples":directivity,
      "layout_hypotheses":out,
      "units_and_limits":[
          "Piston jinc: 2*J1(x)/x, x=(2pi f/c) a sin(theta); infinite rigid baffle FARFIELD only.",
          "Model uses manufacturer Sd LOW/MID and approximate 30mm HF aperture; not measured directivity.",
          "A full multi-driver nearfield array is NOT equivalent to farfield independent pistons.",
          "Edge extra paths are geometrical candidates only, NOT diffraction amplitude or a real baffle step.",
          "Desktop model uses infinite, perfectly planar tabletop and frequency-independent nonnegative pressure reflection.",
          "Specular point may not lie on a real finite desk; speaker/monitor blocking and material absorption omitted.",
          "Head/desk heights and source offsets are hypothetical; user dimensions not supplied.",
          "Ear-axis and per-driver timing calibrated at one reference, not at every head position.",
          "Real manufacturer wavecor on-axis FRD only (previous D2-REAL-01), no source-aligned 3D angular FRD.",
          "No objective system-layout winner is physically justified by this study."
      ]
    }

if __name__=="__main__":
    print(json.dumps(report(),ensure_ascii=False,indent=2))
