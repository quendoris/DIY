/*
 DIY Custom Mouse — ergonomic envelope v0.1
 Status: visual/ergonomic concept model, NOT a manufacturing-ready shell.
 Units: mm. Coordinates: front/cable = y 0; rear/palm = positive y;
 right-hand pinky/ring-finger support = positive x.

 Primary reference: user-provided white angular mouse concept (2026-10-17).
 The shape is intentionally parameterized. Tune after low-cost hand-fit prototypes.
*/

$fn = 40;

// ---- Global envelope ----
body_length = 132;
body_width_max = 78;
body_height_max = 42;
show_shell = true;
show_buttons = true;
show_wheels = true;
show_cable = true;
show_lighting = true;
show_thumb_buttons = true;
show_right_finger_shelves = true;

// ---- Adjustable ergonomics ----
// The current values are a starting envelope, not a hand-fit guarantee.
scale_x = 1.00;
scale_y = 1.00;
palm_hump_delta = 0;          // reserved for raised/curved crown variants
ring_shelf_z = 15;             // higher forward support for ring finger
pinky_shelf_z = 11;            // separate lower/rear support for pinky
shelf_projection = 11.5;       // nominal projection from right body side
shelf_length = 22;

// ---- Visual palette for OpenSCAD preview only ----
metal = [0.61, 0.67, 0.69];
metal_dark = [0.30, 0.35, 0.37];
metal_edge = [0.55, 0.61, 0.63];
wheel_rubber = [0.72, 0.78, 0.79];
cyan = [0.02, 0.86, 0.93];
button_surface = [0.83, 0.87, 0.88];

module faceted_plate(top_points, thickness=2) {
    // Convex hull of tiny vertical prisms yields a robust faceted plate without
    // non-planar polyhedron faces. It is a visual envelope, not a finished part.
    hull() {
        for (p = top_points)
            translate([p[0], p[1], p[2] - thickness/2])
                cube([0.35, 0.35, thickness], center=true);
    }
}

module core_envelope() {
    // Hull through cross-section-sized blocks creates the faceted elongated body.
    hull() {
        translate([0, 7, 12])   cube([48, 18, 20], center=true);
        translate([0, 28, 14])  cube([62, 28, 25], center=true);
        translate([0, 55, 15])  cube([72, 42, 29], center=true);
        translate([0, 81, 15])  cube([76, 40, 29], center=true);
        translate([0, 105, 13]) cube([66, 32, 25], center=true);
        translate([0, 124, 10]) cube([46, 17, 18], center=true);
    }
}

module palm_crown() {
    // Broad, sharply outlined rear palm panel. Its planar top is deliberate for v0.1;
    // later variants can compare faceted/raised crowns against ergonomic hand-fit shells.
    translate([0,0,29])
        linear_extrude(height=3, convexity=4)
            polygon(points=[
                [-28, 83], [-12, 87], [12, 86], [29, 81],
                [32, 101], [22, 122], [-22, 122], [-32, 101]
            ]);
}

module left_click_panel() {
    faceted_plate([
        [-34, 34, 29], [-7, 30, 34.5], [-5, 76, 33.5],
        [-13, 82, 31], [-31, 77, 28], [-36, 52, 27]
    ], 2.2);
}

module right_click_panel() {
    faceted_plate([
        [ 7, 30, 34.5], [34, 34, 29], [36, 52, 27],
        [31, 77, 28], [13, 82, 31], [5, 76, 33.5]
    ], 2.2);
}

module click_panels() {
    color(button_surface) {
        left_click_panel();
        right_click_panel();
    }
}

module main_scroll_wheel() {
    // Wheel axis runs left-right (X). Contactless angle sensing + active detents are separate internals.
    translate([0, 22, 27]) {
        color(metal_dark)
            rotate([0,90,0]) cylinder(h=17, r=6.1, center=true, $fn=36);
        color(wheel_rubber)
            rotate([0,90,0]) cylinder(h=13.5, r=5.6, center=true, $fn=32);
        color(cyan)
            for (s = [-1,1])
                translate([s*8.7,0,0]) rotate([0,90,0])
                    difference() {
                        cylinder(h=1.0, r=6.8, center=true, $fn=36);
                        cylinder(h=1.3, r=5.9, center=true, $fn=36);
                    }
    }
}

module dpi_wheel() {
    // A small independent wheel replaces the conventional DPI +/- buttons.
    // Its exact reach and height are to be checked with a real-hand mockup.
    translate([0, 40, 29.4]) {
        color(metal_dark)
            rotate([0,90,0]) cylinder(h=10, r=3.6, center=true, $fn=28);
        color(wheel_rubber)
            rotate([0,90,0]) cylinder(h=7.8, r=3.1, center=true, $fn=28);
        color(cyan)
            for (s = [-1,1])
                translate([s*5.1,0,0]) rotate([0,90,0])
                    difference() {
                        cylinder(h=0.7, r=3.9, center=true, $fn=28);
                        cylinder(h=1.0, r=3.25, center=true, $fn=28);
                    }
    }
}

module side_shelf(y0, y1, z_top, side=1, projection=11.5) {
    // Separate polygonal ledge, partially embedded into the shell for a load-bearing interface.
    // Rounded/contact-edge treatment will be a later CAD layer, not a visual assumption.
    inner_x = 34.0;
    outer_x = inner_x + projection;
    pts = [
        [side*inner_x, y0, z_top],
        [side*outer_x, y0+3, z_top-0.8],
        [side*outer_x, y1-3, z_top-0.8],
        [side*inner_x, y1, z_top]
    ];
    color(metal_edge) faceted_plate(pts, 2.6);
}

module right_hand_finger_shelves() {
    // Two independent support steps: forward/higher ring-finger shelf and rear/lower pinky shelf.
    // The gap between them is intentional and may be tuned parametrically.
    side_shelf(55, 55+shelf_length, ring_shelf_z, 1, shelf_projection);
    side_shelf(77, 77+shelf_length, pinky_shelf_z, 1, shelf_projection);
    if (show_lighting) {
        color(cyan) {
            light_segment([40,58,ring_shelf_z-1.0], [40,69,ring_shelf_z-1.0], 0.55);
            light_segment([40,80,pinky_shelf_z-1.0], [40,91,pinky_shelf_z-1.0], 0.55);
        }
    }
}

module thumb_side_buttons() {
    // Two recessed side-button placeholders on the left/thumb side of a right-handed mouse.
    for (yy = [53, 66]) {
        color(metal_dark)
            translate([-36.5, yy, 20]) rotate([0,0,-8])
                cube([2.5, 9, 3.6], center=true);
        if (show_lighting)
            color(cyan)
                translate([-37.8, yy, 20]) rotate([0,0,-8])
                    cube([0.35, 5.2, 0.7], center=true);
    }
}

module light_segment(a, b, r=0.65) {
    hull() {
        translate(a) sphere(r=r, $fn=10);
        translate(b) sphere(r=r, $fn=10);
    }
}

module shell_lighting() {
    // Recessed-line visual guides only. Production light-pipe cross-sections are not yet modeled.
    color(cyan) {
        light_segment([-34,39,28.5], [-35,51,27.5], 0.48);
        light_segment([-35,51,27.5], [-31,69,28.5], 0.48);
        light_segment([34,39,28.5], [35,51,27.5], 0.48);
        light_segment([35,51,27.5], [31,69,28.5], 0.48);
        light_segment([-38,95,16], [-37,105,15], 0.55);
        light_segment([38,95,16], [37,105,15], 0.55);
    }
}

module cable_stub() {
    color([0.18,0.20,0.21])
        translate([0,-7,12]) rotate([90,0,0]) cylinder(h=22, r=2.6, center=true, $fn=24);
}

module mouse_envelope() {
    scale([scale_x, scale_y, 1]) {
        if (show_shell) {
            color(metal) core_envelope();
            color(metal) palm_crown();
        }
        if (show_buttons) click_panels();
        if (show_wheels) {
            main_scroll_wheel();
            dpi_wheel();
        }
        if (show_right_finger_shelves) right_hand_finger_shelves();
        if (show_thumb_buttons) thumb_side_buttons();
        if (show_lighting) shell_lighting();
        if (show_cable) cable_stub();
    }
}

mouse_envelope();
