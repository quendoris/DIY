# ADR-003 — Research Hardware Tolerance versus Production Qualification

Date: 2026-11-01. Status: **OWNER-DEFINED PROTOTYPING POLICY**, complementing ADR-001 and ADR-002.

## Boundary 1: NUCLEO and exploratory optical benches are scientific fixtures

The user's forthcoming marketplace board described as "Spot NUCLEO-H7S3L8 with STM32H7R3L9" may be a clone or contain deviations from official ST MB1737. The owner expressly prioritizes **a working imperfect experimental fixture over an ideal unavailable platform**.

Thus a manufacturer's unexpected marking, non-standard component, modified pin assignment or imperfect signal quality should cause **factual identification, independent tests, and a narrower evidence grade**, NOT automatic rejection of the entire optical research project.

But this policy does NOT override electrical safety, chip absolute maximum ratings, wiring checks or data integrity: 
- before connecting power, identify actual supply pins/voltage ranges from board photos, continuity and regulator measurements;
- use a known safe, current-limited supply and appropriate protection, do not flash arbitrary stock binary against a different MCU/flash setup;
- document oscillator, CPU/PHY and pin deviations, changed bootflow, serial ID and available debug;
- firmware must be built for the **actual detected silicon and PCB**; independently verify intended peripheral pin assignments and avoid irreversible option-byte changes;
- isolate or discard a bench unit with overheating, shorts, unsafe leakage, damaged USB/optical transmitters or unacceptable noise;
- hardware quirks are named **stress conditions**. A failed case informs robustness design but is not proof that the protocol tolerates arbitrary hostile hardware.

**Research claim status:** `KNOWN_REFERENCE` (official identified board), `DOCUMENTED_VARIANT`, `UNKNOWN_VARIANT`, or `UNSAFE_DO_NOT_POWER`. Claim `MEASURED_ON_THIS_DEVICE` only for real results with a stored configuration and unit ID. Research packet integrity on a variant cannot certify ST's nominal PHY specifications or all hardware revisions.

## Boundary 2: Custom final audio PCBs are production candidates

For every unit intended for a finished audio system, maintain a test and calibration workflow:

1. Exact silicon part/order code, chip authenticity provenance/lot and PCB revision; components with known ratings and documented pinouts.
2. Schematic/PCB ERC/DRC, creepage/clearance/ESD/power rails as appropriate; mechanical tolerance and serviceability plan.
3. Before expensive chips populated: PCB inspection for shorts, opens, bad solder joints and polarity under microscope. Where appropriate check supply continuity, ground isolation and component orientation.
4. Current-limited first low-voltage power; measure rails and transient behavior without sensitive loads, then assemble MCU/DAC/amp stages in a staged, reversible order.
5. Program signed/versioned reproducible firmware only after debug and power are healthy; secure boot/identity provisioning are separate later lifecycle gates and must not preclude recovery during early integration.
6. Post-program self-check, watchdog/reset/power-state, thermal, analog noise, clock/drift, inter-channel crosstalk, DAC linearity and control/link failure injection.
7. Per-unit calibration data, measurement uncertainty and serial/revision trace; acceptance signature and any explicit `NOT_TESTED` fields.
8. Reinspect after final mechanical assembly and thermal run-in; no automatic extrapolation from PCB-only acceptance to finished-speaker acoustics.

"Exact known module" is insufficient: the built PCB must be tested again after soldering, flashing and assembly. Use independently powered fault protection and refuse to test mains hazard by improvised destructive shorting.

## What does not change

- Fixed architecture: left LF/MID/HF, right LF/MID/HF, independent SUB = 7 separately controllable analog DAC output and amplifier channels, four logical optical network planes.
- The STM research board is **not** a gate to selecting speaker drivers, developing the active 3-way crossover or studying the sub.
- Optical transport can be prototyped with ready-made PHY converters initially, and its timing/security claims remain scoped to observed measurements.
- Complete open source hardware/software publication goal, with evidence levels and known limits retained.
- Finished wooden/composite futuristic enclosure is **last**; temporary plywood measurement fixtures are allowed.

## Engineering metaphor, applied precisely

"Grow a crystal" means model → smallest measurable prototype → falsifying experiment → evidence records → next layer, with re-qualification when dependencies change. It does not mean *a broken prior layer is acceptable merely because something works*. Documented board defects may be retained as **deliberate test stimuli** under safe constraints.

Recommended issue fields: `hardware_role` [research/production], `device_id`, `source_claims`, `known_deviations`, `safety_status`, `measurements`, `coverage`, `failure_observations`, `claim_evidence_grade`, `retest_trigger`.
