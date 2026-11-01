# OPT-00 through OPT-04 — Runnable Lab Procedure (Before Custom Power)

Date: 2026-11-01. Status: **prepared**, no physical board, media converter or fiber tested.

This is a strict research procedure, not a declaration that a link or embedded device already works.

## 0. Verify physical board and IDE

The exact original `NUCLEO-H7S3L8 (MB1737)` should have `STM32H7S3L8H6` MCU, built-in 10/100 Ethernet via LAN8742 and RJ45, STLINK-V3EC and USB-C. The marketplace string `STM32H7R3L9` is inconsistent with official ST identifiers.

Before wiring or firmware:
- take top/bottom PCB photos with clearly legible MCU and board revision labels;
- confirm connector reference designators, power pins, ST-LINK detection, firmware version and actual MCU recognized by STM32CubeProgrammer;
- choose ST official **STM32CubeH7RS** examples for `NUCLEO-H7S3L8`, not generic older H7; this platform typically uses a `Boot_XIP` stage in internal 64KB flash and an application in 256-Mbit external NOR flash;
- do not change device lifecycle/option bytes, enable irreversible boot security or provision permanent keys merely to make an Ethernet echo example run;
- restore debugger access / factory baseline before attempting custom TX/RX.

If this is a modified clone with `STM32H7R3L8` rather than STM32H7S3L8H6, firmware and pinout must be revalidated for that actual PCB.

## 1. Simulate code first

```bash
cd projects/diy-speakers/simulation
python3 -m unittest -v
python3 optical_bench_contract.py > optical_estimates.json
```

For the **host-only, actual UDP localhost test**:

Terminal A:
```bash
python3 optical_host_probe.py serve --bind 127.0.0.1 --port 50808 --limit 100
```

Terminal B:
```bash
python3 optical_host_probe.py probe --host 127.0.0.1 --port 50808 --count 100 --size 1024
```

The host probe uses UDP packet framing `!4sBBHIQII`, 28 bytes, followed by payload length 0..1444. Fields:
```text
magic = OPTF
version = 1
type = REQUEST (1), REPLY (2)
flags = 0
epoch = u32
sequence = u64
payload_len = u32
crc32 = u32 over network-order [epoch:u32, seq:u64] + payload
payload = deterministic SHAKE256-generated test bytes
```

All integers use **network byte order (big endian)**. An echo endpoint verifies CRC, magic, length and type, and returns REPLY preserving epoch, sequence and payload. This is a diagnostic test format, *not* an authenticated production protocol. CRC32 is for accidental corruption; the deterministic test payload is not encryption or cryptographic proof.

This initial synchronous request/response test does **not** saturate the link or represent production buffered audio. Use a separate windowed/asynchronous benchmark after the basic integration works.

## 2. First genuine MCU baseline

A single NUCLEO and one PC suffice:
- direct CAT5e, PC ethernet ↔ board RJ45 (static addresses e.g. PC `192.168.77.1/24`, board `192.168.77.2/24`, isolated test network);
- flash an **actual STM32CubeH7RS** Ethernet echo example (ST's example may be TCP echo, unlike the Python UDP protocol); confirm ordinary ping/echo and counters BEFORE adding custom UDP firmware;
- then implement **compatible UDP test echo** on the MCU and verify it independently against the Python host (not present in repository yet);
- retain known-good app and build artifacts, clock tree and firmware hash.

Only after this gate passes, place media converters and optical fiber in between.

## 3. Fiber bench setup and safety

```
 PC RJ45
     |  electrical CAT5e, short
 100BASE-FX media converter #1 (multimode duplex SC)
     ||
 Duplex SC/UPC–SC/UPC 50/125 OM2 or OM3 fiber patch: 1m, then 2m, then 5m
     ||
 100BASE-FX media converter #2 (same model, duplex MM)
     |  electrical CAT5e, short
 NUCLEO-H7S3L8 RJ45
```

Use separately plugged normal factory-approved DC adapters for the converters and USB for the MCU. Verify adapter voltage/current polarity; do not connect any 5V powered TTL output directly to a non-tolerant STM32 3.3V pin. Do not peer into powered optical sockets.

When using duplex SC multimode equipment, choose matching **50/125 μm** OM2/OM3 fiber patch cables; **Broadcom POF Versatile Link and Toshiba TOSLINK use DIFFERENT connector, fiber and optical standards**. No generic interchangeability.

## 4. Test matrix and independent findings

For each of 0m copper-only, then fiber 1m,2m,5m:

| Parameter | Nominal sweep | Report |
|---|---|---|
| Media input load | idle, low PCM equivalent, 16.128Mb/s full seven-channel equivalent, synthetic stress up to 80% observed application capacity | throughput over 30s and sustained intervals; no promised performance |
| Packet payload | 32, 512, 1024, 1444 bytes plus test header | loss, MTU/fragmentation, counters |
| Playback conditions | 96kHz 24b, 192kHz 24b, 192kHz 32b; 128 frames/block then adapt MTU | application frame pacing, queues, FIFO margin |
| Cable | 1,2,5m, connector reseating, controlled bends within patch cable spec | link up/down duration, CRC, tested max insertion cycles |
| Control | STOP and PAUSE while media queue is full, discard old epoch after restart | time to execute, old frame rejection, safe fallback |
| Faults | disconnect one fiber strand, optical disconnect/reconnect, receiver stall, MCU software reset, wrong session/CRC | deterministic per-node diagnostics, never output unverified data |
| Telemetry | board reset reason, Ethernet link status, PHY counters if available, CPU and memory usage | `READY/DEGRADED/UNKNOWN/FAULT` restricted to actually supported sensors |
| Timing | host RTT distribution, embedded timer capture where possible; later hardware timestamp and oscilloscope | NEVER claim 5ns/m propagation based on jittery PC RTT |
| Endurance | first shorter smoke, then 30-60min, then overnight separate run | raw CSV+JSON and 95% bounds under declared failure model |

Also compare **actual electrical RJ45 path vs converted fiber path** with the same MCU firmware and host software. If optic RTT is larger or more variable, determine which part of the chain is responsible rather than ignoring extra converter latency.

Do not label an end-to-end UDP zero-loss result as `BER=0`: ordinary Ethernet hardware drops corrupted frames. Use `correct_reply / sent`, missing/duplicate/reordered and CRC counters. BER requires access to raw physical error measurements or a dedicated PHY PRBS tester.

## 5. Strict next crystal layer

Pass conditions for OPT-02:
- board identity and correct pin/boot firmware verified;
- PC direct Ethernet baseline passed with logged firmware hash;
- two verified 100BASE-FX multimode SC duplex converters and matching optical patchcord;
- 1m connected, received stream with matching source bytes, correctly detected corrupt frame and stale epoch;
- **measured** results with raw logs and measured quantity, not qualitative 'works fine';
- documented test setup, electrical supplies and unknowns.

At **OPT-03**, repeat at 2m and 5m. Longer cables may add propagation but should not need manual recalibration to remain *functional* at basic packet level; precise clock alignment is a separate OPT-05 qualification requiring two independent real clock domains.

The physical test does not wait for the custom mains power supply. Only when the transport layer is characterized do we integrate a locally protected DC power design.
