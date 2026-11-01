# Near-field Stereo 2.1 Acoustic Research Bench

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
