# D2-REAL-01 — First REAL Wavecor Complex-Response Import and 3-Way DSP Study

Date: 2026-11-01. Status: MANUFACTURER INPUTS DOWNLOADED; REAL THREE-WAY LOUDSPEAKER NOT BUILT OR MEASURED.

This experiment develops the owner-selected active three-way stereo satellite plus separately powered subwoofer architecture. We will NOT treat two-way speakers as alternative project targets. The goal is a final-quality open, auditable three-way design.

## Primary source evidence — now actually fetched

GitHub Actions first real manufacturer source acquisition:
https://github.com/quendoris/DIY/actions/runs/41319037700

Independent verified components:
- Wavecor WF168WA06 8Ω low-frequency driver (L)
- Wavecor MR120BD02/04 8Ω dedicated midrange driver (M)
- Wavecor TW030WA22 8Ω high-frequency driver (H)

All SIX original text downloads succeeded. For EACH driver we received **800 samples** of frequency, measured SPL (dB), per-driver phase (degrees), and **800 independent impedance samples** with resistance magnitude and electrical phase. This is a total of **4,800 original numerical triples**.

The original manufacturer data are made available on:
- https://www.wavecor.com/html/wf168wa05_06.html
- https://www.wavecor.com/html/mr120bd01_02_03_04.html
- https://www.wavecor.com/html/tw030wa21_22.html

Original source URLs and **full SHA-256 fingerprints** for every file are in [source manifest](simulation/threeway_acoustic_sources.json). [wavecor_threeway_realdata.py](simulation/wavecor_threeway_realdata.py) downloads and parses them, validates strictly increasing frequency, rejects missing phase, records metadata, and now fails if any source file hash changes without review.

**Correction to previous assumption:** the numerical files DO contain phase. The missing piece is a **shared cross-driver acoustic zero/time origin**, because factory samples were measured separately in a flush-mounted INFINITE BAFFLE at 1m. They are NOT automatically synchronous measurements made on our three-way temporary baffle. Own consistent-reference measurements are still required before final crossover validation.

## What the original component measurements report

The manufacturer SPL at 2.83Vrms / 1m, interpolated at named test frequencies (dB):

| Frequency | LOW WF168WA06 | MID MR120BD02/04 | HIGH TW030WA22 |
|---|---:|---:|---:|
| 400 Hz | 87.739 | 85.721 | 80.601 |
| 1000 Hz | 86.983 | 85.225 | 94.060 |
| 2500 Hz | 89.153 | 88.235 | 92.540 |
| 5000 Hz | 88.409 | 89.829 | 91.525 |

These are independent *raw infinite-baffle driver curves* before an active low/mid/high crossover. For example, tweeter SPL at 1000Hz does NOT certify the TW030WA22 as safe to cross at 1kHz; the manufacturer recommends operation above about 2kHz. Similarly a woofer's output at 5kHz is not a reason to use it there.

## Critical negative result: naive TWO-STAGE LR4 cascade is NOT a flat three-way

Two individually flat-summing 4th-order Linkwitz–Riley filter pairs cannot be combined naïvely in series to obtain a flat sum of THREE branches, because MID+HF inherits upper-crossover allpass phase rotation while LOW does not.

Let L1/H1 be lower LR4 complex transfer functions (nominal 450Hz). Let L2/H2 be upper LR4 complex transfer functions (nominal 2500Hz). Define **upper crossover allpass A2=L2+H2**.

Naive:
- LOW=L1
- MID=H1×L2
- HF=H1×H2
- Combined=L1+H1×A2; this is not guaranteed constant magnitude.

Phase-bridged:
- LOW=L1×A2
- MID=H1×L2
- HF=H1×H2
- Combined=(L1+H1)×(L2+H2), whose magnitude is exactly 1 for ideal identical flat-phase drivers.

The **low-frequency branch phase bridge** is now encoded and checked in [wavecor_phase_sensitivity.py](simulation/wavecor_phase_sensitivity.py). The tests intentionally implement the WRONG unbridged cascade and establish that it is not flat, while checking the correct bridged design yields an ideal constant-magnitude response.

This is a mathematical filter property, not a proof that real three-way measured loudspeaker is flat; real drivers are NOT ideal flat-response sources and physical propagation/time-zero must be measured.

## Preliminary 3-way crossover using real measured input datasets

Conditional assumptions:
- Wavecor manufacturer responses are used as published, even though their absolute phase origins are NOT verified to be common.
- Individual driver voltage trims are fitted to a nominal 86dB level at LF 180Hz, MID 1100Hz and HF 6000Hz.
- Ideal LR4 cascades + LOW upper allpass correction are used, WITHOUT finite-baffle diffraction, real DSP/amplifier/DAC latencies, real in-cabinet driver phase, 3D directivity or distortion.
- Separate SUB not included in this particular mid/tweeter crossover calculation.
- The following levels are NOT measured complete-system SPL.

| Illustrative variable | Conditional result |
|---|---|
| 450Hz low/mid and 2500Hz mid/high | At 450Hz about **85.52dB** |
| Same configuration | At 2500Hz about **87.98dB** |
| Apply +100us HF relative delay | At 2500Hz about **84.98dB** |
| Model 70cm distance, shift head up +10cm | With assumed LF/MID 150mm and MID/HF 115mm centres: relative LF path +59.2us, relative HF path −47.6us |
| Same head shift and assumed phase scenario | At 2500Hz changes from ~87.98dB to ~87.36dB |

The original unbridged conceptual calculation gave about 85.66dB at 450Hz. **It is superseded** by the phase-correct three-way chain above (~85.52dB under the same source assumptions). This records the actual model revision rather than silently overwriting history.

Experimental filter sweeps cover roughly 350–600Hz low/mid and 2000–3000Hz mid/high. A reported small RMS figure from an illustrative sparse frequency grid is NOT permission to declare an optimal crossover. More frequencies, real phase reference, baffle, distortion, driver protection and angled acoustics are required first.

## Why ±100us matters

A nominal 2.5kHz wave period is 400us. A 100us mismatch is a quarter-cycle. If two filtered branches have comparable strength, this can cause large cancellation at the crossing. Thus **seven synchronous digital playback indices do not by themselves guarantee simultaneous physical sound arrival**. DSP filters, DAC reconstruction, amp/driver acoustic centers, cabinet geometry, ear position and sub-room propagation still contribute.

The geometric example numbers (150mm,115mm) are illustrative and **NOT measured mounting dimensions**; real baffle CAD must derive exact flange dimensions and listening-window constraints. These results justify using an adjustable temporary measuring baffle and measuring vertical response over a practical ±10cm head range.

## Source and test automation

- [wavecor_probe.py](simulation/wavecor_probe.py) discovered non-invented links from manufacturer's HTML via GitHub runner.
- [wavecor_threeway_realdata.py](simulation/wavecor_threeway_realdata.py) imports true 3-column SPL and impedance, phase unwrap, input SHA, and produces a CONDITIONAL crossover report.
- [wavecor_phase_sensitivity.py](simulation/wavecor_phase_sensitivity.py) performs phase-bridged frequency and delay/head-motion sweeps on the original manufacturer curves.
- [test_wavecor_threeway_realdata.py](simulation/test_wavecor_threeway_realdata.py), [test_wavecor_phase_sensitivity.py](simulation/test_wavecor_phase_sensitivity.py), and [test_wavecor_source_manifest.py](simulation/test_wavecor_source_manifest.py) catch common wrong assumptions.
- [wavecor-primary-phase.yml](../../.github/workflows/wavecor-primary-phase.yml) fetches/validates original data in Actions and retains derived evidence artifacts. Source raw data are not redistributed into this repo pending explicit license review.

To run locally on Arch Linux, from projects/diy-speakers/simulation:
- python3 -m unittest -v
- python3 wavecor_threeway_realdata.py --out wavecor-source-analysis.json
- python3 wavecor_phase_sensitivity.py --out wavecor-phase-sensitivity.json

## What remains REQUIRED, not hand-waved

1. Use source drawings to determine actual flange widths, acoustic-center offsets, and physically possible 3-way temporary baffle geometry.
2. Build cheap sealed wooden test boxes, with a dedicated **isolated 2L MR120BD02 MID measurement chamber**; final enclosure is LAST.
3. Independently collect amplitude+phase with a common microphone clock and reference impulse, plus angular measurements (horizontal and vertical) at 0.6/0.7/0.8m.
4. Determine crossover with LOW phase bridge or equivalent correctly derived phase solution, add explicit per-driver safe high-pass/low-pass, gain, limiter and startup mute.
5. Measure SPL-dependent THD/IMD, compression and differences between at least two driver specimens at matched output levels.
6. Integrate sub, PSU, seven channels and optical clocking only with independently bounded end-to-end physical timing.
7. **Retain final-production candidacy** of owner-sourced HiVi M6N/D6G for the lower band until their own FRD/impedance and comparison are measured in the same fixture.

This is the first real, source-audited layer of crossover engineering, not an assertion of a finished high-end speaker.
