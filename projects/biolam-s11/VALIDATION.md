# Validation strategy · preliminary release gates

## G0 — non-destructive metrology
Photograph front, side, top, knobs, turret, condenser and table with scale. Caliper the base, stage screws, optical center, lamp mount, knob shafts, focusing stroke and external gear spaces. Measure safe objective swept envelopes and work distances in all positions. Record focus force/torque and whether the tube drifts under gravity.

## G1 — V4L2 baseline
Run the following on the Linux machine that currently has the microscope USB camera attached:

    v4l2-ctl -d /dev/video2 --list-formats-ext
    v4l2-ctl -d /dev/video2 --list-ctrls-menus
    v4l2-ctl -d /dev/video2 --get-ctrl=auto_exposure,exposure_time_absolute
    v4l2-ctl -d /dev/video2 --stream-mmap --stream-count=150 --stream-to=/dev/null --verbose

Identify the camera by stable /dev/v4l/by-id or by-path link; /dev/video2 can change on reconnect. Test MJPG and YUYV with explicitly set modes, FPS measurements, dropped-frame accounting, actual sensor-detail tests, flat-field and noise. Manual exposure only after saving original settings.

## G2 — independent lighting power/thermal bench
Use regulated **current-limited** source and attached heatsink to establish actual COB voltage/current/thermal behavior; distinguish the contradictory 9–11 V, 300 mA, 10 W advertisement. Choose constant-current LED drivers, two independently controllable channels, check flicker/banding and thermal soak with passive cooling. Validate RGB level shifting and supply separation.

## G3 — actuators and geometry
Test upper-head miniature actuator candidates for real angular repeatability, backlash, stiffness, hold power, noise and park sensor. Check focus gearbox torque and brake or self-holding behavior. Use real measured full swept volumes (head, cable, X/Y/Z, objective turret); OpenSCAD v0.1 visual arcs are not collision evidence.

## G4 — fault injection and emergency stop
Physical E-STOP must interrupt the enable/power path without Linux, Orange Pi or Ethernet. Verify on hardware: PC hang, Orange Pi crash, LAN unplug, sensor cable break, excessive force and current, lost position, overtravel, stuck outputs, uncontrolled focus drop, interrupted homing, queued commands at reboot. E-STOP reset may not restore motion without explicit re-arm and a fresh command.

## G5 — optical and image quality acceptance
Compare original condenser/auxiliary lens/iris against alternative layouts at 8x, 40x, 90x oil-immersion as applicable. Quantify uniformity, contrast, vignetting, actual detail; determine whether top illumination is geometrically possible for a selected objective. Preserve raw capture records, all illumination setpoints, X/Y/Z feedback, exposure and timestamps for mosaics, focus stacks and multi-light captures.
