# First Wired Audio Fabric Simulation

This executable baseline models **a receiver's digital control and buffer contract**. It is not a USB/fiber PHY simulator, digital clock servo, cryptographic implementation or acoustic/analog signal model. Only Python stdlib is needed.

## Run

From `projects/diy-speakers/wired-audio-fabric/simulation`:

```bash
python3 -m unittest -v
python3 fabric.py > demo.json
```

## Demonstrated in the code

- Five independent output channels of 96 kHz/24-bit PCM require 11.52 Mbit/s raw application payload.
- A 128-sample block at 96 kHz is 1.333 ms. Buffer depth must be specified in samples/time rather than vaguely '3–4 stages'.
- Free-running clocks differing by 50 ppm at 96 kHz accumulate 4.8 sample periods per second, 288 per minute.
- A buffered source can be paused **without exhausting the audio FIFO first**, and can resume from its preserved sample index.
- STOP invalidates the old stream epoch. Old blocks/commands cannot resume playback.
- CRC32 detects the injected accidental corruption; wrong session IDs, duplicates, old epochs and old command counters are rejected.
- Underflow returns no audio bytes (a caller can mute/fade) rather than passing unverified content.
- The toy ideal-MDS erasure model allows at most the parity-block count of known erasures; this is **not** an FEC encoding/decoding implementation.

## Safety and epistemic boundaries

- The `verified_by_auth_oracle` flag simulates the outcome of a separately verified cryptographic authenticator. This simulator **does not implement or prove cryptographic authenticity**.
- `next_audio` is called at an assumed output block boundary. No real-time scheduling, DAC/filter delay, transport delay or maximum Pause response time is measured or guaranteed.
- No actual analog signal has been reconstructed; sample identity is asserted only for transmitted digital byte payloads.
- No physical power supply or electrical interface is connected.
- No channel alignment across **independent receivers** is implemented. That requires a separately specified clock discipline/renderer clock domain.
- CRC is not adversarial integrity protection; it is not a MAC.
- FEC capacity is a mathematical *erasures-only* bound on an ideal MDS code, not a guarantee that any QR-style redundancy will recover 50% of arbitrary corruption.

## Next gates

1. Add an event-driven simulator for link delay, loss bursts and independently drifting DAC clocks.
2. Add bounded control-event latency with a separately modeled priority queue and a target worst-case guarantee.
3. Specify and model real optical physical-layer candidates with full-duplex command traffic.
4. Model a multi-device synchronized sample-index playout timeline and independent safety fault paths.
5. Formalize authorization, epoch and buffer invariants in Lean/TLA+ after the state-space contract stabilizes.

See [../CONTRACT.md](../CONTRACT.md) and [../SIMULATION-PLAN.md](../SIMULATION-PLAN.md).
