# Custom Mouse

A fully wired, high-mass, repairable and deeply programmable precision mouse.

The project intentionally rejects several assumptions of mainstream gaming mice:

- minimum possible weight is not the primary goal;
- wireless operation is unnecessary;
- mechanical switch contacts and contact wheel encoders are avoidable wear mechanisms;
- the physical feel of controls does not need to be permanently fixed by springs and plastic geometry;
- the mouse should remain serviceable at module level;
- security should be part of the architecture from the start even if secure hardware is added later.

## Primary goals

- 20,000+ DPI, primarily optimized for a normal mouse pad;
- high-rate wired USB;
- recessed detachable USB-C connector;
- titanium-focused exterior and controls;
- target mass roughly 200–300 g;
- low center of mass biased toward the palm;
- replaceable ballast for center-of-mass tuning;
- contactless sensing for primary controls wherever practical;
- programmable electromagnetic feel for LMB/RMB and main scroll wheel;
- replaceable LMB and RMB cartridges;
- precision main-wheel rotation without a contact encoder;
- **proposed second compact DPI wheel** replacing the original two DPI +/- top buttons;
- configurable RGB gradient on the DPI wheel and restrained titanium-case accent lighting;
- replaceable feet, cable and connector daughterboard;
- firmware fully under our control;
- future secure host/device authentication.

## Core design principle

**Measure motion contactlessly; create tactile feel separately.**

**Passive-first button rule:** LMB/RMB must provide their basic tactile click and return with the electromagnetic coils disconnected. Active control may refine a good passive force curve but must not be required to create the click.

A control should not require the same mechanical element to perform sensing, return force and tactile feedback.

For the primary buttons this means:

```text
finger
  ↓
titanium lever
  ↓
precision pivot bearings
  ↓
moving permanent magnet
  ├── Hall position sensing
  └── passive magnetic return / support
            +
     controlled electromagnet
            ↓
 programmable force profile
```

For the main wheel:

```text
titanium wheel
    ↓
precision bearings
    ↓
absolute magnetic angle sensor
    +
electromagnetic torque/detent actuator
```

For the proposed secondary wheel:

```text
small DPI wheel
    ↓
contactless angular sensing
    ↓
DPI selection/profile mapping
    ↓
smooth RGB indication (green → yellow → red → violet → blue)
```

## Current status

**Architecture/design phase.**

The first hardware work should not begin with the final titanium shell. It should begin with independent bench modules for the two most novel mechanisms:

1. primary-button magnetic cartridge;
2. precision electromagnetic wheel.

See:

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [MECHANICS.md](MECHANICS.md)
- [MODULES.md](MODULES.md)
- [ROADMAP.md](ROADMAP.md)
- [DPI-WHEEL-AND-LIGHTING.md](DPI-WHEEL-AND-LIGHTING.md)
- [PASSIVE-BUTTON-FEEL.md](PASSIVE-BUTTON-FEEL.md)
- [OPENSCAD-WORKFLOW.md](OPENSCAD-WORKFLOW.md)
- [DESIGN-DIRECTION.md](DESIGN-DIRECTION.md)
