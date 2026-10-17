# Engineering Notes — Earbuds

## Audiophile reference and measurement discipline

Treat the player and earbuds as one carefully engineered audio instrument. Reference complete signal paths—not only DAC-chip headline numbers—and record the actual measurement conditions. Track digital correctness, noise, THD+N, frequency response, channel matching, crosstalk, output impedance/load behavior, acoustic response, ANC stability, latency and power separately. See [../audio-system/REFERENCE-STUDY.md](../audio-system/REFERENCE-STUDY.md).

## Simulation-first radio and ANC gate

Use waveform and packet-level software simulation before selecting final radio hardware; use numerical acoustic/control models before building the ANC mechanism. Simulation inputs, uncertainty and unmodeled effects must be recorded. Development boards and calibrated acoustic fixtures later confirm the predictions. See [../audio-system/SIMULATION-AND-VALIDATION.md](../audio-system/SIMULATION-AND-VALIDATION.md).

## Radio proof gate

A Nordic nRF54H20-class part supports proprietary 2.4 GHz protocols with a stated PHY/throughput target up to 4 Mbit/s; **that is not an automatic application payload guarantee** and cannot alone justify worst-case 24/96 stereo lossless.

First test:

- sustained payload throughput and error/retransmit rate;
- bursts and interference from Wi-Fi and neighboring devices;
- head/body shadowing and changing orientation;
- packet deadline misses and audio-buffer underruns;
- L/R synchronization/clock drift;
- power draw and antenna detuning near a metal enclosure;
- encryption/authentication and recovery after reconnect.

Compare at least 16/44.1, 24/48 and 24/96 using actual music, incompressible test content and fallback behavior.

Official Nordic radio context: https://www.nordicsemi.com/Products/nRF54H20

## ANC vs audio

Music and ANC may use separate processing priority/domains, but ultimately share transducer dynamics. Require acoustic bench results before claims about '−45 dB' or any ambient-gain setting.

Safety concerns for a transparency/boost mode:

- controlled max output SPL;
- safe limiting and detection of unexpected loud inputs;
- limiter latency/dynamic stability;
- hearing safety under ANC/transparency transitions.

## Removable battery cartridge

The removable cylindrical battery is a priority, but '10400' or '10×35 mm' must not be treated as a known safe available part without sourcing and measurement.

The cap design needs seals, corrosion-resistant contacts, polarisation/short protection, retention, drop tests and an approved charger matched to actual cell chemistry.

The project is not automatically IPX7 simply because it has an O-ring.

## Metal body

The desire is a high-quality metal feel and a textured secure grip; radio still needs dielectric antenna volume. Test RF with wet fingers/ears, not only open-air on the bench.

## Reference baselines

- Nordic proprietary 2.4 GHz support: https://www.nordicsemi.com/Products/Wireless/2-4-GHz-proprietary
- FLAC: https://www.rfc-editor.org/rfc/rfc9639.html
- Existing Bluetooth lossless capability: https://www.qualcomm.com/snapdragon/audio
