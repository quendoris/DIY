// D2-STEREO-01: two Wavecor 3-way satellites above THREE monitor PLACEHOLDERS.
// Parametric conceptual viewer, NOT a cut-ready baffle or certified support.
// Source research: threeway_stereo_multimonitor.py
// UNITS: METRES. World X=left/right, Y=depth from listener towards monitors,
// Z=height above desk. Ear reference [0,0,.60] is user's HEAD height proxy.
// USER MEASURED: head +.60m, 32in top +.70m, existing 27in side top +.60m.
// NOT USER MEASURED: all screen x/depth/width, future screen top, ear canal,
// actual speakers, stand clamp/bracket strength, room ceiling, baffle diffraction.
//
// Render F5/OpenSCAD. Switch scenario from current to future.
// Both speakers maintain horizontal ±30deg stereo axis; local driver array
// rolls ±90deg so the two L/R speaker fronts mirror each other.
// The module computes exact yaw + down-pitch from each satellite to ears.

$fn=60;
scenario="future";  // "current" / "future"
speaker_depth=.70;    // distance from listener toward desk/monitors
source_axis_height=.92;
head_reference_height=.60; // MEASURED HEAD not ear canal
speaker_roll_deg=90;  // 0 vertical, ±45 diagonal, ±90 horizontal
nominal_horizontal_stereo_half_angle=30;
triangle_strategy="true_3d_equilateral";  // "plan_60deg" or "true_3d_equilateral"
show_baffles=true;
show_rays=true;
show_table=true;
show_supports=false; // these would be non-loadbearing illustrative rods!
show_ear_reference=true;

function dot(a,b)=a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
function cross(a,b)=[a[1]*b[2]-a[2]*b[1],
                      a[2]*b[0]-a[0]*b[2],
                      a[0]*b[1]-a[1]*b[0]];
function len(a)=sqrt(dot(a,a));
function normalized(a)=a/len(a);
function add(a,b)=a+b;
function scaled(t,a)=t*a;
function speaker_half_base()=
    triangle_strategy=="plan_60deg"
      ? speaker_depth*tan(nominal_horizontal_stereo_half_angle)
      : sqrt((speaker_depth*speaker_depth+
             (source_axis_height-head_reference_height)*
             (source_axis_height-head_reference_height))/3);
function drivers_x(side)=side*speaker_half_base();

module line3(a,b,r=.002){
  hull(){translate(a) sphere(r=r);translate(b) sphere(r=r);}
}
module displayed_screen(x,depth,width,top,bottom=0){
  color([.18,.22,.31],.5)
    translate([x-width/2,depth, bottom])
      cube([width,.013,top-bottom]);
  color([.12,.15,.20],.95)
    translate([x-width/2,depth,top-.008]) cube([width,.014,.008]);
}
if(show_table) color([.70,.60,.48],.3)
    translate([-1.65,-.11,-.025])cube([3.3,1.45,.025]);

// Width estimates for 16:9 geometry ONLY; future top heights are scenarios.
if(scenario=="current"){
    displayed_screen(0,.35,.708,.70);
    displayed_screen(.66,.40,.598,.60);
} else {
    displayed_screen(0,.35,1.196,.80);
    displayed_screen(-1.065,.42,.93,.73);
    displayed_screen(1.065,.42,.93,.73);
}

if(show_ear_reference) color([.16,.9,.84])
  translate([0,0,head_reference_height]) sphere(r=.017);

// WF168WA06 168mm; MR120BD02 120mm; TW030WA22 104mm.
// 205x440mm original reference baffle centers relative to MID/HIGH midpoint.
low_local=[0,-.2075,0];
mid_local=[0,-.0585,0];
high_local=[0,.0585,0];

module speaker(side){
  sx=drivers_x(side);
  center=[sx,speaker_depth,source_axis_height];
  direction=normalized([-sx,-speaker_depth,
                         head_reference_height-source_axis_height]);
  horizontal=normalized([speaker_depth,-sx,0]);
  local_up=normalized(cross(direction,horizontal));
  roll=side*speaker_roll_deg;
  u=cos(roll)*horizontal+sin(roll)*local_up;
  v=-sin(roll)*horizontal+cos(roll)*local_up;

  function_to_world_nothing=0; // just keep helper variables local
  mat=[
    [u[0],v[0],direction[0],center[0]],
    [u[1],v[1],direction[1],center[1]],
    [u[2],v[2],direction[2],center[2]],
    [0,0,0,1]
  ];

  module mount_source(p,d,colorv){
    color(colorv,.80) translate(p)
      cylinder(d=d,h=.01,center=true);
    color([.05,.08,.13],1) translate(p+[0,0,.009])
      cylinder(d=d*.6,h=.007,center=true);
  }

  multmatrix(mat){
    if(show_baffles)color([.57,.68,.74],.30)
      translate([-.205/2,-.0905-.440/2,-.014])
        cube([.205,.440,.022]);
    mount_source(low_local,.168,[.35,.55,.80]);
    mount_source(mid_local,.120,[.24,.75,.60]);
    mount_source(high_local,.104,[.78,.47,.64]);
  }
  if(show_rays) {
    color([.34,.82,.95],.75)
      line3(center+low_local[0]*u+low_local[1]*v,
            [0,0,head_reference_height]);
    color([.25,.88,.70],.80)
      line3(center+mid_local[0]*u+mid_local[1]*v,
            [0,0,head_reference_height]);
    color([.84,.62,.89],.8)
      line3(center+high_local[0]*u+high_local[1]*v,
            [0,0,head_reference_height]);
  }
  if(show_supports) color([.55,.56,.57],.55) {
    translate([sx,speaker_depth+.07,.02])
      cylinder(r=.013,h=source_axis_height-.09);
    translate([sx,speaker_depth+.07,.025])
      cube([.14,.14,.05],center=true);
  }
}

speaker(-1);
speaker(1);
// The rendered supports are NOT a load-bearing construction.
// Real table/wall mounting must be calculated, proof-loaded and secured
// to avoid falling multi-kilogram loudspeakers above the listener.
