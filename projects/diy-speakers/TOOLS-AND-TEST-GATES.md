# Low-Cost Modeling and Validation

Research-first workflow. Simulations predict behavior for assumed inputs; physical measurement validates drivers, construction and room interactions. The design must not require a commercial anechoic chamber for ordinary DIY development.

## Tools

- **Python / SciPy / NumPy**: linear electro-mechanical-acoustic enclosure modeling, parameter sweeps, Monte Carlo tolerances, system identification, DSP, frequency/phase response and comparison. Own code and tests should be published.
- **CamillaDSP (open source)**: existing FIR/IIR, crossovers, mixing, convolver, room-EQ and automated benchmark reference. https://www.camilladsp.com/
- **VituixCAD**: excellent enclosure/crossover/diffraction/directivity tool, **freeware rather than open-source**; Windows-focused. Evaluate usability through a VM or separate OS rather than assuming native Linux. https://kimmosaunisto.net/
- **REW / Room EQ Wizard**: free acoustic measurement software, available for Linux and other platforms, **freeware rather than open-source**. https://www.roomeqwizard.com/
- **open-source additional projects** for BEM/FEM or structural/thermal modeling can be explored only when their geometry and measured material parameters are available.

## Current proposed system to test

The user prefers a **modular 2.1 system**: two compact near-field two-way satellites and a 10–12-inch independent subwoofer. Room area is approximately 19 m²; the listener is **60–80 cm** from the main speakers; the heard reference is **ADAM T5V** and the comparison benchmark **ADAM T8V**. Total cost develops incrementally (initially 50–100k RUB, potentially up to ~200k RUB over time). Compare bass extension with SPL/THD/excursion constraints and reserve clean midrange headroom in the satellites. Details in [STEREO-2.1-ARCHITECTURE.md](STEREO-2.1-ARCHITECTURE.md).

## Executable initial model

[simulation/](simulation/README.md) contains Python stdlib tests for sealed small-signal resonance and ideal LR4 electrical sub/satellite crossovers. This establishes implementation correctness for simplified formulas, not actual loudspeaker acoustic performance. CI executes the tests and JSON report smoke test.

## Stage S0 — Requirements

Room/listening distance, placement, cabinet maximum dimensions, preferred appearance and finish, target SPL, bass frequency at defined SPL, expected movie/music use, speakers/subwoofer topology, and whole-system budget.

## Stage S1 — Candidate driver comparison

Acquire current primary manufacturer datasheets. Capture T/S, sensitivity, impedance, off-axis response, excursion Xmax criterion, max recommended power and dimensional drawings.

Never claim 'better' from the membrane material, prestige or price alone.

## Stage S2 — Box and bass

Sealed, vented and optional passive-radiator variants. Compute volume, tuning, f3/f6, excursion vs frequency and drive, port air velocity and group delay when applicable. Simulate at the target listening SPL and realistic input power/voltage, not merely 1 W small-signal curves. Identify and cap EQ excursions.

## Stage S3 — Crossover and directivity

Use actual frequency/phase response and driver offsets. Model diffraction/baffle step, off-axis response, crossover summation and spatial response. Parametric waveguide design only when the measured integration needs it.

## Stage S4 — Enclosure structure

Compare simple braced plywood/MDF, structurally valid pear solid wood, pear-faced composite and optional CLD. Model panel modes as a first approximation; input density, elastic constants, joint stiffness and damping assumptions. Simulate internal absorption separately from structural wall damping.

## Stage S5 — DSP and amplifier

Compare passive crossover vs active crossover. Use realistic amplifier modules and power supplies. Model voltage/current headroom, thermal dissipation, ground noise and hiss. Benchmark IIR, direct FIR and partitioned FFT FIR rather than relying on the raw tap-count GMAC figure.

## Stage S6 — Low-cost measurement

Use REW and an individually calibrated measurement microphone such as miniDSP UMIK-1 or Dayton iMM-6C as suitable. At home:
- gated measurements before first reflection for mid/high-frequency response;
- near-field woofer/port bass and/or suitable outdoor ground-plane method;
- horizontal/vertical angular series and pair matching;
- distortion, level sweep, thermal compression and enclosure resonance checks;
- careful loudness-matched listening and response comparison.

**Limitations:** gating sets a low-frequency resolution floor; near-field requires correct merging and radiation assumptions; non-anechoic measurements must state their limitations. Don't claim KLIPPEL NFS-equivalent results from a few microphone positions.

## Stage S7 — Experiment beyond baseline

Only after a satisfying first pair: compare nonlinear equalization, direct velocity sensing/current measurement with a validated observer, and active cabinet vibration control. Each needs independent baselines and stable controlled tests. Do not assume predicted THD reductions.

## Sound-engine integration

Maintain two separate processing domains:

1. **Content/sound engine** — source analysis, deterministic reconstruction where enabled, optional explicit synthesis and user listening profiles. Preserve an unprocessed reference path.
2. **Speaker compensation** — fixed calibrated driver crossovers, delay, gain, protection, equalization and optionally room/loudness correction. It must not silently alter content semantics.

Do not let two independent automatic 'quality correction' systems stack EQ gains or defeat driver protection. Define a shared interface with metadata, processing state and headroom budget.

## Starter evaluation

Initial candidates worth **modeling**, not buying yet:
- 5–7 inch two-way stereo with a dome/waveguide tweeter, 2ch passive vs 4ch active comparison;
- three-way only if measured target SPL/bass/directivity justifies it;
- separate subwoofer later if full bass extension from stand-mount speakers exceeds excursion and budget limits.
