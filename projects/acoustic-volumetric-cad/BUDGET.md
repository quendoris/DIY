# Preliminary Budget

This file is a planning envelope, not a purchasing list.

Prices can change substantially with transducer choice, array size, PCB strategy and whether laboratory-grade hardware is purchased or built.

## Stage budgets

| Stage | Purpose | Rough hardware envelope |
|---|---|---:|
| V0 | software only | existing PC/cameras |
| V1 | small acoustic trap | $100–500 |
| V2 | controlled RGB volumetric primitives | $300–1,000 |
| V3/V4 | useful custom phased-array display | $800–3,000 |
| V5/V6 | CAD + tracking + haptics + robust mechanics | $2,000–5,000+ |

## Cost drivers

A serious prototype is expected to spend money primarily on:

- hundreds of ultrasonic transducers;
- multi-channel driver electronics;
- custom PCBs;
- FPGA or other deterministic high-rate controller;
- power electronics;
- cameras/tracking;
- mechanical array alignment;
- RGB illumination and optics;
- measurement/calibration equipment;
- iteration failures.

The levitated particle itself is essentially negligible in cost.

## Cost-control strategy

Do not begin with the final 16×16-class arrays.

A better sequence is:

```text
small array
    ↓
prove capture/control
    ↓
medium opposed arrays
    ↓
prove fast XYZ trajectories
    ↓
RGB + renderer
    ↓
scale only after measurements
```

This avoids committing most of the budget before the control stack and acoustic geometry are validated.

## Reference directions

Useful prior art to revisit before implementation:

- Multimodal Acoustic Trapping Display (MATD), Nature, 2019
- open acoustic levitation projects such as AcoustiFly
- phased-array mid-air haptics research
- OpenSCAD as the first deterministic CAD front-end

Before purchasing hardware, update this file from current distributor prices and build a concrete BOM.
