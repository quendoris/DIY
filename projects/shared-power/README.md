# Shared Power, Protection & Cooling — DIY Foundation

Status: **cross-project research, no live-mains circuit approved**. This should be reusable in the wired stationary speakers, optical controller and other DIY hardware where applicable. If later separated into a `DIY-snippets` repository, preserve links, licenses, interface specification, test vectors and version history. No separate repository has been created yet.

## Why start here?

The owner chose the **power module as the first physical development target**. Each stationary left/right speaker, subwoofer and digital controller has independent AC input (or preferably a certified external AC/DC supply first), local power rails, monitoring and fault protection. The objective is serviceable reliable power, measurable output-noise limits and deterministic response to supply failures, overloads, overheating, short circuits and recovery.

Do not extrapolate that a PC PSU with an '80 PLUS Gold' efficiency label certifies noise, signal fidelity, overshoot or safe modification. Avoid modifying or operating exposed mains switching converters in the first DIY bench.

## Two-tier reference architecture

```text
  wall AC ─> professionally certified isolated external AC/DC PSU
                     |  low voltage (candidate 24 / 48 V DC)
                     v
              PROTECTED INPUT MODULE
       fuse/eFuse | reverse polarity | surge/ESD
       inrush/soft-start | OVP | UVP | OCP | telemetry
                     |
       +-------------+-------------------+
       |             |                   |
 AMP rails       AUDIO analog        DIGITAL logic
 bounded ripple  post-filter/DC/DC    DC/DC + filters
 load transients low-noise LDO         MCU, fiber, fan
       |             |                   |
 class-D amp     DAC/reference          watchdog
       |
  speaker limiter, output-short detection,
  thermal cutoff, hardware-latched fail-safe
```

A power brick's factory certification does not automatically certify our **finished assembly**, nor does a lab pass constitute third-party certification. Requirements, test protocols and evidence can be **our own**, but must not be mislabeled as an external IEC/CB certificate.

Each speaker module chooses its actual power envelope; a universal connector/pinout cannot be frozen until safe hotplug/current/grounding/cable voltage-drop issues are reviewed. Share interface contracts and supervisor design first, then circuit topologies by power class.

## Standards and scope

| Reference | Covers | Does NOT automatically cover |
|---|---|---|
| IEC 62368-1:2023 | AV/ICT equipment hazard-based electrical/fire safety | low-noise DAC supplies, audio THD, any custom DIY 'certification' |
| IEC 61000-4-2:2025 | ESD immunity test method | general electrical safety |
| IEC 61000-4-4:2012 | repetitive electrical fast-transient/burst immunity methods | normal steady-state ripple |
| IEC 61000-4-5:2014+A1:2017 | surge immunity test methods | immunity beyond selected test severity |
| IEC 61000-4-11:2020 | AC voltage dips/interruptions/variations immunity methods | universal survival of all AC failures |
| CISPR 32:2015+A1:2019 | multimedia equipment emissions limits | DAC SNR / noise or immunity |
| 80 PLUS (PC PSU) | power conversion efficiency at defined test points | low audio noise, short-circuit survival or safe redesign |

Relevant IEC basic EMC publications describe reproducible **test methods and levels**, not a promise every unit will withstand any imaginable event. Applicability and pass criteria are selected for the equipment/environment and require appropriate lab setup.

Primary references:
- https://webstore.iec.ch/en/publication/69308
- https://webstore.iec.ch/en/publication/68954
- https://webstore.iec.ch/en/publication/4222
- https://webstore.iec.ch/en/publication/4223
- https://webstore.iec.ch/en/publication/63503
- https://webstore.iec.ch/en/publication/65836

## Internal engineering 'certificate': what it actually is

A **versioned engineering verification dossier**, signed or hashed as an integrity measure, not an externally recognized certificate:
- requirements/spec version and intended operating environment;
- exact module/hardware revision, BOM, firmware and measurement equipment calibration status;
- test procedures and ranges, setup photographs and uncertainties;
- raw measurements, tolerance bands, pass/fail results and deliberate **NOT TESTED** fields;
- reproducibility hashes, human/CI signoff and known failure envelope;
- expiry/revalidation conditions after component or firmware changes.

This can be called `DIY Power Qualification Dossier`. It cannot be marketed as IEC-certified without applicable formal conformity assessment.

## Qualification matrix for future benches

1. **Input and soft-start**: inrush energy, hotplug, startup ordering, undershoot/overshoot under defined input-voltage ranges; no spurious speaker pop.
2. **Voltage quality**: DC regulation at 0/10/50/100% load; ripple/noise integrated and peak-to-peak measured with declared bandwidth, probe grounding and test loads; LF audio-band and switching-spectrum characterization separated.
3. **Dynamic loads**: realistic amplifier music-envelope load steps, DAC/control activity, thermal transients and load release with measured settling time, overshoot, no control resets.
4. **Electrical protection**: OCP/OVP/UVP, eFuse trips, input reverse polarity, brownout and output short *at qualified safe low-voltage points* with electronic current limiting. Do not short mains, bypass fuses or run destructive surge tests on a DIY bench.
5. **Thermal**: equilibrium temperatures at specified ambient and maximum load, heatsink/PCB hot spots, fan-failure fault response and restore hysteresis.
6. **Isolation/earth**: protective-earth decisions, creepage/clearance, leakage, insulation and connector safety reviewed by an appropriately qualified expert or accredited lab for mains-related testing.
7. **Audio integrity**: output hiss, hum and amplifier/DAC noise measured as a separate full-system criterion, including load changes and fan PWM coupling.
8. **System faults**: multiple failures, sensor disconnect, stale telemetry, watchdog reset, controller/fiber loss, power reboot, persistent short and disabled fan. Simulators should contain these first, then safe low-voltage bench tests.

Every requirement must specify levels, instrumentation, sampling bandwidth, accepted failure behavior and test duration; choose thresholds after initial power/amp/thermal characterization, not by inventing a universal `0 mV ripple`.

## Cooling: keep the cabinet acoustically sealed where required

Compare:
- A: passive conduction/heatsinks into a dedicated exterior heat-spreader or ventilated electronics sub-compartment;
- B: fan with temperature control, low-RPM limits and damped mount in the **separate electronics bay**;
- C: always-on fan only if measured thermal profile requires it, with noise and vibration budget at the 0.6–0.8m listening point.

The **woofer's sealed acoustic cavity** must not be ventilated into the room or into the electronics bay by an incidental fan hole. For vented speakers, acoustic port geometry is designed separately.

Candidate: ARCTIC P8 PWM PST (80mm, manufacturer 200–3000 rpm PWM, 0 RPM at low PWM, ~39.76 m³/h at full speed, 0.3 sone max-rated condition). These are *free-air manufacturer conditions*, not in-cabinet noise. Other diameters/fully passive design may be preferable. Tach failure, dust, bearing wear, acoustic panel vibration and fan PWM injection require testing.

Manufacturer: https://www.arctic.de/en/P8-PWM-PST/

**Fail-safe requirement:** amplifier protection must work with failed/stopped fan; local thermal shutdown independent of networked diagnostics. A quiet-fan condition is not equivalent to a safe-fan condition.

## First physical prototype (safest useful form)

Use a **certified external low-voltage AC/DC adapter** with proper connectors and a small isolated-downstream *DC-only* distribution board, hardware current limit, supervisor, sensors, dummy loads and data logger. Research power and heat at the low-voltage DC stage **before** custom mains design. External adapter can remain final if it meets size/noise/safety objectives.

No high-voltage destructive testing by hobbyist shorting to 'see what survives'. Independent accredited lab tests are the route for dangerous mains transients and conformity.
