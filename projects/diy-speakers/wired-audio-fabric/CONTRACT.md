# Contract: Data, Commands, Clocks, Trust and Failure

Status: formalization sketch, **not a completed mathematical proof or cryptographic design**.

## Fundamental division of concerns

The sound engine builds or decodes source content. The digital controller schedules, routes and optionally applies speaker-calibration DSP. Receivers consume strictly ordered sample blocks and independently convert to analog audio. Power/analog/acoustics are separate models.

### Audio transport data model

A block carries at minimum:

```text
protocol_version
session_id
stream_id
format_id (PCM_F32, PCM_S24_LE, lossless frame family, ...)
epoch
first_sample_index
frame_count
channel_layout_id
payload_length
integrity (CRC for accidental errors; authenticated integrity under adversarial model)
payload
```

No silent lossy fallback, unannounced sample-rate change or channel reassignment. Format changes occur as a separately authorized, scheduled transition.

### Control events

```text
session_id
epoch
monotonic_command_counter
action: PLAY | PAUSE | STOP | FLUSH | SET_GAIN | CHANGE_ROUTE
effective_sample_index OR ASAP_with_bounded_latency
command_auth_tag/verified_provenance
```

Commands do not depend on the audio FIFO being drained first. Explicit STOP/FLUSH invalidates the old epoch, making replayed/stale audio blocks rejectable. PLAY after pause resumes a documented sample position or starts a new epoch; neither behavior may be implicit.

### Clock contract

For every receiver: local audio clock + measured relation to the shared time domain. Sample-index-to-time mapping, phase/skew tolerance, drift tolerance, acceptable rate correction and clock-loss behavior must all be specified. Do not promise that identical PCM bytes imply coherent stereo without shared clock/discipline.

### Control latency

Upper bound should be composed from verified worst-case components:

```text
L_effect <= L_control_link + L_auth + L_scheduler
            + L_block_boundary + L_DAC_filter + L_amp
```

Each bound is separately measured or justified. The inequality holds only if every contributing bound is valid and the receiver is in a supported state. 'Instantaneous' is a goal, not literal zero time.

### Example invariants — require model proof

- **P1 — Authenticity:** no accepted state-changing command without validated session/authorization.
- **P2 — Anti-replay:** command counters and epochs never move backward; old sessions cannot alter a new session.
- **P3 — Ordering:** a receiver may render sample index i only from the correct stream+epoch and previously verified block.
- **P4 — Pause:** once PAUSE has taken effect, no future buffered PCM is emitted until authorized RESUME.
- **P5 — Flush:** after an epoch change, stale blocks cannot become playable.
- **P6 — Fault handling:** deadline miss never produces *unverified* audio; choose deterministic mute/fade/resync instead.
- **P7 — Channel alignment:** within an explicitly stated clock-offset and propagation-delay envelope, corresponding left/right/sub sample indices play within a target skew bound.
- **P8 — Isolation:** PC cannot issue direct endpoint commands outside the authorized controller route/policy.

Proving P1/P2 cryptographically requires an actual verified cryptographic implementation, not a boolean `authenticated=true` in a simulation. Proving P7 additionally depends on measured hardware clock and latency parameters. Lean proofs are proofs about *formalized assumptions/models*; a specification may be free of `sorry` and custom axioms and still rely on underlying logic and hardware assumptions.

### Representation and sampling

- Finite-precision PCM can represent a finite vector of digital samples **exactly** as bits and can be transported without loss or codec degradation.
- Shannon–Nyquist exact reconstruction is an ideal theorem for appropriately bandlimited signals and exact sampling; finite quantization of arbitrary analog amplitude is a separate nonzero error source.
- A finite symbolic description can reconstruct a function exactly **only for specified function classes**, e.g. a synthesizer with a fully specified generator and parameters, not for every analog waveform.
- Any finite lossless encoding must be invertible on its declared source domain. Unbounded worst-case compression gain cannot be promised.

### Identity graph

Trust edge PC→controller and trust edges controller→endpoints. Endpoints only accept controller-authorized commands. The controller knows which endpoint streams it routes but need not possess unnecessary user metadata or audio library information.

Control authority and content confidentiality are distinct. It is valid to **not encrypt** a physically private optical PCM link. But unauthenticated audio chunks may still be replaced/replayed by a malicious middle device; choose a threat model and integrity granularity. Cheap CRC for accidental noise is not a substitute for MAC under adversarial attacks.

### Composition proof obligations

If source decoding, transport, buffer, sample-clock and DAC models are each verified under assumptions, their composition also requires interface contracts: matching samples/channel layouts/epochs, bounded jitter vs buffer depth and consistent clock domain. An isolated unit-test suite is not a proof of the composed audio system.
