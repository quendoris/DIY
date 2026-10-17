# Passive Magnetic Button Feel

Status: **architectural requirement; detailed magnet geometry remains experimental**.

## Non-negotiable behavior

LMB and RMB must each be satisfying, repeatable physical controls when their electromagnetic actuators are fully unpowered.

With the coil disconnected, a cartridge must provide:
- passive stable rest and return;
- a perceptible tactile force peak followed by a controlled drop or similarly clear passive tactile transition;
- predictable press and release behavior;
- low side-play and no sticking;
- quiet top-out and bottom-out without metal-to-metal impact;
- no conventional electrical switch contacts.

The coil may refine the force curve, provide gentle dynamic damping, or allow optional profiles. It must **not** be necessary for the fundamental click feel or return.

## Button-specific geometry

Unlike a keyboard key, each mouse button is a short-travel pivot lever. The finger load acts at a distance from the bearing axis, so the mechanism must be measured as a lever system.

Keep the following independently tunable in the parametric model:
- fingertip lever arm;
- pivot-axis position and bearing spacing;
- total travel and safety-stop position;
- magnet-to-magnet and magnet-to-pole-piece clearances;
- sensing magnet orientation and Hall/TMR placement;
- coil location and travel clearance;
- replaceable stop material and thickness;
- cartridge mounting datums.

A bearing-supported lever remains the preferred baseline over a flexure because a plastic flexure's behavior does not transfer directly to a titanium final part.

## Passive force profile

A simple axial pair of repelling magnets generally creates a smooth restoring force; it does not automatically create a satisfying click-like force peak and drop.

Investigate at least:
1. separate passive return magnets plus a symmetric magnetic pass-by/detent geometry;
2. a moving magnet interacting with a shaped ferromagnetic pole piece/flux path;
3. alternative magnet orientation and spacing that preserve one stable rest state.

Avoid accidental bistability or a latch that can leave the button depressed. The released button must return from every intended point in the stroke with the coil off.

The design decomposition is:

    F_finger(x) = F_return_passive(x)
                + F_tactile_detent_passive(x)
                + F_coil(x, I, direction, velocity, profile)
                + F_friction_and_damping(x, velocity)

This is a useful bookkeeping model, not a guarantee that magnetic components superpose linearly. Interactions and lever torque must be measured.

## Sensing and control

Hall/TMR is a continuous displacement sensor, not the tactile mechanism itself. The controller separately decides:
- actuation threshold;
- release/reset threshold;
- filtering and debounce;
- optional resting-finger compensation;
- optional coil assistance.

Never allow adaptive baseline tracking to swallow a slow intentional press. Test slow presses, long holds, repeated taps, off-axis force and finger resting loads.

## Bench gate

Before integrating LMB/RMB into the chassis, record with the coil disconnected:
- force vs fingertip travel on press and release;
- peak force and force drop;
- rest-return from multiple intermediate positions;
- return latency;
- repeatability across cycles and temperature;
- button vibration and sound;
- bearing friction and side-play.

Then repeat with a modest coil assist. The active system passes only if it improves a satisfactory passive baseline without excessive heat, audible coil noise or unpredictable click behavior.

A coil-free cartridge remains an acceptable final configuration if active assistance does not justify its cost and complexity.
