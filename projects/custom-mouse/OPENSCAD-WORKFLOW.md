# OpenSCAD Workflow

Status: **preferred parametric mechanical source of truth** for mouse development.

## Principle

Mechanical geometry should be generated from version-controlled OpenSCAD source, with named parameters and repeatable exports. The source model is the authority for intended dimensions; exported meshes are build artifacts and should be regenerated from a known commit.

OpenSCAD provides deterministic parametric geometry, but **does not guarantee the manufactured part's physical precision**. Accuracy depends on the process, material, machine calibration, tool, slicing/meshing, orientation, shrinkage and measurement.

## Model layers

Keep distinct files/modules for:
- global coordinate system and reference datums;
- outer ergonomic envelope;
- shell and split lines;
- LMB/RMB cartridges;
- main scroll-wheel cartridge;
- secondary DPI wheel;
- optical-sensor module and lens opening;
- USB-C recessed port/daughterboard;
- PCB/component keep-outs and cable routing;
- feet, ballast pockets and service screws;
- exploded-view / assembly scene;
- fit-check gauges and test coupons.

Prefer reusable modules with explicit interfaces instead of a monolithic file. Parameterize mirrored LMB/RMB parts when their mechanics are genuinely symmetric, while preserving independent calibration and assembly tolerances.

## Parameters that must remain explicit

- nominal bearing and shaft sizes;
- bearing seat and shaft-fit allowance;
- axis positions and spacing;
- pivot/lever lengths;
- nominal stroke and hard-stop location;
- magnet dimensions, orientation and air gaps;
- Hall/TMR sensor position and adjustment range;
- coil envelope, wire clearance and thermal keep-out;
- PCB outline, connector envelope and screw locations;
- shell wall thickness and minimum ligament around apertures;
- screw/insert engagement;
- foot thickness and ground clearance;
- replaceable-module datum surfaces;
- cable plug envelope and recessed USB-C geometry.

Do not bury clearance allowances as unexplained constants inside geometry expressions.

## Tolerance strategy

For each fit, specify:
1. nominal dimension;
2. intended manufacturing process;
3. target tolerance or clearance;
4. measurement method;
5. allowed adjustment during prototype;
6. final acceptance criterion.

A bearing's nominal dimensions are not the whole fit specification. Consider actual bearing tolerances, shaft tolerance, housing material, temperature, retention method and whether the ring must be fixed or rotate.

For 3D-printed prototypes, use coupons to calibrate hole/shaft compensation before printing a full cartridge. Printed prototypes validate packaging and approximate kinematics; they do not automatically validate final titanium friction, acoustic behavior or stiffness.

For CNC titanium/aluminium, design bearing seats, datum faces and threaded features around the chosen shop's achievable tolerances and metrology. Do not specify arbitrary micron tolerances without a process capable of holding and verifying them.

## Geometry and export checks

For every tagged prototype:
- render and export STL/3MF from a recorded source revision;
- inspect manifoldness, self-intersections and thin-wall artifacts;
- check bounding dimensions and assembly clearances;
- generate a simple dimensional report;
- build a low-cost fit coupon for critical seats;
- record actual measured deviations;
- never overwrite a known-good mesh without retaining the source revision.

Use higher mesh resolution for curved surfaces only where it changes the manufactured geometry; facet count controls tessellation, not machining precision.

## Iteration naming

Recommended:
- mouse-envelope.scad
- button-cartridge.scad
- main-wheel.scad
- dpi-wheel.scad
- optical-module.scad
- usb-daughterboard.scad
- assembly.scad
- fit-coupons.scad

Store dimension reports, rendered views and exported manufacturing meshes alongside commit/parameter metadata. Keep experimental dimensions in named configuration files rather than editing constants in multiple modules.
