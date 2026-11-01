# ADR-002 — Optical Transport as FIRST Physical Experiment

Date: 2026-11-01. **Owner decision:** test a real optical connection **before** building a DIY power module, then progressively add full four-plane protocol, real clock sync, power, DACs and finally the exquisite permanent cabinets. This is compatible with [ADR-001](ADR-001-ACTIVE-THREE-WAY-SUB.md), the fixed 7-output-channel active 3-way stereo + SUB architecture.

## The 'growing a crystal' method

A new implementation layer is introduced ONLY after the preceding layer's **documented assumptions, data, tests, boundary cases, and failure behavior** are sound. No layer may turn `SIMULATED` into `PHYSICALLY_MEASURED` or `ATTESTED` merely because its integration tests are green. Maintain successful and rejected hypotheses with test-vector and version evidence. Results are open and reconstructible, not claimed as vendor certification.

### Key hardware identification warning (DO FIRST)

Marketplace offer: https://ozon.ru/t/CrUL8aa (not accessible via external inspection).

Owner's listing says `Spot NUCLEO-H7S3L8` and, inconsistently, `STM32H7R3L9`. Official ST **NUCLEO-H7S3L8 (MB1737) uses STM32H7S3L8H6**; a separate STM32H7R3L8 is a valid MCU model, but we did not find STM32H7R3L9 in the ST selector. This may be a seller title typo or nonstandard cloned board. Photograph actual chip markings and PCB label, PCB connectors and oscillator; compare with original MB1737 user manual **UM3276**. Pinout, security and flash/boot settings must follow the *physical PCB*, never a mismatched listing.

Official sources:
- https://www.st.com/en/evaluation-tools/nucleo-h7s3l8.html
- https://www.st.com/en/microcontrollers-microprocessors/stm32h7s3l8.html
- https://www.st.com/resource/en/user_manual/um3276-stm32h7rx7sx-nucleo144-board-mb1737-stmicroelectronics.pdf
- https://wiki.st.com/stm32mcu/wiki/Security:Secure_Boot_STM32H7RS_How_to_Introduction

Official board includes **100M/10M Ethernet, USB Type-C HS, STLINK** and connectors. The Ethernet MAC routes through **onboard copper LAN8742ACZ RMII PHY → RJ45**, NOT to a fiber optical transceiver automatically. The MCU has 64 KB internal BootFlash, 620 KB SRAM and external **256 Mbit** NOR flash (32 MiB); ST's XIP software examples generally boot small internal code and run application from external flash. Don't accidentally interpret 256 Mbit as 256 MByte from inconsistent marketing text. Use exact **STM32CubeH7RS** package and NUCLEO-H7S3L8 example; don't assume old STM32CubeH7 projects can be flashed without porting.

- https://www.st.com/en/embedded-software/stm32cubeh7rs.html
- https://community.st.com/stm32cubeide-mcus-28/problem-with-lwip-tcp-echo-server-on-nucleo-h7s3l8-eval-board-157086

### Bench A — fastest and low risk: external 100BASE-FX media conversion

```text
            USB debug/power          standard CAT5e (electrical)
[Host PC]  ------------------------------ [NUCLEO-H7S3L8 RJ45]
                                             |
                         (Copper RJ45 Ethernet adapter)
```

Actual optical test topology:

```text
[PC RJ45 100BASE-TX] -- CAT5e -- [media converter #1]
                                  ||
                          duplex SC 50/125 multimode
                          fiber patch: 1, 2, 5 m
                                  ||
[NUCLEO RJ45] ------ CAT5e ----- [media converter #2]
             local board power through USB, independently
```

Use **two matching 100BASE-TX↔100BASE-FX multimode, dual-strand duplex-SC media converters** (not one media converter; and not mismatched single-fiber 1310/1550 BX A/B transceivers). Connect TX→RX for each direction (some duplex SC cords pre-cross fibers). Choose properly **SC/UPC–SC/UPC duplex OM2/OM3 50/125 multimode patch cords** for the verified products. ST onboard LAN8742 is copper 100BASE-TX; external active media converters are REQUIRED for optical. Cheap bare SFP modules cannot plug into RJ45 or RMII without a compatible PHY/PCS and electrical interface.

Observed **seller prices, not verified invoices**:
- MT-MC-100-31-02-SA duplex-SC 100BASE-FX multimode media converter, 2km rated; seller quotes **1,069 RUB each** (two required): https://modultech.ru/goods/mediakonverter-duplex-sc-2-km-10-100-base-t-100-base-fx-tx-1310-rj-45/
- Planet FT-802 commercial multimode reference ~6,147 RUB each: https://shop.planet.com.ru/catalog/converters/media/FT-802.html
- Duplex SC-SC 50/125 OM2 **1m** patch cable observed **583.2 RUB** (other lengths/stock to confirm): https://leolan.ru/catalog4578.html

**Do not buy** until checking converter ports, duplex multimode, connectors, actual Tx/Rx wavelengths, optical power/range at **1m**, adapter type, two 100BASE-FX compatible units and how link indicators behave. 2km maximum range does not establish measured correctness at 1/2/5m or prove an arbitrary minimum distance; use datasheet optical Rx saturation limits if provided. No looking into fiber/laser ports, even if invisible.

Advantage: use existing high-quality PHY/FCS hardware; test practical packet transport immediately and reserve large bandwidth for seven PCM outputs. Limitation: vendor media converters are a **reference transport, not an open silicon design**, obscure internal latency and may not preserve hardware clock timestamps transparently. No sub-nanosecond/nanosecond synchronization guarantee from network ping.

### Bench B — direct, documented optical transceiver (next independent PHY experiment)

**Broadcom AFBR-1624Z transmitter + AFBR-2624Z receiver**: 650nm 1mm plastic optical fiber, 3.3V/5V TTL level, **0–50 Mbaud**, up to 50m under applicable conditions, active semiconductor parts (data sheet and component documentation available). Purchase separate TX and RX for **each direction**; duplex needs 2 TX + 2 RX overall for a 2-endpoint link. Requires proper voltage supply/logic-level checks, supply bypass, impedance/rise-time signal design, connector termination, exact optical power budget, MCU peripheral/DMA clocking and suitable encoding.

- https://www.broadcom.com/products/fiber-optic-modules-components/industrial/industrial-control-general-purpose/650nm/afbr-1624z
- Broadcom industrial catalog: https://docs.broadcom.com/doc/AV00-0269EN

**Important:** 50 Mbaud is physical symbol rate, not necessarily 50 Mbit/s application payload. Physical encoding/framing overhead must be modeled. A GPIO bitbang or UART cannot be assumed to reach 50MBd even when the transceiver is rated for it. First measure at deliberately low speed with reliable DMA/pins/timing; only later attempt high-speed PHY.

Lower-end fiber device **Broadcom HFBR-1521Z / 2521Z** is 5MBd/20m, active but receiver is 5V/open-collector, not directly pin-compatible with a 3.3V MCU without correctly designed level and pull-up circuitry. Suitable only for an early slow-speed control/optical loopback, not future seven-channel PCM throughput. Toshiba **TOTX147+TORX147** historically supports 15 Mb/s NRZ over 0.2–5m, but 15 Mb/s line rate can be inadequate for combined seven-channel 96kHz/24bit PCM **16.128 Mb/s before any overhead** (although per-satellite link 6.912 Mb/s would fit under appropriate encoding). Check lifecycle and actual BOM before selection.

### Why the 1, 2, 5m experiment matters

In ordinary silica fiber, a 1m length difference contributes roughly **5 nanoseconds of one-way optical propagation delay**; 1→5m contributes about **20ns**. Optics with plastic 1-mm POF has different propagation and loss parameters, so do not reuse a silica-fiber number as a measured POF constant. At 96kHz one sample period is ~10.4167 microseconds.

The optical distance alone generally adds far less delay than software scheduling, media-converter serialization, DAC reconstruction, filter group delay, speaker geometry and acoustic time of flight. **No ordinary PC software ping** can directly establish a 5ns/m propagation effect. Compare measurable end-to-end packet latency and loss first; only later use appropriate hardware timestamping/oscilloscope, calibration and clear uncertainty budgeting for line/clock effects.

### Four separate protocol planes; capacity sizing

Seven independent 24bit 96kHz PCM outputs: **16.128 Mb/s combined**. Each 3-band satellite receives **6.912 Mb/s**; sub gets **2.304 Mb/s**. At 192kHz/24bit: total 32.256 Mb/s, per 3-band satellite 13.824 Mb/s, sub 4.608 Mb/s. At 192kHz/32bit: total 43.008 Mb/s and per-satellite 18.432 Mb/s. All are raw media payload BEFORE IPv4/UDP/Ethernet/physical and protocol overhead. 100 Mb/s Ethernet is plausible for a carefully engineered seven-channel aggregate, still measure usable deadline, buffering and packet loss.

1. Trust/health: freshness, device report and attestation (simulated initially, not real hardware authentication).
2. Commands: Pause/Mute with bounded high-priority treatment; never wait for media FIFO to drain. Separate queues, a link not guaranteed by software priorities alone.
3. Media: byte-exact sequence/epoch/CRC with receiver FIFO ahead of playout; no lossy substitution.
4. Sync: timestamp/epoch, drift estimate and disciplined clock with a **separate proof obligation**. On a single STM board we can demonstrate media and packet timing, NOT independently synchronized distributed DACs. Need a second independent MCU or DAC clock source plus hardware measurement to prove real endpoint synchronization.

### Progressive lab gates

| Gate | Build | Acceptance / negative test | Honest limitation |
|---|---|---|---|
| **OPT-00 Board identity** | photograph MCU+PCB+components; verify genuine MB1737 or clone, ST-Link/boot settings | matching STM32H7S3L8H6 / compatible reference pinout and power rails or documented differences | no flashed optical firmware yet |
| **OPT-01 Digital baseline** | official STM32CubeH7RS LED + Ethernet echo, **direct RJ45** PC⇄STM | stable link 10/100, controlled packet ping/echo, reset and reconnection | not optical |
| **OPT-02 Fiber 1m** | 2 matched SC duplex 100BASE-FX converters and 1m OM2/3 | 1m optical traffic, decoded frame counter, sequence, CRC, bytes, throughput + loss | not proof of nanosecond propagation |
| **OPT-03 Length A/B/C** | swap identical-type patch cords **1,2,5m** while keeping same power, converter pair, firmware, conditions | 30min+ overnight as follow-up, collect packets, length, elapsed seconds, measured distributions, link flap, CPU use; clock calibrated for macro latency | zero observed errors not zero BER proof |
| **OPT-04 Four logical planes** | four queues, fault simulator and synthetic PCM rates at same time | bounded PAUSE response under saturation; stale epoch rejected; media underflow safely mutes | crypto only simulated until implemented |
| **OPT-05 Independent clocks** | second board or true independent playback endpoint, common sample counter and reference measurement | drifting oscillator, delayed line, measured resync, phasing/skew within declared uncertainty envelope | cannot validate on one MCU |
| **OPT-06 Raw optical PHY** | AFBR transceivers, own electrical PCB/wiring, duplex; verify 3.3V signaling | error injection, deterministic framing, throughput and safe miswire recovery | no unsupported PCB or bitrate promise |
| **PWR-01** | independently monitored DC power and hardware cutoff; first own PCB | rails/OVP/UVP/thermal fault response with low voltage and safe current limits | final AC mains integration not authorized by simulation |
| **DAC-01** | one DAC+amp channel, then 3, then 7 | noise floor, startup mute, phase/latency, thermal, no speaker damage | progressive open evidence |
| **CAB-LAST** | final beautiful, calculation-driven shell | matches measured acoustic and thermal contract; no silent regression | explicitly last |

**Power at OPT-01–06:** factory power for board/converters. Never probe mains circuitry. Maintain separate wall supplies if available without defeating grounding safety.

### Measurements and statistics

Do not call received Ethernet UDP payload a raw optical **BER** test. FCS/error frames are usually discarded in PHY/MAC; without PHY raw bit counters, what we observe are *packet omission/corruption, CRC at application layer, clock timestamp distribution, and firmware statuses*. To estimate true raw optical BER use suitable PHY bit error counters or a dedicated PRBS tester at transceiver IO.

If **N independent transmitted packets** yielded zero losses/mismatches, the approximate one-sided 95%-confidence upper bound under a stationary independent Bernoulli failure assumption is `1-0.05^(1/N) ≈ 2.996/N` **per packet**, not a certified zero-error guarantee. Independency and stationarity are hypotheses; burst failures require separate analysis.

Record CSV+JSON with: board revision, code hash, converter serials, fiber type/length, software versions, payload rate, queue depth, clock policy, durations, sent/received/duplicate/lost/out-of-order/corrupted, RTT distributions, CPU load, reset links, faults, conditions, issue IDs. Artifacts should be independently replayable.

## Practical first purchase (ONLY if board verifies)

- 2 × same-model duplex SC 100BASE-TX→100BASE-FX **multimode** media converters;
- 1 × duplex SC-SC 50/125 OM2 or OM3 patch cord 1m; later 2m and 5m of same type;
- 2 × short standard copper RJ45 patch cords to PC and NUCLEO;
- existing stock USB supplies, no custom mains and no direct optical photodiode wiring yet;
- PC Ethernet port or existing adapter (verify first).

Do not mix SC with TOSLINK / Broadcom Versatile Link plastic fiber; different optical standards, connectors, fiber and wavelength, not interchangeable. A bare laser-diode driver is NOT a safe replacement for a certified transceiver module.

## Documentation and source roots

- [Original optical four-plane architecture](wired-audio-fabric/FOUR-PLANE-ARCHITECTURE.md)
- [First protocol mathematical and adversarial logical model](wired-audio-fabric/CONTRACT.md)
- [Production topology ADR-001](ADR-001-ACTIVE-THREE-WAY-SUB.md)
- [Physical supply later gate](../shared-power/README.md)
- [Simulation and protocol/throughput readiness checks](simulation/optical_bench_contract.py)

**No optical hardware has yet been tested.** This is a design and sourcing plan with source-linked manufacturer claims and observed vendor prices, not measured hardware claims.
