// D2-OVERHEAD-01 -- OpenSCAD 3D experimental OVER-MONITOR arrangement.
// NOT a final cabinet, stand, bracket, speaker cutout/drill, safety design.
// Units METRES, scene is scaled in absolute SI units. OpenSCAD F5/F6.
// World coordinates: x = sideways, y = depth from ear towards speakers,
// z = height ABOVE desk. Listener ear is [0,0,ear_height_m].
// Real screen/stand dimensions are still unknown and example-only.
//
// The front face normal points DIRECTLY at reference ear from an acoustic
// axis placed at [0,speaker_distance_m,acoustic_axis_height_m].
// 0° roll: vertical LOW->MID->HIGH; 45° diagonal; 90° horizontal.
// The local 3-way driver centres are dimensioned from factory flange models
// WF168WA06 (168mm), MR120BD02 (120mm), TW030WA22 (104mm).
//
// Source: projects/diy-speakers/simulation/threeway_overhead_geometry.py
// The display-screen obstruction is a GEOMETRIC ray proxy only.
// Actual stand/baffle support geometry, mass/centre of gravity, clearance,
// monitors and cable loads require separate physical engineering.

$fn=64;
layout_type="vertical"; // "vertical" or "side_low_left"
roll_deg=90; // 0, 45, 90; arbitrary experimental roll allowed
acoustic_axis_height_m=.65;
ear_height_m=.35;
speaker_distance_m=.70;
monitor_front_distance_m=.35;
screen_top_height_m=.45;
screen_width_m=.60;
screen_thickness_m=.02;
show_monitor=true;
show_desk=true;
show_reference_rays=true;
show_placeholder_stand=false;
show_reference_listener=true;
show_baffle=true;

is_vertical=(layout_type=="vertical");
assert(is_vertical || layout_type=="side_low_left",
       "layout_type must be vertical or side_low_left");
assert(acoustic_axis_height_m>0 && ear_height_m>0 && speaker_distance_m>0);

pitch_deg=atan((acoustic_axis_height_m-ear_height_m)/speaker_distance_m);
baffle_width_m=is_vertical?.205:.330;
baffle_height_m=is_vertical?.440:.290;
// panel center offset from nominal acoustic-axis XY, before body roll
panel_offset=is_vertical?[0,-.0905]:[-.0865,-.016];
low_xy=is_vertical?[0,-.2075]:[-.149,-.0585];
mid_xy=[0,-.0585];
high_xy=[0,.0585];

function local3(xy)=[xy[0],xy[1],0];
function to_world(xy)=
  // This intentionally mirrors the order of the two rigid rotations:
  // R_x(90+pitch) * R_z(roll)
  let(x=xy[0], y=xy[1],
      c=cos(roll_deg), s=sin(roll_deg),
      xr=x*c-y*s, yr=x*s+y*c)
  [
    xr,
    speaker_distance_m-yr*sin(pitch_deg),
    acoustic_axis_height_m+yr*cos(pitch_deg)
  ];

module line3(a,b,r=.0018){
  hull(){
    translate(a) sphere(r=r);
    translate(b) sphere(r=r);
  }
}

module flange(xy, diameter, col){
  color(col,0.72) translate([xy[0],xy[1],.004])
    cylinder(d=diameter,h=.006,center=true);
  color([.12,.12,.12],1) translate([xy[0],xy[1],.011])
    cylinder(d=diameter*.63,h=.008,center=true);
}

if(show_desk)
  color([.68,.58,.42],.33)
  translate([-.55,-.12,-.026])
    cube([1.1,1.08,.026]);

if(show_monitor)
  color([.18,.21,.25],.56)
  translate([-screen_width_m/2,monitor_front_distance_m,
             .0])
    cube([screen_width_m,screen_thickness_m,screen_top_height_m]);

if(show_reference_listener)
  color([.15,.8,.8])
    translate([0,0,ear_height_m]) sphere(r=.012);

if(show_placeholder_stand)
  color([.55,.55,.55],.7) {
    translate([.0,speaker_distance_m+.03,0])
      cylinder(r=.01,h=max(.01,acoustic_axis_height_m-.08));
    translate([0,speaker_distance_m+.03,.012])
      cube([.13,.13,.024],center=true);
  }

translate([0,speaker_distance_m,acoustic_axis_height_m])
rotate([90+pitch_deg,0,0])
rotate([0,0,roll_deg]) {
  if(show_baffle)
    color([.55,.65,.73],.28)
    translate([panel_offset[0],panel_offset[1],-.012])
      cube([baffle_width_m,baffle_height_m,.024],center=true);
  flange(low_xy,.168,[.27,.49,.76]);
  flange(mid_xy,.120,[.31,.75,.54]);
  flange(high_xy,.104,[.77,.51,.62]);
}

if(show_reference_rays) {
  color([.19,.84,.9],.8)
    line3(to_world(low_xy),[0,0,ear_height_m]);
  color([.19,.84,.9],.8)
    line3(to_world(mid_xy),[0,0,ear_height_m]);
  color([.19,.84,.9],.8)
    line3(to_world(high_xy),[0,0,ear_height_m]);
}
// For engineering measurements, record real screen plane, heights,
// speaker/stereo x positions and monitor arms before choosing an assembly.
