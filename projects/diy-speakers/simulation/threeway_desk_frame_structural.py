#!/usr/bin/env python3
"""D2-FRAME-01: owner's 2000x1000 desktop, 50x50 PROFILE and 50mm SOLID WOOD.

FACTS:
 * main desk envelope 2.0 x 1.0 metres
 * frame made from 50 x 50 millimetre profile
 * main tabletop and raised shelf on the frame
 * proposed solid-wood MAIN top thickness 50mm
 * owner plans "двусторонние винты" to fasten wood to frame
 * two over-monitor ~10kg loudspeakers; >=50kgf working / 100kgf proof
MISSING: profile alloy/steel, tube vs extruded solid/slot profile, WALL,
 spans/cross-braces, frame joint/welds, desk support location, upper shelf
 footprint/thickness, solid wood species/grain/moisture movement, bolt type,
 accurate centre-of-mass and room support surfaces.

Section properties are idealized SHARP-CORNER CLOSED SQUARE TUBE
candidate calculations ONLY. If real profile is aluminum T-slot, solid or
rolled/sharp-radius steel, REJECT these simplified numbers. Euler-Bernoulli
test-beam is not a desk FEM and gives no rigging rating.

Our alternative puts the structural upright DIRECTLY into reinforced
metal frame nodes, with independent secondary support, while the 50mm
solid-wood top is attached by separate wood-movement-compatible joints.
"""
from __future__ import annotations
import json
import math

G=9.80665
MEASURED_PLAN_MM=[2000,1000]
PROFILE_OUTER_MM=[50,50]
TOP_SOLID_WOOD_THICKNESS_MM=50
SHELF_EXISTS=True
SHELF_THICKNESS_MM=None
PROFILE_MATERIAL=None
TUBE_WALL_MM=None
WOOD_DENSITY_KG_PER_M3=None
WOOD_SPECIES=None
GRAIN_DIRECTION=None
DOUBLE_ENDED_FASTENER_STYLE=None
FRAME_SUPPORT_LAYOUT=None
SPEAKER_ESTIMATE_KG=10.0
PER_SAT_WORKING_EQUIVALENT_KGF=50.0
PER_SAT_PROOF_EQUIVALENT_KGF=100.0
TWO_SATELLITES=2
E_HYPOTHETICAL_STEEL_N_PER_MM2=200_000
WEIGHT_DENSITIES_HYPOTHETICAL=[450,550,650,750,850]
HYPOTHETICAL_TUBE_WALL_MM=[1.5,2.,2.5,3.,4.]
SPAN_FOR_IDEAL_BEAM_MM=[500,1000,2000]
MOMENT_ARMS_MM=[150,200,300,400]

def gravity_N(equivalent_mass_kg:float)->float:
    if equivalent_mass_kg<=0:
        raise ValueError("positive mass equivalent required")
    return equivalent_mass_kg*G

def desktop_volume_m3(width_mm:float=2000,length_mm:float=1000,
                      thickness_mm:float=50)->float:
    if min(width_mm,length_mm,thickness_mm)<=0:
        raise ValueError("positive solid wood dimensions")
    return width_mm*length_mm*thickness_mm/1e9

def indicative_wood_mass(density_kg_m3:float)->float:
    if density_kg_m3<=0:
        raise ValueError("positive density")
    return desktop_volume_m3()*density_kg_m3

def ideal_square_hollow_section_mm(B_mm:float,wall_mm:float)->dict:
    if B_mm<=0 or not 0<wall_mm<B_mm/2:
        raise ValueError("invalid closed square tube idealization")
    inner=B_mm-2*wall_mm
    area=B_mm**2-inner**2
    i=(B_mm**4-inner**4)/12
    z=i/(B_mm/2)
    return {"outer_width_mm":B_mm,"wall_mm":wall_mm,
            "ideal_area_mm2":area,"ideal_I_mm4":i,
            "ideal_elastic_section_modulus_mm3":z,
            "actual_profile_section_unknown":True}

def theoretical_beam_response(force_N:float,span_mm:float,ideal_I_mm4:float,
                              elastic_modulus_N_mm2:float=E_HYPOTHETICAL_STEEL_N_PER_MM2)->dict:
    """ONE simply supported straight ideal single beam, ONE midpoint point load.

    This does NOT resemble a rated multidirectional welded 2m desk frame.
    Ignore torsion, sway, deflection from other monitor loads, joint
    stiffness, local tube wall crushing, shear, weld quality, and fatigue.
    """
    if min(force_N,span_mm,ideal_I_mm4,elastic_modulus_N_mm2)<=0:
        raise ValueError("invalid beam parameters")
    midspan_moment_Nm=force_N*(span_mm/1000)/4
    midspan_deflection_mm=force_N*span_mm**3/(48*elastic_modulus_N_mm2*ideal_I_mm4)
    return {"force_N":force_N,"simple_span_mm":span_mm,
            "max_ideal_midspan_moment_Nm":midspan_moment_Nm,
            "ideal_midspan_deflection_mm":midspan_deflection_mm,
            "supports":"TWO PIN/ROLLER ends; NO torsion or multiple beam-sharing",
            "reflects_real_desk_frame":False}

def hypothetical_local_section_bending_stress_MPa(moment_Nm:float,section_modulus_mm3:float)->float:
    if min(moment_Nm,section_modulus_mm3)<=0:
        raise ValueError("positive ideal section demand")
    return moment_Nm*1000/section_modulus_mm3

def base_joint_couple_N(load_equivalent_kgf:float,arm_mm:float,
                        two_row_spacing_mm:float)->float:
    if min(load_equivalent_kgf,arm_mm,two_row_spacing_mm)<=0:
        raise ValueError("invalid anchor geometry")
    return gravity_N(load_equivalent_kgf)*arm_mm/two_row_spacing_mm

def report():
    base={
       "stage":"D2-FRAME-01",
       "owner_measured_geometry":{
         "desk_plan_mm":MEASURED_PLAN_MM,
         "frame_profile_outer_mm":PROFILE_OUTER_MM,
         "main_desktop_material":"solid wood",
         "main_desktop_thickness_mm":TOP_SOLID_WOOD_THICKNESS_MM,
         "upper_shelf_present":SHELF_EXISTS,
         "shelf_thickness_mm":SHELF_THICKNESS_MM,
         "wood_to_frame_fastening_planned":"двусторонние винты; exact fastener not identified"
       },
       "unknown_requirements":{
          "frame_profile_material":PROFILE_MATERIAL,
          "profile_is_closed_steel_tube":None,
          "tube_wall_mm":TUBE_WALL_MM,
          "load_support_span_layout_and_bracing":FRAME_SUPPORT_LAYOUT,
          "frame_cross_members_welds_and_joints":None,
          "solid_wood_species":WOOD_SPECIES,
          "grain_direction":GRAIN_DIRECTION,
          "wood_moisture_and_expected_transverse_movement":None,
          "wood_to_metal_fastener_detail":DOUBLE_ENDED_FASTENER_STYLE,
          "fastener_diameter_thread_strength_quantity_spacing":None,
          "lower_table_frame_to_floor_support_and_tip_resistance":None,
          "upper_shelf_dimensions_mass_and_loads":None,
          "speaker_real_mass_and_com":None,
          "joint_and_frame_proof_loading_certification":None
       },
       "speaker_load_target":{
           "satellites_count":TWO_SATELLITES,
           "estimated_per_satellite_mass_kg":SPEAKER_ESTIMATE_KG,
           "total_estimated_satellite_mass_kg":TWO_SATELLITES*SPEAKER_ESTIMATE_KG,
           "per_satellite_working_target_kgf":PER_SAT_WORKING_EQUIVALENT_KGF,
           "per_satellite_proof_target_kgf":PER_SAT_PROOF_EQUIVALENT_KGF,
           "both_nominal_speaker_gravity_N":2*gravity_N(SPEAKER_ESTIMATE_KG),
           "both_hypothetical_proof_forces_simultaneous_N":2*gravity_N(PER_SAT_PROOF_EQUIVALENT_KGF),
           "both_simultaneous_proof_is_required_by_owner":None
       },
       "main_desktop_volume_m3":desktop_volume_m3(),
       "main_solid_wood_mass_scenarios_not_actual":[
         {"assumed_density_kg_m3":d,
          "top_mass_kg":round(indicative_wood_mass(d),2)}
           for d in WEIGHT_DENSITIES_HYPOTHETICAL
       ],
       "illustrative_tube_sections":[],
       "illustrative_tube_span_model":[],
       "load_case_moments":[],
       "architecture_preference":{
         "primary_load_path":"separate speaker frame -> positive-lock double-sided yoke -> post -> locally reinforced metal frame node -> table legs/frame -> floor",
         "main_tabletop_role":"work surface and acoustical/visual cover; DO NOT rely on wood-only threaded pullout",
         "tabletop_attachment":"wood-movement-compatible independent fasteners; avoid rigid restriction of across-grain expansion",
         "support_position":"above and depth-aligned with monitor front planes; screen full-solid clearance to test separately",
         "metalframe_connection":"through-bolts with engineered doubler/reinforcing box OR welded reinforced socket only after real structural drawings and fabrication checks",
         "wood_fastener_type":"not yet known; double-ended studs to be analyzed only as tabletop attachment not primary loudspeaker restraint",
         "redundancy":"secondary independent load-bearing catch to independently verified desk frame/floor/wall member",
         "not_qualified":True
       },
       "real_structural_capacity_certified":False,
       "real_fastener_load_rated":False,
       "beam_model_equivalent_to_frame":False,
       "safety_status":"NOT_BUILT_NOT_REVIEWED_NO_LOAD_RATING"
    }
    for t in HYPOTHETICAL_TUBE_WALL_MM:
        section=ideal_square_hollow_section_mm(50,t)
        M=gravity_N(100)*.3
        section["stress_from_294Nm_hypothetical_MPa"]=round(
            hypothetical_local_section_bending_stress_MPa(M,section["ideal_elastic_section_modulus_mm3"]),2)
        section["ideal_stress_not_allowable_stress_or_safety_margin"]=True
        base["illustrative_tube_sections"].append(section)
        if t in (2.,3.):
            for span in SPAN_FOR_IDEAL_BEAM_MM:
                r=theoretical_beam_response(gravity_N(100),span,section["ideal_I_mm4"])
                base["illustrative_tube_span_model"].append({
                    "assumed_wall_mm":t,
                    "span_mm":span,
                    "midpoint_100kgf_deflection_mm":round(r["ideal_midspan_deflection_mm"],4),
                    "ideal_midspan_bending_moment_Nm":round(r["max_ideal_midspan_moment_Nm"],2),
                    "not_actual_tableframe_deflection":True
                })
    for arm in MOMENT_ARMS_MM:
        base["load_case_moments"].append({
            "assumed_local_arm_mm":arm,
            "per_satellite_10kg_Nm":round(gravity_N(10)*arm/1000,2),
            "per_satellite_50kgf_working_target_Nm":round(gravity_N(50)*arm/1000,2),
            "per_satellite_100kgf_proof_target_Nm":round(gravity_N(100)*arm/1000,2),
            "couple_for_proof_with_80mm_anchor_row_separation_N":round(base_joint_couple_N(100,arm,80),1)
        })
    base["limitations"]=[
        "50x50mm external profile is not a unique cross section until tube vs extrusion, material, wall and design tolerances are known.",
        "All formulae use IDEAL sharp-corner closed square tube; real rounded corners reduce/use different properties.",
        "E=200GPa is HYPOTHETICAL steel-only; no aluminum or timber properties substituted.",
        "Beam span models are one simple beam loaded at centre, not the 2x1m whole braced steel frame, torsion, welded joints, or fatigue.",
        "Solid wood gross top volume 0.1 m3; density and final glued-up top assembly unknown, not a verified 45-85kg weight or safe frame stabilizer.",
        "Solid timber moves across grain seasonally: slotted/figure-8 fasteners or equivalent must retain top while allowing movement; actual allowance needs species/moisture calculation.",
        "A double-threaded wood-metal stud can attach a tabletop, but does not prove pullout resistance or frame stability and must not be dual-used for 100kgf speaker retention.",
        "The upper shelf geometry, monitor weights and anchor positions change local moments and global table stability.",
        "Any through-bolt or reinforced socket to 50x50 metal must consider local wall crippling, bolt tear-out, weld strength and cross-member distance to legs.",
        "Never do static proof load tests near people/screens; mechanical engineer to select rated hardware and controlled independent proof/testing.",
        "High working and proof target per satellite does not imply 100kgf simultaneous proof for both; owner criterion and actual structural load combinations need explicit confirmation.",
        "Unknown desk-to-floor anchorage and frame self-weight prevent reliable global uplift/overturn check."
    ]
    return base

if __name__=="__main__":
    print(json.dumps(report(),ensure_ascii=False,indent=2))
