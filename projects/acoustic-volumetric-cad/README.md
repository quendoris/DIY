# Acoustic Volumetric CAD

## Idea

Build a true volumetric CAD interface in physical space using an acoustically levitated particle as the visible voxel.

The system should eventually allow a generated or parametric 3D model to appear in front of the user, be viewed from arbitrary angles, manipulated with hand gestures and partially felt through acoustic haptic feedback.

This is intentionally **not** a conventional screen, VR headset or Pepper's-ghost display.

The long-term interaction loop is:

```text
natural-language request
        ↓
parametric CAD / OpenSCAD
        ↓
mesh + semantic features
        ↓
volumetric trajectory planner
        ↓
acoustic phased arrays
        ↓
levitated particle
        ↓
RGB illumination
        ↓
physical-space image

hand / eye tracking
        ↓
gesture + contact estimation
        ↓
CAD parameters / transforms
        ↓
re-render
```

## Design direction

The preferred physical implementation is **acoustic levitation**, not an optical trap.

Reasons:

- no open high-power trapping laser near the user's eyes and hands;
- the acoustic field can participate in both levitation and haptic feedback;
- hands can interact around the display volume more naturally;
- the same controller can eventually schedule trapping, rendering and haptic focal points.

## CAD philosophy

The display should be driven from deterministic parametric geometry wherever possible.

OpenSCAD or an equivalent code-first CAD representation is a particularly attractive first target because:

- dimensions are explicit parameters;
- generated models can be reproduced exactly;
- AI can modify geometry by changing readable source;
- Git diffs remain meaningful;
- gesture input can map to parameters instead of destructive mesh editing.

## Rendering philosophy

One particle cannot illuminate an entire dense voxel volume simultaneously.

The renderer therefore should prioritize information rather than brute-force every possible point:

- silhouettes;
- feature edges;
- section lines;
- selected components;
- construction geometry;
- contact regions;
- view-dependent detail.

Future versions may use head/eye position to assign more trajectory time to geometry carrying the most information for the current viewpoint.

## Interaction goal

For a model such as the custom mouse:

1. generate or update the CAD model;
2. render its important contours in real 3D space;
3. rotate, scale or select it with hand gestures;
4. approach the surface with a finger;
5. create an acoustic haptic focus corresponding to the nearest virtual surface;
6. modify a parameter;
7. immediately render the new geometry.

The haptics are not expected to reproduce the inertia or rigidity of a real solid object. They are intended to provide localized touch cues, edges, regions, controls and surface feedback.

## Status

**Deferred concept.**

The project is worth preserving now, but hardware construction should wait until the budget for a serious phased-array prototype is comfortable.

See also:

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [ROADMAP.md](ROADMAP.md)
- [BUDGET.md](BUDGET.md)
