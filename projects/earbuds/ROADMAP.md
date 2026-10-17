# Roadmap — Earbuds

| Gate | Deliverable |
|---|---|
| E0 | Record fit, grip, sound, battery service and ANC requirements; collect real transducer/microphone/cell datasheets |
| E1 | Build FLAC/MP3 reference decode tests and a common PCM/DAC interface; verify channel/sample-rate/gapless behavior |
| E2 | Model audio packet scheduling, buffer depths, retransmission deadlines, L/R synchronization, power and worst-case payloads |
| E3 | GNU Radio waveform/channel simulations across SNR, interference, body shadowing, timing/frequency offsets and fading; define a candidate link budget |
| E4 | Numerically model DAC/amp, transducer and ANC/transparency loops with declared assumptions; sweep fit leakage, phase/delay, limiter and output constraints |
| E5 | Component-level power/thermal model for radio, decoder, DAC/amp, ANC and sensors; determine feasible battery budget with margin |
| E6 | Confirm radio and digital-audio behavior on development boards against predicted payload, latency, errors, synchronization and power |
| E7 | Confirm ANC and acoustic predictions on a calibrated safe measurement fixture; tune using measured transducer/microphone data |
| E8 | Prototype fit, grip, touch controls and removable cylindrical battery cap with seals and short-circuit protection |
| E9 | Confirm RF and sound in metal/dielectric enclosure; final charging, ingress, thermal and reliability tests |

No final metal machining or custom production PCB until the corresponding simulation and development-board gates pass. Physical results that diverge from prediction require model correction and rerun, not an undocumented tuning workaround.

Joint dependency: player and earbuds share the audio transport contract. No lossless/bit-perfect or ANC cancellation claim is accepted without corresponding evidence.
