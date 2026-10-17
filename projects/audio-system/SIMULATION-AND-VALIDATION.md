# Simulation-First Validation Plan

Status: **simulation-first workflow; physical hardware is a later confirmation gate.**

## Owner requirement

Develop and stress the design with purpose-built software before ordering custom PCBs, machining final enclosures or building the finished coil/antenna system. The purpose of physical prototypes is to confirm quantified predictions and validate model boundaries—not to replace analysis with trial and error.

Every model must state its assumptions, parameter ranges, uncertainty and pass/fail criteria. A simulation result is evidence only for the behavior represented by that model.

## Toolchain by question

### 1. Audio codec and transport reference
Use trusted FLAC/MP3 decoders and reproducible PCM reference vectors. Script deterministic tests for sample counts, channel mapping, gapless boundaries, exact lossless output, buffering, jitter and packet loss. Use Python/NumPy/SciPy or equivalent for repeatable signal and buffer analysis.

### 2. Baseband modem and radio channel
GNU Radio is a leading candidate for a reproducible waveform/modem testbench. Its documented channel models can inject AWGN, frequency offset, sample-timing offset and multipath; dynamic models can include time-varying offsets and fading.

Model and sweep:
- candidate modulation/coding and symbol rates;
- occupied bandwidth and spectral mask assumptions;
- synchronization acquisition and loss;
- CFO and sample-clock offsets;
- AWGN and multipath/fading profiles;
- packet error rate vs SNR;
- retransmission deadlines and goodput;
- interference and coexistence scenarios;
- application payload throughput, not only nominal PHY rate;
- buffer underruns, end-to-end latency and energy per delivered audio minute.

GNU Radio models are not a complete substitute for a standards-conformant RF compliance test or a calibrated real channel.

### 3. Packet / real-time scheduling model
Build a deterministic packet-level simulator alongside the waveform model. Vary codec payload distributions, retransmission policy, queue depths, radio duty cycle, left/right synchronization and decoder scheduling.

Report distributions and worst cases, not only averages:
- deadline-miss rate;
- maximum and percentile jitter;
- buffer low-water marks;
- burst-loss recovery time;
- stereo skew and clock drift;
- worst-case throughput for FLAC stress files and MP3 bitrate profiles;
- energy and radio-on time per hour of playback.

### 4. Antenna and metal-enclosure electromagnetics
Use an electromagnetic solver such as openEMS for geometry-based antenna and near-field investigations, provided the target geometry, materials, boundaries, mesh and solver assumptions are represented appropriately.

Model:
- antenna placement behind the intended dielectric rear insert;
- display/front stack and PCB component keep-outs;
- battery, shields and metallic body proximity;
- matching network sensitivity and feed position;
- efficiency, S11/return loss, radiation pattern and near-field coupling;
- head/hand proximity and wet-surface variants for earbuds;
- charging-coil/antenna interaction and mutual coupling.

A solver cannot predict an unknown material stack or connector geometry. Use measured material parameters and keep uncertainty ranges explicit. Final OTA performance and regulatory compliance still need confirmation.

### 5. Wireless power and single-coil time multiplexing
Treat the proposed coil schedule (charge, cooldown, data transfer) as an engineering hypothesis, not an established capability.

Use a coupled analysis:
1. equivalent-circuit model for coil/receiver/rectifier/charger and load changes;
2. electromagnetic model for coil geometry, ferrite, metal eddy currents, coupling and alignment;
3. thermal model for coil, ferrite, receiver, battery and surrounding metal;
4. data-link model for the proposed modulation, bandwidth, coding, receiver sensitivity and application payload;
5. interference model covering charging switching harmonics, data receiver sensitivity and the separate audio radio.

Sweep coil alignment, gap, load, battery state, charging current, data rate, duty cycle, temperature and component tolerances. The result must show whether the same physical coil can meet both the required charging power and bulk-data throughput with acceptable thermal rise and error rate. If the data PHY cannot close the link budget, reject or revise the architecture before physical construction.

A Qi power-control/negotiation channel must not be assumed to carry bulk files at high speed. Any data path through the coil requires its own defined and modeled PHY.

### 6. ANC / acoustic / transducer system
Use a numerical acoustic/control model for early feasibility: transfer functions, microphone placement, feedback/feedforward loop stability, delay budgets, limiter behavior and worst-case phase variation. Use measured transducer/microphone data when available; otherwise label results as assumed-parameter studies.

Model:
- acoustic paths from external field to error microphone and eardrum;
- ANC loop stability margins across fit/leakage variation;
- transparency-path delay and gain;
- interaction between music and cancellation;
- limiter attack/release and maximum output level;
- battery/CPU load versus worst-case ANC scheduling.

Simulation is a design filter, not proof of safe sound pressure or stable behavior in every ear. A final calibrated acoustic fixture and safe listening validation are mandatory before user exposure.

### 7. Battery, power and thermal budgets
Use explicit component-level power models with low/typical/worst-case ranges, state transitions and regulator losses. Model playback, ANC, RF retransmission, screen-on time, charging, idle and recovery.

For every estimate, publish:
- assumptions and source for each component value;
- uncertainty bounds;
- average and peak current;
- cell voltage range and conversion efficiency;
- heat generation and thermal resistance assumptions;
- usable capacity after protection and aging margin.

Do not infer real battery life from nominal cell capacity alone.

## Evidence format

Every gate should retain:
- source code and exact tool/version;
- input data and seeds;
- configuration and model assumptions;
- machine-readable results plus a readable summary;
- plots for key curves and worst-case points;
- expected vs observed assertions;
- known unmodeled effects;
- a reproduction command.

## Physical confirmation gates

Physical tests occur only after simulation shows a feasible design and tolerances. They confirm the highest-risk model parameters first: antenna matching/efficiency in the metal/dielectric stack, radio packet performance in representative positions, coil temperature/coupling, and acoustic stability/response. If results differ from simulation, update and validate the model rather than hand-waving the discrepancy away.

## Stop conditions

- No measured/defensible payload budget: do not freeze the radio.
- Unclosed worst-case buffer/deadline budget: do not claim dropout-free playback.
- Unclosed antenna link budget in the real material stack: do not freeze the enclosure.
- Unclosed thermal or data-throughput budget for the shared coil: do not build the final charging/data mechanism.
- Unproven ANC stability/output limit: do not test at unsafe sound levels.
