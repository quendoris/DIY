# Passive Magnetic Tactility — Core Requirement

Status: **owner-approved architectural principle**, mechanism to be validated with one-key bench measurements.

## Non-negotiable behavior

A key must remain a **complete, pleasant mechanical input device when its electromagnetic actuator is unpowered**:

1. A perceptible and repeatable tactile transition on the downstroke.
2. Monostable return to its rest position after release.
3. Stable support of the resting finger without false actuation.
4. Acceptable travel, force, rebound and quiet end stops.
5. No conventional electrical contact switch.
6. A metal touch surface without a sharp metallic click or ringing.

The active electromagnet is **a small optional correction**, not the source of the basic click feel or the essential return mechanism. A fully passive, coil-free key module is a valid product configuration.

## Force architecture

Use separate passive contributions, such that a candidate design can be tuned independently:

```text
F_total(x, I, v) = F_return_passive(x)
                 + F_detent_passive(x)
                 + F_actuator(x, I, v)
                 + F_mechanical_losses(x, v)
```

Here:
- `x` is downward displacement;
- `F_return_passive` ensures positive restoring action across the useful stroke;
- `F_detent_passive` produces a perceptible force peak then a controlled drop;
- `F_actuator` is zero with the coil off and must not be relied upon for return;
- `F_mechanical_losses` includes guide friction, damping and impact behavior.

The force profile above is a design decomposition, **not a measured or guaranteed linear superposition of independent magnetic fields**; nonlinear cross-coupling must be measured.

## Why one repulsive magnet pair is insufficient

Simple axial repulsion typically yields a smooth force rise with decreasing separation. It does not inherently generate a satisfying tactile force peak followed by a decrease.

Investigate at least two passive detent topologies:

**A. Symmetrical side-magnet pass-by**
- One magnet mounted to the traveling stem.
- Matched stationary magnets placed symmetrically to suppress unwanted lateral loads.
- Geometry chosen to produce a downstroke force peak/drop.
- Independent axial repulsion or other passive monostable return force.

**B. Magnet + shaped ferromagnetic flux path**
- Traveling permanent magnet interacts with a defined fixed steel pole profile.
- Magnetic attraction varies non-monotonically with position.
- An independently verified restoring component prevents unintended latching.

Both require FEM/bench evaluation of force, tolerances, field interference and magnetic hysteresis.

**Avoid an unintended second stable equilibrium.** Do not equate a tactile force drop with a two-position latch. Across the intended range, the unloaded assembly must return to rest without coil power.

A purely conservative one-dimensional magnetic force curve does not create dissipative hysteresis on its own. The firmware may use separate actuation/reset thresholds, but true mechanical hysteresis depends on multi-stable geometry, friction or dynamics and must be characterized separately.

## Active actuator responsibilities

The coil may *optionally*:
- adjust the peak force slightly;
- fine-tune reset/rebound feel;
- dynamically damp aggressive bottom-out/top-out;
- provide user-selectable profiles within measured safe limits.

In normal use it should not have to draw continuous current to hold the key up. Pulse durations and currents are to be determined by measured coil dynamics and thermal limits, not guessed.

If the active driver, firmware or power fails, the passive key still functions physically and safely. Ordinary electrical key reporting requires the keyboard controller to remain powered.

## Magnetic sensing challenges

The stem may carry a magnet for Hall/TMR sensing, but passive force magnets and any energized coil can corrupt the sensed position.

Bench validation must include:
- sensor transfer curves with all passive magnets installed;
- coil current polarity sweeps;
- all four neighboring keys actuated;
- thermal drift;
- positional calibration and magnetic interference across modules.

Separate the sensing magnet geometrically, orient fields strategically or compensate only when compensation is proven repeatable.

## Mechanical and acoustic constraints

- Metal cap must not strike metal at bottom- or top-out.
- Low-play guides, replaceable soft stops and optional internal cap damping remain necessary even when switching is contactless.
- Avoid excessive snap acceleration that makes a metal cap ring.
- Maintain visual sharpness independently from key guide/stop dimensions.

## First bench experiment

Build **one straight-stroke replaceable key cartridge** with no powered coil first.

Compare:
1. Magnet-return-only baseline.
2. Symmetrical pass-by tactile assembly.
3. Shaped flux-path tactile assembly (if manufacturable).
4. Optional active coil switched on, only *after* a satisfactory passive profile exists.

Capture plots:
- press and release force vs travel;
- passive return force from every point in the stroke;
- force peak and relative drop;
- mechanical ringing and acoustic transient;
- travel repeatability and off-axis wobble;
- degradation with repeated cycles and temperature changes.

**Gate P0:** a self-returning, satisfying and acceptably quiet tactile key exists with coil completely disconnected. No full keyboard tooling or active-coil matrix is justified before P0 passes.
