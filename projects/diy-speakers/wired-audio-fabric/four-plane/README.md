# Four-plane contract simulator

```bash
cd projects/diy-speakers/wired-audio-fabric/four-plane
python3 -m unittest -v
python3 plane_model.py > demonstration.json
```

This **Python stdlib, deterministic logical contract model** demonstrates:

- three separately assessed endpoint telemetry reports, freshness and status aggregation;
- `READY / DEGRADED / MUTED / UNKNOWN / FAULT` decision reasons;
- local amplifier/power trip overriding otherwise valid identity evidence;
- clock unlock + low audio buffer states;
- scheduling priority of local safety and time/control events ahead of audio traffic;
- a simple numerical estimate for extra fiber length and oscillator drift.

**Not implemented**: real cryptography, secure boot, independent hardware monitoring, actual optical PHY, PCB power measurements, operating-system real-time guarantees, deadline-bounded scheduling, clock discipline/PLL/ASRC, physical speaker/acoustic propagation correction or full compositional formal proof.

A priority heap only makes dequeue order deterministic; it **does not** prove that a real link guarantees latency under saturation. Also status telemetry truthfulness is **assumed** by the simulator. The hardware project requires independent sensors/protection and attestation before translating these checks into a meaningful guarantee.

Tests exercise deliberately failing conditions; code only certifies its own simplified logic against those assertions.
