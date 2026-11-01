# D2-OVERHEAD-01 — Elevated Three-Way Stands, Downward Aim, 0° / 45° / 90° Driver Arrays

2026-11-01 · **RESEARCH OPTION ADDED TO ACTIVE 3-WAY SYSTEM DESIGN**. This new study is about how loudspeaker placement relative to **multiple displays and the desk** can dominate small baffle-only geometry refinements. It **does not freeze final cabinet or purchase**. Owner-proposed stand-mounted speakers 40–50cm above table and 20–30cm above the head, aimed downward; layout is free to be vertical, horizontal or diagonal. We study these alternatives before designing a future visual enclosure.

## Crucial clarification of geometry (not a question; two test cases)

The project previously assumed ear height **35cm above desk** solely as a hypothetical. Owner's new proposal says both speaker **stand level 40–50cm above desk** and speaker **20–30cm above the head**. These values are not necessarily consistent if interpreted as *speaker acoustic axis* versus *ear height*, because head-top/ear height and stand-platform/head/axis locations differ. In particular, a 45cm acoustic-axis height with ear height 35cm produces only **+10cm**. A stand **platform** at 45cm could support a panel whose acoustic axis is **65cm** high, depending on shape and bracket. We therefore test:
- A: acoustic-axis 45cm / ear height 20cm => delta +25cm, 70cm forward, aim down **19.65°**;
- B: acoustic-axis 50cm / ear height 35cm => delta +15cm, aim **12.09°**;
- C: acoustic-axis 65cm / ear height 35cm => delta +30cm, aim **23.20°**; this could correspond to a 45cm *platform with a 20cm axis offset*, but bracket clearance/structural safety is not yet validated.

At horizontal listener ranges **60–80cm** the tilt for a source +20cm above ears is **14.0–18.4°**; +25cm is **17.4–22.6°**; +30cm is **20.6–26.6°**. For conventional stereo monitors, **Genelec recommends keeping down/up tilt to ≤15°** if possible, aimed at the listening position; high placements beyond that aren't forbidden but are a change in reproduction geometry and should be tested for vertical sound-image perception, ceiling/room interaction and listening zone. Source: https://www.genelec.com/monitor-placement and https://www.genelec.com/en/studio-monitor-calibration .

## Manufacturers confirm screens and desks matter

- Genelec official positioning guidance recommends stands behind mixing surfaces high enough to avoid direct obstruction, with speaker acoustical axes aimed at ears. https://support.genelec.com/hc/en-us/articles/360013435879-Small-studio-monitors-are-often-placed-either-horizontally-or-vertically-on-the-mixing-console-meter-bridge-Which-orientation-is-better
- Genelec cautions that **horizontal MID/HF separation moves interference lobes into side-to-side head motion**; conventional two-way monitor guidance recommends vertical placement, especially at the crossover. This is relevant to our three-way MID↔HF pair but not a universal proof against horizontal mounting. https://www.genelec.com/en/studio-monitor-calibration
- Elevated positions can also create stronger ceiling reflections, new panel reflections and altered vertical localization. This is not universally better independent of room geometry.

## Actual 3D rigid-body implementation

[threeway_overhead_geometry.py](simulation/threeway_overhead_geometry.py) converts the prior real driver geometries (Wavecor WF168WA06 Ø168, MR120BD02 Ø120, TW030WA22 Ø104) into a **real 3D coordinate system**:
- source acoustic reference at `(x=0, height=H, depth=.7m)`, reference ear at `(0, h_ear, 0)`; downward pitching follows `atan((H-h_ear)/.7)` exactly;
- whole-baffle **roll** around the acoustic axis at **0°,45°,90°** (i.e. vertical to diagonal to horizontal driver-center alignment), plus already supported vertical and side-LOW initial layouts;
- 3D source-to-ear travel times and pressure summing with our corrected LR4 450/2500Hz phase bridge; theoretical circular piston farfield direction factors are only a model, not measured Wavecor angular phase;
- head moves ±8cm sideways, ±10cm vertically, 60/70/80cm axial distance; test frequencies 350–4000Hz. Calibrates **each** direct acoustic path at the **one** reference ear, not after every head move;
- model rectangle computer screen at 35cm in front of the speaker/listener coordinate origin, 60cm wide, with **three hypothetical top heights 35/45/55cm** from tabletop; direct source→ear rays tested independently for LOW/MID/HIGH;
- a **conservative projected flange bound** checks whether the whole 168/120/104mm faceplate is guaranteed to be outside the screen silhouette (sufficient, not necessary condition). The actual three-dimensional baffle/cabinet, monitor array and diffraction remain unknown.
- an ideal rigid infinite desk image-source reflection function exists, but the primary reported **head-window score excludes screen obstruction and reflections** to avoid inflating the importance of a toy ray-blockage model.

We are NOT solving finite edge diffraction, screen scattering, acoustic reflections from monitor faces or real 3-way off-axis FRD. Ears, screen geometry and stand installation heights are deliberately hypothetical. **Monitor ray interception is not total audible blockage**, particularly for long wavelengths.

## First 18 configuration CI results

All below are **analytical output only**, not built-speaker measurements. The detailed machine-readable JSON artifact is attached to the [3D CI run](https://github.com/quendoris/DIY/actions/runs/41324088770).

### The monitor obstruction result is the surprise

Hypothesis C: acoustic axis **65cm** above desk, ears **35cm**, monitor rectangle top **45cm**, 60cm width, located halfway along direct path between ear and speaker:

| Wavecor A layout rotated around acoustic axis | Downward pitch | LOW/MID/HIGH direct centre-ray occlusion | Conservative complete flange clearance from monitor | Model head-window p95 |
|---|---:|---|---|---:|
| **0° vertical** | 23.20° | **LOW BLOCKED** / MID,HIGH clear | LOW and MID not certified clear | **1.0436 dB** |
| **45° diagonal** | 23.20° | **LOW BLOCKED** / MID,HIGH clear | LOW and MID not certified clear | **0.9510 dB** |
| **90° horizontal** | 23.20° | **all three centre rays clear** | **all three nominal faceplates conservatively clear** | **0.8768 dB** |

This is a **geometry-based counterexample** to the claim that "vertical always clears screens better", not a universal acoustic ranking. The screen can change (a 55cm tall model blocks all three driver center rays even in the horizontal placement).

Hypothesis B: axis 50cm, ear 35cm, screen top 45cm. **All three driver center rays are geometrically obstructed for the 90° horizontal candidate**, despite its smaller modeled head-window p95 **0.816dB** (vertical **1.0503dB**). This proves that optimizing a free-field head-window score can prefer a physically hidden layout if we do not separately gate screen visibility.

Hypothesis A: axis 45cm, ears 20cm, screen top 35cm. Horizontal and diagonal center rays remain obstructed; merely aiming the baffle downward **does not bypass the monitor**.

**Faceplate projected clearance** is more stringent than testing only the line to each source's center. A line through the clear half of a screen's vertical gap is insufficient if the driver's outer ring or acoustic aperture remains substantially behind it.

### Why the physically elevated horizontal result is not yet an acoustic win

The p95 values are produced by *ideal piston/point source + simulated filters and phase*, with an intentionally symmetric single-speaker head-motion grid and no:
- real measured angular SPL **phase** and breakup of the Wavecor MID/HIGH;
- finite baffle diffraction or the screen's actual boundary acoustic scattering;
- two separate stereo speakers with different x locations and yaw/toe-in;
- real desk depth, high-ceiling/boundary reflections, monitor stands or speaker cabinets;
- actual human horizontal localization/soundstage preferences;
- support vibration/tilt creep, electro-mechanical limits, safe mechanical bracket and fall hazards.

The diagonal **45°** test is a real research candidate, not merely decorative. Our model's 45° p95 (~0.951dB in hypothesis C) hides a worse maximum over some sampled head positions (~2.505dB vs 1.2785dB for horizontal); record both p95 AND worst-case rather than cherry-pick one metric.

### Stand and overhead safety

The owner has not selected actual speaker weights or final shape; heavy multi-kilogram baffles above people's heads **must not be supported by an unverified desk clamp, 3D-printed joint or arm**. Before a real physical elevated prototype:
- structural support base, fastening to wall/desk/independent floor stand and potential overturning are designed from actual mass/centre of gravity, applied tilt angle and lever arm;
- locked pitch/roll joints, proof load appropriate to installation, anti-fall independent tether/retainer and strain-relieved cables;
- vibration isolation without compromising mechanical fixation, angular repeatability and clearance to arms/ventilation;
- assess whether a table-mounted stand transmits vibration to monitors and microphone;
- avoid electrical/optical tether snag paths above the user's head and avoid compromising monitor ventilation.

No physical stand load rating or installation approval is claimed by these scripts. [OpenSCAD overhead scene](simulation/threeway_overhead_scene.scad) has `show_placeholder_stand=false` by default, for good reason. This is a **viewing model, NOT certified mounting hardware**.

## Consequence for next 'crystal' layer

We now need a **three-dimensional stereo installation contract**, not just an isolated flat baffle model:
1. Record *real* desk and monitor widths/heights, top edges and depth from ears; speaker-arm mounting limitations, ear height, target distance, head movement range and available free space above screens.
2. Stereo L/R speaker positions and yaw/toe-in are important. A single virtual screen centered at x=0 can overestimate obstruction if the real speakers sit outside the monitor edges, or underestimate it with several screens. Model actual monitor rectangles and both channel source rays.
3. Keep **0°,45°,90°** as distinct test configurations and repeat with a realistic finite baffle diffraction model, actual same-clock off-axis phase on interchangeable panel and controlled elevated/desk measurements.
4. Test true acoustic direct-to-reflected ratio, listening-window spatial response, horizontal stereo image stability, IMD/THD vs acoustic SPL, and stand resonance.
5. Freeze installation *geometry* only after measured qualified candidate, then design the future enclosure around it. A legitimate **over-monitor horizontal three-way** may indeed outperform a desk-placement design **in this setup**. The current ideal model cannot yet prove it.

## Reproducible implementation

- [threeway_overhead_geometry.py](simulation/threeway_overhead_geometry.py) — 3D rigid rotation, true centre coordinates, conservative screen ray-blocking, sample-phase/piston model and single desk image ray.
- [test_threeway_overhead_geometry.py](simulation/test_threeway_overhead_geometry.py) — 15 tests of pitch, 3D rotation, geometric clearance, zero-reflection model, phase reference, test uncertainty and correct OpenSCAD setup.
- [threeway_overhead_scene.scad](simulation/threeway_overhead_scene.scad) — adjustable 3D scene containing experimental baffle, driver envelopes, down-tilt, sample screen, table and reference rays. Param `roll_deg=0,45,90`. OpenSCAD is a preview, NOT finished CAD or safe stand mount.
- [threeway-overhead-study.yml](../../.github/workflows/threeway-overhead-study.yml) — runs the study on GitHub-hosted CI and retains complete JSON; [actual successful first run](https://github.com/quendoris/DIY/actions/runs/41324088770).

```bash
cd projects/diy-speakers/simulation
python3 -m unittest -v test_threeway_overhead_geometry.py
python3 threeway_overhead_geometry.py > d2-overhead-scene-hypotheses.json
```

**Evidence status:** driver flange dimensions `MANUFACTURER_PUBLISHED`; 3D rigid rotation & center ray/sphere-envelope `GEOMETRY_MODEL_VALIDATED`; reflection + ideal piston head-window `ANALYTICAL_ONLY`; actual multi-monitor geometry `MISSING`; acoustic winner `NOT_IDENTIFIED`; stand structural safety `NOT_EVALUATED`.
