# Wired Optical Audio Fabric — Stationary 2.1 System

> **PROJECT TOPOLOGY FIXED — 2026-11-01:** the target is **L:LF/MID/HF, R:LF/MID/HF, SUB**, seven independent digital-to-analogue output channels and amplifiers over three synchronized, optical-networked device enclosures. It does not require seven distinct DAC ICs. See [ADR-001](../ADR-001-ACTIVE-THREE-WAY-SUB.md). Four network planes retain their logical roles; their tests must not claim physical synchronization or certified health before measurements.

Status: **new owner design hypothesis, verification-first**, no selected custom PHY/PCB/BOM.

This is a new wired transport/control research branch for the **stationary desktop satellites and subwoofer**. Do **not** silently replace the separately discussed **portable player + dedicated-radio earbuds** design with this policy; they are distinct systems.

## Owner statements (verbatim excerpts)

The motivating design is based on the owner's **original quotations**, not only a third-party summary:

> «между цапом и системой ... использовать оптоволокно?»

> «между цапом и пк скоростнрй type-c ... параллельно команды, тогда цап уже сам решает что и куда он будет отправлять»

> «сигнал описывает функцией и можно передавать не сигнал а его представление»

> «управляющая плата отдельно создаёт буфер ... сигнал загружен сильно наперёд ... 3-4 щага впереди»

> «каждый уровень имеет строгие математические границы и покрыт нужными тестами»

> «колонки знают цап, но не знают пк, а пк знает цап, но не знает колонок»

> «шифровать всё ... намного лучше параллельный канал криптографии ... никаких беспроводных протоколов физически»

These remain conceptual user goals, not validated correctness or performance properties.

## Most important translation: digital transport vs DAC location

When sending **digital** audio over fiber, the DAC belongs **after** the fiber link in each active loudspeaker/satellite/subwoofer path. The central box should therefore be called a **digital audio controller / renderer / router**, even if it contains an *optional additional DAC* for an analog headphone/line output. Sending analog light-intensity-modulated waveforms is a distinct alternative, with a new E/O and O/E analog noise/distortion budget and no automatic advantage.

```text
               PC / sound engine / source files
                             |
              USB-C physical connector
              USB device/host protocol, framing
                             |
                 DIGITAL AUDIO CONTROLLER
            route plan / format-aware decode or relay
            processing / time master / command service
            safety state / device identities
                  |           |           |
             duplex fiber duplex fiber duplex fiber
                  |           |           |
              LEFT active   RIGHT active   SUB active
              receive       receive        receive
              verify        verify         verify
              prebuffer     prebuffer      prebuffer
              local clock   local clock    local clock
              local DAC     local DAC      local DAC
              amp+protect   amp+protect    amp+protect
                  |            |             |
                 LF/HF        LF/HF          10-12"
                  |            |             |
               AC + PSU    AC + PSU      AC + PSU
```

For active two-way satellites, local 2-channel DACs and amplifier channels are candidates; the sub uses its own output. Alternative: hub sends four bandlimited satellite driver feeds plus one sub channel, requiring **5 independent PCM channels** for 2.1 (not a 5.1 program).

## Core properties

- **Stationary system is entirely wired.** Audio, control and timing may share a duplex fiber PHY with separate logical channels/queues. No wireless radio is required anywhere in this stationary design.
- Independent local AC supplies with proper protection and local low-noise rails; an external pre-certified power module is safer than modifying an existing computer ATX PSU. 80 PLUS efficiency rating is *not* output-noise, overvoltage, short-circuit or thermal-safety certification.
- **Source-aware representation:** FLAC stays lossless; MP3 never suffers an additional lossy transcode. PCM is a valid exact digital interface after a lossless decoder where input format warrants it. Symbolic/parametric source representation is a research option only for a restricted mathematically defined class of signals with a formally specified reconstruction.
- **Separate latency domains:** high-throughput audio prefetch and time-critical authenticated control events. A PAUSE must prevent queued future audio from being rendered even if the content buffer remains full. Actual stop latency has physical lower bounds including control transfer, scheduling, sample-block and DAC/output latency.
- **Sample-index/timestamp addressing:** independent DAC clocks drift. Each receiver needs a defined synchronization method, playout epoch, monotonic stream sequence, controlled clock correction/ASRC policy and finite-drift budget. A playback FIFO alone does not achieve synchronized stereo.
- **Bounded recovery:** CRC catches accidental transmission corruption; ARQ and/or erasure FEC should be compared under measured *fiber link* errors, not assumed essential. An MDS (k+r, k) erasure code can recover at most r known erasures per block at an n/k overhead; 'half damaged' is not a universal guarantee.
- **Split trust boundaries:** PC authenticates the controller; endpoints authorize the controller; the host does not need endpoint-specific certificates. But the controller necessarily has device topology/routing knowledge. Cryptographic *authentication* and data *confidentiality* are separate requirements. A one-time session handshake does not prevent replay, forgery or later tampering of audio/control packets; use sequence/epochs and keyed integrity tags or equivalent authenticated framing where threat model requires it.
- **Good physical behavior is an actual proof obligation:** no assumption that ideal bit-correct transmission guarantees distortion-free analog power, DAC, amplifier or transducer output.

## First sanity numbers

For 5 independent PCM channels at 96 kHz × 24 bit: **11.52 Mbit/s** payload, before overhead. At 192 kHz this doubles to **23.04 Mbit/s**. A hypothetical full-duplex 100 Mbit/s optical Ethernet link could therefore be worth investigating; application throughput and real implementation availability must still be established.

For blocks of 128 samples at 96 kHz: 1.333333 ms/block. Four such blocks provide only **5.333 ms**, not arbitrary '3–4 steps'. Buffer depths must be specified in **samples or milliseconds**, not an ambiguous number of stages.

At 96 kHz, a **50 ppm relative clock error** accumulates 4.8 sample periods of offset per second; without correction even an error-free transport eventually causes underruns/overruns or channel skew.

## Candidate first interfaces; not selected

1. **PC → controller**: normal USB Audio Class (native OS support), plus separate compliant control channel; benchmark against USB bulk endpoint plus custom device protocol. USB-C is the *connector*, not the data protocol. 'TCP over UDP at hardware level' is not a concrete USB layer: specify reliability, framing, queues, priority and deadlines instead.
2. **Controller → satellite/sub**: compare fiber-backed full-duplex Ethernet (e.g. 100BASE-FX or 1000BASE-SX with appropriate devices), dedicated digital audio optical links (TOSLINK/ADAT when adequate), and proprietary optical framing only if requirements demand it. A bidirectional control/telemetry link must be included in topology, whether same pair or separate fibers.
3. **Synchronization**: PTP-inspired measurement and clock discipline / timestamp schedule, compared with a dedicated optical time-reference path. Do not assert that software NTP-like timestamps alone solve DAC-clock phase alignment.
4. **Device identity**: pinned/provisioned public-key identities in secure elements, authenticated enrollment, revocation, authorization; allow a policy of *unencrypted content* if confidentiality is not needed, but authenticate commands and any bits whose malicious alteration matters.

Reference standards:
- [AES67-2023](https://aes.org/publications/standards-store/?id=140): timing, media clocks, streaming and connection management baseline.
- [USB Audio Class](https://www.usb.org/document-library/usb-audio-devices-release-40-and-adopters-agreement): native device audio interface option.
- [NIST message authentication code](https://csrc.nist.gov/glossary/term/message_authentication_code): origin/integrity without requiring payload confidentiality.

See [CONTRACT.md](CONTRACT.md), [SIMULATION-PLAN.md](SIMULATION-PLAN.md), [FOUR-PLANE-ARCHITECTURE.md](FOUR-PLANE-ARCHITECTURE.md), and the [four-plane logical model](four-plane/README.md). The earlier [single-receiver model](simulation/README.md) remains a separate first-stage baseline.
