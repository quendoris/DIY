# Biolam S-11 · system architecture v0.1

## Responsibility boundaries

PC GUI / calibration / experiment planner
  → authenticated structured Ethernet commands, timeouts, IDs
  → Orange Pi Linux supervisor
    → UVC camera manager (MC50-B)
    → two independent white constant-current LED driver channels
    → two WS2812 RGB ring controls
    → motion-request broker
      → dedicated deterministic motion/safety controller
        → limit sensors, real-position feedback, park latch
        → monitored actuator drivers, force/current supervision
        → fail-safe actuator power enabling

Independent **normally-closed physical E-STOP** acts on a hardwired safety chain to inhibit hazardous motion **without Linux or networking**. Software STOP is useful, but cannot claim to stop motion if the host, network or supervisor fail. E-STOP reset must never automatically restart a queued motion.

**Gravity-loaded Z:** design mechanical holding/brake before arranging torque-removing emergency shutdown. Detecting motor overcurrent alone does not protect an objective against collisions. Mechanical hard stops and sensor-validated limits remain mandatory.

## Functional subsystems

| Subsystem | Interface | Gate / invariant |
|---|---|---|
| Video | USB UVC / capture control | Stable ID, explicit settings; actual FPS measured |
| Optics | Objective and condenser model | Preserve iris until optical experiments justify removal |
| Upper light | Azimuth, elevation arc, head pitch | Park sensor, latch, swept-volume and lens keep-out |
| Lower light | White current, RGB | Independent current control and thermal budget |
| Stage | X/Y encoder + drive | Travel limits, repeatability, removable ESD insert |
| Focus | Coarse/fine Z commands | Position sensing, no collision, no gravity drop |
| Safety | Hardware chain, faults, interlocks | Fault latched, deliberate reset, no automatic resume |
| Power | Single fanless external PSU | Separate regulated protected compute/motor/light branches |
| Recipes | Validated device capabilities | Image metadata: settings, angles, actual coordinates |

## State transitions (conceptual; not yet certified)

Power-up: DISARMED → HOMED → TRANSMITTED_READY.

Switch to reflected mode:
TRANSMITTED_READY → Z_SAFE → LIGHT_OFF → UNLOCK_UPPER → UNPARK → POSITION_VERIFIED → REFLECTED_READY.

Return:
REFLECTED_READY → LIGHT_OFF → Z_SAFE → PARK_UPPER → PARK_SENSOR_VERIFIED → LOCK_UPPER → TRANSMITTED_READY.

Any failure → FAULT_LATCHED, inhibit unsafe motion, require deliberate investigation and reset. State transitions **do not substitute** for measured swept-volume collision checking, hard limits and safety electronics.

## Mechanical interfaces

1. Original body is a metrology reference, not immediately a machining target. Prefer reversible bolt-on clamps.
2. Upper illumination is a 3-DOF geometry with separate parking. The 6–8 g metal microservos are only candidates; backlash, hold and audible noise require trials.
3. Transmitted-light optics: preserve condenser plus iris and auxiliary lens initially; quantitatively compare before simplifying.
4. Focus: external removable coupler to existing handles, reduction gearing or belt; measure effort and axial backlash before choosing motors. Closed-loop Z feedback.
5. XY stage: precision guides with a nonmetallic replaceable ESD-safe work surface, exchangeable PCB and slide holders, optical clear aperture designed from illumination cone.
6. White COBs: **constant-current regulation**, not 12 V direct. MCP4725 is a single-channel DAC; MP1584EN is a voltage buck, not automatically a current regulator.

## Open decisions

Measured mounting geometry and swept clearances; actuator choices; objective working distances; true COB power/current; final PSU voltage; runtime/deterministic controller; acoustic and thermal constraints; exact camera sensor/optical resolving power. None is frozen.
