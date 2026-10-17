# Shared Audio System Architecture

Status: **architecture baseline only; component choices and performance targets remain open.**

This document defines the shared contract between the independent local audio player and the companion earbuds. Device-specific details stay in [audio-player/](../audio-player/README.md) and [earbuds/](../earbuds/README.md). The intent is to settle interfaces and acceptance tests before buying expensive parts or machining final metal enclosures.

The owner requires an **audiophile-grade engineering process**, format-specific FLAC/MP3 handling, and a simulation-first workflow. See [Reference Study](REFERENCE-STUDY.md), [Audio Format Paths](AUDIO-FORMAT-PATHS.md), and [Simulation and Validation](SIMULATION-AND-VALIDATION.md).

## Non-negotiable direction

### Player
- Local music library and local playback control only.
- No internet dependency, Wi-Fi stack or Bluetooth stack.
- Dedicated digital radio link to the companion earbuds; no analog headphone jack.
- Premium compact/heavy metal device, with protected internal storage and owner-controlled firmware.
- Touchscreen and minimal sealed physical input.
- Wireless charging preferred; no conventional exposed data/power port if feasible.
- Bulk library import must be treated separately from real-time audio streaming.

### Earbuds
- Dedicated proprietary 2.4 GHz digital receiver; no Bluetooth capability in the intended design.
- Replaceable cylindrical rechargeable cells remain a user requirement, but cell dimensions, chemistry, safe charging and serviceable cap design are unresolved.
- Music playback and ANC/transparency require separately managed real-time processing priorities.
- Secure in-ear retention, wet-condition grip and serviceability matter as much as the electronics.

## System boundary

```text
LOCAL PLAYER
local files -> library/index -> decoder -> audio framing/packetizer
                                             |
                                    dedicated 2.4 GHz link
                                             |
                                             v
EARBUDS
radio -> authentication / sequence validation -> jitter & reorder buffer
     -> decoder -> DAC/amplifier -> transducer
                                                ^
feedforward/feedback microphones -> low-latency ANC DSP/controller
                                                |
                                 controlled acoustic summation
```

The diagram is a logical partition, not a fixed chip count. Do not assume that every block needs a separate processor. Prove compute, memory, latency, and power needs on development hardware first.

## Highest-priority unresolved decision: audio delivery target

The radio must be selected against an explicit target, not the other way around. FLAC and MP3 are separate format-aware source paths; neither is to be silently transcoded into a common lossy format. Compare native compressed-stream transport against a lossless PCM path, and select only after codec-corpus, payload, latency and energy measurements. See [AUDIO-FORMAT-PATHS.md](AUDIO-FORMAT-PATHS.md).

Raw stereo PCM payload rates before packet overhead:

| Format | Raw rate |
|---|---:|
| 16-bit / 44.1 kHz | 1.4112 Mbit/s |
| 24-bit / 48 kHz | 2.304 Mbit/s |
| 24-bit / 96 kHz | 4.608 Mbit/s |

A radio advertised at 4 Mbit/s PHY cannot carry raw 24/96 stereo PCM with zero overhead. FLAC can lower the rate for many music tracks, but compression is content-dependent and must be tested on real tracks and deliberately difficult signals. PHY rate is not application payload rate.

Before freezing the codec or radio, define:
1. Required baseline playback profile.
2. Whether lossless delivery is mandatory at every supported profile or only selected profiles.
3. Whether the system may adapt sample rate/bit depth, use lossless compression, or select a higher-capacity radio.
4. Maximum acceptable buffering/latency and reconnect behavior.
5. Measurable drop-out, bit-integrity, synchronization and power criteria.

No lossless/bit-perfect claim is accepted until the entire path has passed sustained tests with interference and worst-case test content.

## Radio transport contract to design

The protocol needs explicit handling for:
- packet sequence numbers and integrity checks;
- authentication and encryption, including replay protection;
- buffer sizing, jitter, reordering and bounded recovery;
- stereo synchronization and clock drift;
- packet-loss / retransmission / concealment policy with deadlines;
- interference, body/head shadowing, antenna detuning and reconnection;
- measured application payload throughput, power draw and thermal behavior.

A candidate such as the nRF54H20-class proprietary 2.4 GHz radio is not selected merely because its headline PHY rate looks close. Verify current datasheet limits and measure real throughput on the intended boards and antenna layout.

## ANC and transparency

- ANC microphone sampling and control must meet a measured low-latency deadline independent of radio packet arrival.
- Music decoding/radio buffering must not starve ANC processing.
- The music and ANC paths can have separate scheduling or DSP resources, but their acoustic outputs still interact at the transducer and in the ear.
- Validate feedforward/feedback stability, limiter behavior, maximum output SPL, transparency gain and transitions on an acoustic rig.
- Do not commit to a dB cancellation figure before measurement.

## Player charging and bulk library import

Wireless charging and high-rate data transfer are separate engineering functions, even if a future design reuses one physical coil or aperture.

The proposed single-coil time-multiplexed approach (charging window, cooldown window, data-transfer window) remains a hypothesis to test—not an established capability. Measure coil/receiver temperatures, alignment tolerance, charging efficiency, data PHY throughput, interference, and whether simultaneous or alternating operation disturbs the audio radio.

For reference, transferring decimal 1 TB in two hours requires about 1.11 Gbit/s average application payload. A low-rate Qi control channel cannot meet this by itself. If this import target remains important, benchmark a separate data PHY through the same coil/aperture before accepting or rejecting the concept.

Metal enclosure design must preserve a dielectric RF/charging region and characterize eddy-current heating, ferrite, antenna detuning and near-body performance. Do not promise water-resistance, battery longevity or high transfer speed without assembled-device tests.

## Earbud power and mechanical service

- Do not select a cylindrical cell from a size nickname alone; source a real datasheet, dimensions, protection requirements and charging limits.
- Design for polarity control, short-circuit prevention, independent cell protection, temperature sensing, retention and replaceable seals.
- Test repeated cap cycles, sweat/water exposure, drops, contact resistance, charging temperature and cell replacement.
- A metal exterior needs an RF-transparent antenna region; wet skin and head proximity must be part of the RF test plan.

## Validation gates

| Gate | Evidence required |
|---|---|
| A0 — requirements | Audio profiles, lossless policy, latency budget, battery-life goal, storage capacity and import-time target recorded |
| A1 — radio bench | Sustained application payload, packet errors, interference, body blocking, power and temperature |
| A2 — digital audio | Decoder/framing, bit-integrity, jitter buffering, dropout and reconnect tests |
| A3 — stereo | L/R synchronization and clock drift under sustained operation |
| A4 — ANC | Acoustic stability, attenuation, transparency, limiter and SPL tests independent of music traffic |
| A5 — power | Measured player and per-earbud consumption with realistic workloads |
| A6 — import | Measured bulk transfer rate through the chosen data PHY; single-coil multiplexing validated if pursued |
| A7 — mechanical | Battery service, seals, RF window, comfort, grip and thermal tests in representative housings |
| A8 — integration | Long-duration playback, recovery, firmware update and reliability evidence |

## Executable software-validation baseline

The first runnable model and its unit tests live in [validation/](validation/README.md). CI runs deterministic packet-model tests and a JSON-output smoke test. This is an initial packet scheduling model only; it is not yet a waveform, codec-conformance, RF or acoustic proof.

## Simulation-first workflow

Before ordering radio boards, final coils or metal enclosures, build reproducible software models for source decoding, packet scheduling, waveform/channel behavior, antenna geometry, charging/data time multiplexing, ANC stability and power/thermal budgets. Use declared assumptions, sweeps, uncertainty bounds and explicit stop gates. The physical prototype later confirms quantified predictions and model boundaries. See [SIMULATION-AND-VALIDATION.md](SIMULATION-AND-VALIDATION.md).

## Reference design discipline

Study high-end portable players, reference DAC/headphone stages, IEM acoustic systems, ANC designs and wireless audio links as complete architectures. Use primary datasheets and reproducible measurement methods; do not select parts from prestige or headline chip metrics alone. See [REFERENCE-STUDY.md](REFERENCE-STUDY.md).

## Current decisions intentionally left open

- Codec(s), supported sample rates/bit depths and lossless acceptance policy.
- Radio silicon, antenna, topology and actual payload budget.
- Buffer depth, transport reliability policy and target latency.
- ANC DSP/codec architecture and microphone/transducer selection.
- Exact cylindrical cell and charging arrangement.
- Bulk-import PHY and whether the charging coil is reused.
- Screen, storage and main processor.
- Final metal/dielectric enclosure design.

Keep expensive custom PCBs, titanium machining and final waterproofing until the relevant bench gates have passed.
