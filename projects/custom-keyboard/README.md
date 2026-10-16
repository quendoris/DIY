# Custom Keyboard — Concept

Status: **requirements capture and feasibility studies**, not a frozen design.

## Owner requirements

- Fully wired; detachable cable; custom STM32-based controller and firmware.
- High-profile keys, broadly similar in height/feel to an MSI Vigor GK20-style keyboard.
- User-facing keycaps in titanium or aluminium alloy (e.g. 7075), with a substantial metal chassis; considerable total mass is acceptable.
- No conventional electrical switch contacts in the main sensing path.
- Per-key adjustable actuation and reset, possibly with programmable force/tactile feel.
- Passive permanent-magnet return rather than conventional return springs, subject to mechanical verification.
- Optional active electromagnetic assistance for feel/damping; avoid continuous power consumption.
- Independent, replaceable/hot-serviceable key modules and/or keycaps.
- Very quiet operation; aspirational noise target around 30 dBA, **measurement conditions TBD**.
- Liquid/spill resistance and safe cleaning: design for serviceability, not unverified waterproof claims.
- Reliable multi-key input and deterministic firmware event handling; no ghosting and robust simultaneous-key behavior.
- Locally configurable profiles, per-key calibration, diagnostics and reproducible tests.

## Device philosophy

**Separate position sensing, passive return force, tactile feedback and digital event generation.**

Candidate key mechanism:

```text
metal keycap
    ↓
guided replaceable stem
    ↓
moving magnet ──→ Hall/TMR displacement sensor
    ↓
passive magnetic restoring assembly
    +
optional controlled electromagnetic actuator
    ↓
soft replaceable end stop
```

Magnetic sensing avoids **electrical contact wear** but not necessarily mechanical friction, fatigue, contamination or magnetic drift. A full keyboard needs an explicit power, crosstalk, thermal, calibration and maintenance budget.

## Initial technology baseline

Modern Hall/TMR keyboards already offer analog displacement, adjustable actuation, rapid trigger and high polling rates. This project is differentiated by **metal keys, independent modular mechanics, acoustic quietness, cleanability and verified event behavior**, not simply by adding Hall sensors.

## Critical interface distinction

A standard USB HID keyboard usually reports **pressed-key state**, not a timestamped total ordering of every keypress. If two edges enter the same report, their order may be indeterminate for the host.

Our firmware can preserve and timestamp events internally and send intermediate state reports. A strict, auditable event stream requires a **separate vendor protocol with host support**; it cannot be promised for ordinary OS text entry solely by changing the keyboard scan logic.

## Engineering documents

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [ROADMAP.md](ROADMAP.md)

## Scope control

No purchase of ~100 active actuators and no CNC titanium keycap batch until the one-key and 4-key benches establish force, thermal behavior, magnetic isolation, sound and reproducibility.
