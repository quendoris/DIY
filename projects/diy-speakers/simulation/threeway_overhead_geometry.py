#!/usr/bin/env python3
"""D2-OVERHEAD-01: three-dimensional elevated, down-aimed 3-way placement.

This intentionally separates:
  * geometric line-of-sight to a HYPOTHETICAL rectangular monitor,
  * body roll (0, +/-45, 90 deg) around a down-aimed acoustic normal,
  * physically different 'stand bottom height' vs 'acoustic axis height',
  * ideal monopole/piston array head-window and a single tabletop image ray.
It is NOT measured Wavecor polar/diffraction, room/monitor scattering,
finite mechanical mounting/safety, stereo binaural spatial imaging, nor
an acoustic recommendation. Geometry uses exact factory driver FLANGES,
but ideal source positions at baffle-plane centers, not measured z-centers.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import cmath
import json
import math
from threeway_baffle_geometry import (
    ORDER, SPEED_SOUND_M_S, default_layouts, panel_dimensions, ideal_filters, DRIVERS
)
from threeway_wave_desk_model import piston_directivity

CENTER_TO_LISTENER_Z_M = .7
FREQS_HZ=(350,450,700,1000,1800,2200,2500,2800,3200,4000)
DISTANCES_M=(.6,.7,.8)
HEAD_X_M=(-.08,0,.08)
HEAD_Y_M=(-.10,-.05,0,.05,.10)

@dataclass(frozen=True)
class Setup:
    name:str
    layout_id:str
    roll_deg:float
    center_height_m:float
    ear_height_m:float
    z_separation_m:float=.7

@dataclass(frozen=True)
class Screen:
    plane_z_m:float
    top_height_m:float
    halfwidth_m:float
    bottom_height_m:float=0.
    center_x_m:float=0.

def tilt_deg(setup:Setup)->float:
    if not (setup.ear_height_m>0 and setup.center_height_m>0 and setup.z_separation_m>0):
        raise ValueError("heights and axial distance positive")
    return math.degrees(math.atan2(
        setup.center_height_m-setup.ear_height_m,setup.z_separation_m))

def unit_vectors(setup:Setup):
    # source-to-listener unit n is normal, pitch chosen automatically.
    tilt=math.radians(tilt_deg(setup))
    # x-pivot axial roll rotates planar driver offsets in the baffle plane.
    roll=math.radians(setup.roll_deg)
    unrolled_u=(1.,0.,0.)
    unrolled_v=(0.,math.cos(tilt),-math.sin(tilt))
    u=tuple(math.cos(roll)*a+math.sin(roll)*b
            for a,b in zip(unrolled_u,unrolled_v))
    v=tuple(-math.sin(roll)*a+math.cos(roll)*b
            for a,b in zip(unrolled_u,unrolled_v))
    normal=(0.,-math.sin(tilt),-math.cos(tilt))
    return u,v,normal

def sources(setup:Setup, layouts=None):
    layouts=layouts or {l.name:l for l in default_layouts()}
    if setup.layout_id not in layouts:
        raise ValueError("unknown layout")
    layout=layouts[setup.layout_id]
    u,v,_=unit_vectors(setup)
    out={}
    for name,(xmm,ymm) in layout.positions_mm.items():
        x,y=xmm*.001,ymm*.001
        out[name]=tuple(start+x*uu+y*vv
            for start,uu,vv in zip(
                (0.,setup.center_height_m,setup.z_separation_m),u,v))
    return out

def distance(a,b):
    return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))

def projected_baffle_extents(setup:Setup):
    # Source and flange circle swept under rotation around body center.
    s=sources(setup)
    ymin=min(p[1]-DRIVERS[k].outer_diameter_mm/2000 for k,p in s.items())
    ymax=max(p[1]+DRIVERS[k].outer_diameter_mm/2000 for k,p in s.items())
    xmin=min(p[0]-DRIVERS[k].outer_diameter_mm/2000 for k,p in s.items())
    xmax=max(p[0]+DRIVERS[k].outer_diameter_mm/2000 for k,p in s.items())
    # Envelope of driver's flange spheres is conservative for center's
    # vertical projection and may overstate actual elliptical projection.
    return {"minimum_flange_y_m":ymin,"maximum_flange_y_m":ymax,
            "minimum_flange_x_m":xmin,"maximum_flange_x_m":xmax,
            "has_mechanical_safety_margin":False}

def crossing(source,ear,screen:Screen)->dict:
    sz,ez=source[2],ear[2]
    if not 0<screen.plane_z_m<sz or abs(sz-ez)<1e-12:
        raise ValueError("screen must lie between source and ear in this scenario")
    t=(screen.plane_z_m-sz)/(ez-sz)
    if not 0<t<1:
        return {"intersects":False,"height_m":None,"x_m":None,
                "blocked":False}
    x=source[0]+t*(ear[0]-source[0])
    y=source[1]+t*(ear[1]-source[1])
    blocked=(screen.bottom_height_m<=y<=screen.top_height_m and
             abs(x-screen.center_x_m)<=screen.halfwidth_m)
    return {"intersects":True,"height_m":y,"x_m":x,
            "blocked":blocked,
            "top_margin_m":y-screen.top_height_m}

def visibility(setup:Setup,screen:Screen):
    """Center-ray visibility + a conservative finite faceplate clearance proxy.

    If the center ray passes above the monitor, the full flange still may
    intersect its angular silhouette. Project the entire nominal round
    flange within a bounding sphere, yielding a conservative (not exact)
    projected radius at the screen plane.
    """
    ear=(0.,setup.ear_height_m,0.)
    rows={}
    for k,p in sources(setup).items():
        c=crossing(p,ear,screen)
        t=(screen.plane_z_m-p[2])/(ear[2]-p[2])
        radius=DRIVERS[k].outer_diameter_mm/2000
        bound=(1-t)*radius
        # Entirely clear in vertical or lateral silhouette, as a sufficient
        # (not necessary) condition for geometrical unobstructed aperture.
        above=c["height_m"]-bound>screen.top_height_m
        lateral=abs(c["x_m"]-screen.center_x_m)-bound>screen.halfwidth_m
        c["conservative_full_flange_clear_above"]=above
        c["conservative_full_flange_clear_laterally"]=lateral
        c["conservative_full_flange_clear"]=above or lateral
        c["projected_flange_bound_radius_m"]=bound
        c["full_flange_top_clearance_m"]=c["height_m"]-bound-screen.top_height_m
        rows[k]=c
    return rows

def angle_to_normal(normal, direction):
    r=math.sqrt(sum(v*v for v in direction))
    if r<=0: raise ValueError("zero direction")
    c=sum(x*y for x,y in zip(normal,direction))/r
    return math.degrees(math.acos(max(-1.,min(1.,c))))

def band_pressure(setup:Setup, f_hz:float, ear:tuple,
                  reflection_coeff:float=0, 
                  table_forward_extent_m:float|None=None,
                  use_piston:bool=True):
    if not (f_hz>0 and 0<=reflection_coeff<=1):
        raise ValueError("invalid parameters")
    if table_forward_extent_m is not None and table_forward_extent_m<0:
        raise ValueError("negative table depth")
    ref=(0.,setup.ear_height_m,0.)
    positions=sources(setup)
    normal=unit_vectors(setup)[2]
    filters=ideal_filters(f_hz)
    wave_num=2*math.pi*f_hz/SPEED_SOUND_M_S
    out=0j
    for k,source in positions.items():
        r=distance(source,ear)
        r0=distance(source,ref)
        if r<=0 or r0<=0 or ear[1]<=0 or source[1]<=0:
            raise ValueError("receiver/source must be above table")
        direction=tuple(a-b for a,b in zip(ear,source))
        ref_direction=tuple(a-b for a,b in zip(ref,source))
        ang=angle_to_normal(normal,direction)
        ang0=angle_to_normal(normal,ref_direction)
        if ang>=90 or ang0>=90:
            raise ValueError("listener is on back side of ideal baffle")
        if use_piston:
            p0=piston_directivity(k,f_hz,ang0)
            p=piston_directivity(k,f_hz,ang)
            if abs(p0)<.05: raise ValueError("cannot calibrate piston near a null")
            factor=p/p0
        else:
            factor=1
        contribution=filters[k]*(r0/r)*factor*cmath.exp(-1j*wave_num*(r-r0))
        if reflection_coeff:
            # Image source in y<0. The ray hits y=0 at t=s/(s+ear_y).
            t=source[1]/(source[1]+ear[1])
            point=tuple(a+t*(b-a) for a,b in zip(source,ear))
            point=(point[0],0.,point[2])
            forward=source[2]-point[2] # from source toward listener, longitudinal
            if table_forward_extent_m is None or 0<=forward<=table_forward_extent_m:
                reflected=math.sqrt((ear[0]-source[0])**2
                  +(ear[1]+source[1])**2 +(ear[2]-source[2])**2)
                direction_ref=tuple(a-b for a,b in zip(point,source))
                ref_angle=angle_to_normal(normal,direction_ref)
                if use_piston:
                    coeff=piston_directivity(k,f_hz,ref_angle) if ref_angle<90 else 0.
                    coeff/=piston_directivity(k,f_hz,ang)
                else:
                    coeff=1.
                contribution*=1+reflection_coeff*(r/reflected)*coeff*cmath.exp(
                   -1j*wave_num*(reflected-r))
        out+=contribution
    return out

def compare_window(setup:Setup,reflection_coeff=0.,desk_extent_m=None):
    errs=[]
    for depth in DISTANCES_M:
        for head_x in HEAD_X_M:
            for head_y in HEAD_Y_M:
                center=(0.,setup.ear_height_m,setup.z_separation_m-depth)
                moving=(head_x,setup.ear_height_m+head_y,
                        setup.z_separation_m-depth)
                for f in FREQS_HZ:
                    a=band_pressure(setup,f,moving,reflection_coeff,desk_extent_m)
                    b=band_pressure(setup,f,center,reflection_coeff,desk_extent_m)
                    if min(abs(a),abs(b))<1e-10: raise ValueError("deep cancellation")
                    errs.append(abs(20*math.log10(abs(a/b))))
    errs.sort()
    return {"grid_samples":len(errs),"p95_abs_db":round(errs[math.ceil(.95*len(errs))-1],4),
            "rms_abs_db":round(math.sqrt(sum(e*e for e in errs)/len(errs)),4),
            "worst_abs_db":round(errs[-1],4)}

def stand_height_for_acoustic_center(setup:Setup):
    """Solve nominal distance from panel bottom to reference axis in local plane.

    Assumes mounting platform supports panel at its nominal lower envelope
    not under individual flanges, and ignores support hardware and tilt
    clearance. Use as a dimensional semantic check, NOT a stand CAD.
    """
    layout={v.name:v for v in default_layouts()}[setup.layout_id]
    p=panel_dimensions(layout)
    _,v,_=unit_vectors(setup)
    nominal_bottom_to_axis=p["nominal_ear_projection_from_lower_left_mm"][1]/1000
    # Roll changes which edge is physically lowest: use actual flange envelopes
    # as a conservative min physical lower projection instead.
    envelope=projected_baffle_extents(setup)
    return {"acoustic_axis_height_m":setup.center_height_m,
            "hypothetical_lower_flange_envelope_m":envelope["minimum_flange_y_m"],
            "difference_axis_to_lower_flange_m":
                 setup.center_height_m-envelope["minimum_flange_y_m"],
            "legacy_panel_axis_from_bottom_mm":p["nominal_ear_projection_from_lower_left_mm"][1],
            "note":"stand platform position requires real cabinet mass, support and orientation measurements"}

def scenarios()->dict:
    layouts={"A_minimum_practical_vertical":"vertical",
             "F_side_LOW_left":"side_left"}
    setups=[]
    for h_s,h_e in ((.45,.20),(.50,.35),(.65,.35)):
        for layout in layouts:
            for roll in (0,45,90):
                name=f"{layouts[layout]}_roll{roll}_s{int(h_s*100)}_e{int(h_e*100)}"
                setups.append(Setup(name,layout,roll,h_s,h_e))
    screens=[
      Screen(.35,.35,.3),
      Screen(.35,.45,.3),
      Screen(.35,.55,.3),
    ]
    out=[]
    for st in setups:
        pos=sources(st)
        bounds=projected_baffle_extents(st)
        view={}
        for sc in screens:
            per=visibility(st,sc)
            view[f"screen_top_{int(sc.top_height_m*100)}cm"]={
                "blocking_bands":[k for k,v in per.items() if v["blocked"]],
                "not_certified_full_flange_clear":[k for k,v in per.items() if not v["conservative_full_flange_clear"]],
                "flange_lower_edge_top_margin_m":{k:round(v["full_flange_top_clearance_m"],4) for k,v in per.items()},
                "ray_crossing_y_m":{k:round(v["height_m"],4) for k,v in per.items()},
                "top_clearance_m":{k:round(v["top_margin_m"],4) for k,v in per.items()}
            }
        score=compare_window(st)
        # Avoid false mixing of acoustic listening window with monitor
        # obstruction: scores assume no screen even when LOS is blocked.
        out.append({
          "scenario":st.name,
          "layout":st.layout_id,"roll_deg":st.roll_deg,
          "stand_axis_height_above_table_m":st.center_height_m,
          "listener_ear_height_above_table_m":st.ear_height_m,
          "center_vertical_offset_m":st.center_height_m-st.ear_height_m,
          "direct_target_down_tilt_deg":round(tilt_deg(st),3),
          "absolute_driver_center_coordinates_m":{
             k:[round(x,5) for x in v] for k,v in pos.items()},
          "envelope":{k:round(v,4) if isinstance(v,float) else v for k,v in bounds.items()},
          "support_semantics":stand_height_for_acoustic_center(st),
          "monitor_occlusion_proxies":view,
          "unobstructed_ideal_piston_head_window":score,
          "stand_mechanics_qualified":False,
          "true_angular_array_measured":False
        })
    return {
      "study":"D2-OVERHEAD-01",
      "real_monitor_geometry_known":False,
      "real_ear_height_known":False,
      "real_stationary_hardware_mounting_tested":False,
      "true_wavecor_angular_phase_known":False,
      "physical_ceiling_reflection_simulated":False,
      "real_baffle_diffraction_calculated":False,
      "declaration":"all results hypothetical conditional physical geometry and ideal piston monopoles",
      "scenarios":out,
      "warnings":[
        "40-50cm stand platform height is NOT the same as 40-50cm speaker acoustic-axis height.",
        "Owner's 40-50cm-above-table AND 20-30cm-above-ear must be reconciled with measured ear and monitor tops, not guessed.",
        "Aiming down increases vertical imaging elevation and can exceed common ±15 degree placement guidance.",
        "Turning MID/HF separation horizontal transfers crossover lobing into side-to-side head movement.",
        "Elevated supports require static tip/fall load verification, mechanical stops, vibration isolation and cable strain relief.",
        "Line-of-sight rectangles treat sound as rays; real diffraction around monitor edges and reflections aren't modeled.",
        "A clear line of sight to acoustic center doesn't prove all individual driver rays and full radiation are unobstructed.",
        "No real room ceiling or computer display-panel reflections/desk depth/desk occlusion included in window score.",
        "True stereo left/right toe-in, stereo triangle and head-related perception not included."
      ]
    }

if __name__=="__main__":
    print(json.dumps(scenarios(),ensure_ascii=False,indent=2))
