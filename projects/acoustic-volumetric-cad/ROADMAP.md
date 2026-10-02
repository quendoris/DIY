# Roadmap

The project is deliberately staged so that early software work survives later hardware revisions.

## V0 — software renderer

No levitation hardware.

Build:

- OpenSCAD/mesh import;
- feature extraction;
- trajectory generation;
- viewpoint-aware simplification;
- simulated particle renderer;
- basic hand tracking;
- gesture-to-transform mapping.

Exit condition:

A CAD model can be converted into a stable real-time trajectory representation and manipulated through tracking input.

## V1 — acoustic capture

Small opposed arrays.

Goals:

- trap one lightweight particle;
- move it controllably in X/Y/Z;
- calibrate array geometry;
- detect particle loss;
- establish repeatable reacquisition.

No requirement for a useful visual image yet.

## V2 — visible volumetric primitives

Add synchronized RGB illumination.

Goals:

- line;
- circle;
- box;
- simple wireframe;
- stable brightness;
- predictable geometry.

Measure:

- usable display volume;
- peak trajectory speed;
- positioning error;
- flicker;
- recovery time after particle loss.

## V3 — CAD display

Connect the physical backend to the V0 software stack.

Goals:

- render OpenSCAD-derived contours/features;
- viewpoint-dependent simplification;
- live model rotation/scale;
- parameter updates without restarting the renderer.

## V4 — automatic particle handling

Add a particle reservoir/cartridge and automatic recovery.

State machine:

```text
TRACKING
   ↓ loss
SEARCH
   ↓ not found
DISPENSE
   ↓
CAPTURE
   ↓
CALIBRATE
   ↓
TRACKING
```

## V5 — haptic interaction

Add hand-surface correspondence and acoustic tactile cues.

Goals:

- fingertip tracking;
- closest-surface estimation;
- localized haptic feedback;
- distinct surface/edge/control patterns;
- simultaneous trapping + haptic scheduling.

## V6 — serious CAD workstation prototype

Integrate:

- larger phased arrays;
- wider useful volume;
- better cameras;
- automatic particles;
- eye/head-aware rendering;
- haptic semantic feedback;
- polished CAD bridge;
- persistent calibration;
- diagnostics and safety monitoring.

## Deferred experiments

Interesting but not required for the first useful system:

- multiple independently trapped particles;
- adaptive multiple-particle rendering;
- sound output from the same arrays;
- material-dependent haptic textures;
- collaborative/networked scenes;
- direct AI-generated parametric CAD edits.
