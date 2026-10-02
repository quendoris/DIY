# Architecture

## System overview

```text
                          ┌────────────────────┐
                          │     STM32H7S3      │
                          │ realtime controller│
                          └─────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
       tracking domain        control domain          USB / policy
             │                      │                      │
       optical sensor          LMB/RMB Hall            USB HID
       optional IMU            wheel angle             config channel
                               wheel press              future security
             │                      │
             └──────────────┬───────┘
                            ▼
                    realtime state fusion
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
          HID event path            force-control path
                                          │
                           ┌──────────────┼──────────────┐
                           ▼              ▼              ▼
                        LMB coil       RMB coil       wheel actuator
```

## Controller

Initial architecture target: STM32H7S3-class MCU.

Reasons:

- more than enough compute for mouse input;
- high-rate deterministic control loops;
- USB High Speed capability;
- DMA/timers for low-jitter sensor acquisition;
- future security features can coexist without disturbing the realtime path.

The internal control rate should be significantly faster than the USB HID report rate.

Candidate targets:

- input/force-control loop: 20–50 kHz;
- USB HID: up to 8 kHz;
- lower-rate telemetry/ergonomic analysis: separate task/domain.

These values are targets to validate rather than hard-coded requirements.

## Tracking

Primary optical sensor target: modern high-end PixArt-class device capable of at least 20,000 DPI.

The design is primarily for mouse pads and ordinary surfaces. Exotic glass/mirror tracking is not a core requirement.

The optical sensor should be mounted as its own module during early ergonomic tests so that its longitudinal position can be varied before the final chassis is frozen.

## Primary buttons

LMB and RMB are independent replaceable cartridges.

Each cartridge should eventually contain:

- titanium button/lever;
- two miniature precision bearings;
- axle;
- permanent magnet system;
- Hall position sensor;
- bidirectional electromagnetic actuator;
- hard mechanical safety stop;
- local calibration data;
- connector to the main board.

The permanent magnets provide the passive equilibrium/return force and support the resting finger.

The electromagnet modifies the force curve only when required.

Conceptually:

```text
F = F_passive(x) + F_coil(x, I, direction, velocity, profile)
```

This allows different actuation depths, reset points, tactile snaps and force profiles without changing the electrical sensing mechanism.

## Wheel

The wheel separates three functions that conventional mice often combine mechanically:

1. precise angular measurement;
2. rotational tactile feel;
3. middle-button/vertical movement.

Rotation:

- precision bearings;
- permanent magnet rotor;
- absolute magnetic angle sensor, AS5047-class or better;
- electromagnetic torque/detent actuator.

The firmware may implement:

- free-spin;
- coarse detents;
- fine detents;
- variable detent spacing;
- speed-dependent detent strength;
- application-defined tactile landmarks.

Wheel press:

- separate Hall-based displacement sensing;
- passive magnetic return;
- programmable tactile force where useful.

## Center of mass

The mouse is intentionally relatively heavy.

Initial target:

- nominal mass: approximately 220–260 g;
- adjustable development envelope: approximately 180–300 g.

The center of mass should be:

- low in the chassis;
- biased toward the palm;
- independently tunable from optical sensor position.

Dense removable ballast such as tungsten is preferred over making every structural part unnecessarily thick.

## Mechanical architecture

The chassis should be long-lived while service items remain replaceable.

```text
mouse chassis
├── LMB cartridge
├── RMB cartridge
├── wheel module
├── optical sensor module
├── main controller PCB
├── USB-C daughterboard
├── ballast modules
└── replaceable feet
```

External material direction:

- titanium shell/buttons/wheel where tactile value justifies it;
- hardened steel or ceramic for shafts/bearing interfaces where appropriate;
- engineered polymers for low-friction stops or isolation;
- PTFE-class replaceable feet.

Avoid titanium-on-titanium sliding pairs.

## USB

Fully wired.

The USB-C receptacle is recessed into the front of the chassis so the cable exits naturally without the plug becoming the primary mechanical strain member.

The USB connector should preferably live on a small replaceable daughterboard.

Normal operating system behavior:

- enumerate as a standard USB HID mouse;
- function without custom drivers.

Advanced behavior:

- separate configuration/vendor interface.

## Security

Security is architectural from V1 but optional hardware can be populated later.

Reserve:

- secure-element bus/pads;
- signed firmware/update path;
- device identity;
- future mutual host/device authentication;
- privileged vendor protocol independent from ordinary HID input.

The ordinary HID path must remain simple and interoperable.

## Telemetry and adaptation

An optional IMU plus the normal sensors can characterize real use:

- translational vs rotational movement;
- resting button displacement;
- actual click travel;
- click velocity;
- wheel acceleration;
- settling/overshoot after motion.

Adaptive behavior should initially **recommend** calibration changes rather than silently changing the mouse during use.

The purpose is to tune the device to the owner, not to introduce unpredictable automation.
