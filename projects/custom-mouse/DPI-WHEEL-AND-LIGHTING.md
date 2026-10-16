# Secondary DPI wheel and lighting

Status: **proposed ergonomic/UI revision** to the existing custom mouse design.

## Purpose

Replace the original two top DPI +/- buttons with a **smaller independent rotary wheel** for sensitivity control.

The main scroll wheel remains the existing precision, absolute-angle, electromagnetically haptic wheel.

The secondary DPI wheel is a distinct low-profile control, intended to be easy to find without unintended activation.

## Input architecture

```text
main wheel
  ├── absolute angle → scroll events
  ├── active haptic torque → programmable scroll detents
  └── axial press → middle click

secondary DPI wheel
  ├── angular displacement → DPI/sensitivity selection
  ├── optional gentle detents → tactile profile markers
  └── RGB/light-pipe indicator → active DPI preset
```

Candidate sensing: compact contactless magnetic angle encoder. Avoid a traditional wear-prone contact encoder if the mechanical package permits. Reuse existing wheel sensor interface/driver concepts where practical; no second full haptic actuator is required by default.

## Color mapping

Proposed visually ordered range:

```text
low CPI/DPI     → green
                 → yellow
                 → red
                 → violet
high CPI/DPI    → blue
```

The color reports **configured DPI/CPI**, not cursor velocity. Store the numeric setting independently and display it in desktop configuration software; color should never be the sole way to identify a profile.

The mapping should be configurable, include low-brightness and off modes and ideally use a smooth color gradient rather than only five discrete bins.

## Titanium integration

Aim for understated lighting:

- a narrow diffused ring or arc near the secondary wheel;
- an indirect perimeter line or restrained translucent accent;
- no glaring top-facing RGB LEDs;
- physically protected diffuser/light-pipe in the titanium housing.

Do not force light through solid titanium: the design needs controlled gaps/light guides/dielectric inserts. Protect the optical tracking sensor from internal RGB light leakage and electrical PWM noise.

## Ergonomics validation

Before moving from DPI buttons to the secondary wheel, test:

- reach with the normal resting hand position;
- accidental adjustments during LMB/RMB and scrolling;
- rotational resistance and precision;
- mechanical space next to the main haptic wheel;
- light visibility in normal desk use;
- firmware behavior when DPI changes mid-motion.

Recommendation: allow fine steps and explicit presets, optional click-to-lock or hold-to-change if inadvertent activation is observed.

## Power and reliability

Treat the LED subsystem as noncritical. Loss of light cannot alter input processing. Include thermal/current budget, dimming and off profiles.

This file proposes a control change; final top-panel layout is not frozen.
