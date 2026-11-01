#!/usr/bin/env python3
"""D2: parametric crossover & timing sensitivity using REAL manufacturer FRD.

WARNING: independent Wavecor measurements are NOT calibrated in a common
acoustic/temporal reference. All composite plots and rankings remain
CONDITIONAL on those assumptions. No final crossover selection.
"""
from __future__ import annotations
import argparse
import cmath
import json
import math
from pathlib import Path

from threeway_acoustic_geometry import lr4_pair
from wavecor_threeway_realdata import SOURCES, fetch, parse_wavecor

BASELINE_DB=86.0
ANCHORS={"LOW":180.,"MID":1100.,"HIGH":6000.}
KEY_FREQS=(300.,400.,450.,500.,600.,1000.,2000.,2500.,3000.,4000.,7000.,9000.)


def trims_for(curves):
    return {name:10**((BASELINE_DB-curves[name].at(f)[0])/20) for name,f in ANCHORS.items()}


def responses_for(curves, fc1: float, fc2: float, 
                  low_delay_us: float=0., mid_delay_us: float=0., high_delay_us: float=0.,
                  freqs=KEY_FREQS) -> list[tuple[float, float]]:
    if not 200 <= fc1 < fc2 <= 5000:
        raise ValueError("invalid crossover hypothesis")
    factors=trims_for(curves)
    delays={"LOW":low_delay_us,"MID":mid_delay_us,"HIGH":high_delay_us}
    out=[]
    for f in freqs:
        lo,hi=lr4_pair(f,fc1)
        l2,h2=lr4_pair(f,fc2)
        filters={"LOW":lo,"MID":hi*l2,"HIGH":hi*h2}
        amplitudes=[
          curves[n].complex_at(f)*factors[n]*filters[n]*
             cmath.exp(-2j*math.pi*f*delays[n]*1e-6)
          for n in ("LOW","MID","HIGH")
        ]
        combined=abs(sum(amplitudes))
        out.append((f,20*math.log10(combined) if combined>1e-12 else -240.))
    return out


def flattening_metric(rows):
    """RMS error to 86dB *of hypothetical summed response*; not true quality."""
    if not rows:
        raise ValueError("empty curve")
    errors=[v-BASELINE_DB for _,v in rows]
    return math.sqrt(sum(x*x for x in errors)/len(errors))


def physical_path_increment_us(head_z_m, source_z_m,
                                listener_distance_m=.7, sound_speed_m_s=343.):
    if listener_distance_m<=0 or sound_speed_m_s<=0:
        raise ValueError("invalid geometry")
    source_path=math.hypot(listener_distance_m,head_z_m-source_z_m)
    reference=math.hypot(listener_distance_m,-source_z_m)
    mid_path=math.hypot(listener_distance_m,head_z_m)
    mid_reference=listener_distance_m
    return 1e6*(source_path-reference-mid_path+mid_reference)/sound_speed_m_s


def investigate(curves) -> dict:
    baseline=responses_for(curves,450,2500)
    sample_points=[(250,350),(350,500),(400,2000),(400,2500),
                   (450,2000),(450,2500),(450,3000),
                   (500,2500),(600,3000),(700,3500)]
    sweep=[]
    for fc1,fc2 in sample_points:
        if not fc1 < fc2: continue
        rows=responses_for(curves,fc1,fc2)
        sweep.append({"lower_hz":fc1,"upper_hz":fc2,
                      "rms_deviation_from_86db_hypothesis":round(flattening_metric(rows),3),
                      "sample_response_db_at_450hz":round(dict(rows)[450.],3),
                      "sample_response_db_at_2500hz":round(dict(rows)[2500.],3)})
    delay=[]
    for d in (-100.,-50.,-25.,0.,25.,50.,100.):
        a=responses_for(curves,450,2500,low_delay_us=d)
        b=responses_for(curves,450,2500,high_delay_us=d)
        delay.append({
            "relative_delay_us":d,
            "LF_delayed_response_at_450hz_db":round(dict(a)[450.],3),
            "HF_delayed_response_at_2500hz_db":round(dict(b)[2500.],3),
            "LF_delayed_hypothetical_rms":round(flattening_metric(a),3),
            "HF_delayed_hypothetical_rms":round(flattening_metric(b),3),
        })
    head=[]
    for distance in (.6,.7,.8):
        for head_shift in (-.1,-.05,0.,.05,.1):
            lf=physical_path_increment_us(head_shift,-.15,distance)
            hf=physical_path_increment_us(head_shift,+.115,distance)
            pred=responses_for(curves,450,2500,low_delay_us=lf,high_delay_us=hf)
            head.append({
               "listener_distance_m":distance,"vertical_head_offset_m":head_shift,
               "assumed_woofer_to_mid_centers_m":.15,
               "assumed_mid_to_tweeter_centers_m":.115,
               "relative_LF_acoustic_path_change_us":round(lf,3),
               "relative_HF_acoustic_path_change_us":round(hf,3),
               "nominal_phase_scenario_f450_db":round(dict(pred)[450.],3),
               "nominal_phase_scenario_f2500_db":round(dict(pred)[2500.],3),
            })
    return {
      "model":"real_magnitude_and_per_driver_phase + ideal cascaded LR4 with hypothetical common phase origin",
      "measured_system":False,
      "phase_origins_cross_driver_verified":False,
      "finite_baffle_or_on_axis_acoustic_centers_measured":False,
      "valid_for_component_selection":False,
      "reference_lf_mid_hz":450,
      "reference_mid_hf_hz":2500,
      "amplitude_reference_db":BASELINE_DB,
      "manufacturer_data_not_republished":True,
      "baseline_frequency_response_db":{str(f):round(v,3) for f,v in baseline},
      "crossover_hypothetical_ranking":sorted(sweep,key=lambda v:v["rms_deviation_from_86db_hypothesis"]),
      "relative_channel_delay_sensitivity":delay,
      "geometry_only_head_motion_scenarios":head,
      "known_limitations":[
         "Not a three-way real speaker measurement or proof of optimal crossover.",
         "Manufacturer responses from independently measured drivers without demonstrated common time origin.",
         "Ideal LR4 electrical transfer; real enclosure, baffle diffraction, directivity, amplifier, DSP and EQ excluded.",
         "Driver locations .15m and .115m separations are illustrative; no verified installation geometry.",
         "Source/speaker response calibration, individual gain trim and acoustic delay remain to be measured.",
         "Choosing minimum RMS in conditional simulations is not an optimization certificate.",
      ],
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--offline-dir",type=Path)
    p.add_argument("--out",type=Path)
    args=p.parse_args()
    curves={}
    for name,source in SOURCES.items():
        if args.offline_dir:
            text=(args.offline_dir/f"{name}_spl.txt").read_text(encoding="utf8-sig")
        else:
            text,_,_=fetch(source["spl"])
        curves[name]=parse_wavecor(text,"spl")
    report=investigate(curves)
    content=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(content,encoding="utf8")
    print(content)

if __name__=="__main__":
    main()
