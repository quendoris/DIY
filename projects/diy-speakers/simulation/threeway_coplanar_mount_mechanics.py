#!/usr/bin/env python3
"""D2-MOUNT-01: coplanar screen-top speaker placement and load-path demand.

FACTS from owner: head reference 0.60m, existing monitor tops 0.70/0.60m,
future THREE monitors (42-54in). Owner asks acoustic-axis depth equal to
screen plane, horizontal 3-way, rigid TABLE-ANCHORED support, mass ~10kg
per speaker, 50kgf working / 100kgf proof load TARGETS.

This is a DEMAND MODEL, not structural design verification, rated hardware
or evidence of a safe overhead mounting. Full system acceptance requires
real screen/stand/cabinet dimensions, fastener/desktop material strengths,
structural calculation and professional load qualification where applicable.
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass

from threeway_baffle_geometry import DRIVERS, panel_dimensions, default_layouts
from threeway_stereo_multimonitor import (
    Monitor, Satellite, array_basis, evaluate, monitor_scenario,
    source_centers, true_equilateral_3d_lateral_x, USER_HEAD_MARK_M
)

G=9.80665
OWNER_SATELLITE_DESIGN_MASS_KG=10.0
OWNER_REQUESTED_MIN_WORKING_EQUIV_KG=50.0
OWNER_REQUESTED_PROOF_EQUIV_KG=100.0
OWNER_DESK_ATTACHMENT="recessed/embedded screw or bolt (exact fastening construction not verified)"
RECOMMENDED_PLACEMENT="speaker reference plane coplanar with actual monitor front/top array"
MIN_SCREEN_CLEARANCE_M=.020
DESK_ANCHOR_LEVER_ARM_M=(.15,.20,.30,.40)
JOINT_COM_OFFSET_M=(.03,.08,.15)
BOLT_ROW_SPACING_M=(.06,.08,.12)
TRIAL_AXIS_HEIGHT_M=(.82,.85,.90,.925,1.00)
AUDIT_HEAD_GRID_POSITIONS=27

def load_equivalent_kgf_to_newtons(equiv_mass_kg:float)->float:
    if equiv_mass_kg<=0:raise ValueError("positive load equivalent required")
    return equiv_mass_kg*G

def structural_demands(mass_kg:float,arm_m:float,lever_row_spacing_m:float)->dict:
    """Demand from pure GRAVITY with horizontal offset.

    f=mg. M=F*e. Nominal two-row anchorage couple F_tension~M/h.
    THIS DOES NOT INCLUDE direct shear, unequal fastener group share,
    prying, desk creep, dynamic load, vibration, impact or user contact.
    """
    if min(mass_kg,arm_m,lever_row_spacing_m)<=0:
        raise ValueError("mass/eccentricity/row pitch positive")
    f=mass_kg*G
    m=f*arm_m
    return {
      "force_N":round(f,4),
      "moment_Nm":round(m,4),
      "ideal_two_row_force_couple_N":round(m/lever_row_spacing_m,4),
      "row_spacing_m":lever_row_spacing_m,
      "horizontal_gravity_moment_arm_m":arm_m,
      "ideal_two_row_force_is_not_validated_bolt_tension":True,
    }

def certification_envelope():
    row=[]
    for location in ("TABLE_BASE","TILT_JOINT"):
        arms=DESK_ANCHOR_LEVER_ARM_M if location=="TABLE_BASE" else JOINT_COM_OFFSET_M
        for e in arms:
            for pitch in BOLT_ROW_SPACING_M:
                row.append({
                    "component":location,
                    "source_CoM_horizontal_eccentricity_m":e,
                    "fastener_effective_row_spacing_m":pitch,
                    "nominal_10kg_demand":structural_demands(10,e,pitch),
                    "working_target_50kgf_demand":structural_demands(50,e,pitch),
                    "proof_target_100kgf_demand":structural_demands(100,e,pitch),
                    "load_case_is_analytical_only":True,
                    "not_certified_for_overhead_use":True,
                })
    return row

def transformed_baffle_envelope(speaker:Satellite)->dict:
    """Ideal FRONT-PLANE baffle corners/flange circular perimeter geometry.

    Original factory flanges and reference rectangle are transformed with
    yaw+pitch+roll. Frame walls, cabinet depth and mechanical brackets are
    NOT included; this is only a nominal initial design envelope.
    """
    layouts={a.name:a for a in default_layouts()}
    l=layouts[speaker.layout_id]
    p=panel_dimensions(l)
    origin=p["nominal_ear_projection_from_lower_left_mm"]
    w,h=p["required_flat_panel_width_mm"],p["required_flat_panel_height_mm"]
    u,v,_=array_basis(speaker)
    c=(speaker.center_x_m,speaker.axis_height_m,speaker.axial_depth_m)
    def world(x_mm,y_mm):
        x=x_mm/1000
        y=y_mm/1000
        return tuple(c[i]+x*u[i]+y*v[i] for i in range(3))
    corners=[world(-origin[0],-origin[1]),
             world(w-origin[0],-origin[1]),
             world(w-origin[0],h-origin[1]),
             world(-origin[0],h-origin[1])]
    speaker_sources=source_centers(speaker)
    # An exact circular flange in tilted planar orientation has vertical
    # extremum r*sqrt(u_y^2+v_y^2); this is a planar faceplate projection,
    # not a conservative bound on the whole DEEP cabinet volume.
    min_flange=min(
        pt[1]-DRIVERS[name].outer_diameter_mm/2000*
          math.hypot(u[1],v[1])
        for name,pt in speaker_sources.items())
    min_baffle=min(pt[1] for pt in corners)
    return {
       "min_baffle_front_plane_y_m":round(min_baffle,5),
       "min_nominal_flange_front_plane_y_m":round(min_flange,5),
       "lowest_front_plane_y_m":round(min(min_flange,min_baffle),5),
       "front_panel_z_range_m":[round(min(pt[2] for pt in corners),5),
                                 round(max(pt[2] for pt in corners),5)],
       "front_panel_x_range_m":[round(min(pt[0] for pt in corners),5),
                                 round(max(pt[0] for pt in corners),5)],
       "full_cabinet_depth_checked":False,
       "mounting_hardware_clearances_checked":False,
       "any_heavy_moving_stand_qualified":False,
    }

def screen_top_clearance(speaker:Satellite,screen_top_m:float,
                         mechanical_margin_m:float=MIN_SCREEN_CLEARANCE_M)->dict:
    if screen_top_m<=0 or mechanical_margin_m<0:
        raise ValueError("invalid screen clearance requirements")
    e=transformed_baffle_envelope(speaker)
    gap=e["lowest_front_plane_y_m"]-screen_top_m
    return {
       "screen_top_m":screen_top_m,
       "idealized_front_plane_min_gap_m":round(gap,5),
       "desired_additional_clearance_m":mechanical_margin_m,
       "front_plane_passes_nominal_top_margin":gap>=mechanical_margin_m,
       "solid_cabinet_above_screen_certified":False,
       "note":"Nominal circle and rectangular FRONT panel only; no cabinet solid, cable, enclosure depth or active arm in this pass",
    }

def coplanar_stereo(screen_plane_m:float,axis_height_m:float,
                    screen_top_m:float,
                    use_true_equilateral:bool=True,
                    roll_deg:float=90.)->dict:
    if screen_plane_m<=0 or axis_height_m<=0:
        raise ValueError("positive depth and height")
    sx=(true_equilateral_3d_lateral_x(screen_plane_m,axis_height_m)
        if use_true_equilateral else screen_plane_m/math.sqrt(3))
    pair=[Satellite("L",-sx,axis_height_m,screen_plane_m,roll_deg),
          Satellite("R",sx,axis_height_m,screen_plane_m,-roll_deg)]
    clear=[screen_top_clearance(s,screen_top_m) for s in pair]
    # The screen itself is IN the same nominal center depth plane.
    # Some individual rotated baffle sources lie behind its front plane,
    # so a coplanar axis is not sufficient for guaranteed ray clearance.
    # For future 3-monitors, use future screen scenario; overwriting
    # top heights below would invent owner measurements, so this is
    # explicitly a hypothetical height-bound comparison only.
    hypothetical=monitor_scenario("FUTURE_54_CENTER_42_SIDES")
    hypothetical=[Monitor(s.id,s.center_x_m,screen_plane_m,s.width_m,screen_top_m,
                           future_scenario=True) for s in hypothetical]
    rays=evaluate(pair,hypothetical)
    return {
      "axis_height_m":axis_height_m,
      "speaker_center_depth_m":screen_plane_m,
      "both_reference_acoustic_axes_coplanar_with_monitor_surface":True,
      "true_3d_equilateral":use_true_equilateral,
      "local_driver_array_roll_deg":roll_deg,
      "source_horizontal_positions_m":[round(-sx,4),round(sx,4)],
      "true_full_baffle_front_plane_extents":[transformed_baffle_envelope(s) for s in pair],
      "front_face_clearance_l_r":clear,
      "source_to_listener_screen_ray_grid":rays,
      "screen_sizes_and_spatial_offsets_are_hypotheses":True,
      "cabinet_mechanics_and_solid_collision_tested":False,
    }

def report():
    row=[]
    for top in (.70,.80):
        for h in TRIAL_AXIS_HEIGHT_M:
            for geometry in ("PLAN_60","TRUE_EQUILATERAL_3D"):
                row.append(coplanar_stereo(.35,h,top,
                    use_true_equilateral=(geometry=="TRUE_EQUILATERAL_3D")))
    return {
      "study":"D2-MOUNT-01",
      "owner_measured":{"head_above_table_m":.60,
                        "current_main_32_top_above_table_m":.70,
                        "current_side_27_top_above_table_m":.60,
                        "future_three_large_monitors":True},
      "owner_requested":{"satellite_estimated_mass_kg":OWNER_SATELLITE_DESIGN_MASS_KG,
                         "minimum_working_load_equivalent_kgf":OWNER_REQUESTED_MIN_WORKING_EQUIV_KG,
                         "minimum_proof_load_equivalent_kgf":OWNER_REQUESTED_PROOF_EQUIV_KG,
                         "desk_anchor_specification":OWNER_DESK_ATTACHMENT,
                         "speaker_depth_relative_to_screen_plane_m":0.0,
                         "horizontal_drivers_as_leading_hypothesis":True},
      "screen_and_ear_unknowns":{
        "actual_ear_canal_above_table_m":None,
        "exact_main_screen_front_plane_depth_m":None,
        "actual_future_monitor_top_m":None,
        "actual_future_screen_bounds_and_supports":None,
        "tabletop_material_thickness_structure_strength":None,
        "cabinet_mass_cog_and_center_of_mass_offset":None,
        "leg/stand_base_location_and_mounting_fasteners":None,
      },
      "force_and_moment_demands":certification_envelope(),
      "coplanar_speaker_position_scenarios":row,
      "source_plane_is_not_full_cabinet_envelope":True,
      "load_rating_claimed_for_real_joint":False,
      "preinstallation_passed":False,
      "warnings":[
        "50kgf working is ~490N; 100kgf equivalent is ~981N; these are force-load EQUIVALENTS, not Nm torque ratings or validated load capacities.",
        "100kgf proof target alone does not certify a 50kgf working load for overhead usage, long-term fatigue, or desk attachment; select verified hardware and qualified load path.",
        "The load must transfer through cabinet hard points, pitch/yaw/roll hinges and locks, column, base, anchors, tabletop, frame and any independent secondary restraint.",
        "A screw/insert recessed into a particleboard desktop cannot be assumed pull-out safe. Verify material, sufficient through-bolt backing plates and structural frame; single insert lacks anti-rotation/fail redundancy.",
        "Joint pivot should be near center of mass or demand includes substantial extra torque; passive clamp friction is insufficient as the sole lock.",
        "One large proof force applied to a perfectly centered pivot is NOT an offset proof moment or a substitute for separate worst-case position tests.",
        "Main and secondary attachments must be independently adequate; 'safety cable' to a failing shared bracket is not independent.",
        "Static 10kg supported and 50kgf WLL+100kgf proof are user acceptance TARGETS, not certified standards applied here.",
        "When acoustic axes are in monitor planes, some tilted/yawed flanges and future cabinet solids may extend behind the screen plane and intersect screen clearance.",
        "Actual protected 3D stereo room and audio performance, physical stereo geometry and future large monitor heights remain unknown.",
      ],
    }

if __name__=="__main__":
    print(json.dumps(report(),indent=2,ensure_ascii=False))
