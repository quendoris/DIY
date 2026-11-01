# D2-GEO-01 — Driver Placement BEFORE Cabinet Design

2026-11-01 · Decision: **two legitimate removable-fixture layouts preserved**; finished aesthetic cabinet still **LAST**.

## Owner constraint and what is/isn't frozen

The owner explicitly does **not** require a preselected vertical, diagonal or symmetrical arrangement. We should allow acoustics and driver requirements to determine the future enclosure shape, rather than force a predesigned shape onto driver positions.

Current system architecture from [ADR-001](ADR-001-ACTIVE-THREE-WAY-SUB.md): two individually active **LOW + dedicated MID + HIGH** satellites (3 DAC output/amp channels each) + independently powered 10–12-inch sub (one channel). Seven actual analogue channels; four digital-network planes. The optical STM32 test bench is parallel research, not a blocking prerequisite.

We used exactly three **real reference driver models** for the first geometry:
- LOW: Wavecor WF168WA06-01, 8Ω, 6.5-inch
- MID: Wavecor MR120BD02-01, 8Ω, 4.75-inch, **separate rear air chamber**
- HIGH: Wavecor TW030WA22-01, 8Ω, 30-mm dome

This does not disqualify HiVi M6N and D6G as final LF contenders. Their true mounting diameters, hole circles and behavior require their own source-backed geometry and FRD requalification.

## Primary source drawing dimensions, not estimated from driver names

All dimensions below are nominal **millimetres**, directly from factory PDF drawing pages. **Do not use a max rear chassis diameter as the approved machined cutout without measurements and tolerances**.

| Feature | WF168WA06 LOW | MR120BD02 MID (round) | TW030WA22 HIGH |
|---|---:|---:|---:|
| Outside circular faceplate/flange | **168** | **120** | **104** |
| Maximum rear assembly diameter | 143 | 98 | 80 |
| Mounting-bolt pitch-circle diameter | 159 | 110 | 92 |
| Stated nominal mounting depth | 73 | 64 | 30 |
| Position of four flange holes | cardinal | cardinal | diagonals |
| Future isolated cavity | separate satellite LF enclosure | **mandatory isolated sealed MID cavity** | factory-integrated rear system, confirm installed part |

Manufacturer PDFs (view and physically inspect their illustrations, not just scraped table):
- WF168WA05/06: https://www.wavecor.com/Driver%20specifications%20PDF/WF168WA05_06_specifications.pdf — Page 3
- MR120BD01/02/03/04: https://www.wavecor.com/Driver%20specifications%20PDF/MR120BD01_02_03_04_specifications.pdf — Page 4
- TW030WA21/22: https://www.wavecor.com/Driver%20specifications%20PDF/TW030WA21_22_specifications.pdf — Page 4

MID *truncated* flange is **MR120BD04**, not MR120BD02. Its 105mm trimmed-side width does not automatically make the round 120-mm part fit closer in a vertical arrangement. Swapping to that variant requires validating the separate physical footprint and same-SKU sourcing.

## Geometric minimum, before any acoustics

The sum of the two adjacent flange radii is a hard planar packing boundary:
- LOW+MID: 168/2 + 120/2 = **144mm** centre distance with tangent rims. With **5mm** planning gap: **149mm**.
- MID+HIGH: 120/2 + 104/2 = **112mm** tangent; with **5mm** planning gap: **117mm**.

This is faceplate non-overlap only, NOT proof of sufficient screwdriver access, mechanical stiffness, router tolerances, flange sealing, rear/magnet clearance or physically achievable acoustic centres. A 2mm rim-gap alternative is rejected by the current **5mm engineering fixture rule**.

## Two equal-priority candidate baffles (front view)

Coordinates are **[x,y] in mm from the lower-left corner of the flat plywood fixture**, NOT final speaker locations or driver acoustic centres.

### A — narrow, vertically stacked

**Panel: 205 × 440mm; 18mm plywood preview thickness.**

| Centre | X | Y |
|---|---:|---:|
| LOW | 102.5 | 103.0 |
| MID | 102.5 | 252.0 |
| HIGH | 102.5 | 369.0 |

Rim gaps LOW/MID and MID/HIGH both 5mm. A nominal ear-centre projection halfway between MID/HIGH is **[102.5,310.5]mm**, so the whole panel is not centered on the ear at the panel's geometric midpoint. The test stand would set this acoustic-reference line to actual ear height.

**Advantages:** width only ~205mm, helpful in front of multiple monitors; L/M/H all share horizontal axis; easiest initial test fixture. Disadvantage: ~440mm tall before any actual structural cabinet height, which may require shelf/stand/monitor clearance.

### F/G — low, wide, mirrored side-LOW

**Panel: 330 × 290mm.** Same 5mm rim gaps; preserve vertical MID/HIGH compactness and move LOW sideways where first crossover is much lower (nominal ~450Hz).

LEFT LOW:
- LOW=[102.5,102.5]
- MID=[251.5,102.5]
- HIGH=[251.5,219.5]
- nominal ear projection [251.5,161.0]

RIGHT LOW (mirror):
- LOW=[227.5,102.5]
- MID=[78.5,102.5]
- HIGH=[78.5,219.5]
- nominal ear projection [78.5,161.0]

**Advantages:** approximately 150mm shorter, allows mirrored futuristic low-profile designs. Disadvantages: ~125mm extra desk width, strong potential for different finite-baffle diffraction and left/right horizontal room interaction; requires measurement, not speculative superiority. Mirrored placement is geometric equivalence under ideal free-space assumptions only.

**Editable OpenSCAD**: [threeway_baffle_reference.scad](simulation/threeway_baffle_reference.scad). Set `layout_mode` to `"vertical"`, `"side_left"` or `"side_right"`. The drawing has colored flange envelopes and nominal screw-guide markers; **actual rear cutouts are disabled by default** and even if visualized they are NOT a CNC-ready template. Physical components must be checked before cutting.

## D2-GEO-01 ideal acoustic window

[threeway_baffle_geometry.py](simulation/threeway_baffle_geometry.py) checks the drawings, flange collisions and an intentionally idealized THREE-way acoustical model:

- all three drivers treated as **perfectly flat omnidirectional point monopoles**;
- electrical **LR4 450Hz + 2500Hz** with the already proven **upper-crossing allpass bridge on the LOW channel**;
- fixed per-driver amplitude/phase calibration at the reference ear [0,0,0.7m], but no magical recalibration when the head moves;
- spherical distance and 1/r pressure, 343m/s sound speed, phase `exp(-j2πfΔdistance/c)`;
- ear sweep: 0.6,0.7,0.8m; vertical -10/-5/0/+5/+10cm, horizontal -8/0/+8cm; 13 frequencies from 300 to 4000Hz;
- report is relative deviation in dB at each distance compared with a centered listener **at the same distance**, not measured loudness or human hearing quality.

All scores below are computed from **the above hypothetical model**, *not from measured Wavecor off-axis response*. 585 samples per viable geometry:

| Candidate | Flat-panel mm | 95th percentile absolute head-change | Worst head-change | RMS |
|---|---:|---:|---:|---:|
| **A: vertical, 5mm gaps** | 205×440 | **0.979dB** | **1.3404dB** | 0.4241dB |
| B: vertical, 15/20mm gap | 205×465 | 1.2046dB | 1.6373dB | 0.5136dB |
| C: HF shifted horizontally 40mm | 215×435 | 0.9736dB | 1.9113dB | 0.4352dB |
| D: 2mm rim gaps | — | **REJECTED by 5mm clearance rule** | — | — |
| E: large 35/40mm gaps | 205×505 | 1.5525dB | 2.1117dB | 0.6506dB |
| **F: LOW left of MID/HF** | 330×290 | **0.9769dB** | **1.3401dB** | 0.4169dB |
| **G: LOW right of MID/HF** | 330×290 | **0.9769dB** | **1.3401dB** | 0.4169dB |

The nominal difference **1.3404 vs 1.3401dB** in worst case is ~**0.0003dB**, utterly beneath confidence in this idealized model. **A, F and G are practically tied; no acoustic winner or optimal shell has been demonstrated.** F/G predict identical summary scores because the simulated head grid is left/right symmetric.

C offers a slightly smaller p95 but significantly worse worst-case response, so a 40mm horizontal tweeter offset has no present justification solely for acoustic quality.

**Important missing physics that may reverse the results:** Wavecor real angular patterns (cone/dome directivity and breakup), finite-baffle diffraction and frequency-dependent baffle-step (especially 205 vs 330mm), real acoustic-center depths and noncoincident timing references, speaker/room reflections, desk boundary interaction, MID enclosure loading, actual ear/monitor placement, thermal/nonlinear distortion and chosen sub integration.

Existing manufacturer **800-point FRD/phase curves are on-axis, separately measured in INFINITE BAFFLE**; they cannot supply real 3D directivity or phase reference for this geometry by themselves. See [D2-REAL-01](D2-REAL-01-WAVECOR-PHASE.md).

## Preferred practical research order, NOT a final product geometry freeze

1. Adopt **A narrow vertical** as the first interchangeable-baffle prototype if desk width matters. Build **F/G** if a shorter form is more useful or if we want a direct same-drivers geometric comparison.
2. Use only a simple plywood *measurement fixture*; don't freeze fancy enclosure materials, grille, waveguide, passive radiators or mechanical styling.
3. Confirm actual measured driver mounting cutouts, screw-head access and rear volumes. The MR120 MID must have its own airtight isolated test volume; manufacturer's harmonic-distortion measurements used **2 litres internal volume**, with no explicit published net/gross displacement convention. This is a **comparison fixture**, not final design spec. Record both gross chamber volume and corrected net air volume after driver displacement, internal bracing and damping.
4. On a common acoustic clock/measurement origin, obtain same-level **on-axis and off-axis complex FRD** (horizontal and vertical angles), genuine source time delay and decay including finite panel.
5. Test listening-window map at actual 60–80cm ±head positions with microphone at controlled heights and mic-distance corrections; record objective deviations and real phase/lobing. Use DSP delays to align one reference point and evaluate *other* points without reoptimization.
6. Re-run with HiVi M6N or D6G as final-intent LOW contenders, respecting their actual frames and mounting restrictions.
7. Only **after** actual head-window/THD/power/thermal qualification, shape a futuristic enclosure *around* the proven arrangement, then re-qualify cabinet effects.

## Reproducibility and limits

From `projects/diy-speakers/simulation`:

```bash
python3 -m unittest -v test_threeway_baffle_geometry.py
python3 threeway_baffle_geometry.py > threeway-baffle-model.json
```

GitHub workflow [threeway-geometry-study.yml](../../.github/workflows/threeway-geometry-study.yml) runs tests and retains the full generated JSON as an Actions artifact. The paper drawing dimensions and simulation code are open to scrutiny, while the actual vendor drawing PDF stays at the manufacturer's original link.

**Proof state:** dimensions **FACTORY_PUBLISHED**; non-overlap **GEOMETRY_TESTED**; acoustic head-window **IDEAL_POINT_SOURCE_MODEL_ONLY**; real finite-baffle response **NOT_TESTED**; actual 3-way speaker mechanical/safety qualification **NOT_TESTED**. Not a certification, not an optimality proof.

This project's "crystal growth" rule: don't claim a more accurate layer until source dimensions and model assumptions were independently checked; and re-test after every material/geometry change.
