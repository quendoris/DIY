# Architecture and validation notes

## Conceptual paths

```text
per-key magnets/sensors ─→ ADC/MUX or sensor bus ─→ sampled positions
                                                        │
                                                        ▼
                                             calibration/filtering
                                                        │
                                                 threshold/hysteresis
                                                        │
                                                timestamped event log
                                                   ┌────┴────┐
                                                   ▼         ▼
                                              USB HID    vendor protocol
                                               states    ordered telemetry

per-key displacement ─→ force-profile controller ─→ optional current driver/coil
```

Use DMA, deterministic sampling, explicit sequence numbers and ring buffers where they improve measurement. Do not assume 'every interrupt is highest priority' is a correct real-time design.

## Analog sensing

Compare **Hall effect vs TMR** empirically with the actual magnetic geometry, nearby metal and neighboring keys. Sensor technology alone does not guarantee accuracy or latency.

For 80–110 keys, budget:

- sensor power and bias stability;
- ADC channels and MUX settling time, leakage and crosstalk;
- simultaneous vs sequential sampling time skew;
- temperature/field drift;
- magnet orientations and interaction with adjacent keys;
- RGB PWM and active coil interference;
- mechanically repeatable calibration.

Each key needs its own ID/calibration data only if the module/interface actually supports service replacement.

## Magnetic return and active actuation

Permanent magnets provide passive return/rest equilibrium without consuming continuous coil power. Constraining guides/stops are still required; stable unconstrained passive magnetic levitation is not an assumed solution.

Actuator questions to test:

1. Return force vs displacement at several finger loads.
2. Control authority in both current directions.
3. Ability to create a tactile snap and damping without an audible metallic impact.
4. Energy/temperature under dense typing, prolonged key holds and many simultaneous operations.
5. Power-off and firmware-fault behavior.
6. Electromagnetic interaction between adjacent keys and their Hall/TMR sensors.

An individually driven coil on every key is **optional research**, not a baseline requirement; a USB power budget may make it unattractive. A passive-only magnetic keyboard is a valid outcome.

## Silence and waterproofing

Metal-to-metal collisions are prohibited in the normal stroke. Use replaceable compliant stops and constrained guides.

The noise target of ~30 dBA needs a documented method: room background, meter distance, typing speed, key set, peak vs equivalent level and acoustic weighting.

"Can be washed" is a **testable requirement**, not a consequence of applying epoxy. Design seals, drainage, corrosion protection, electrical isolation, wet USB prevention and drying instructions. Never promise IP65/IP67 until testing to the applicable standard is completed.

## Deterministic input semantics

Test at least:

- every key individually;
- all-key rollover and rapid chords;
- nearly simultaneous down/up edges at 0–5 ms separation;
- event queues at wraparound, overflow, disconnect/reconnect and rollover;
- worst-case scheduling jitter;
- complete HID report sequences;
- custom timestamped event-stream consistency.

The device cannot force generic host applications to reconstruct a strict temporal ordering of transitions that a standard HID report represents only as simultaneous state.

## Hot swapping

Separate three things:

1. User-removable metal keycap.
2. Mechanically removable magnetic actuator/stem assembly.
3. Electrically hot-swappable cartridge with module identification.

Contactless **measurement** does not automatically make modules electrically hot-swappable. The sensor/coil connectors, alignment and power-off procedure must be specified independently.

## References for baseline

- Wooting 80HE and 80HE+: https://wooting.io/wooting-80he
- Hall vs TMR analysis: https://wooting.io/post/hall-effect-vs-tmr-pause-the-funeral
- USB HID 1.11 specification: https://www.usb.org/sites/default/files/hid1_11.pdf
- QMK matrix ghosting: https://docs.qmk.fm/how_a_matrix_works

These sources establish existing capabilities and protocol constraints, not proof of our proposed mechanism.
