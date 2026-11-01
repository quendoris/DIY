# D2-STEREO-01 — Measured Height Reset: Horizontal 3-Way Pair Above MULTIPLE Monitors

Date: 2026-11-01. Status: **owner measurements applied, 3D geometric stereo analysis verified, real placement still OPEN**.

This records user-supplied facts and separates them from geometric simulations. The final premium DIY system remains **two fully active LF/MID/HF three-way satellites plus independent 10–12-inch subwoofer**, seven independent analog DAC/amp outputs, open-source hardware/software. We must design the FINAL futuristic cabinet LAST, around the physically validated array. Experimental STM32 board works in a separate research track and does not block the acoustic cabinet/stereo work.

## Newly measured facts (supersede all former hypothetical ear=35cm placements)

**Owner's direct readings, above the existing desktop:**
- **+60cm:** head height above tabletop (**head**, not explicitly center of ear canal; do not silently reinterpret as ear reference).
- **+10cm:** shelf above desk, underneath/along the main monitor mounting geometry.
- **+70cm:** TOP edge of existing **32-inch** central monitor above desk (user describes +10cm shelf and +60cm display assembly above it). This is a measured physical *top*, not nominal pixel screen height.
- **+60cm:** top edge of existing **27-inch** side monitor above desk. Side is occupied; no safe free lateral speaker footprint.
- **FUTURE REQUIREMENT:** scalable to **three large monitors**, central potentially 42–54-inch and additional substantial left/right monitors. Their frame widths, exact tops, offsets and distances are **NOT YET MEASURED**. Never freeze 32/27-era positions as final.
- Proposed arrangement: **two horizontal 3-way satellites above the monitor array** on strongly fixed desk-anchored stands, tilted downward and aimed at the head; possible 45° diagonal; future shell follows acoustic placement. Desire externalized, surrounding stereo image not inside-head headphone presentation.

**Don't repeat legacy ear=35cm as a user measurement.** It was only a hypothetical used in D2-OVERHEAD-01.

## Stereo geometry rather than a single centered speaker

[threeway_stereo_multimonitor.py](simulation/threeway_stereo_multimonitor.py) models a **LEFT/RIGHT pair** of the original real-dimensioned Wavecor 3-way reference geometry, roll at 0/45/90° per side and correctly applies **independent yaw plus downward pitch** to point each acoustic reference toward a central listener.

Nominal example:
- speaker front-centre horizontal depth from listener, **70cm** (still a scenario, not a user measured horizontal distance);
- symmetric left/right coordinates **x=±40.4cm** with respect to central head, yielding **±30° plan-view stereo angle / 60° included**, near a conventional listening triangle;
- when acoustic reference is **92cm above desk** and head reference 60cm, vertical gap 32cm; each satellite's axis aims down about **21.6°**, and FULL 3D included stereo angle drops to **~55.4°**, even though the plan view remains 60°;
- **the real distance from each elevated satellite to the ear is longer than 70cm**, since it includes lateral x and vertical height; a plan-view equilateral triangle does NOT automatically prove a 3D equilateral speaker-ear triangle;
- when monitors move closer to listener, the stereo pair must be re-aimed in yaw. The simulation also varies speaker depth 70/60/55/40/25cm and acoustic axis height 80/88/92/96/100cm.

Published vertical driver reference flanges retained from factory source drawings: LF Ø168mm, MID Ø120mm, HF Ø104mm. For horizontal three-way rotation, LF/MID/HF run along the front panel roughly across its width. Left/right roll sign is mirrored so two speakers can be symmetric about listener. This is a physical test fixture geometry, NOT a production-approved baffle cutout, diffraction response, actual individual acoustic centers, DAC delays or production enclosure design.

## Three-screen obstacle scenarios: measured vs unknown

Current example:
- center 32-inch screen top **+70cm MEASURED** and a side 27-inch top **+60cm MEASURED**; widths are estimated from **16:9 aspect ratio**, not actual physical bezel measurements.
- Hypothetical screen distances from listener **35cm / 40cm**, side screen assumed right, x positions guessed solely for research; 27in may physically be on another side.

Future example:
- **54-inch CENTER**, **42-inch sides**, three monitor geometry to stress the owner's scalability intent. Approximate **1.196m / 0.930m nominal 16:9 visible widths**, not measured frame widths.
- Top edges **+80cm** (center) and **+73cm** (sides) are chosen test assumptions, NOT facts about intended purchases. These can easily be wrong; a 54-inch display's visible height is ~67cm at 16:9 and mount position determines its actual top.
- L/R/S monitor placements and depths are illustrative; not claimed to be the actual desk.

**Critical condition:** every screen is tested against six separate driver rays (LOW/MID/HIGH × L/R) at **27 head positions** (3x lateral offsets, 3x vertical offsets, 3x forward distances). Then each ray is widened by a conservative projected outer circular faceplate radius plus **2cm clearance**. This is a source-to-ear **geometric visibility** test, not audible attenuation by an actual monitor or the final rigid cabinet silhouette.

## Reproducible results: horizontal roll=90° and stereo ±30° plan

All quantities model-only; microphones, actual screens, cabinet build, support and stereo psychoacoustics untested.

**Acoustic axis 92cm, head reference 60cm, L/R 70cm plan depth (x±40.4cm):**
- downward tilt **21.60°**, real stereo 3D included angle **55.41°**;
- existing 32/27 monitor scenario: all six central rays clear **21/27** head locations, and all six full nominal faceplates conservatively clear **9/27**;
- future 54/42/42 with ASSUMED +80/+73cm top heights: all six central rays clear **3/27**, all full faceplates clear **0/27**.

**Acoustic axis 100cm, head reference 60cm, same 70cm depth:**
- down tilt **26.33°**, real stereo 3D angle **53.25°**;
- existing scenario: all six center rays **24/27**, full faceplates **15/27**;
- future hypothetical three-screen scene: all six center rays **9/27**, full faceplates **0/27**.

**Move acoustic plane to 40cm from user (x±23.1cm to preserve 60° plan stereo) and raise to +100cm:**
- down tilt **40.89°** (considerably larger than the owner's stated aim of gentle tilt), true 3D included stereo angle ~44.42°;
- existing: all full faceplates clear **27/27**, future: **12/27**.
- Thus **just moving the speaker near monitor plane without accounting for tilt/stereo changes is not a free fix**.

**Place speaker front ahead of every monitor plane (e.g. in the model at 10cm from head reference):** direct sound rays cannot be blocked by monitors behind the speaker; this is mathematically obvious but **mechanically a poor/unverified placement**: speaker might strike the user, obstruct video, create dangerous desk cantilever and alter stereo imaging. Not a recommendation. A feasible intermediate front-of-screen arm is still open and requires actual desk geometry.

**Counterexample:** In the first naive 80cm source-centre case, at a 60cm head and monitor plane halfway to source, the center ray reaches ~70cm at screen plane and strikes the measured top edge of the 32-inch monitor. It certainly cannot clear an entire Ø168mm woofer faceplate with a protective margin. The intuitive statement "monitor top 70cm, speaker centre 80cm, therefore clear" is false.

These numbers emphasize the problem with selecting solely based on center acoustical axis or one stationary head point.

## The external speaker literature and its valid scope

- [Genelec studio monitor placement](https://www.genelec.com/monitor-placement) recommends symmetric aiming at the listener, near ±30° horizontal stereo angle and generally no more than 15° down tilt in conventional 2-channel critical monitoring. This is **reference guidance, not a ban on a custom tilted system**.
- [Genelec small-monitor orientation answer](https://support.genelec.com/hc/en-us/articles/360013435879-Small-studio-monitors-are-often-placed-either-horizontally-or-vertically-on-the-mixing-console-meter-bridge-Which-orientation-is-better) explains why horizontal MID/HF spacing may cause phase cancellation when the listener moves sideways. It also confirms co-axial 3-way designs can be placed horizontally with fewer such issues. The owner's dedicated MID+HF reference Wavecor are NOT coaxial and therefore require angular/phase testing in horizontal form.
- [Neumann loudspeaker arrangement FAQ](https://www.neumann.com/globalassets/digizuite/15354-en-monitors-faq-acoustical-and-application-answers_en.pdf) likewise recommends stereo ±30° and per-channel aim/delay calibration, not arbitrary desk-placement symmetry.

Horizontal placement can avoid many screens, but it's **not automatically acoustically superior to a vertical three-way** absent real MID/HF directivity, desk/monitor diffraction, ceiling reflection, stereo externalization, time/phase calibration, and listening tests. No amount of separate DACs physically eliminates non-coincident wavefronts and room reflections. Accurate sources outside the head can produce externalized sound, but that subjective goal must be tested, not promised from diagrams.

## Installation and production boundary

A heavy 3-way column fixed on a stand at head height / above a desk is a load-bearing engineering problem. A 40–50cm **stand platform** does not necessarily equal acoustic-axis height; a horizontal baffle ~205mm tall will not magically raise its source center by another 40cm. Any platform-to-driver rise must come from a load-rated bracket/crossbar, with:
- measured total unit mass (woofer 2kg class plus isolated chamber/amps/structure), center of gravity and stand lever arms;
- static overturning/dynamic vibration under worst tilt and lever arm; credible attachment to a proven desktop/substructure, not an unqualified thin laminate edge;
- mechanical stops and independent fall retention/tether; isolated wiring path, no clamp collision with screens, no screen cooling blockage;
- physical audit after fixture assembly and genuine accelerometer/impulse/acoustic and thermal measurements.

The full Wavecor 3-way+sub architecture and final enclosure-last strategy remain unchanged.

## What to build before final cabinet

1. Continue **horizontal roll=90° over-monitor** as a priority hypothesis; **45° and vertical** remain falsifying controls. Do not order a permanent stand without actual monitor/desk geometry.
2. Put current real values +60/+70/+60 and future three-screen stress scenarios in a versioned CSV/JSON contract. The latest geometry model does this; measured and assumed fields are separate.
3. Once physically possible, collect exact **ear canal height**, screen top y and lateral x edges, monitor plane depth relative to ear, likely future screen top height, speaker-plane safe depth, allowable bracket base on desktop. No need for all dimensions immediately to keep modeling.
4. Optimize a **Pareto frontier** instead of one audio score: stereo included horizontal angle, vertical aim, 27/27 conservative aperture clearance, available mounting positions, room ceiling/desk reflections, MID/HF spatial lobing and repeatable mechanical safety.
5. Keep a **coaxial MID/HF three-way** as a future alternative investigation *if* horizontal separation proves destructive under actual measured soundfield. Coaxial still preserves three true frequency bands; it isn't a two-way fallback.
6. Only after acoustic and safety fit tests: design the future futuristic cabinet to satisfy the placement envelope, electronics/power/thermal and sealed MID chamber.

## Reproducible links

- [Stereo+multi-monitor model](simulation/threeway_stereo_multimonitor.py), with hard-coded user measurements distinctly labelled.
- [Source-vs-assumption and stereo geometry tests](simulation/test_threeway_stereo_multimonitor.py).
- [Stereo 3-screen OpenSCAD visualization](simulation/threeway_stereo_multimonitor_scene.scad), change `scenario`, `speaker_roll_deg`, `source_axis_height`, `speaker_depth`. Stand-only preview disabled.
- [CI test + 150-scenario JSON artifact](https://github.com/quendoris/DIY/actions/runs/41326336519), with same reference files, no inferred real acoustics.

**Claim grades:** +60/+70/+60 heights = OWNER_MEASURED; 10cm shelf = OWNER_STATED; future 42–54-inch = OWNER_TARGET; nominal 16:9 widths = DERIVED_ONLY; monitor x and depth/future tops = HYPOTHETICAL; driver geometry = MANUFACTURER_DRAWINGS; 3D source visibility and no-obstruction fractions = MODEL_ONLY; soundfield/thermal/mechanical safety/psychoacoustics = NOT_YET_MEASURED.
