# Mouse CAD

## Current model

- [mouse-envelope-v0.1.scad](mouse-envelope-v0.1.scad) — parametric exterior/ergonomic blockout based on the user's selected white angular reference.
- Status: **visual and ergonomic envelope only**. Not a manufacturing-ready shell, not yet hollow, and not dimensionally validated against a hand.

## Coordinate system

- Units: millimetres.
- Front/cable exit: `y = 0`; rear/palm: positive Y.
- Left/thumb side: negative X.
- Right/ring-finger and pinky side: positive X.
- Z is height from the nominal desk plane.

## First parameters to tune

- `body_length`: longitudinal scale of the envelope.
- `body_width_max`: width of the central body; the right-side finger shelves extend beyond it.
- `body_height_max`: height scale of the current visual envelope.
- `palm_hump_delta`: raises/lowers the rear palm panel.
- `ring_shelf_z`, `pinky_shelf_z`: separate step heights.
- `shelf_projection`, `shelf_length`: right-side finger support projection and length.
- `show_*`: toggle visual subassemblies.

The overall width includes the finger shelves and is therefore greater than `body_width_max`.

## Approximate v0.1 envelope

- Central body: about 132 mm long × 76 mm maximum width.
- Right-side shelves extend the total width to about 91 mm at their widest points.
- Current maximum modeled height: about 34.5 mm.
- Cable stub extends forward beyond the 132 mm body envelope.

These are CAD envelope dimensions, not ergonomic or manufacturing acceptance dimensions.

## What this version establishes

1. Long, faceted body inspired by the selected reference.
2. Separate LMB/RMB top panels.
3. Main scroll wheel plus a smaller independent DPI wheel (preserving the project's earlier control decision).
4. Two separate right-side finger-support steps: higher/front for the ring finger, lower/rear for the pinky.
5. Two thumb-side button placeholders.
6. Cable stub and visual-only cyan accent guides.

## Known limitations

- The main body is a solid envelope, not a hollow shell.
- Button panels, wheels, side shelves and cable are preview solids; module fasteners, bearing seats, Hall/TMR sensor, coils, USB-C recess, lens aperture and internal PCBs are not modeled yet.
- The two support steps are geometric placeholders. Their position, angle and contact area must be checked using hand-fit mockups.
- The model has not been verified for assembly clearance, 200–300 g mass distribution, wall thickness or final material behavior.
- OpenSCAD numeric precision does not guarantee manufacturing precision. Bearing/shaft fits and other critical dimensions require process-specific tolerances and physical fit coupons.

## Render and mesh validation

The current v0.1 source has been rendered through OpenSCAD's CGAL solid renderer; the combined concept mesh reports a simple 3D object. This is only a geometry-integrity check, not proof that the parts are manufacturable or ergonomic.

Example commands:

```bash
openscad -o mouse-envelope-v0.1.stl mouse-envelope-v0.1.scad
openscad -o mouse-envelope-preview.png --imgsize=1200,1000 --viewall mouse-envelope-v0.1.scad
```

Before fabrication, split the model into separately printable/machinable components, add shell thickness and serviceable joints, and run fit/clearance tests.
