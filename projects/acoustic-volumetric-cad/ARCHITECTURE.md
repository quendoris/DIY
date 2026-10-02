# Architecture

## High-level system

```text
                         ┌──────────────────────┐
                         │ Parametric CAD model │
                         │ OpenSCAD / equivalent│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Geometry front-end   │
                         │ CSG → mesh/features  │
                         └──────────┬───────────┘
                                    │
                                    ▼
┌──────────────┐          ┌──────────────────────┐
│ Head / hand  │─────────▶│ Display planner      │
│ tracking     │          │ visibility/features  │
└──────┬───────┘          └──────────┬───────────┘
       │                              │
       │                              ▼
       │                   ┌──────────────────────┐
       │                   │ Trajectory planner   │
       │                   │ XYZ + RGB timeline   │
       │                   └──────────┬───────────┘
       │                              │
       ▼                              ▼
┌──────────────┐          ┌──────────────────────┐
│ Haptic       │─────────▶│ Acoustic field       │
│ interaction  │          │ scheduler / solver   │
└──────────────┘          └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         ▼                      ▼
                  phased-array A         phased-array B
                                             /
                                            /
                                  ●        /
                            levitated particle
                                   │
                              RGB lighting
```

## Major subsystems

### 1. Acoustic arrays

Start with opposed arrays around a central interaction volume.

The array controller must support individually phase-controlled transducers and rapid field updates.

The physical array geometry should be replaceable without forcing a rewrite of the higher software layers.

### 2. Particle subsystem

Responsibilities:

- introduce a suitable lightweight particle into the capture volume;
- detect successful capture;
- detect particle loss;
- reacquire or dispense another particle;
- return a calibrated particle position to the controller.

Particle loss should be treated as an expected recoverable state, not as a catastrophic failure.

### 3. Field solver

Inputs:

- transducer geometry;
- particle target position;
- optional haptic focal points;
- calibration parameters.

Outputs:

- phase/amplitude commands for each emitter.

The solver should eventually support temporal multiplexing between:

- stable trapping;
- motion;
- haptic focal points;
- calibration pulses.

### 4. Volumetric trajectory planner

The planner converts geometry into a time-ordered path.

It should optimize at least:

- visible information per unit time;
- travel distance;
- acceleration limits;
- local brightness;
- RGB timing;
- retracing and flicker;
- viewpoint relevance.

A dense voxelizer is useful for testing but should not be the final rendering strategy.

### 5. RGB subsystem

RGB illumination is independent from acoustic position control.

The controller therefore produces synchronized:

```text
t → x, y, z, r, g, b
```

samples.

Color may represent either literal material color or CAD semantics such as:

- selected;
- constrained;
- invalid;
- reference;
- hidden/internal;
- contact region.

### 6. Tracking

Use stereo/depth cameras for:

- hands;
- fingertips;
- head position;
- optionally gaze direction;
- particle verification.

Tracking and acoustic control must use one calibrated coordinate frame.

### 7. Haptic interaction

Given a fingertip position and the CAD surface, estimate the closest relevant surface point.

When the finger enters a configurable interaction distance, request one or more acoustic haptic focal points.

Possible semantic feedback:

- surface: continuous texture;
- edge: stronger narrow cue;
- button: distinct modulation;
- wheel/detent: periodic pulses;
- selected object: low-frequency pulse.

### 8. CAD bridge

Initial target: OpenSCAD.

The bridge should expose:

- source file;
- named parameters;
- generated mesh;
- feature metadata where available;
- bidirectional parameter updates.

Gesture operations should preferably become deterministic parameter/transform changes rather than destructive edits.

## Safety

The acoustic system still requires explicit safety engineering:

- sound-pressure characterization;
- thermal limits;
- transducer fault detection;
- automatic shutdown on controller failure;
- hand/face proximity policies where necessary.

No implementation should assume that ultrasound is harmless merely because it is inaudible.

## Software boundary

Keep the physical renderer separate from CAD.

A useful abstraction is:

```text
scene + viewpoint + interaction state
             ↓
      render primitives
             ↓
       trajectory stream
             ↓
       physical backend
```

That allows the same renderer to be tested first on a normal monitor or simulator before any acoustic hardware exists.
