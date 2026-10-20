/*
Biolam S-11: parametric *layout envelope* v0.1 (2026-10-20)
Not metrology, not a printable adapter, not collision certification.
All dimensions in mm. External nominal limit 230 x 140 x 360 mm
(source: original Biolam documentation); this placeholder uses
140 mm across X and 230 mm front-back Y, subject to direct measurement.
Coordinates: x = left/right, y = front(-)/back(+), z = upward.
Optical axis = x:0, y:-25. All physical dimensions except the
external envelope are explicitly ASSUMED, not measured.
*/
$fn = 48;

// ---- Owner-editable parameters (MEASURE before fabrication) ----
show_microscope = true;
show_lower_light = true;
show_upper_light = true;
upper_parked = false;
show_work_envelopes = true;
show_reference_axes = true;
show_dimensions_outline = true;

base_width = 140;           // ASSUMED orientation of 230 x 140 footprint
base_depth = 230;
base_height = 15;
foot_radius = 20;
post_y = 61;               // ASSUMED
post_radius = 18;          // ASSUMED
optical_y = -25;           // ASSUMED
stage_z = 125;             // ASSUMED
stage_width = 105;         // ASSUMED
stage_depth = 95;          // ASSUMED
stage_thickness = 7;      // ASSUMED
stage_aperture_d = 28;     // ASSUMED; optical vignetting not evaluated

focus_knob_y = 47;        // ASSUMED
focus_knob_z = 187;       // ASSUMED
focus_knob_x = 51;        // ASSUMED
focus_knob_d = 34;        // ASSUMED

upper_work_xyz = [76, -43, 181];    // ASSUMED
upper_park_xyz = [103, 58, 205];   // ASSUMED; no collision proof
upper_azimuth_sweep = 90;           // REQUIREMENT: total ~quarter circle
upper_elevation_sweep = 34;         // ASSUMED
upper_head_tilt_sweep = 60;         // ASSUMED
upper_head_diameter = 26;          // ASSUMED COB + heatsink volume
lower_head_diameter = 29;          // ASSUMED
lower_head_height = 16;           // ASSUMED

xy_x_travel = 35;           // PLACEHOLDER, NOT a spec
xy_y_travel = 35;           // PLACEHOLDER, NOT a spec

upper_xyz = upper_parked ? upper_park_xyz : upper_work_xyz;
optic_xyz = [0, optical_y, stage_z];

// ---- Drawing helpers ----
module capsule_link(a, b, r1, r2) {
    hull() {
        translate(a) sphere(r = r1);
        translate(b) sphere(r = r2);
    }
}
module cylinder_between(a, b, r) {
    d = b - a;
    h = norm(d);
    if (h > 0.0001)
        translate(a)
            rotate(a = acos(d[2]/h), v = cross([0, 0, 1], d))
                cylinder(h = h, r = r, center = false);
}
module hoop(ro, ri, height) {
    difference() {
        cylinder(r = ro, h = height, center = true);
        cylinder(r = ri, h = height + 0.2, center = true);
    }
}
module translucent_box(size, center_pos, tint = [0.1, 0.6, 1.0, 0.15]) {
    color(tint) translate(center_pos) cube(size, center = true);
}

// ---- Existing microscope: symbolic body + optics ----
module frame_body() {
    color([0.22, 0.25, 0.28]) {
        hull() {
            for (x = [-base_width/2+foot_radius, base_width/2-foot_radius])
                for (y = [-base_depth/2+foot_radius, base_depth/2-foot_radius])
                    translate([x,y,base_height/2]) cylinder(r = foot_radius, h = base_height, center = true);
        }
        capsule_link([0,post_y,31], [0,post_y,231], post_radius, 20);
        capsule_link([0,post_y,233], [0,optical_y,253], 20, 16);
    }
    color([0.7,0.72,0.73]) {
        translate([0,optical_y,259]) cylinder(r = 16, h = 57);
        translate([0,optical_y,316]) cylinder(r = 11, h = 26);
        translate([0,optical_y,342]) cylinder(r = 15, h = 13); // camera adapter envelope
    }
    // Three objective stations: schematic only, no actual turret geometry
    color([0.45,0.47,0.49]) translate([0,optical_y,219]) cylinder(r = 26, h = 13);
    for (ang=[0,120,240]) {
        xx = 15*cos(ang);
        yy = 15*sin(ang);
        color([0.75,0.76,0.78]) translate([xx,optical_y+yy,184]) cylinder(r = 7, h = 38);
        color([0.22,0.22,0.24]) translate([xx,optical_y+yy,183]) cylinder(r = 8, h = 5);
    }
    // Visible external focusing knobs; the mechanism is NOT modeled.
    color([0.15,0.17,0.19])
        for (s=[-1,1])
            translate([s*focus_knob_x,focus_knob_y,focus_knob_z])
                rotate([0,90,0]) cylinder(r=focus_knob_d/2,h=8,center=true);
}

module stage_and_condenser() {
    color([0.36,0.40,0.42])
        translate([0,optical_y,stage_z])
            difference() {
                cube([stage_width,stage_depth,stage_thickness],center=true);
                cylinder(d=stage_aperture_d,h=stage_thickness+2,center=true);
            }
    // ESD insert / PCB support is a removable design proposal, not an existing part.
    color([0.20,0.40,0.35])
        translate([0,optical_y,stage_z+stage_thickness/2+2])
            difference() {
                cube([stage_width-10,stage_depth-10,4],center=true);
                cylinder(d=stage_aperture_d,h=6,center=true);
            }
    color([0.5,0.51,0.52]) {
        translate([0,optical_y,94]) cylinder(r=19,h=19);
        translate([0,optical_y,89]) cylinder(r=23,h=4);
    }
    color([0.1,0.1,0.1]) translate([0,optical_y,87]) hoop(22,15,2); // iris envelope
}

// ---- Proposed lower lighting: placeholder modules ----
module rgb_ring(r = 17, z = 0) {
    color([0.14,0.16,0.18]) translate([0,0,z]) hoop(r+2,r-1.8,3);
    for (a=[0:45:315])
        color([0.10+0.60*(1+cos(a))/2,0.12+0.65*(1+sin(a))/2,0.3])
            translate([r*cos(a),r*sin(a),z]) cube([3,3,2],center=true);
}
module lower_light() {
    translate([0,optical_y,50]) {
        color([0.55,0.55,0.57]) cylinder(d=lower_head_diameter+12,h=lower_head_height);
        color([1.0,0.87,0.65]) translate([0,0,lower_head_height]) cylinder(d=lower_head_diameter,h=2);
        translate([0,0,lower_head_height+3]) rgb_ring(r=21);
    }
}

// ---- Upper head: three DOF shown as envelopes, not manufactured joints ----
module upper_light_head() {
    // Main support is shown only as a rigid conceptual link.
    color([0.50,0.52,0.54]) {
        cylinder_between([0,post_y,215], [upper_xyz[0]*0.72,upper_xyz[1]*0.65+post_y*0.35,upper_xyz[2]+15],3.5);
        cylinder_between([upper_xyz[0]*0.72,upper_xyz[1]*0.65+post_y*0.35,upper_xyz[2]+15],upper_xyz,3.0);
    }
    // Lighting head points toward specimen in working mode.
    vec = optic_xyz - upper_xyz;
    head_len = norm(vec);
    translate(upper_xyz)
        rotate(a=acos(vec[2]/head_len),v=cross([0,0,1],vec)) {
            color([0.55,0.56,0.58]) cylinder(d=upper_head_diameter+12,h=16);
            color([1.0,0.88,0.70]) translate([0,0,16]) cylinder(d=upper_head_diameter,h=2);
            translate([0,0,19]) rgb_ring(r=upper_head_diameter/2+5);
        }
    color([0.8,0.4,0.13]) translate(upper_xyz) sphere(r=4);
}

module motion_envelopes() {
    // Pale translucent slabs only: never interpreted as verified collision bounds.
    translucent_box([stage_width+xy_x_travel,stage_depth+xy_y_travel,3],
                    [0,optical_y,stage_z+15],[0,0.85,0.7,0.14]);
    color([0.95,0.45,0.10,0.12])
        for (a=[-upper_azimuth_sweep/2:5:upper_azimuth_sweep/2])
            translate([75*cos(a), optical_y+75*sin(a), 176]) sphere(r=4);
    // Park-clearance candidate; needs physical measurements and full swept-volume check.
    color([0.15,0.85,0.25,0.25]) translate(upper_park_xyz) sphere(r=upper_head_diameter);
}
module drawing_axes() {
    color([1,0.2,0.2]) cylinder_between([-85,0,0],[85,0,0],0.7);
    color([0.2,0.85,0.2]) cylinder_between([0,-140,0],[0,140,0],0.7);
    color([0.2,0.3,1]) cylinder_between([0,0,0],[0,0,380],0.7);
    color([1,0.1,0.8]) cylinder_between([0,optical_y,0],[0,optical_y,350],0.5);
}
module outer_envelope() {
    // Documented overall bounding dimensions only; actual orientation pending.
    color([0.8,0.8,0.2,0.06]) translate([0,0,180]) cube([base_width,base_depth,360],center=true);
}

if (show_microscope) {frame_body();stage_and_condenser();}
if (show_lower_light) lower_light();
if (show_upper_light) upper_light_head();
if (show_work_envelopes) motion_envelopes();
if (show_reference_axes) drawing_axes();
if (show_dimensions_outline) outer_envelope();
