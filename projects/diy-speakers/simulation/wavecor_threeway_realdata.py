#!/usr/bin/env python3
"""Wavecor 3-way D2 analysis using downloaded ORIGINAL numeric measurement files.

No 3-way real speaker has yet been measured. Manufacturer infinite-baffle
acoustic measurements have potentially unrelated phase time zeros and
different driver positions. Model predictions are explicitly hypothetical.
No false phase=0 substitutions, extrapolation or DSP performance claims.
No third-party data are embedded/redistributed into this repository.
"""
from __future__ import annotations

import argparse
import bisect
import cmath
import hashlib
import json
import math
from pathlib import Path
from urllib.request import Request, urlopen

from threeway_acoustic_geometry import lr4_pair

BASE="https://www.wavecor.com/Driver%20measurements%20TXT"
SOURCES={
    "LOW": {
      "model":"WF168WA06","page":"https://www.wavecor.com/html/wf168wa05_06.html",
      "spl": BASE+"/SPL%20response/WF168WA06_FR.txt",
      "impedance":BASE+"/Impedance%20response/WF168WA06_IMP.txt",
    },
    "MID": {
      "model":"MR120BD02/04","page":"https://www.wavecor.com/html/mr120bd01_02_03_04.html",
      "spl":BASE+"/SPL%20response/MR120BD02_04-SPL-response.txt",
      "impedance":BASE+"/Impedance%20response/MR120BD02_04-impedance-response.txt",
    },
    "HIGH": {
      "model":"TW030WA22","page":"https://www.wavecor.com/html/tw030wa21_22.html",
      "spl":BASE+"/SPL%20response/TW030WA22_SPL_response.txt",
      "impedance":BASE+"/Impedance%20response/TW030WA22_impedance_response.txt",
    },
}
EXAMPLE_F=[100,250,400,500,1000,2000,2500,3000,5000,10000]

class Curve:
    def __init__(self, kind: str, rows: list[tuple[float,float,float]]):
        if kind not in ("spl","impedance") or len(rows)<3:
            raise ValueError("invalid curve kind or point count")
        if any(not all(math.isfinite(x) for x in row) or
               row[0]<=0 or (kind=="impedance" and row[1]<=0)
               for row in rows):
            raise ValueError("nonphysical or nonfinite curve values")
        if any(a[0]>=b[0] for a,b in zip(rows,rows[1:])):
            raise ValueError("frequency samples must strictly increase")
        self.kind=kind
        self.rows=rows
        self.freqs=[row[0] for row in rows]
        phase_unwrapped=[math.radians(rows[0][2])]
        for i in range(1,len(rows)):
            phase_new=math.radians(rows[i][2])
            delta=math.atan2(math.sin(phase_new-phase_unwrapped[-1]),
                             math.cos(phase_new-phase_unwrapped[-1]))
            phase_unwrapped.append(phase_unwrapped[-1]+delta)
        self.phase=phase_unwrapped

    def at(self,f: float) -> tuple[float,float]:
        """Log-frequency linear interpolation, unwrapped phase (radians)."""
        if not self.freqs[0]<=f<=self.freqs[-1]:
            raise ValueError(f"frequency {f} outside measured [{self.freqs[0]}, {self.freqs[-1]}]")
        if f==self.freqs[-1]:
            return self.rows[-1][1],self.phase[-1]
        i=max(0,bisect.bisect_right(self.freqs,f)-1)
        if f==self.freqs[i]:
            return self.rows[i][1],self.phase[i]
        a,b=self.rows[i][0],self.rows[i+1][0]
        t=(math.log(f)-math.log(a))/(math.log(b)-math.log(a))
        val=self.rows[i][1]+t*(self.rows[i+1][1]-self.rows[i][1])
        phase=self.phase[i]+t*(self.phase[i+1]-self.phase[i])
        return val,phase

    def complex_at(self,f:float) -> complex:
        val,phase=self.at(f)
        if self.kind=="spl":
            amp=10**(val/20)
        else:
            amp=val
        return cmath.rect(amp,phase)


def parse_wavecor(text: str, kind: str) -> Curve:
    rows=[]
    for n,raw in enumerate(text.splitlines(),1):
        line=raw.strip()
        if not line or line.startswith(("#",";","*")):
            continue
        cols=line.replace(",",".").split()
        if cols and cols[0].lower() in ("freq","frequency"):
            if len(cols)!=3:
                raise ValueError(f"line {n}: manufacturer response header must include phase")
            if kind=="spl" and not ("db" in cols[1].lower() and "phase" in cols[2].lower()):
                raise ValueError("SPL header is not Freq dB Phase")
            if kind=="impedance" and not ("ohm" in cols[1].lower() and cols[2].lower() in ("deg","phase")):
                raise ValueError("IMP header not Freq Ohm Deg/Phase")
            continue
        if len(cols)!=3:
            raise ValueError(f"line {n}: expected exactly three columns")
        try:
            row=tuple(float(x) for x in cols)
        except ValueError as exc:
            raise ValueError(f"line {n}: invalid numeric row") from exc
        rows.append(row)
    return Curve(kind,rows)


def fetch(url: str) -> tuple[str,str,int]:
    if not url.startswith(BASE+"/") or not url.endswith(".txt"):
        raise ValueError("source URL not pinned to manufacturer TXT directory")
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (DIY Wavecor research data audit)"})
    with urlopen(req,timeout=25) as r:
        b=r.read(5_000_000)
        if len(b)>=5_000_000:
            raise ValueError("large/unexpected content")
    return b.decode("utf-8-sig",errors="strict"),hashlib.sha256(b).hexdigest(),len(b)


def make_report(
  curves: dict[str,dict[str,Curve]],
  source_meta:dict[str,dict[str,dict]],
  fc_low_mid:float=450,
  fc_mid_high:float=2500,
) -> dict:
    if not 150<=fc_low_mid<fc_mid_high<=5000:
        raise ValueError("crossovers out of exploration range")
    reference_db=86.0
    anchors={"LOW":180.,"MID":1100.,"HIGH":6000.}
    trims={name:10**((reference_db-curves[name]["spl"].at(f)[0])/20)
           for name,f in anchors.items()}
    sample_f=[200,300,450,600,1000,1700,2500,3000,4000,7000,10000]
    responses=[]
    for f in sample_f:
        l1,h1=lr4_pair(f,fc_low_mid)
        l2,h2=lr4_pair(f,fc_mid_high)
        filters={"LOW":l1,"MID":h1*l2,"HIGH":h1*h2}
        raw={name:curves[name]["spl"].complex_at(f)*trims[name]*filters[name]
             for name in SOURCES}
        coherent=sum(raw.values())
        amplitude=sum(abs(v) for v in raw.values())
        responses.append({
          "freq_hz":f,
          "assumed_published_phase_combined_db":round(20*math.log10(abs(coherent)),3)
                if abs(coherent)>1e-15 else None,
          "max_constructive_phase_envelope_db":round(20*math.log10(amplitude),3),
          "per_band_mag_db":{name:round(20*math.log10(abs(v)),2)
                             if abs(v)>1e-15 else None for name,v in raw.items()},
        })
    per_driver={}
    for name,src in SOURCES.items():
        sl=curves[name]["spl"]
        imp=curves[name]["impedance"]
        per_driver[name]={
          "model":src["model"],
          "manufacturer_page":src["page"],
          "spl_txt":source_meta[name]["spl"],
          "impedance_txt":source_meta[name]["impedance"],
          "spl_samples":len(sl.rows),"imp_samples":len(imp.rows),
          "spl_range_hz":[sl.freqs[0],sl.freqs[-1]],
          "imp_range_hz":[imp.freqs[0],imp.freqs[-1]],
          "spl_ref_2v83_1m":{str(f):round(sl.at(f)[0],3)
                 for f in EXAMPLE_F if sl.freqs[0]<=f<=sl.freqs[-1]},
          "impedance_magnitude_ohms":{str(f):round(imp.at(f)[0],3)
                 for f in EXAMPLE_F if imp.freqs[0]<=f<=imp.freqs[-1]},
          "phase_column_present":True,
          "same_time_reference_as_other_drivers":False,
          "per_driver_voltage_trim_relative_to_2v83":round(trims[name],5),
        }
    return {
      "status":"MANUFACTURER_MEASURED_INFINITE_BAFFLE_INPUTS; INTEGRATED_SPEAKER_NOT_MEASURED",
      "candidate":"Wavecor WF168WA06 + MR120BD02/04 + TW030WA22",
      "fc_low_mid_hz":fc_low_mid,"fc_mid_high_hz":fc_mid_high,
      "electrical_filter":"ideal 4th-order Linkwitz-Riley cascaded, not an actual acoustic target",
      "normalization":"Each source scaled to 86dB magnitude at LF180/MID1100/HF6000Hz; relative voltage gains only.",
      "measured_three_way_phase_aligned":False,
      "measured_finite_baffle":False,
      "actual_dsp_validated":False,
      "raw_phase_simultaneous_sum_is_only_a_sensitivity_scenario":True,
      "drivers":per_driver,
      "illustrative_responses":responses,
      "warnings":[
        "Each driver was measured independently in manufacturer infinite baffle; phase time zero not validated across drivers.",
        "Summation of published phases is not valid prediction until common acoustic origin, baffle and timing are measured.",
        "SPL data smoothed 1/6 octave, free-air impedance from different measurement fixture; both are published samples.",
        "8-ohm nominal not equal measured minimum impedance; use actual impedance and amplifier loading envelope.",
        "Response samples and selected crossover frequencies exploratory, not proof of design or guaranteed flatness.",
        "No angular FRD, IMD, THD vs SPL or finite cabinet volume used in this computation.",
      ],
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--offline-dir",type=Path,
                        help="Optional local folder with files LOW_spl.txt LOW_impedance.txt etc.")
    parser.add_argument("--low-mid",type=float,default=450.)
    parser.add_argument("--mid-high",type=float,default=2500.)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    data={}
    provenance={}
    for name,src in SOURCES.items():
        data[name]={}
        provenance[name]={}
        for kind in ("spl","impedance"):
            if args.offline_dir:
                b=(args.offline_dir/f"{name}_{kind}.txt").read_bytes()
                raw=b.decode("utf8-sig")
                sha=hashlib.sha256(b).hexdigest()
                n=len(b)
            else:
                raw,sha,n=fetch(src[kind])
            curve=parse_wavecor(raw,kind)
            data[name][kind]=curve
            provenance[name][kind]={"url":src[kind],"sha256":sha,"size_bytes":n}
    report=make_report(data,provenance,args.low_mid,args.mid_high)
    content=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if args.out:
        args.out.write_text(content,encoding="utf8")
    print(content)


if __name__=="__main__":
    main()
