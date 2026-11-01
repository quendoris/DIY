# D2-WAVE-02 — Realistic Uncertainty Boundaries: Directivity, Baffle Edges, Desktop

Date: 2026-11-01. Status: **SOURCED FIRST-ORDER PHYSICAL HYPOTHESES, NOT A MEASURED FINITE-BAFFLE WAVE SOLUTION**.

Owner architectural authority: [ADR-001](ADR-001-ACTIVE-THREE-WAY-SUB.md), two active LF/MID/HF satellites plus separate SUB, seven independent DAC output/amp channels, distributed optical timing. The eventual futuristic enclosure is designed **around qualified driver placement LAST**; temporary plywood fixtures only. [ADR-003](ADR-003-RESEARCH-HARDWARE-QUALIFICATION.md) keeps the imperfect STM32 research board separate from final production PCB qualification; waiting for STM has no bearing on acoustic research.

This experiment continues [D2-GEO-01](D2-GEO-01-WAVECOR-BAFFLE.md) and [manufacturer 4,800 real numerical data points](D2-REAL-01-WAVECOR-PHASE.md). Original factory FRD measurements are **independently captured, infinite-baffle on-axis responses**, not co-phased off-axis data on either plywood baffle.

## Credible external physical references

- Canonical infinite-baffle rigid circular piston **farfield** angular response: `D(theta)=2*J1(k*a*sin(theta))/(k*a*sin(theta))` (see Beranek & Mellow reference and derived model summary at https://docs.jmrp.io/phonometry/devices/electroacoustics/loudspeakers/). This is an ideal aperture, not a real complex membrane or finite baffle. Low/mid effective radii are derived from manufacturer **Sd = 131/50cm²**; tweeter uses nominal **30mm** diameter as an assumption.
- Bews & Hawksford, *Application of the Geometric Theory of Diffraction (GTD) to Diffraction at the Edges of Loudspeaker Baffles*, **Journal of the AES 34(10), 771–779 (1986)**, https://aes.org/publications/elibrary/elibrary-page/?id=5245 . Their published analysis shows uneven source-to-edge distances may smooth edge diffraction effects; an edge-distance **proxy does NOT implement their physics** or predict the SPL.
- Filevski, *Optimum Placement for Small Desktop/PC Loudspeakers*, **AES 125th Convention, paper 7606 (2008)**, https://aes.org/publications/elibrary/elibrary-page/?id=14757 : even an ideal loudspeaker's direct and desk-reflected sound can combine to form a frequency-dependent comb; physical positioning matters.
- Current VituixCAD 3.0 diffraction tool documentation, https://kimmosaunisto.net/Software/VituixCAD/VituixCAD_help_30.html : it employs **72 edge rays** (5° steps), shortest first-order paths, frequency-dependent scattering weights and actual listener geometry. A useful *independent next simulator* to compare with our scripts; manufacturer drawings/measurements still require real validation. Do not equate our four projected edge paths with its diffraction response.

## Three separate physical layers and exact limitations

**1. Infinite-baffle piston** [threeway_wave_desk_model.py](simulation/threeway_wave_desk_model.py):
- computes Bessel jinc `2J1(x)/x` with a tested power series, not an arbitrary angular constant;
- builds an ideal 3-way LR4 with LF **upper-split allpass phase bridge**, calibrates coherent direct sound at 0.7m, and rechecks ±10cm vertical, ±8cm horizontal, 0.6/0.7/0.8m distance;
- assumes low/mid/HF diaphragms have **uniform piston velocity**, ideal acoustic response, and simple propagation `1/r`;
- explicitly **cannot** predict real cone breakup, Wavecor off-axis FRD, finite panel edge scattering or full multi-driver nearfield radiation.

**2. Baffle edge distance and delays** from true provisional flat-panel geometry:
- low/mid/high nearest left/right/top/bottom faceplate-to-edge paths, four paths per head;
- lists extra `source→edge→listener` path length and relative time for each; an edge is not a secondary source with specified amplitude in this model;
- does **not** evaluate scattering coefficients, physical diffraction amplitude, baffle step, baffle thickness/rounding or power response. You CANNOT convert these delay candidates into dB notches without a legitimate diffraction model or measurement.

**3. Desktop first reflection**:
- each channel emits direct and a single virtual-image-source copy reflected by a **hypothetical infinite hard horizontal table**;
- tests **positive pressure reflection coefficient Γ=0,0.3,0.6** with no frequency dependence and unknown material/lateral extent;
- tests specular reflection allowed if the projected ray reaches a table with forward reach from the speaker of infinite, 20cm, 30cm or 45cm;
- this binary geometrical "ray exists" condition for finite desks is intentionally only a visibility **heuristic**, NOT a finite-table acoustic solution. Even when this filter disables the specular ray, actual edge scattering may persist.
- [threeway_desk_array.py](simulation/threeway_desk_array.py) superposes direct and specular-image source **complex pressures** through the allpass-corrected three-way filter at a fixed reference listening position; per-driver electronics/phase are assumed perfectly calibrated in the DIRECT path, but reflected sound remains, as in reality.

## Geometry: two research panels with equal positioning of critical MID/HF

| Provisional baffle | Dimensions | Panel bottom above table for assumed ears 350mm above table | LOW center above table | MID center | HIGH center |
|---|---|---:|---:|---:|---:|
| **A vertical** | **205×440mm** | **39.5mm** | **142.5mm** | 291.5mm | 408.5mm |
| **F/G mirrored LOW side** | **330×290mm** | **189.0mm** | **291.5mm** | 291.5mm | 408.5mm |

This 350mm ear-height hypothesis is **not a measured user desk**. If ear height is 250mm, the large vertical panel cannot be entirely above tabletop with its MID/HF midpoint at the ear height, while the side one can; that is not a reason to discard the vertical panel until real desk furniture and stand geometry are known. Physical source heights use **front-panel centre coordinates** only; true acoustical centres differ in depth and perhaps height.

The wide panel is **not** mechanically shorter above the desk if it must stand 189mm above the tabletop; their top edges align near 480mm. It gives greater width and a higher LOW center, and might open creative shaping possibilities, but cannot be called more compact in every dimension.

## Results from GitHub CI

Run: https://github.com/quendoris/DIY/actions/runs/41322456911 ; advanced coupled model: https://github.com/quendoris/DIY/actions/runs/41322713877 . Generated raw report JSON is available as workflow artifacts.

**Head-window deviation** at same-distance centre reference, 585 virtual positions/frequencies, ideal LF/MID/HF sources:

| Layout | 95th percentile abs, monopoles | 95th percentile abs, ideal circular pistons |
|---|---:|---:|
| A vertical | 0.9790dB | **1.0211dB** |
| F side LOW (G mirrored equal in symmetric grid) | 0.9769dB | **1.0188dB** |
| E wide vertical gaps | 1.5525dB | 1.5895dB |

Thus the model does NOT meaningfully discriminate A vs F/G. In contrast, large vertical gaps worsened the reference-window indicator in both idealizations.

**Desktop geometrical first halfcycle path differences** at 0.7m depth / ears 0.35m above desk:

| Driver and layout | Extra image-path length | Ideal halfcycle frequency |
|---|---:|---:|
| LOW, narrow vertical | 125.79mm | **1363.4Hz** |
| LOW, side/raised | 247.05mm | **694.2Hz** |
| MID (both layouts) | 247.05mm | **694.2Hz** |
| HIGH (both layouts) | 329.7mm | **520.2Hz** |

**DO NOT PRESENT THE HALFCYCLE FREQUENCIES AS ACTUAL MEASURED NOTCHES.** They are geometry-driven interference scales for a specular image ray, before finite table width, real frequency-dependent reflection coefficient, driver directivity, filters and other source interference. HF first halfcycle at 520Hz, for example, is far below intended HF operation; higher odd halfcycle frequencies are relevant but require complete frequency/angle response.

Full **three-band combined** conditional example with **Γ=0.6** and infinite / 45cm+ accessible desk, relative to direct-only 3-way output calibrated at centre:

| Hz | A vertical change | F/G side-LOW change |
|---:|---:|---:|
| 350 | +2.389dB | +0.810dB |
| 450 | +0.924dB | −0.907dB |
| 700 | **−4.119dB** | **−5.082dB** |
| 1000 | +0.004dB | +0.186dB |
| 2000 | −1.786dB | −1.794dB |
| 2500 | −0.844dB | −0.848dB |
| 3000 | +2.168dB | +2.168dB |

These results come from **perfect coherent ideal-driver DSP + single image ray, not Wavecor real angular responses or actual assembly**. Their large changes reveal a risk, not the true magnitude for the owner's desk.

**A stronger negative check:** if the hypothetical tabletop reflecting part ended **20cm forward of the speaker**, all specular ray reflection points in these particular 35cm/70cm reference examples lie beyond that point, so the **binary visibility model** disables the contribution entirely. Real finite tabletop still diffracts and scatters. This illustrates WHY actual speaker placement and desk dimensions must be recorded before believing "predicted -5dB notch".

### Key warning: this model is not finite baffle diffraction

Although we found source-edge travel distances, **we have NOT solved the finite-baffle wave equation**. The source-backed AES study and VituixCAD method use diffraction-coefficient/edge-ray physics absent from this implementation. Our first-order piston model assumes an **infinite** baffle, therefore calling the output "diffraction-corrected three-way speaker" would be false.

These transparent limitations are **a feature of the evidence-grade architecture**, not a flaw to hide.

## Engineering conclusions, without overclaiming

1. Keep **two** real fixture layout classes A and mirrored F/G, as with D2-GEO-01. Both share tightly grouped MID/HF, helpful for short-range vertical acoustic coherence.
2. For the **first** cheap, removable laboratory panel, prefer **A 205×440 vertical** only as an easy desk-width-saving construction choice; do **not** freeze final enclosure. Side-F/G remains equally valuable and physically plausible if headphone/monitor desk clearance demands.
3. Stop assuming that precision digital clocks and per-driver DAC outputs remove **acoustic reflection and geometrical time differences**. The model deliberately presumes ideal direct calibration, yet desk comb effects remain.
4. Next reproduce REAL edge diffraction / baffle step for the two panel outlines using an **independent validated simulation tool** (e.g. VituixCAD's integrated ray simulator) and benchmark our geometry/FRD assumptions rather than pretending edge delays alone give SPL.
5. Measure desktop positions: top surface dimensions, distance from front edge to speaker, ear height above table, 0.6–0.8m horizontal speaker-ear distance, monitor occlusions and allowable stands. These are genuinely required before an installed acoustic layout can be selected.
6. Before any finished cabinet: rig baffles with interchangeable driver positions and **isolated MID test chamber**, measure simultaneous-clock complex `.frd`/impulse response, vertical/horizontal angles and real 0.6–0.8m listener window. Compare each at same acoustic level and record desk elevated/off-desk/desktop with fixture IDs; gate time-window effects against room reflections.
7. Room and desk measurements should include impulse ETC, frequency response, off-axis and differences with controlled stand adjustments. Short indoor time-gating won't resolve low frequencies well, particularly when desk reflection arrives within the first millisecond; merge near/far-field methods only with careful reference and calibration.

## Reproducibility

```bash
cd projects/diy-speakers/simulation
python3 -m unittest -v test_threeway_baffle_geometry.py test_threeway_wave_desk_model.py test_threeway_desk_array.py
python3 threeway_baffle_geometry.py > d2-geometry.json
python3 threeway_wave_desk_model.py > d2-directivity-desk.json
python3 threeway_desk_array.py > d2-3way-desk-superposition.json
```

CI workflow: [threeway-geometry-study.yml](../../.github/workflows/threeway-geometry-study.yml) includes all tests and retains model JSON artifacts. Geometry source and OpenSCAD remain [D2-GEO-01](D2-GEO-01-WAVECOR-BAFFLE.md).

**Proof state:** factory dimensions — `PUBLISHED`; geometry pack — `MODEL_TESTED`; piston/Bessel and specular images — `ANALYTIC_ASSUMPTION_AND_TESTS`; finite baffle acoustic radiation — `NOT_SOLVED`; manufacturer angle-specific FRD — `NOT_AVAILABLE_IN_THIS_DATASET`; full tri-way/room desk SPL or THD — `NOT_MEASURED`; production architecture/baffle freeze — `OPEN`.

The test firmware/STM optical track is unaffected; it may continue independently when hardware arrives.
