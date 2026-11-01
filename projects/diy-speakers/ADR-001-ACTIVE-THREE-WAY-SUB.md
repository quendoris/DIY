# ARCHITECTURE DECISION 001 — Active 3-Way Stereo Satellites + Independent Subwoofer

> **RESEARCH VERSUS PRODUCTION BOARD:** [ADR-003](ADR-003-RESEARCH-HARDWARE-QUALIFICATION.md) explicitly permits an imperfect NUCLEO variant as an electrically safe, identified and documented optical research/stress fixture, while every finished custom speaker PCB has stronger source, solder, firmware, electrical and post-assembly acceptance requirements. The active pre-STM task is [D2 acoustic integration](D2-THREE-WAY-ACOUSTIC-INTEGRATION.md).

> **Stage ordering amendment:** [ADR-002](ADR-002-OPTICAL-FIRST-BENCH.md) supersedes **the physical order only**: optical link on NUCLEO-H7S3L8 with factory supplies first; custom monitored power module second. The 7-channel/3-way+sub topology remains fixed. Physical optical testing must not be represented as already completed.

Date: 2026-11-01. Decision status: **OWNER-SELECTED AND FROZEN AS PROJECT TOPOLOGY**. Driver models, crossover points, DAC chip count, power rails, enclosures and supplier quotes are **not** frozen.

## Decision and its force

The owner has explicitly selected **two fully active three-way satellite speakers** (LF / dedicated MID / HF for each) **plus a separately powered deep-bass subwoofer**, with eventual seven independently controlled digital-to-analog *output channels* and seven driver-specific amplifier outputs.

This replaces the earlier *architecture-option comparison* between 2-way and 3-way. Do NOT present a two-way speaker as an alternative goal, a budget upgrade ladder, or a mandatory pass/fail gate to justify 3-way. Existing 2-way models remain archived **measurement baselines** and possible external competitors, not purchase or system topology candidates.

The owner prioritizes exceptionally clean midrange, full-range natural dynamics, precise synchronization and electrical-noise containment. Delivery may take 4, 6, 8 months or longer; time and total price do not redefine the topology. Transparent publicly reproducible engineering and open documentation are essential rather than price-based marketing or opaque proprietary modules.

## Concrete end-to-end topology

```text
PC / audio renderer / sound engine  -- USB-C digital -->
           DIGITAL CONTROLLER / SYNC MASTER
        routing / PCM integrity / policy / clocks
                  │             │           │
             duplex fiber  duplex fiber  duplex fiber
                  │             │           │
          LEFT SATELLITE    RIGHT SATELLITE    SUBWOOFER
          endpoint+DSP      endpoint+DSP       endpoint
           shared local      shared local      local clock
            audio time        audio time       discipline
           ├ LF  DAC out     ├ LF  DAC out      └ SUB DAC out
           │ LF  amplifier   │ LF  amplifier      SUB amplifier
           ├ MID DAC out     ├ MID DAC out
           │ MID amplifier   │ MID amplifier
           └ HF  DAC out     └ HF  DAC out
             HF amplifier      HF amplifier
```

Seven independent *DAC conversion paths / analogue output channels*: 2 satellites × 3 bands + 1 sub. **Seven discrete DAC ICs are NOT required**: high-quality simultaneous multi-channel conversion is acceptable if it has documented shared clock, independent outputs, low interchannel crosstalk and per-output controls. Using seven separate converter chips is an experiment to compare on evidence, not a guaranteed audio-quality feature. Different clock domains MUST be aligned before making synchronized acoustic claims.

Initial input programme is **stereo L/R**, not a 7-channel surround source. A controlled active crossover produces seven driver feeds. The controller/DSP partition (global band separation and per-endpoint DSP, or local splitting in each enclosure) is a design trade-off: do not freeze it before proving clock/latency and safety interfaces. Each receiver has independent analog/hardware fault protection even if the controller fails.

## Four separate logical network planes

1. **Attestation + health**: authenticated device identity, approved/verified firmware state under explicit root-of-trust assumptions; fresh diagnostic reports of rail voltage/current, temperature, fan, clock, buffer, link and amplifier condition. Identification is not proof of actual acoustic correctness.
2. **Control**: authenticated MAC/signature and anti-replay session/epoch/counter; high-priority, bounded Play/Pause/Stop/limiter, profile and safe mute. Controls shall pre-empt buffered audio. Not all data must be encrypted.
3. **Audio**: deterministic lossless digital sample/payload identity within stated input/processing contract, buffered and sequenced; clear audio is allowed given a documented threat model, but authenticated commands and frame integrity are separate.
4. **Sync**: common sample-to-time mapping, clock drift correction, scheduled playback, end-to-end delay calibration, link latency measurements; lengths of optical fiber of several meters do not guarantee synchronization without disciplined receivers.

Implement separate service guarantees and autonomous safety hardware; four logical planes do not require four physical fibers.

## Speaker acoustic/magnetic requirements

- **Satellite LF driver**: Chinese HiVi M6N, D6G, Wavecor WF168WA06 or other serious final-intent option. Dedicated LF driver covering sub split ~70–110Hz to mid split; low-mid IMD/thermal compression to be measured.
- **Satellite dedicated MID**: Wavecor MR120BD02 8Ω, WF120BD04 or a stronger measured match, with isolated sealed rear chamber. Candidate 350–600Hz lower split and 2–3kHz upper split; actual geometry/excursion/polars determine values.
- **HF**: Wavecor TW030WA22, later higher-tech TW030WA24, waveguide TW030WA11 or international top comparator. Protection must never depend solely on a software crossover: require startup mute, fault handling and acceptable analog/hardware safety.
- **Independent SUB**: evaluate 10–12in Wavecor SW312WA05, Dayton RSS315HF-4 and other long-throw designs, including enclosure/phase/power/25Hz distortion rather than Fs alone. Its location/acoustic time-of-flight must be part of total synchronization.
- **Head movement:** at 0.60–0.80m three physical drivers can create near-field vertical interference and lobing. Test 3D geometry and listening-window response over realistic head positions.
- **No final cabinet yet.** Use interchangeable-baffle **temporary plywood measurement cabinets** and isolated MID chambers; open-frame use only at conservative levels for T/S and basic electric checks. Future futuristic wood/composite enclosure is last and must reproduce final measured acoustic volumes, shapes, damping, diffraction and thermal isolation.

## Electronics, clock, protection

- Independent analogue output gain, appropriate full-scale voltage, digital headroom and channel calibration; each amplifier optimized for **its actual driver** (no universal 300W tweeter channel).
- Each enclosure uses a **coherent local DAC clock domain**. Distributed end devices must align playout samples and correct relative frequency drift; measure propagation, DAC reconstruction/group delays, crossover group delays, amps, acoustic propagation and physical loudspeaker centre displacement.
- Power: independently powered and isolated, using **certified external AC/DC for early benches** plus DC-only independently supervised rails and protection; DAC reference/analogue supply filtered away from class-D power and fan PWM rails.
- Safety: independent protected input/PSU, voltage/current/temp monitoring, local hardware short/thermal cutoffs and controlled pop-free startup/stop; network or MCU dead must not remove the hardware cutoff.
- Cooling: passive first; optional low-noise tach-monitored fan in a **separate electronics bay**, never casually ventilating a sealed acoustic chamber.

## Why this is an ambitious but grounded target

Many existing **premium active three-way monitors** already use three separate amplifiers, DSP and digital inputs. For example, ADAM S3V explicitly implements 9-inch LF, 4-inch MID, ribbon HF, three amps, DSP and AES3 (https://www.adam-audio.com/en/s-series/s3v/). Therefore, **three-way active DSP alone is not a new architecture**; neither separate amplifiers nor separate DAC conversion automatically prove audibly superior sound.

Our distinctive research deliverable is the *composition* of open/inspectable optical digital transport, four monitored planes, signed reproducible configuration, independent supply/thermal hardware protections, rigorous acoustic model/measurement validation, precise latency/clock characterization, and documented design files with reproducible build steps. Whether the result matches or beats premium monitors is an empirical question, not an architectural promise.

## Open source and qualification contract

The owner wants **reproducible complete designs** rather than undisclosed commercial proprietary modules. Publish, at a selected appropriate stage, source trees, architecture specifications, device firmware, reproducible DSP profiles, test harnesses, model math, board schematics+PCB layouts, documented protocols and full reproducible BOM/assembly instructions, with source versions and measurement datasets. License choice and third-party copyright/distribution restrictions are still unresolved: open-source chip datasheets and usable open interfaces do not imply open silicon internals. Avoid restricted vendor IP and respect hardware safety.

- Engineers can independently rebuild and retest. Pinned source hashes and signed releases may authenticate provenance.
- Every gate distinguishes `MODEL_ONLY`, `UNIT_TESTED`, `FORMALLY_PROVED_UNDER_ASSUMPTIONS`, `BENCH_MEASURED`, `EXTERNAL_CERTIFIED`, `NOT_TESTED`. No false safety or acoustic 'certification'.
- Do not call homemade reports official IEC safety certificates. Use a reproducible internal qualification dossier for device specs/limits/telemetry and competent labs where formal electrical/EMC certification is warranted.
- Mathematical Lean proofs are scoped to precise models and assumptions, not physical analog hardware. No proof of perfect audio from SHA-512 or endpoint handshake.

## Stage ordering; no deadline promise

**Immediate**: finalize compatibility of satellite LF + dedicated MID + HF + SUB, using manufacturer FR/impedance/THD/angle data where available. Then formalize *per-channel audio, timing, protection and gain contracts* for 7 channels. Power/protection is the FIRST physical DC-only module, but must be sized after component electrical requirements. A temporary acoustic fixture can be built before final electronics.

**Next**: instrumented reproducible stand, measured driver parameters and breakup, separate MID chamber, DSP crossover trials and low-noise amplifier evaluations. Keep optical synchronization and cryptographic transport software research parallel.

**Last**: integrate multi-endpoint optical transport and the final visually ambitious enclosure only after preserving desired acoustic geometry and thermal budgets.

## Explicitly frozen vs free

Frozen topology: 2 active 3-way satellites + 1 independent sub, 7 independent DAC-output/amp channels, four logical planes, openness/reproducibility, final aesthetic enclosure LAST.

Still open: exact manufacturer drivers, crossover frequencies/slopes, 4Ω vs 8Ω mix, per-band DAC chip count, global vs local DSP allocation, analog amplifier classes and power, exact optical PHY, circuit parts, cabinet dimensions, realistic performance metrics, implementation language and release license.


## Acoustic layout is a derived requirement, not aesthetic input

[Dimensioned geometric investigation D2-GEO-01](D2-GEO-01-WAVECOR-BAFFLE.md) now preserves **two viable real-dimension fixture shapes**, 205×440mm vertical and 330×290mm mirrored side-low; the source-based ideal monopole study cannot physically distinguish them because angular data, finite baffle and common-driver acoustic phase have not been measured. **Do not freeze the futuristic cabinet until the driver layout and acoustic directivity are measured**. Future shell geometry is built around the validated acoustics, and any shell change triggers requalification.


## Current D2 physics boundary

The [D2-WAVE-02](D2-WAVE-02-DIRECTIVITY-DESK-DIFFRACTION.md) geometry-plus-desk study adds ideal finite-diaphragm directivity, geometric baffle edge path delays and desk image-source models. All are explicitly tagged **analytical model**, not a solved actual finite-baffle acoustic response; the builder still needs directivity and common-phase measurements. The final enclosure is designed around the chosen qualified placement **last**, not fixed by the current plywood panel rectangles.


## Installation envelope frozen as a goal, NOT as dimensions (D2-STEREO-01)

The owner has measured **head +60cm above the desk; 32-inch central monitor TOP +70cm; existing 27-inch side TOP +60cm; shelf +10cm**. Lateral desk space is unavailable. The system MUST remain capable of integrating into **a future three-large-monitor array** (potentially 42–54in), not merely the existing two screens. Ear canal height and monitor array width/depth are not measured.

**The leading mechanical-acoustic arrangement under investigation** is a pair of mirrored, HORIZONTAL Wavecor LF/MID/HF baffles on strongly fixed DESK-ANCHORED raised supports, physically ABOVE screens, aimed/down-tilted toward the listener, preserving a symmetric L/R stereo triangle. Diagonal (±45°) and vertical arrays remain adversarial controls and are not technically forbidden.

**This is NOT a frozen final acoustical/production layout.** [D2-STEREO-01](D2-STEREO-01-MULTIMONITOR-REAL-HEIGHTS.md) now controls the measured-position contract and the 3D paired stereo/multi-monitor test, including all six driver rays/full flanges, proper L/R toe-in and future monitor growth. Desired perception (externalized/out-of-head stereophonic image) still requires real listening tests; aiming speakers at the ears cannot remove physical source elevation or guarantee enveloping localization.

Potential horizontal MID/HF acoustic lobing, diffraction from the screens, ceiling reflections and bracket loads remain independent constraints. **The shell comes last** as a consequence of actual acoustic placement and test evidence; custom supports must be separately engineered for structural safety, not assumed safe because rigidly clamped to the tabletop.


## New user mechanical placement requirements, 2026-11-01 (D2-MOUNT-01)

In addition to actual owner heights (+60cm head, +70cm 32-inch top, +60cm side 27-inch top), the horizontal-over-monitor array's nominal longitudinal/depth offset is **ZERO** to the monitor plane; no deep-back setback requiring excessive elevation. Owner estimates **~10kg per satellite** and REQUIRES load path / joints working target **≥50kgf** and stress/proof target **≥100kgf**, and a desk attachment with a recessed/embedded bolt. These are *minimum desired engineering targets*, NOT proof that such hardware currently exists or the tabletop can carry it. Full loads include gravity moments at worst-case lever offsets and independent retention to an actually reliable structural support.

[Structural/placement contract D2-MOUNT-01](D2-MOUNT-01-COPLANAR-STRUCTURAL-SAFETY.md) supersedes any earlier assumption that the speaker should sit 20–35cm behind the monitors. Front-panel speaker source zero-depth is not the same as entire rotated rigid housing remaining out of monitor clearances. Future 3-monitor scalability and true stereo geometry remain fixed requirements. The actual shell remains the last design task.


## Desk framework updated from owner measurements

The main tabletop is now planned as a **50mm solid wood slab** over a **2m×1m structure with 50×50mm profiles** and a separate upper shelf. Structural primary load should be delivered to the frame, with timber fasteners allowing real grain-direction expansion. [D2-FRAME-01](D2-FRAME-01-50X50-STEEL-WOOD-DESK.md) supersedes unknown generic table materials and offers only hypothetical steel-tube wall/deflection examples until alloy/wall/crossmembers/welds are identified. No table top mass or large-section claim alone can qualify 50kgf WLL/100kgf proof support.
