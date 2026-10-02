# Development Modules

The project should be developed as independent bench modules first.

The ordering below is intentional: validate the unusual/high-risk mechanisms before spending money on the titanium chassis.

## M1 — Button Mechatronics Bench

Build one standalone LMB/RMB-equivalent cartridge.

Minimum elements:

- lever;
- two miniature bearings;
- axle;
- permanent magnets;
- linear Hall sensor;
- electromagnet/coil;
- bidirectional current driver;
- hard stop;
- temporary MCU/dev board.

What to measure:

- force vs travel;
- Hall linearity;
- resting-finger stability;
- attainable actuation travel;
- response time;
- coil current and temperature;
- repeatability;
- magnetic hysteresis;
- audible noise.

Success means one mechanism can convincingly produce several distinct button feels without mechanical switch contacts.

## M2 — Wheel Mechatronics Bench

Build the wheel independently.

Minimum elements:

- wheel/rotor;
- dual bearings;
- diametric magnet or suitable rotor magnet;
- absolute magnetic angle sensor;
- electromagnetic brake/torque actuator;
- temporary driver/controller.

Implement:

- raw absolute angle;
- velocity/acceleration estimate;
- free-spin;
- configurable detents;
- speed-dependent detent weakening;
- aggressive and very fine detent profiles.

This module should be tested before integrating it into a mouse shell.

## M3 — Main Controller + USB

Bring up the STM32H7S3-class controller.

Goals:

- stable USB HID mouse;
- high-speed USB path;
- deterministic timers/DMA;
- high-rate internal input loop;
- configuration/vendor interface;
- logging/telemetry.

At first, inject synthetic mouse events. Do not block this milestone on the optical sensor.

## M4 — Optical Tracking Module

Add the high-end optical sensor and optics.

Goals:

- raw motion acquisition;
- DPI configuration;
- lift-off behavior;
- stable tracking on the intended mouse pad;
- USB integration;
- adjustable sensor position in the development chassis.

Only after this milestone does the project become a functional pointing device.

## M5 — Integrated Button Pair

Convert M1 into two independently calibrated cartridges:

- LMB;
- RMB.

Add:

- per-cartridge ID/calibration;
- hot-serviceable mechanical mounting;
- independent force profiles;
- synchronized control loop.

## M6 — Integrated Wheel Module

Combine M2 with:

- middle-click displacement sensing;
- wheel force profiles;
- USB wheel events;
- application/configuration commands.

## M7 — Development Chassis + Mass System

Do **not** use the final titanium shell yet.

Build an adjustable chassis that permits:

- palm/shape experiments;
- button position changes;
- sensor position changes;
- ballast movement;
- cable exit experiments.

Add tungsten or equivalent dense removable ballast.

This stage determines the real center of mass and geometry.

## M8 — Ergonomic Telemetry

Add IMU and logging.

Measure actual owner use:

- translation vs rotation;
- acceleration;
- settling;
- preferred sensor location;
- resting button positions;
- click travel/velocity;
- wheel usage.

Use the data to choose final geometry and center of mass.

## M9 — Final Electronics

Design the integrated PCB set:

- main MCU board;
- button connectors;
- wheel interface;
- optical sensor interface;
- USB-C daughterboard;
- power/ESD;
- optional IMU;
- reserved secure-element footprint.

Freeze electrical interfaces before final chassis machining.

## M10 — Titanium Mechanical Prototype

Only now manufacture the expensive parts:

- titanium shell;
- titanium button levers;
- titanium wheel;
- final bearing seats;
- final ballast pockets.

Validate that the measured button/wheel dynamics still match the bench models.

## M11 — Security Module

Populate/enable the reserved security architecture.

Goals:

- secure boot/update;
- signed firmware;
- device identity;
- optional secure element;
- host/device challenge-response;
- privileged vendor channel.

Standard USB HID must continue to work without authentication.

## M12 — Calibration and Adaptive Software

Build the desktop/configuration tool.

Functions:

- DPI;
- button force curves;
- actuation/reset;
- wheel detent model;
- mass/sensor-position experiment logging;
- firmware updates;
- calibration;
- telemetry analysis;
- suggested adaptive profiles.

Automatic adaptation should be explicit and controllable by the user.
