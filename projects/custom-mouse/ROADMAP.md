# Roadmap

## Phase 0 — lock interfaces, not shapes

Define electrical and mechanical boundaries for:

- button cartridge;
- wheel module;
- optical sensor module;
- USB daughterboard;
- main MCU board.

Avoid committing to final titanium geometry.

## Phase 1 — prove programmable physical controls

Complete:

- M1 button bench;
- M2 wheel bench.

These are the most novel subsystems and therefore deserve validation first.

Deliverables:

- repeatable force/travel plots;
- stable Hall measurement;
- several convincing button profiles;
- free-spin + programmable wheel detents;
- thermal/current measurements.

## Phase 2 — make a real wired mouse

Complete:

- M3 main controller;
- M4 optical tracking.

Deliverable:

A plain but extremely low-level-controlled wired mouse that moves a cursor and reports buttons/wheel through standard HID.

## Phase 3 — integrate the novel mechanics

Complete:

- M5 dual button cartridges;
- M6 full wheel module.

Deliverable:

Functional mouse with the intended contactless input philosophy.

## Phase 4 — fit it to the owner

Complete:

- M7 development chassis;
- M8 ergonomic telemetry.

Experiment with:

- 180–300 g mass range;
- palm-biased CG;
- low CG;
- sensor fore/aft position;
- button lever geometry;
- wheel position.

Freeze geometry only after actual-use measurements.

## Phase 5 — final electronics and titanium

Complete:

- M9 production-like electronics;
- M10 titanium mechanical prototype.

This is the point where expensive machining becomes justified.

## Phase 6 — security and software polish

Complete:

- M11 security;
- M12 calibration/adaptive software.

The security layer should not compromise ordinary HID compatibility or the realtime input path.

## Definition of success

The mouse should feel like a precision instrument rather than a consumable peripheral:

- no contact wheel encoder;
- no conventional switch contacts in the primary buttons;
- replaceable control modules;
- programmable force and detents;
- stable high-rate wired input;
- owner-tuned mass/CG/sensor position;
- long-lived titanium exterior;
- replaceable wear items;
- firmware and security under owner control.
