// D2-GEO-01: Wavecor three-way EXPERIMENTAL FLAT BAFFLE (not a final cabinet).
// Dimensions from official Wavecor factory PDF outline drawings.
// Nominal mm; repeat measurements on purchased exact speaker parts before cutting.
// This is a viewing and fixture-planning model, NOT a CNC/drill production template.
// LOW: WF168WA06 Ø168 outer, rear max Ø143, bolt circle Ø159, depth 73.
// MID: MR120BD02 round Ø120 outer, rear Ø98, bolt circle Ø110, depth 64.
// HIGH: TW030WA22 Ø104 outer, rear max Ø80, bolt circle Ø92, depth 30.
//
// An independent SEALED net ~2L MID chamber is required for the future bench.
// It is NOT modeled here. Do not attach a 3-way speaker to an open panel for
// unrestricted bass testing.
//
// Correct reference layout: center XYZ from BOTTOM-LEFT FRONT VIEW:
// LOW=(102.5,103.0); MID=(102.5,252.0); HIGH=(102.5,369.0).
// Vertical acoustic ear target is halfway between MID and HF at y=310.5mm
// measured from lower edge; nominal only.
// Source: https://www.wavecor.com/Driver%20specifications%20PDF/
// Fixture study: projects/diy-speakers/simulation/threeway_baffle_geometry.py

$fn = 128;
panel_w = 205; // mm
panel_h = 440; // mm
panel_thickness = 18; // preview-grade plywood only

show_plate = true;
show_driver_flange_envelopes = true;
show_mount_circle_guides = true;
show_ear_axis = true;
// DO NOT set this to true and machine the result without remeasuring parts.
illustrative_rear_cutouts = false;

low_xy = [102.5,103.0];
mid_xy = [102.5,252.0];
high_xy= [102.5,369.0];

low_outer_d = 168;
mid_outer_d = 120;
high_outer_d = 104;

// These are BACKSIDE ENVELOPES, not approved production routings.
low_rear_max_d = 143;
mid_rear_max_d = 98;
high_rear_max_d = 80;

// Bolt circle positions are FOR VISUAL GUIDANCE ONLY.
module envelope(center, d, tint, depth=2) {
  color(tint, 0.58)
    translate([center[0],center[1],panel_thickness+0.5])
      cylinder(d=d,h=depth);
}

module bolt_guides(center, bolt_circle_d, angles) {
  for (angle = angles)
    color([0.14,0.24,0.27,1])
      translate([
        center[0]+bolt_circle_d/2*cos(angle),
        center[1]+bolt_circle_d/2*sin(angle),
        panel_thickness+2.6
      ])
        cylinder(h=1.2,d=4.5);
}

if (show_plate)
  color([0.8,0.72,0.55,1])
    difference() {
      cube([panel_w,panel_h,panel_thickness]);
      if (illustrative_rear_cutouts) {
        // Rough visualization, NOT a machining allowance or tolerance plan.
        for (rec = [
          [low_xy,low_rear_max_d],
          [mid_xy,mid_rear_max_d],
          [high_xy,high_rear_max_d]
        ])
          translate([rec[0][0],rec[0][1],-0.1])
            cylinder(d=rec[1]+1,h=panel_thickness+0.2);
      }
    }

if (show_driver_flange_envelopes) {
  envelope(low_xy,low_outer_d,[0.23,0.39,0.58]);
  envelope(mid_xy,mid_outer_d,[0.18,0.57,0.49]);
  envelope(high_xy,high_outer_d,[0.61,0.45,0.67]);
}

if (show_mount_circle_guides) {
  bolt_guides(low_xy,159,[0,90,180,270]);
  bolt_guides(mid_xy,110,[0,90,180,270]);
  bolt_guides(high_xy,92,[45,135,225,315]);
}

if (show_ear_axis)
  color([0.05,0.74,0.85,0.8])
    translate([0,310.5,panel_thickness+3.0])
      cube([panel_w,0.8,0.8]);

// Keep the panel as a REMOVABLE jig. Real speaker construction should use
// actual measured acoustic centres, angular FRD/IR and updated clearances.
