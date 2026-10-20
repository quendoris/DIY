# OpenSCAD system envelope v0.1

**Source:** [biolam-s11-envelope-v0.1.scad](biolam-s11-envelope-v0.1.scad)

This is a **schematic whole-system model**, NOT an accurate factory replica, a set of 3D-printable parts, or a proven collision-free toolpath.

Coordinate frame: X left/right, Y forward(-)/back(+), Z upward. Optical axis nominally at X=0, Y=-25 mm (**assumed**). Documented maximum outer family size 230x140x360 mm; first model orients 140 mm across X and 230 mm across Y pending physical measurement. Except for this overall published value, geometry is **unmeasured**.

Modeled modules: pedestal + arm + tube + nominal objective turret, coarse-focus knobs, removable XY stage with center aperture, condenser and iris envelopes, lower COB/RGB, proposed 3-DOF upper lamp with working and parked poses, swept-zone illustrations.

## Usage

Open the SCAD source in OpenSCAD; set upper_parked=true or false to compare poses. Also toggle show_microscope, show_lower_light, show_upper_light, show_work_envelopes, show_reference_axes, show_dimensions_outline. Always check models from several camera angles.

Syntax-check using:
    
    openscad -o /tmp/biolam-v0.1.csg cad/biolam-s11-envelope-v0.1.scad

Headless preview (requires xvfb-run):

    xvfb-run -a openscad -o /tmp/biolam-v0.1.png --imgsize=1200,900 --autocenter --viewall cad/biolam-s11-envelope-v0.1.scad

## Measurements before detailed mechanical design

1. Exact base width/depth and optical axis relative to its center; curved arm dimensions.
2. Tube travel, focus knob position/diameter/shaft and available coupler clearance.
3. Stage fasteners and contact-plane height, XY travel budget, optical cone through opening.
4. Revolver and objectives: rotational sweep, working distance, Z collision thresholds.
5. Upper head: stationary clamping region, azimuth/elevation arcs, pitch, cable path and positively locked park zone.
6. Condenser components, led-heatsink geometry and working light distribution.

An actual 3-DOF collision model requires detailed kinematics plus sensor-error margins, not only the colored arc/sphere visualization in v0.1.
