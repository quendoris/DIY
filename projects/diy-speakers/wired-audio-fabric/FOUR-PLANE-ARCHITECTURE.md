# Four-plane optical audio fabric — architecture v0.1

Date: 2026-11-01. Status: **requirements interpretation and falsifiable architecture**, not a completed security/clock/protocol proof.

## User-proposed four simultaneous functions

1. **Attestation + health monitoring (trust/diagnostics)**: the computer learns from the controller whether the distributed speakers have authenticated and their independently reported health is within the declared operating envelope. Diagnose abnormal temperature, rail voltage/ripple, amplifier fault, clock instability, optical CRC/BER and watchdog reset.
2. **Control**: prioritized, independently authorized low-volume messages: Play, Pause, Stop, mute, gain, route, gain limits, fault acknowledge and firmware lifecycle. Non-repeating session/counter based integrity. Commands must never wait for audio FIFO to empty.
3. **Audio**: large bandwidth, buffered digital data. The owner prefers **clear (not encrypted) content**, provided the threat model allows it; retain integrity/replay policy separate from confidentiality.
4. **Clock synchronization**: its own priority/timing budget with local disciplined DAC clocks and a common sample timeline. Fiber lengths of several meters are explicitly supported after propagation and device delay compensation.

These are **four logical planes, not necessarily four optical strands**, processors, sockets or independent physical transceivers. The design must demonstrate *bounded interference* between them, including multiple simultaneous failures. A scheduling hierarchy with dedicated timing slots or priority queues may be enough. For severe fail-safe actions, local independent protection and watchdogs are not contingent on the shared link.

## Trust graph and precise statement of guarantees

```text
                 [ PC / AUDIO SOURCE ]
                  paired to controller
                         |
                  USB-C link
                         |
               [ CONTROLLER / ROUTER ]
             identity + policy + clocks
                /             |           \
         duplex fiber    duplex fiber   duplex fiber
             |                |              |
         LEFT unit        RIGHT unit      SUB unit
           root key          root key       root key
           monitor           monitor        monitor
           DAC+amp           DAC+amp        DAC+amp
```

The computer learns a controller-authenticated **signed status report** for the whole system; it does not need the endpoint private keys. Endpoints trust the enrolled controller identity. The controller *does* know which endpoints it controls: privacy minimization is not logical ignorance.

**Identity != approved firmware != live health != acoustic correctness.** These are different claims and require separate evidence.

- Identity: challenge-response with an asymmetric private key in a hardware trust anchor.
- Firmware state: authenticated/measured boot bound to known software versions/measurement values, secure update and rollback resistance where attainable; needs an immutable first stage and a trusted measurement path. A secure element alone does **not** automatically attest arbitrary MCU RAM/firmware.
- Freshness: verifier nonce, session identifier, monotonic counters, expiration and signed/MACed reports.
- Health: independently instrumented rail voltage and current, temperature, fan tachometer if present, reset/fault latches, local clock offset, link error counts and amplifier electrical fault indicators. A device self-report may lie if its privileged firmware is compromised; independent monitor ICs, hardware cutoffs and controller cross-checking reduce but do not eliminate this risk.
- Acoustic correctness: DAC/output loopback and microphone/accelerometer measurements where required. A successful secure handshake cannot prove the speaker sound output is correct.

### Attack boundary: hashes and authentication

**SHA-512(data)** is an unkeyed digest. Whoever replaces a file can recalculate its digest; it is not an authentication mechanism. Likewise an endless sequence of unkeyed 'unrepeatable hashes' does not grant authority.

Potential protocol: pinned device key -> challenge signature/verified boot -> authenticated session -> MAC over `(version, device_id, session, epoch, counter, action, parameters, execution-time)`. HMAC is a standards-based keyed authentication method; an implementation should use mature primitives and assessed key derivation rather than original cryptography.

The owner's desire to avoid bulk encryption is compatible with **MAC-authenticated commands** and with **MAC-authenticated or batch-committed clear PCM**, depending on attacker model. CRC alone is for accidental corruption. The initial handshake does not authorize arbitrary later *clear unauthenticated* packets under an active attacker.

### Decision: what does the PC see?

Use a status record rather than an unjustified 'all perfect' bit:

```
status_version
system_epoch
controller_identity
measurements_age_ms
clock_reference_state / worst_estimated_skew_ns
audio_buffer_margin_ms
optical_link_errors
endpoint_state[L/R/SUB]: authenticated, firmware_measurement,
                        independent_power_rails_ok, amp_faults,
                        temp_margin, local_clock_lock, last_heartbeat_age_ms
aggregate: READY | DEGRADED | MUTED | FAULT | UNKNOWN
reason_codes[]
```

`READY` means all **specified, instrumented** health contracts passed recently, not a guarantee of no undetectable faults. Missing, expired or untrusted telemetry results in `UNKNOWN` or `FAULT`, never unqualified READY.

## Control-plane execution

- Separate authenticated control admission from media packet acceptance.
- Scheduled commands target a future **sample index** on the shared timebase, or execute ASAP with a bounded measured worst-case latency.
- STOP/FLUSH advances the epoch; preloaded old-epoch samples are discarded.
- PAUSE freezes the local playout cursor without draining data. MUTE/OVERTEMP can be enforced by analog/digital local hardware regardless of network availability.
- Split queue priorities: safety & stop > synchronization/time > normal control > health reporting > audio bulk, while reserving minimum periodic slots to avoid starvation of required timing/control.
- Clock/safety priorities must be tested during 100% audio traffic and at invalid/flooded control load.

## Clock and fiber length

The constraint is not 'fiber length never affects synchronization'. Light travels at about 2×10⁸ m/s in typical silica optical fiber, giving about **5 ns/m one-way**. An extra 5 m adds approximately **25 ns propagation difference** before transceiver, serializer, buffers, DSP, DAC reconstruction and speaker acoustic distance are accounted for.

At 96 kHz one sample lasts **10.4167 μs**. Cable propagation differences of a few meters are usually minor relative to a sample, but a coherent multi-speaker system must estimate/bound and, where needed, compensate total delays.

Without clock discipline a 50 ppm relative oscillator error at 96 kHz builds ~4.8 samples of drift per second. Timestamps are not enough alone: a local PLL/VCXO/ASRC or a qualified shared clock must reconcile ongoing rate mismatch.

For synchronization research compare shared-clock optical reference and IEEE 1588/PTP-style hardware timestamping with measured link asymmetry. Subwoofer positioning also introduces substantial **acoustic time-of-flight** changes (~2.9 ms per meter in air), orders of magnitude greater than fiber propagation. DSP/limiter latency and acoustic output phases require calibration.

## Loss and fault behavior

- corrupted media block: CRC rejects; per-session keyed MAC or frame commitment if integrity is adversarial requirement;
- missed media deadline: do not emit unverified data; bounded mute/fade/hold according to format and limits;
- clock out of bounds: freeze/safe mute and request resynchronization, without loud snap;
- endpoint loses attestation: remove privileged control authority; deterministic power/quiet fallback;
- controller disappears: local thermal/electrical protection remains autonomous, mute by defined deadline;
- fan stalls or rail goes out of range: temperature-dependent controlled power reduction and/or local amp mute;
- compromised PC: cannot alter endpoint firmware or bypass controller's authenticated authorization policy.

## Reference sources

- NIST FIPS 198-1 HMAC: https://csrc.nist.gov/pubs/fips/198-1/final
- NIST SP 800-193 protect/detect/recover: https://csrc.nist.gov/pubs/sp/800/193/final
- IEEE 1588/PTP time sync: https://standards.ieee.org/ieee/1588/6825/

## Next milestone

A deterministic four-plane event model to falsify the `READY` status and control preemption invariants; bounded timing simulations next. No cryptographic security, hardware-clock accuracy or physical completeness claim until implementation/instrumentation evidence exists.
