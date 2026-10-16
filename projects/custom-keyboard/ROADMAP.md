# Development order

| Gate | Bench | Evidence required |
|---|---|---|
| K0 | Formalize layout and test plan | Key positions, target stroke, seal strategy, acoustic and event-order definitions |
| K1 | One passive magnetic key | Reproducible displacement/force/return curves and off-state stability |
| K2 | One analog key with MCU | Calibration, latency/jitter, reset behavior and temperature drift |
| K3 | One active tactile key (optional) | Bidirectional force modulation, thermal and power limits, acoustic measurements |
| K4 | Four-key magnetic cluster | Neighbor crosstalk, simultaneous operation, MUX/ADC timing, replaceability |
| K5 | 16-key prototype matrix | Real wiring, key profiles, timestamped event log and HID reports |
| K6 | Basic wired prototype | Typing use, NKRO tests, custom config and firmware recovery |
| K7 | Sealed switch module / cleaning bench | Safe washing procedure, ingress and corrosion observations |
| K8 | Full development keyboard | Long-duration field use, fatigue and acoustic measurements |
| K9 | Final metal keycaps/chassis | CNC only after dynamics and interfaces are frozen |

## Priority

**Do K1–K4 before committing to full-size hardware.**

Reuse software infrastructure and bench instruments where practical from `projects/custom-mouse`, but do not assume its lever mechanism scales directly to a keyboard key.

## Exit criteria

The final keyboard is not considered validated by marketing numbers alone. It needs measured stroke variation, missed/phantom key counts, worst-case event-handling jitter, acoustic test conditions, cleaning tests and cycling data.
