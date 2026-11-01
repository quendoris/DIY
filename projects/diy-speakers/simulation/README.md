# Near-field Stereo 2.1 Acoustic Research Bench

> **ARCHITECTURE — frozen by owner 2026-11-01:** two active three-way satellite boxes plus an independent sub = **7 DAC output + 7 amplifier channels**. Current authoritative decision [ADR-001](../ADR-001-ACTIVE-THREE-WAY-SUB.md); [architecture_3way_contract.json](architecture_3way_contract.json) and [test_architecture_3way_contract.py](test_architecture_3way_contract.py) assert the fixed topology, four planes, modular clock/power domains, openness and honest proof boundaries. Older two-way models remain useful purely as historical acoustic controls.

The first executable, dependency-free Python bench for the owner's **60–80 cm** desktop listening position and modular stereo 2.1 direction.

## Candidate comparison (new)

The [catalog](candidates.json) has 5 midwoofer, 3 tweeter and 5 subwoofer candidates with individual manufacturer source URLs and explicitly labeled sample enclosure volumes. [compare_candidates.py](compare_candidates.py) computes simple sealed-box Fc, Qtc, F3 and only derives Vd where the manufacturer supplies comparable one-way Xmax; [test_compare_candidates.py](test_compare_candidates.py) validates provenance, representative sealed results and unknown data handling. These are **not buying recommendations**.

Run:

```bash
python3 compare_candidates.py --format markdown
python3 compare_candidates.py --format json > candidate-comparison.json
python3 -m unittest -v
```

Narrative interpretation: [../CANDIDATE-COMPARISON.md](../CANDIDATE-COMPARISON.md). Development gates: [../ATOMIC-ROADMAP.md](../ATOMIC-ROADMAP.md).

## Usage

```bash
cd projects/diy-speakers/simulation
python3 -m unittest -v
python3 acoustic_baseline.py > baseline.json
python3 acoustic_baseline.py --fs 42 --qts .38 --vas 18 --volume 20 --crossover 80 > box20L.json
```

All units are explicit: Fs in Hz, Vas and net sealed-box volume in liters, crossover in Hz.

## Implemented mathematical baselines

**Sealed-box small-signal lumped model:**

- `Fc = Fs × sqrt(1 + Vas/Vb)`
- `Qtc = Qts × sqrt(1 + Vas/Vb)`
- normalized second-order high-pass pressure transfer, and numerical -3 dB crossing relative to its high-frequency unity asymptote.

**Sub/satellite electrical split:** ideal fourth-order Linkwitz-Riley, formed by two cascaded Butterworth second-order filters for each branch. Each idealized branch is -6.0206 dB at the crossover; their phase-aligned electrical sum has constant unity magnitude across frequencies. This is **not** an acoustic guarantee after real speaker rolloffs, propagation/delay, EQ, baffle effects or room reflections.

Example Fs=42 Hz, Qts=0.38, Vas=18 L and Vb=12 L is **purely fictional** for a demonstration—not a measured driver, shopping recommendation or final satellite box.

## What this model deliberately does not establish

- No actual driver, cabinet geometry, bass-reflex port, passive radiator, DAC, amp or volume has been selected.
- No SPL, thermal compression, frequency-dependent coil resistance, Xmax, SPL/THD at 25–30 Hz, port velocity or excursion.
- No real driver frequency response, impedance curve, polar/directivity data, baffle/diffraction, tweeter/midwoofer offsets or desk reflections.
- No room response, stereo geometry or effect of a nearby wall.
- No fact about T5V/T8V can be inferred from the demonstration box parameters.

These are separate next stages. Only after importing manufacturer-measured T/S, FRD/ZMA and box constraints should enclosure results be compared as potential builds.

## Reference benchmark

The owner's heard reference is ADAM Audio **T5V**, and the desired comparative benchmark is **T8V**:

- T5V manufacturer: 298 × 179 × 297 mm; 5-inch LF; 45 Hz at -6 dB; crossover 3 kHz.
- T8V manufacturer: 400 × 250 × 335 mm; 8-inch LF; 33 Hz at -6 dB; crossover 2.6 kHz.

Sources:
- https://www.adam-audio.com/en/t-series/t5v/
- https://www.adam-audio.com/en/t-series/t8v/

Our proposed 2.1 system distributes deep bass to the independent sub, rather than matching the 8-inch T8V's cabinet size on the crowded desk. Similar or stronger bass requires future defined SPL/distortion and integration tests, not these nominal specifications alone.


## D0: inverse sealed box sizing

[design_sweep.py](design_sweep.py) calculates a hypothetical net sealed volume for a selected target Qtc using manufacturer Fs/Qts/Vas from [candidates.json](candidates.json). Example `python3 design_sweep.py --qtc .707`; independent math checks in [test_design_sweep.py](test_design_sweep.py). At Qtc=.707 the comparison yields SB15MFC30-8 ~6.68 L and F3 ~74.5 Hz, SB17NRX2C35-8 ~14.73 L and ~61.4 Hz, HiVi M6N-B ~9.58 L and ~83.4 Hz. This **is not a fully modeled final cabinet**, nor a midrange-quality ranking; final integration requires measured crossover/directivity, listening geometry, nonlinear output limits and sub coupling. See [../DESIGN-KICKOFF-D0.md](../DESIGN-KICKOFF-D0.md).


## Three Chinese midwoofer offers — source-separated model

The owner supplied descriptions and unit prices for **HiVi F6N, D6G, M6N**. [hivi_offers_2026-11-01.json](hivi_offers_2026-11-01.json) preserves seller parameters, third-party data and significant F6N disagreement as distinct scenarios. [hivi_offer_sweep.py](hivi_offer_sweep.py) compares a purely **hypothetical 8L sealed-box** test fixture and the inverse Qtc=1/sqrt(2) relation; [test_hivi_offer_sweep.py](test_hivi_offer_sweep.py) asserts scenarios aren't silently merged and prices aren't misinterpreted as per pair. Run `python3 hivi_offer_sweep.py` or `python3 -m unittest -v`. See the [full engineering review](../HIVI-F6N-D6G-M6N-REVIEW.md).


## Final-intent Chinese and international benchmark — 2026-11-01

[final_intent_longlist_2026-11.json](final_intent_longlist_2026-11.json) records the serious production-candidate longlist, including HiVi M6N/D6G, Wavecor WF152BD06/14, WF168WA02/06, SB17NBAC 4/8ohm, Scan-Speak 18W, SEAS and PURIFI. Russian seller prices from indexed listings are stored as **observed** prices rather than confirmed payable quotes; incompatible source revisions and absent data remain explicit. The [test_final_intent_longlist.py](test_final_intent_longlist.py) audit asserts provenance, unit currency, corrected nominal 2.83V vs 1W conversion, variant identity and documented uncertainty. No script claims measured THD or determines a brand winner. Full [competitive review](../FINAL-INTENT-MIDWOOFER-COMPETITION.md).


## Three-way satellite combinations + separate SUB

[threeway_system_candidates_2026-11.json](threeway_system_candidates_2026-11.json) contains independently-sourceable Chinese dedicated 4.75in midranges and dome tweeters, other control options, real Russian price observations for 10/12in subwoofer drivers, and explicit replacement warnings for discontinued models. [threeway_system_audit.py](threeway_system_audit.py) reproduces **7 vs 5 amplifier/DAC channel** counts, drivers-only RUB totals and nominal Vd=`Sd × Xmax` while leaving 25Hz SPL/THD unclaimed. [test_threeway_system_audit.py](test_threeway_system_audit.py) verifies the assumptions. Full review [../THREE-WAY-PLUS-SUB-RESEARCH.md](../THREE-WAY-PLUS-SUB-RESEARCH.md).


## Optical-first STM32 bench scripts (ADR-002)

- [optical_bench_contract.py](optical_bench_contract.py) calculates the **96/192kHz × 24/32 bit** seven-channel application bandwidth and per-endpoint share, Ethernet MTU block limits, optical line-rate examples, nominal silica fiber propagation and the statistical upper limit on packet failure if zero independent errors were observed.
- [test_optical_bench_contract.py](test_optical_bench_contract.py) independently exercises the arithmetic and preserves **NOT TESTED** physical status.
- [optical_host_probe.py](optical_host_probe.py) is a runnable, host-only UDP CRC/sequence/epoch echo tool supporting local actual network tests; **no STM32 implementation yet**. [test_optical_host_probe.py](test_optical_host_probe.py) verifies data patterns, corrupted frame rejection and actual localhost UDP echo.

Commands from this directory:

```bash
python3 -m unittest -v
python3 optical_bench_contract.py > optical_estimates.json
# terminal 1 (local-only test)
python3 optical_host_probe.py serve --bind 127.0.0.1 --port 50808 --limit 100
# terminal 2 (local-only test)
python3 optical_host_probe.py probe --host 127.0.0.1 --port 50808 --count 100 --size 1024
```

**Full STM32 → 1/2/5m fiber workflow:** [../OPTICAL-TEST-PROCEDURE.md](../OPTICAL-TEST-PROCEDURE.md). No genuine fiber/device tests have been run yet; this code only validates assumptions and host framing.



## Current acoustic integration task

Wavecor WF168WA06 (LF), MR120BD02 (dedicated MID), TW030WA22 (HF) are the current **8Ω three-way reference triad**; HiVi M6N/D6G remain final-design LF rivals. Independent SUB research continues. See [../D2-THREE-WAY-ACOUSTIC-INTEGRATION.md](../D2-THREE-WAY-ACOUSTIC-INTEGRATION.md) and the exact [manufacturer data availability manifest](threeway_acoustic_sources.json).

[threeway_acoustic_geometry.py](threeway_acoustic_geometry.py) computes **ideal complex LR4** crossover sensitivity to relative delay and **nearfield listener vertical movement**. The [tests](test_threeway_acoustic_geometry.py) show that equal-phase LR4 branches sum coherently in an idealized model but 100µs inter-driver delay mismatch at 2.5kHz creates ~3.01dB cancellation at crossover. A **3-column magnitude-and-phase FRD importer** rejects amplitude-only source files: manufacturer numeric response files **actually include individual phase**, but common time zero across three independent factory measurements and the finite baffle are not verified, so actual acoustic crossover summation is still unproven. All geometry lengths are illustrative, not measured driver mounting layouts.

The optical STM32 experiment is held as a parallel future physical experiment; [ADR-003](../ADR-003-RESEARCH-HARDWARE-QUALIFICATION.md) accepts imperfect, safe, documented research boards but requires full qualification of final custom PCBs.



## D2-REAL-01: original Wavecor phase and impedance (acquired)

Source-based results [full report](../D2-REAL-01-WAVECOR-PHASE.md); raw manufacturer files are retrieved live, not embedded in this repo, and **SHA-256 verified** against [threeway_acoustic_sources.json](threeway_acoustic_sources.json).

- [wavecor_probe.py](wavecor_probe.py) finds manufacturer page links without inventing filenames.
- [wavecor_threeway_realdata.py](wavecor_threeway_realdata.py) fetches **6×800** real manufacturer numeric triples (3 SPL + measured per-driver acoustic phase, 3 impedance + electrical phase), interpolates them, preserves source SHA and calculates a conditional filter transfer function; direct URL/phase mismatch => fail.
- [wavecor_phase_sensitivity.py](wavecor_phase_sensitivity.py) compares crossover hypotheses around **350–600 Hz / 2–3 kHz**, relative delays and vertical head displacement using measured single-driver curves under **explicit unknown cross-driver phase time zero**.
- A NEGATIVE test proves naïve concatenation of two LR4 branches can create nonflat THREE-way response even for perfect transducers. A LOW-channel **upper-split allpass phase bridge** makes the flat-driver ideal transfer a unit-magnitude allpass product. Code and tests do not claim actual production acoustic phase.

Execute in this folder:

```bash
python3 -m unittest -v
python3 wavecor_threeway_realdata.py --out wavecor-report.json
python3 wavecor_phase_sensitivity.py --out wavecor-phase-sweep.json
```

GitHub Action: [wavecor-primary-phase.yml](../../../.github/workflows/wavecor-primary-phase.yml). **Manufacturer FRD does not replace common-reference microphone measurements on a temporary baffle, angular data, driver THD or genuine DAC/amp synchrony.**


## D2-GEO-01: dimensioned baffle and head movement

[threeway_baffle_geometry.py](threeway_baffle_geometry.py) imports nominal factory dimensions **Ø168/120/104mm** (stored with official original PDF sources), checks center packing with 5mm rim clearance, computes board dimensions and head-window phase of three **ideal monopoles** using the already-tested phase-bridged LR4. It sweeps ±10cm vertically, ±8cm horizontally and 0.6–0.8m distance. [test_threeway_baffle_geometry.py](test_threeway_baffle_geometry.py) guards dimensional identity, geometric collisions, correct LR4 sum, limited calibration, mirror symmetry, and **OPENSCAD source consistency**. [threeway_baffle_reference.scad](threeway_baffle_reference.scad) previews vertical 205×440mm and mirrored low-profile 330×290mm experimental plywood panels (default cutouts disabled; NOT machining-ready).

[Full D2-GEO-01 analysis](../D2-GEO-01-WAVECOR-BAFFLE.md) and [CI model artifacts](https://github.com/quendoris/DIY/actions/workflows/threeway-geometry-study.yml). The conditional model cannot distinguish vertical and side layouts as physical winners without measured directional impulse responses and finite-baffle response.


## D2-WAVE-02 — ideal piston, edge paths and desktop risk

See the source-reviewed [physical study](../D2-WAVE-02-DIRECTIVITY-DESK-DIFFRACTION.md). [threeway_wave_desk_model.py](threeway_wave_desk_model.py) implements a validated Bessel jinc (`2J1(x)/x`) for theoretical rigid piston directivity, dimension-correct rectangular baffle edge lag catalogues and an illustrative specular infinite-hard-table image source at hypothetical reflection coefficients. The [adversarial tests](test_threeway_wave_desk_model.py) check shape, source height, geometric delays, reflection limits and preserve the **NOT_ACTUALLY_MEASURED** status.

[threeway_desk_array.py](threeway_desk_array.py) computes **full three-channel complex pressure** with the previous LR4 allpass-bridge and one specular image per radiator, plus optional **finite-table reflection-point visibility**. [test_threeway_desk_array.py](test_threeway_desk_array.py) asserts that Γ=0 recovers the original direct-only model exactly, rejects invalid physical geometry and shows that finite table extent can fundamentally alter the conditional prediction. This is **not a numerical finite-baffle wave solver** and not a measured user desk. The [CI geometry workflow](../../../.github/workflows/threeway-geometry-study.yml) archives all three source model JSON reports.


## D2-OVERHEAD-01 — elevated speaker and multi-monitor clearance hypothesis

[threeway_overhead_geometry.py](threeway_overhead_geometry.py) translates exact nominal Wavecor centre offsets into a 3D baffle, pitches its acoustic normal toward ears and rotates its driver array **0/45/90°** around that normal. The software checks whether LOW/MID/HIGH rays cross a hypothetical monitor rectangle and conservatively bounds projected full flange clearance; it also computes **ideal piston 3D head-window changes** at fixed direct-sound calibration. [15 targeted tests](test_threeway_overhead_geometry.py) audit rigid rotation, angles, center-ray and faceplate clearance, no-reflection baseline and empty certification claims. The reproducible 18-scenario JSON is retained by [threeway-overhead-study.yml](../../../.github/workflows/threeway-overhead-study.yml). [Editable three-dimensional OpenSCAD visualization](threeway_overhead_scene.scad) includes the screen, test panel, driver circles, ear, downward aim and ray lines, with unsafe unengineered 'stand' hidden. Full sourced report [D2-OVERHEAD-01](../D2-OVERHEAD-01-MONITOR-MOUNTING.md).

**Remaining:** real monitor dimensions (especially all screen tops and distances), ear height, stereo positions, support constraints and acoustic measurements. A ray being geometrically blocked is NOT equal to measured attenuated sound from a real screen, and free-field ideal-piston score must not be used to endorse horizontal MID/HF separation universally.
