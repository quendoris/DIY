# Software Validation Bench — First Gate

This directory begins the simulation-first workflow with a small, reproducible packet-level model. It deliberately uses Python's standard library only.

## Files

- `packet_model.py` — deterministic FIFO radio-queue model with packet overhead, PHY rate, effective link efficiency, random loss, retry/backoff, latency/jitter and a playout deadline.
- `test_packet_model.py` — unit tests for high-capacity, capacity-limited, variable-payload and reproducibility cases.

## Run

From this directory:

```bash
python3 -m unittest -v
python3 packet_model.py --duration-seconds 60 \
  --packet-interval-ms 10 \
  --payload-bytes 5760 \
  --phy-rate-mbps 4 \
  --link-efficiency 0.75 \
  --overhead-bytes 32 \
  --playout-buffer-ms 40
```

For a variable packet-size trace, use `--payload-trace-bytes`:

```bash
python3 packet_model.py --payload-trace-bytes 220,260,410,180,720
```

Trace sizes repeat cyclically and represent **payload bytes per packet**, not codec bit rates. Later corpus tooling should produce measured packet-size traces from actual FLAC/MP3 files and record the packetization method.

## Interpretation

This is an intentionally transparent **packet-level scheduling model**, not a physical RF waveform simulator and not a prediction of audible quality. It assumes one FIFO transmitter and handles each packet's retries before proceeding to the next packet. This conservative/simple scheduling policy is only a baseline; alternative retry scheduling, FEC, interleaving, multi-queue traffic and actual protocol framing must be compared before architecture freeze.

- `phy_rate_mbps` is nominal PHY rate.
- `link_efficiency` models the fraction available to modeled on-air packet bits after aggregate PHY/MAC coding and scheduling losses. Do not treat it as a measured device value.
- `overhead_bytes` represents per-packet headers, authentication/tag and other modeled framing.
- `loss_probability` is independent per transmission attempt; real interference is often bursty and correlated.
- `base_latency_ms` and `jitter_sigma_ms` are abstract propagation/scheduling-delay terms.
- `playout_buffer_ms` is the packet deadline budget from packet generation.
- Payload traces repeat cyclically; a real test should use captured frame/packet sizes and a deterministic seed.

The output's deadline-miss rate is not an audibility score. A miss is simply a packet that did not arrive before its modeled playout deadline.

## First experiments

1. Run the tests.
2. Sweep payload size/rate, efficiency, packet overhead, loss, retries and playout buffer.
3. Compare constant-rate PCM traces against measured FLAC and MP3 packet-size traces.
4. Record not just averages but p95 queue delay, deadline misses, retries and on-time goodput.
5. Keep each configuration JSON and result JSON under a run-specific evidence directory with tool/version, source commit and seed.

## Known omissions

No RF waveform, coding, carrier-frequency offset, timing recovery, multipath/fading, burst interference, antenna pattern, clock drift, stereo interleaving, decoder CPU load, energy model, ANC scheduling or actual codec decoder is implemented here. These belong in subsequent gates. GNU Radio waveform simulation and real codec reference tests must remain separate so their evidence is not conflated.
