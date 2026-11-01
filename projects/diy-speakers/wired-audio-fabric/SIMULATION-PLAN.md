# Software-First Validation Program

Status: design sequence, not a hardware purchase proposal.

## A0 — Numeric and information-theoretic contracts

- Define supported source formats (FLAC, MP3, generated signals), exact digital sample/representation invariants and explicit quality changes.
- Define PCM channel topologies including 2.0, 2.1 and the five independent driver-feed model.
- Prove rate and buffer calculations over representative and worst-case source traces.
- Record sample rates, bit depth, group delay and transform error bounds.

## A1 — Deterministic receiver model

- Versioned sessions/epochs, preloaded audio blocks, monotonic sample counters and independently authenticated control.
- Events: play, pause, stop, flush, route change, clock fault, old message replay, late packet, source disconnect.
- Reproducible failure injection and explicit assertions.

First runnable reference in [simulation/](simulation/README.md).

## A2 — Transport alternatives

Compare:
- USB Audio Class + separate command endpoint vs custom compliant USB bulk protocol upstream.
- fiber Ethernet link with application-level framing vs existing optical digital audio PHYs downstream.
- link control/telemetry traffic independent of full audio buffer.

Report wire/payload rate and real deadline distributions. Wired fiber has high expected reliability at short distances; avoid adding arbitrarily heavy FEC without a demonstrated loss/burst model. Evaluate ARQ, CRC and optional erasure coding by actual required latency and memory budget.

## A3 — Clocks and synchronization

Model two independent satellites and a sub with oscillator tolerances, relative phase, free-running drift, recovery and scheduled sample-index playout.

Compare architecture options:
- selected shared physical reference clock / distributed word clock;
- PTP-style clock estimates with hardware timestamps and disciplined local oscillators;
- per-endpoint ASRC and explicit conversion error/latency budgets.

No 'sample-aligned' claim from equal file contents alone.

## A4 — Security and trust

- Independent identity enrollment and revocation for controller/endpoints;
- separation of control authorization and audio transport;
- replay-safe commands/epoch transitions;
- document CRC (fault detection) vs MAC (adversarial message authentication);
- no content encryption **by default** only when defined threat model allows, with optional hardware offload if needed.
- power reset/secure-boot/firmware rollback and cross-device authority tests.

Proofs in Lean/TLA+ may establish state-machine invariants **subject to their assumptions**; crypto primitives and hardware must be chosen and independently validated.

## A5 — Power

Each satellite, sub and controller independently mains powered. Require certified external supply modules / professional isolation, then low-noise rails as needed. Model and measure under/overvoltage, overtemperature, short protection, earth/ground and output noise separately from efficiency ratings.

Do not modify consumer ATX power supplies and claim existing safety/efficiency certifications remain valid after modification. No exposed dangerous mains in early prototypes.

## A6 — System integration

- Central routing DSP must have a bypassable content path and versioned speaker calibration;
- IEC/USB/optical connectors, thermal and acoustic power ceilings;
- map end-to-end failure injection: sudden pause, stop, unplug, missing frame, clock reset, sub dropout, controller reset, invalid auth and multi-fault combinations;
- compare formal predicted control/sample alignment to eventual electrical/acoustic measurement.

## Proposed FIRST milestone

Implement a no-hardware, tiny executable reference state machine with strict tests for control preemption, epoch-based flush, buffer underrun handling, source-independent bit accuracy, audio bandwidth, clock drift and hypothetical erasure FEC. Prove or find counterexamples before selecting a USB device controller or optical transceiver.
