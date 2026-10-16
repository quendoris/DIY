# Development order

| Gate | Bench | Evidence required |
|---|---|---|
| K0 | Formalize layout, industrial design and acoustic test plan | Key positions, sharp-edge samples, finish/legend samples, clear cluster gaps, target stroke, seals, acoustic and event-order definitions |
| K1 | One **passive tactile** magnetic key + metal-cap acoustic trial | **Mandatory:** convincing passive force peak/drop, self-return and quiet travel with coil disconnected; force/travel plots, top/bottom-out and cap resonance tests |
| K2 | One analog key with MCU | Calibration, latency/jitter, reset behavior and temperature drift |
| K3 | One active tactile/damping key (optional) | Bidirectional force modulation; fast-press deceleration limits; thermal/power limits and coil noise |
| K4 | Four-key magnetic cluster | Neighbor crosstalk, simultaneous operation, MUX/ADC timing, replaceability |
| K5 | 16-key prototype matrix | Real wiring, key profiles, timestamped event log and HID reports |
| K6 | Basic wired prototype | Typing use, NKRO tests, custom config and firmware recovery |
| K7 | Sealed switch module / cleaning bench | Safe washing procedure, ingress and corrosion observations |
| K8 | Full development keyboard | Long-duration field use, fatigue and acoustic measurements |
| K9 | Final metal keycaps/chassis | CNC only after dynamics and interfaces are frozen |

## Design and acoustic research gates

- [DESIGN-LANGUAGE.md](DESIGN-LANGUAGE.md): angular chassis, opaque matte high-profile keys, black legends, and discreet localized lighting.
- [ACOUSTICS.md](ACOUSTICS.md): separate keycap resonance, top/bottom-out, guide rattle and electrical noise, with reproducible listening and instrumented measurements.
- Do not order final keycaps until multiple metal-keycap samples have been compared acoustically.
- Silence is a pass/fail user-experience requirement, not a low-priority refinement.

## Mandatory first gate

[PASSIVE-MAGNETIC-TACTILITY.md](PASSIVE-MAGNETIC-TACTILITY.md): a high-quality tactile magnetic key must work with actuator coils disconnected. No coil matrix or premium CNC until this passes.

## Priority

**Do K1–K4 before committing to full-size hardware.**

Reuse software infrastructure and bench instruments where practical from `projects/custom-mouse`, but do not assume its lever mechanism scales directly to a keyboard key.

## Exit criteria

The final keyboard is not considered validated by marketing numbers alone. It needs measured stroke variation, missed/phantom key counts, worst-case event-handling jitter, acoustic test conditions, cleaning tests and cycling data.
