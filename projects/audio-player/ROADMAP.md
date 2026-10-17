# Roadmap — Local Audio Player

| Gate | Goal |
|---|---|
| P0 | Freeze requirements: formats, library capacity, listening profiles, lossless policy, acceptable import time, battery target and no-contacts constraint |
| P1 | Build trusted FLAC/MP3 reference corpus and deterministic decoder/PCM correctness tests; compare format-native transport with a lossless PCM path |
| P2 | Software packet-level model: **baseline implemented and CI-tested**; next compare measured format payload traces, alternate retry policies, stereo clock contract and energy model |
| P3 | GNU Radio waveform/channel simulation and link-budget sweeps; establish candidate modulation/coding, goodput, interference margin and latency budget |
| P4 | Simulate antenna position behind the rear dielectric insert with display, battery, PCB and metal enclosure present; record S11, efficiency/pattern assumptions and uncertainty |
| P5 | Model charging, battery SoC/temperature and the single-coil charge/cooldown/data schedule with coupled circuit, EM, data-link and thermal analyses |
| P6 | Confirm the chosen radio/antenna/audio pipeline on development boards against the simulation's predicted throughput, error rate, latency and power |
| P7 | Prototype display, embedded UI, local library and sealed single-button control |
| P8 | Run physical wireless-power, RF, thermal and ingress tests on representative material-stack mockups; reconcile discrepancies with models |
| P9 | Manufacture final metal housing only after P0–P8 evidence |

The software models must precede expensive physical integration. A simulation result only supports the assumptions represented by the model; development hardware and final assemblies confirm the high-risk predicted behavior.

The audio-link gate is shared with [earbuds](../earbuds/README.md). The proposed single-coil bulk-data link remains unresolved until its modeled bandwidth, coupling, heating and interference budget closes.
