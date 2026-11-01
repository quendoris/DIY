# D2-MOUNT-01 — Zero-Depth Over-Monitor Speakers and 50kgf / 100kgf Support Qualification

Date 2026-11-01. Status **USER REQUIREMENTS FROZEN; STAND STRUCTURAL DESIGN AND ACCEPTANCE NOT CERTIFIED**.

This is the successor to [D2-STEREO-01](D2-STEREO-01-MULTIMONITOR-REAL-HEIGHTS.md) and [D2-OVERHEAD-01](D2-OVERHEAD-01-MONITOR-MOUNTING.md). Future final three-way+sub acoustic architecture: 2 satellites (LF/MID/HF) with seven independent analog amplifier/DAC outputs including independent sub, open hardware/software. The OWNER now explicitly selects **monitor-plane / ZERO nominal front-back offset** as the leading installation, horizontal satellite front with all three drivers nominally beside each other, strongly anchored to the table using a recessed/embedded bolt approach. Future large THREE-screen scalability is a non-negotiable requirement. Cosmetic shell LAST.

## Binding measured user constraints and new mechanical requirement

- Head reference height +**60cm** over tabletop (do not silently claim it equals the ear-canal reference).
- Current primary 32in monitor TOP +**70cm**, placed on/in relation to a +10cm shelf; 27in side screen TOP +**60cm**.
- No side-space provision; future center 42–54in and two large sides. Future monitor TOP HEIGHTS and depth are unknown.
- **Ideal target: satellite front/acoustic plane directly ABOVE and IN PLANE with monitors**, not behind them, not a front-side desk cabinet. This is a research hypothesis to validate with exact front geometry.
- Owner estimates satellite weight **~10kg** and explicitly demands at least **50kg equivalent WORKING capacity** and **100kg equivalent STRESS/PROOF load** for hinges/attachments. Both are targets for each entire load-bearing chain, not certification claims.
- Table anchoring owner preference: **recessed/embedded bolt**. We must identify whether this means a blind threaded insert, countersunk THROUGH-bolt with backing plate, or an actual attachment to load-bearing desk frame: these have very different pullout and bending properties.

## Why '50kg / 100kg' is incomplete until we specify the applied MOMENT

Mass-equivalent kgf is a force, not a measured allowable force, not a `kg` mass rating and not a hinge moment `N m`. At standard g=9.80665m/s²:
- normal 10kg speaker: **98.0665 N** gravity force;
- owner minimum WORKING-LIMIT load-equivalent 50kgf: **490.3325 N**;
- owner minimum STRESS/PROOF load-equivalent 100kgf: **980.665 N**.

Simple conservative pure gravity moment `M=F*e`, with lever arm e = horizontal offset of the ACTUAL assembled center of mass from each pivot. These e values are **sample scenarios**, not measured center of mass:

| Horizontal gravity CoM offset e | Normal 10kg Nm | 50kgf target Nm | 100kgf proof target Nm |
|---:|---:|---:|---:|
| 0.15m | 14.71 | 73.55 | 147.10 |
| 0.20m | 19.61 | 98.07 | 196.13 |
| 0.30m | 29.42 | 147.10 | 294.20 |
| 0.40m | 39.23 | 196.13 | 392.27 |

These are gravitational moments about a single pivot assumed perpendicular to lever; real orientation changes the effective arm. The TILT HINGE (near CoM if properly designed) and DESK BASE (possibly far from CoM) must be evaluated separately. With an effective two-row anchor spacing of e.g. 80mm, a 100kgf hypothetical force applied with a 300mm offset demands an **ideal force couple** `M/h = 294.2/.08 = 3677.5 N`. This is NOT a verified fastener force: actual group tension, compression, shear, preload, prying, eccentric distribution, desk substrate creep and dynamic shock need separate structural computation.

**Safety evidence rule: A component labeled "100kg" without a qualified working LOAD LIMIT at a known MOMENT and orientation is not a qualified bracket.** Applying a 100kgf central load to a joint with a zero moment arm proves almost nothing about a 30cm cantilever. Similarly 100kgf proof of a bracket does not establish desk anchor or cabinet hardpoint strength, and must not be confused with rated destructive ultimate strength. Even a 50kgf manufacturer WLL and an undamaged 100kgf proof event may be insufficient for specific *over-person* safety requirements. Applied standards, permanent suspension and dynamically loaded support must be reviewed with qualified specialists for the actual installation.

Independent manufacturer examples:
- Q-SYS loudspeaker rigging guidance calls out moment/rigging integrity, shock multipliers and support uncertainty: https://support.qsys.com/awareness/pl-la-series-rigging-guide
- Yamaha's rigging guide emphasizes qualified support, inspection, avoiding shock and independent secondary steel: https://data.yamaha.com/zh/download/files/2101975
- d&b safety manual specifies separately designed independent primary/secondary suspension and warns against excessive drop/swing: https://www.dbaudio.com/assets/products/downloads/manuals-documentation/cl-series/dbaudio-rigging-manual-ccli-1.1-en.pdf

## Preliminary load-path architecture — **requirements**, not a DIY-built-rated stand

**Main load path**: loudspeaker HARDPOINTS in its actual frame ↔ mechanically captured yoke / two-sided clevis ↔ discrete yaw/pitch joints with positive locking ↔ stiff upright column/torsion bracket ↔ engineered desk attachment / support frame ↔ desk structure and floor.

- **Driver attachment:** no load should go through the loudspeaker basket, removable front baffle edge, decorative shell, sealant, or 3D printed cover. Tie into a separately engineered frame and quantified threaded/hole fasteners.
- **Hinge/yoke:** prefer a captured two-sided fork with a load-bearing shaft/pin in double shear, wide bearing span, mechanical stops, PLUS a positive mechanical angle lock (toothed engagement, locked crosspin, or independently qualified equivalent). Friction-only tilt lock or a single set-screw is not an acceptable primary restraint over people. Place pivot near actual all-up CoM where feasible to reduce steady tilt torque, then worst-case positions still need independent checks.
- **Column:** resist combined bending, torsion, vibratory acceleration and accidental impact. Internal routing MUST NOT compromise strength. Adjustable height/tilt must be locked and repeatable; final fixed deployment might replace temporary adjustable components.
- **Table attachment:** a blind insert into unspecified laminated particle board is NOT assumed capable of resisting the anchor tension couple and long-term creep. A **recessed/countersunk through-bolt group with broad upper/lower engineered backing plates** or direct attachment to a separately load-verified metal support frame are candidate architectures. Both require tabletop/frame material, thickness, hole spacing, edge distance and load testing. A single bolt by itself does not give safe anti-rotation, redundancy or load distribution.
- **Secondary catch:** independent rated steel retention to an independently reliable structural path, with short slack and restrained swing if the primary joint fails. A wire tied to the same failing tiny insert/plate is NOT independent. Keep it out of the normal acoustic load path.
- **Qualification:** pre-power CAD/FEA and hand calculations with actual frame and support properties, instrumented static worst-offset proof exercises ONLY in a secured remote test fixture, repeated adjustment/lock/thermal/vibration checks and post-assembly inspection. NEVER hang 100kg of weight above the desk or a human to 'see what happens'. Actual overhead installation requires appropriate competent structural review and local regulatory compliance.

No numeric bolt diameter/thread, backing plate thickness, table drill pattern, pipe wall thickness or hinge material is certified or recommended without desk and cabinet materials, tolerances, real loads and professional evaluation.

## Zero depth must mean a SURFACE condition, not only an axis condition

The owner's intended acoustic arrangement is sound. Nonetheless:
- With two inward-aimed baffles and a horizontal LF/MID/HF array, their **nominal axes** may have `z_speaker=z_monitor`, while individual cone faces and corners extend several centimeters ahead/behind that plane because each speaker has nonzero width and yaw.
- A down-pitched rigid front and its actual DEPTH/VOLUME, bracket and ventilation may intersect the monitor even if a zero-thickness circular driver face initially appears above it.
- At same depth as monitor front plane, one section of a baffle still may be *behind* the display; then a low-head viewing/listening ray from this rearward section can cross the monitor top even if panel silhouette is above the top edge.
- Our primary **zero-depth packaging gate** is the minimum y of all nominal transformed baffle corners and nominal full flange boundaries above the screen TOP with an initial, arbitrary **20mm engineering/visualization margin**. That is not sufficient for final solid-body collision, mount clearance, cooling/monitor airflow or acoustic image. We separately test all 6 driver rays against future hypothetical screen boxes in 27 listener positions.
- Exact future screen geometry is unknown. The model uses present measured 70cm top and a *speculative* future 80cm top; do NOT promote 80cm to a user measurement.

### First actual simulation, axial speaker depth aligned to notional monitor plane 35cm from listener (35cm itself NOT MEASURED)

Two Wavecor vertical source arrays rotated **90 degrees** to be horizontal, with a true physical 60-degree stereo triangle and each satellite aimed at reference head +60cm:

| Axis height above desk | Hypothetical screen TOP +70cm: full-flange rays clear /27 | Hypothetical screen TOP +80cm: full-flange rays clear /27 |
|---|---:|---:|
| 82cm | 9 | 0 |
| 85cm | 15 | 0 |
| 90cm | 24 | 0 |
| 92.5cm | **27** | 0 |
| 100cm | **27** | 15 |

The **42mm front-face screen-top gap** calculated at 92.5cm axis / 80cm screen scenario does NOT guarantee direct acoustic unobstruction (still 0/27 whole-aperture criterion): some yawed faceplate centers are behind the nominal monitor plane. This is a strong reason to optimize the COMPLETE BOUNDARY geometry and the actual front-to-back placement instead of assuming `zero center depth` proves no blockage. Moving the nominal axis far in front of the monitor is not the user's intent; improving front-surface alignment, safe slight set-forward or frame/taper depth can be explored if strictly necessary, otherwise move height only as much as genuinely required.

These scores use assumed 54/42/42in 16:9 panels and their hypothetical lateral locations, identical test top heights, 2cm extra projected faceplate margin, limited 27 head positions. No actual real user desk/screen acoustic attenuation, hearing localization or structural safety is demonstrated.

Reproducible Python model [threeway_coplanar_mount_mechanics.py](simulation/threeway_coplanar_mount_mechanics.py) and [adversarial demand tests](simulation/test_threeway_coplanar_mount_mechanics.py); workflow [coplanar mount mechanics](../../.github/workflows/threeway-coplanar-mount-mechanics.yml).

## Layer gates (not design theater)

1. **Owner requirements recorded: DONE.** 10kg estimated mass, 50kgf WLL target, 100kgf proof target, load-rated hinges, recessed anchor preference, speaker faces co-located in monitor depth, above triple-monitor screen.
2. **Simple gravity force, torque, anchor-couple math: DONE AND TESTED.** These are demands not capacity certificates.
3. **Zero-depth front-plane clearance and 27-ear synthetic screen tests: DONE AND TESTED.** They show counterexamples even when speaker central axis and monitor plane coincide.
4. **Measured desk substrate, thickness and support frame: OPEN**; exact threaded-insert vs through-bolt architecture OPEN.
5. **Actual final satellite all-up mass/CoM and rigid frame: OPEN**; estimate 10kg may grow with housing, electronics, safety steel and future driver changes.
6. **Stand material/sections, long-term vibration/strain, locked hinge design, 50kgf WLL/100kgf proof testing, redundant retention, professional over-person review: OPEN**.
7. **Real 3-monitor positions and full solid-body CAD geometry: OPEN**, screen reflection and 3-way directional phase still not measured.
8. **Validated installation and final aesthetic enclosure:** NOT YET APPROVED.

## Commands

```bash
cd projects/diy-speakers/simulation
python3 -m unittest -v test_threeway_coplanar_mount_mechanics.py
python3 threeway_coplanar_mount_mechanics.py > threeway-coplanar-demand-model.json
```

The first successful GitHub Actions source-model run: https://github.com/quendoris/DIY/actions/runs/41328266363

**No mechanical part, anchor, tabletop, power supply or suspended speaker was physically tested. No safe attachment claim is made.**
