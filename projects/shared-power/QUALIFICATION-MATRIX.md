# DIY Power Qualification Dossier — planned test cases

Version: draft 0.1. **No tests in this matrix have yet been executed.**

The goal is a reusable, **first physical** DIY power+fault+cooling bench for mains-isolated **low-voltage DC only**. A dossier is project-local evidence, not an IEC product certificate.

| ID | Stimulus / condition | Observables | Fail-safe condition | Stage |
|---|---|---|---|---|
| PWR-01 | nominal DC input, no/partial/full permitted load | DC V/I regulation; ripple measurement-band declaration | normal operation within explicitly defined rails | DC bench |
| PWR-02 | repeatable electronic-load current steps/release | transient undershoot/overshoot, settling, audio/logic resets | amp mute on invalid rails | DC bench |
| PWR-03 | programmable UVP/brownout within approved low-voltage range | supervisor state, event counter, audio pop | safe mute; reconnection after stable recovery | DC bench |
| PWR-04 | controlled overcurrent (bounded programmable electronic-load condition) | eFuse trip curve/current/temperature | hardware output disabled before component limits | DC bench |
| PWR-05 | short *at protected limited-energy DC output only* | fuse/eFuse behavior, wire/connector temp, recovery | no unsafe heating, repeated fault retries bounded | supervised specialized DC bench |
| PWR-06 | sensor missing/stuck/out-of-range | status age, independent protection | status unknown/fault; conservative mute if applicable | simulation + DC bench |
| PWR-07 | temperature rise at specified ambients | T_j estimates, enclosure/air/heat-sink temperatures | controlled derate/shutdown before rated limits | thermal chamber or safe bench |
| PWR-08 | stalled/removed fan when module is hot | fan tach, temp gradient, protection | safe derate then independent cutoff if required | simulation + safe thermal bench |
| PWR-09 | telemetry/control/fiber failure | watchdog/heartbeat, output mute, reset reason | autonomous electronics protection remains active | simulation then DC bench |
| PWR-10 | USB/control activity & fan PWM while amp quiet | DAC rail audio-band noise, amplifier output hiss/hum | within declared listening-point noise criteria | acoustic/electrical bench |
| PWR-11 | repeated warm/cold starts | inrush/soft-start, rail sequencing, data log | no hazardous state and no loud impulse | DC bench |
| PWR-12 | IEC 62368-1 electrical/fire hazards | accredited safety evaluation | compliance evidence only after formal assessment | qualified professional / lab |
| PWR-13 | IEC 61000-4-2/4/5/11 and CISPR32 | designated immunity/emissions setups | equipment-specific pass criteria | appropriate external lab |

Future numerical thresholds: **TBD** per actual amplifier/DAC controller, ambient profile, cables and measurement uncertainty. A universal 'zero ripple' or 'survives any short or surge' specification would be false.

Each test report fields: `test_id`, `requirements_revision`, `hardware_revision`, `fixture`, `stimulus`, `limits`, `raw_data`, `uncertainty`, `result(PASS/FAIL/NOT_TESTED)`, `faults`, `operator_or_CI`, `timestamp`.

Do not set `PASS` on simulation-only evidence for mains safety, EMC or analog noise.
