#!/usr/bin/env python3
"""D2-STEREO-01: REAL user heights + future-monitor stereo geometric installation.

Measured user facts:
  - head reference +0.60m above desk (NOT proven acoustic ear-center height)
  - 32in top +0.70m above desk (shelf +0.10m and displayed height +0.60m)
  - 27in existing side monitor top +0.60m above desk
  - future 3 monitors, potentially 42-54in, no free lateral side space
All x/z positions, actual screen widths/aspect ratios and future top heights
are HYPOTHESES. They are never presented as user measurements.

This models rigid-body pilot baffle arrays (roll 0/45/90) with stereo yaw+
pitch aiming, ideal geometrical line-of-sight and conservative projected
full-flange visible-zone criteria. NO real diffraction, acoustic SPL,
monitor reflection, phase-directivity, structural stand qualification.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json
import math
from threeway_baffle_geometry import DRIVERS, ORDER, default_layouts

USER_HEAD_MARK_M=.60
CURRENT_32_TOP_M=.70
CURRENT_27_SIDE_TOP_M=.60
SPEAKER_PROPOSED_STAND_PLATFORM_M=(.40,.50)
DISTANCE_RANGE_M=(.60,.70,.80)
HEAD_X_M=(-.08,0.,.08)
HEAD_Y_M=(-.10,0.,.10)
EARS_SOURCE_EXPLICITLY_UNVERIFIED=True

@dataclass(frozen=True)
class Monitor:
    id:str
    center_x_m:float
    plane_depth_m:float
    width_m:float
    top_m:float
    bottom_m:float=0.0
    measured_top:bool=False
    future_scenario:bool=False
    def validate(self):
        if self.width_m<=0 or self.plane_depth_m<=0 or self.top_m<=self.bottom_m:
            raise ValueError("invalid screen geometry")

@dataclass(frozen=True)
class Satellite:
    id:str
    center_x_m:float
    axis_height_m:float
    axial_depth_m:float
    roll_deg:float
    layout_id:str="A_minimum_practical_vertical"

def vector_plus(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(x,v): return tuple(x*a for a in v)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a,a))
def unit(a):
    n=norm(a)
    if n<=0: raise ValueError("zero vector")
    return scale(1/n,a)

def stereo_lateral_x(axial_depth_m:float,stereo_half_angle_deg:float=30.)->float:
    """Free-field horizontal plan view, not including ear-to-speaker elevation."""
    if axial_depth_m<=0 or not 0<stereo_half_angle_deg<80:
        raise ValueError("invalid stereo geometry")
    return axial_depth_m*math.tan(math.radians(stereo_half_angle_deg))

def array_basis(speaker:Satellite,ear=(0.,USER_HEAD_MARK_M,0.)):
    center=(speaker.center_x_m,speaker.axis_height_m,speaker.axial_depth_m)
    n=unit(tuple(e-c for e,c in zip(ear,center)))  # aimed at listener
    # horizontal nominal 'right' in tilted baffle, projected orthogonal to normal.
    horizontal=unit((speaker.axial_depth_m,0.,-speaker.center_x_m))
    if abs(dot(horizontal,n))>1e-9:
        raise ValueError("invalid horizontal speaker basis")
    up=unit(cross(horizontal,n))
    roll=math.radians(speaker.roll_deg)
    u=vector_plus(scale(math.cos(roll),horizontal),scale(math.sin(roll),up))
    v=vector_plus(scale(-math.sin(roll),horizontal),scale(math.cos(roll),up))
    return u,v,n

def source_centers(speaker:Satellite,ear_reference=(0.,USER_HEAD_MARK_M,0.)):
    layouts={l.name:l for l in default_layouts()}
    l=layouts[speaker.layout_id]
    u,v,_=array_basis(speaker,ear_reference)
    c=(speaker.center_x_m,speaker.axis_height_m,speaker.axial_depth_m)
    return {name:vector_plus(c,vector_plus(scale(xmm*.001,u),scale(ymm*.001,v)))
            for name,(xmm,ymm) in l.positions_mm.items()}

def source_ray_to_screen(source,ear,screen:Monitor,nominal_flange_radius_m:float,
                         edge_margin_m:float=.02):
    screen.validate()
    if not 0<=edge_margin_m<.2:
        raise ValueError("invalid clearance margin")
    a,b=source[2],ear[2]
    if abs(a-b)<=1e-12:
        raise ValueError("ray parallel to monitor plane")
    t=(screen.plane_depth_m-a)/(b-a)
    if not 0<t<1:
        return {"screen_is_between":False,"center_blocked":False,
                "full_flange_conservatively_clear":True,
                "nominal_margin_m":None,"source_x_at_screen_m":None,
                "source_h_at_screen_m":None}
    px=source[0]+t*(ear[0]-source[0])
    py=source[1]+t*(ear[1]-source[1])
    rx=(1-t)*nominal_flange_radius_m +edge_margin_m
    # conservative circular speaker in bounding square; source center
    # and ray aperture may already be offset from actual acoustic opening.
    left,right=screen.center_x_m-screen.width_m/2,screen.center_x_m+screen.width_m/2
    x_clear=px+rx<left or px-rx>right
    y_clear=py-rx>screen.top_m or py+rx<screen.bottom_m
    center_blocked=left<=px<=right and screen.bottom_m<=py<=screen.top_m
    vertical_margin=py-rx-screen.top_m
    return {
      "screen_is_between":True,
      "center_blocked":center_blocked,
      "full_flange_conservatively_clear":x_clear or y_clear,
      "is_clear_by_above":py-rx>screen.top_m,
      "is_clear_by_side":x_clear,
      "nominal_margin_m":round(vertical_margin,5),
      "source_x_at_screen_m":round(px,5),
      "source_h_at_screen_m":round(py,5),
      "projected_flange_radius_plus_margin_m":round(rx,5),
    }

def stereo_angle(speakers:list[Satellite],ear=(0.,USER_HEAD_MARK_M,0.)):
    p=[(a.center_x_m,a.axis_height_m,a.axial_depth_m) for a in speakers]
    a=unit(tuple(v-e for v,e in zip(p[0],ear)))
    b=unit(tuple(v-e for v,e in zip(p[1],ear)))
    return math.degrees(math.acos(max(-1.,min(1.,dot(a,b)))))

def horizontal_stereo_angle(speakers:list[Satellite]):
    x1,x2=speakers[0].center_x_m,speakers[1].center_x_m
    d1,d2=speakers[0].axial_depth_m,speakers[1].axial_depth_m
    return math.degrees(abs(math.atan2(x1,d1)-math.atan2(x2,d2)))

def down_tilt(speaker:Satellite,reference_height_m=USER_HEAD_MARK_M):
    return math.degrees(math.atan2(speaker.axis_height_m-reference_height_m,
                   math.hypot(speaker.center_x_m,speaker.axial_depth_m)))

def monitor_scenario(name:str):
    if name=="MEASURED_TOPS_32_27":
        # Widths are inferred ONLY for nominal 16:9 aspect ratio; actual screen
        # edge x/z is unknown. 27in on user's side; left/right not confirmed,
        # use right purely as a geometrical example.
        return [
          Monitor("central_32_current",0.,.35,.708,.70,measured_top=True),
          Monitor("side_27_right",.66,.40,.598,.60,measured_top=True),
        ]
    if name=="FUTURE_54_CENTER_42_SIDES":
        # Hypothetical 16:9 54in and 42in visible rectangular widths.
        # Future top heights .8 and .73m are NOT actual user facts.
        return [
          Monitor("center_54_future",0.,.35,1.196,.80,future_scenario=True),
          Monitor("left_42_future",-1.065,.42,.93,.73,future_scenario=True),
          Monitor("right_42_future",1.065,.42,.93,.73,future_scenario=True),
        ]
    raise ValueError("unknown monitor arrangement")

def evaluate(satellites:list[Satellite],monitors:list[Monitor],
             ear_height_m=USER_HEAD_MARK_M,head_grid=True):
    if len(satellites)!=2 or satellites[0].id==satellites[1].id:
        raise ValueError("exactly two distinct satellites")
    if ear_height_m<=0:
        raise ValueError("ear proxy height positive")
    for m in monitors: m.validate()
    src=[source_centers(s,(0.,ear_height_m,0.)) for s in satellites]
    positions=0
    free_centers=0
    full_flange=0
    restricted_by_screen={m.id:0 for m in monitors}
    sample=None
    depths=DISTANCE_RANGE_M if head_grid else (.70,)
    xvals=HEAD_X_M if head_grid else (0.,)
    yvals=HEAD_Y_M if head_grid else (0.,)
    for distance in depths:
        for x in xvals:
            for h in yvals:
                ear=(x,ear_height_m+h,.70-distance)
                centers_clear=True
                flanges_clear=True
                faults=[]
                for speaker,sources in zip(satellites,src):
                    for name,source in sources.items():
                        for m in monitors:
                            r=source_ray_to_screen(source,ear,m,
                                  DRIVERS[name].outer_diameter_mm/2000)
                            if r["center_blocked"]:
                                centers_clear=False
                            if not r["full_flange_conservatively_clear"]:
                                flanges_clear=False
                                restricted_by_screen[m.id]+=1
                                faults.append([speaker.id,name,m.id])
                positions+=1
                if centers_clear: free_centers+=1
                if flanges_clear: full_flange+=1
                if sample is None and faults:
                    sample={"listener_m":[round(v,4) for v in ear],
                            "not_full_flange_clear":faults[:12]}
    return {
      "positions_checked":positions,
      "two_speaker_all_six_center_rays_clear_count":free_centers,
      "two_speaker_all_six_faceplates_clear_count":full_flange,
      "all_six_centers_clear_fraction":round(free_centers/positions,4),
      "all_six_full_flange_clear_fraction":round(full_flange/positions,4),
      "per_screen_faceplate_overlap_incidences":restricted_by_screen,
      "first_unclear_position":sample,
      "all_hardwares_physically_measured":False,
      "complete_acoustic_diffraction_and_directionality":False,
    }

def scenario_report():
    s=.7
    x=stereo_lateral_x(s)
    scenarios=[]
    for stage in ("MEASURED_TOPS_32_27","FUTURE_54_CENTER_42_SIDES"):
        m=monitor_scenario(stage)
        for source_depth in (.70,.60,.55,.40,.25):
            sx=stereo_lateral_x(source_depth) # maintains ±30° horizontal stereo
            for height in (.80,.88,.92,.96,1.00):
                for roll in (0.,45.,90.):
                    speakers=[
                        Satellite("L",-sx,height,source_depth,roll),
                        Satellite("R",sx,height,source_depth,-roll)
                    ]
                    metrics=evaluate(speakers,m)
                    scenarios.append({
                       "monitor_configuration":stage,
                       "speaker_depth_m":source_depth,
                       "nominal_acoustic_axis_height_m":height,
                       "roll_deg":roll,
                       "speaker_center_offsets_m":[round(-sx,4),round(sx,4)],
                       "horizontal_stereo_included_angle_deg":round(horizontal_stereo_angle(speakers),4),
                       "true_3d_stereo_included_angle_deg":round(stereo_angle(speakers),4),
                       "down_tilt_each_deg":round(down_tilt(speakers[0]),4),
                       "visibility":metrics,
                    })
    return {
       "study":"D2-STEREO-01",
       "user_measured":{
         "head_reference_above_table_m":USER_HEAD_MARK_M,
         "central_32_monitor_top_above_table_m":CURRENT_32_TOP_M,
         "side_27_monitor_top_above_table_m":CURRENT_27_SIDE_TOP_M,
         "desk_shelf_height_m":.10,
         "user_intent":"large three-monitor future setup 42-54in, no lateral free space",
         "ear_height_confirmed":False
       },
       "unmeasured_assumptions":{
         "screen_widths":"from 16:9 diagonals, NOT measured",
         "screen_x_positions":"invented for test only",
         "screen_depths":"0.35/0.40/0.42m from ear reference, NOT measured",
         "future_54_top_height_m":.80,
         "future_42_sides_top_height_m":.73,
         "future_dimensions_are_not_committed_to_purchase":True
       },
       "speaker_layout":"Wavecor original vertical array rolled 0/45/90; L/R rotated oppositely for symmetry",
       "reference_stereo_horizontal_angle_deg":60,
       "reported_stand_height":"not modeled; platform and acoustic axis heights are different constraints",
       "scenarios":scenarios,
       "warnings":[
         "The measured 60cm is HEAD above desk; exact ear canal height is missing; using head as listener reference is conditional.",
         "Left/right reflection from real monitors, multichannel stereo image phase and woofer directivity omitted.",
         "No side escape past 42-54in screens assumed; future monitor widths from 16:9 diagonal only, top heights hypothetical.",
         "No acoustic diffraction/reflections from desk/screens nor room response; center-ray blocked != zero audible sound.",
         "Whole faceplate clearance uses conservative angular envelope with an additional 2cm setup margin.",
         "Speaker-depth 0.25m may be IN FRONT of screens; stand cantilever, overhang, viewing occlusion, mounting safety NOT qualified.",
         "A 60° horizontal stereo angle is not an equilateral three-dimensional triangle when sources are elevated.",
         "Do not claim that 15° tilt is hard law; vendor recommendations pertain primarily to traditional reference monitors.",
         "No actual mounted test speakers, 10-12in sub or hardware sync implemented."
       ]
    }


if __name__=="__main__":
    print(json.dumps(scenario_report(),ensure_ascii=False,indent=2))
