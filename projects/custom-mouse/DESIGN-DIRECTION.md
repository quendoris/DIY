# Industrial Design Direction

Status: **direction approved; exact ergonomic geometry remains open until grip style and hand measurements are confirmed.**

## Primary reference is now selected

The user-selected white angular mouse image shared on 2026-10-17 supersedes the earlier candidate references. Adapt this silhouette deliberately rather than inventing a different mouse: preserve the long faceted top, split LMB/RMB panels, recessed center controls and restrained cyan channels, while replacing the weak right-side finger area with two distinct support steps and removing dust-trapping ornaments.

## Reference synthesis

The supplied white futuristic mouse is the primary silhouette reference:
- elongated, low, forward-reaching body;
- distinct LMB/RMB top panels;
- crisp faceted planes and deliberate seams;
- thin cyan/blue light accents that trace geometry rather than dominate it.

The supplied black mouse contributes secondary styling ideas:
- layered shell surfaces;
- deep but controlled recesses;
- angular shoulder/side transitions;
- narrow luminous channels integrated into the body.

These images are inspiration, not dimensioned engineering drawings. Do not copy ornamental features blindly.

## Core identity

The mouse should read as a **right-handed precision instrument**, not a mass-market gaming shell with decorations added.

- Right-handed ergonomic asymmetry is intentional.
- Target mass remains approximately 200–300 g, with adjustable ballast and a palm-biased center of mass under ergonomic test.
- Long, somewhat low silhouette is preferred over a short, bulbous shell.
- Straight facets and clear planes should dominate; curves are used where the hand needs support or a control needs smooth motion.
- The design must look coherent with lighting completely disabled.
- External titanium is a preferred direction, but material and finish must be selected for actual grip, cleaning, wear and manufacturing—not appearance alone.

## Right-side finger support

The current user-approved ergonomic direction is a **mixed/individual grip** with **two separate steps**: a higher/front ring-finger support and a lower/rear pinky support. Heights and longitudinal positions remain parameters until a hand-fit mockup is evaluated.

The current reference designs do not provide a sufficiently considered support surface for the ring finger and pinky. Our shell must solve this deliberately.

Explore an integrated right-side support with:
- a stable ledge/wing for the ring finger;
- a distinct, comfortable landing area for the pinky;
- controlled separation or a shallow contour between the two contact zones;
- no sharp load-bearing edge against the fingers;
- no exposed decorative wheel/turbine occupying the natural finger-rest area;
- a surface that remains comfortable during lifting, repositioning and fast wrist-driven movements.

Do not freeze the shape until grip style is confirmed and low-cost ergonomic shells have been tried. The finger shelf must not interfere with lifting the mouse or dragging it sideways.

## Cleanability and long service life

Avoid exposed ornamental turbines, open decorative apertures, deep blind grooves, thin fins and tiny cavities that collect skin oil, dust and debris.

Preferred construction:
- light exits through narrow recessed channels with protected diffusers/light pipes;
- light windows are sealed or accessible for cleaning without dismantling the core mechanism;
- panel seams are deliberate, accessible and kept away from the main finger-contact surfaces;
- the primary-button and wheel cartridges can be removed independently;
- bearing and sensor spaces are shielded from ordinary debris;
- no cosmetic component blocks service access to a replaceable part.

Any functional opening must have a documented purpose (motion clearance, heat, fastener, sensor optics, service access, etc.). A decorative slot is not sufficient justification for a through-hole.

## Controls

- LMB and RMB are separate replaceable bearing-supported cartridges.
- Main scroll wheel remains a precision module with contactless angle measurement and programmable electromagnetic detents.
- A separate small DPI wheel is preferred over two top-side DPI +/- buttons.
- The DPI wheel's color gradient represents the selected DPI/CPI profile, not instantaneous cursor velocity. Numeric settings remain available in configuration software.
- Side buttons should be reachable by the thumb without moving the hand off its natural support.
- Recessed detachable USB-C remains part of the front packaging; strain must be carried by the housing, not solder joints or the receptacle.

## Surface and finish

Preferred initial finish studies:
- matte titanium;
- fine satin titanium;
- contrasting darker, wear-resistant inset/insert where needed;
- replaceable textured grip insert only if bare metal proves slippery or uncomfortable.

Avoid mirror-chrome finish as the default. It emphasizes fingerprints and visible micro-scratches. Do not assume that titanium is immune to scratches, galling or finish wear.

Light should be restrained:
- thin cyan/blue geometry accents as the initial visual study;
- low brightness and an off profile;
- protected, diffused light guides rather than exposed LEDs;
- no direct RGB leakage into the optical tracking sensor.

## Open decisions before the first ergonomic shell

1. Grip style: palm, claw, fingertip or hybrid.
2. Hand dimensions and comfortable finger-reach envelope.
3. Required ring-finger/pinky shelf depth and angle.
4. Palm hump location and height.
5. Side-button reach and accidental-press limits.
6. Optical sensor position relative to the grip and center of mass.
7. Minimum wall/edge radii that preserve the crisp visual language without uncomfortable contact.

## CAD implementation

The first OpenSCAD envelope is stored in [cad/mouse-envelope-v0.1.scad](cad/mouse-envelope-v0.1.scad); scope and limitations are documented in [cad/README.md](cad/README.md). It is intentionally a blockout, not a production-ready model.

## CAD implementation

Use OpenSCAD for the parameterized shell envelope and control/module interfaces. Keep the ergonomic outer envelope separate from the button, wheel, sensor, USB-C and ballast modules.

Do not model the final titanium body first. Produce adjustable, inexpensive ergonomic shells and fit-check models; freeze the external silhouette only after actual-hand testing.
