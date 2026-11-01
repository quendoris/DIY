# DIY

Experimental DIY hardware and tools — custom peripherals, mechanisms, electronics, firmware, and fabrication.

## Projects

### Modular KVM / Matrix Switch
A high-bandwidth, fully programmable HDMI/USB/USB-C switching appliance with a separate management MCU, hardware authorization and replaceable video/USB boards. Port count is scalable rather than fixed: simulate 2×2, 3×3, 5×5 and multi-host/multi-display assignments, with 4K240 remaining a per-link research target subject to full protocol and signal-integrity validation.

Status: **feasibility / topology definition**

See: [projects/kvm-switch](projects/kvm-switch/README.md)

### Custom Mouse
A fully wired, high-mass, modular precision mouse with contactless sensing, programmable magnetic button feel, absolute wheel angle measurement, electromagnetic detents and a planned secondary DPI wheel with subtle RGB indication.

Status: **architecture / bench-module development**

See: [projects/custom-mouse](projects/custom-mouse/README.md)

### Custom Keyboard
A heavy metal high-profile wired keyboard with independently sensed magnetic keys, programmable actuation, optional active tactile control, removable modules, quiet operation, washable-design research and testable low-jitter input behavior.

Status: **concept / one-key research next**

See: [projects/custom-keyboard](projects/custom-keyboard/README.md)

### Premium DIY Loudspeakers
Research-first, incremental high-fidelity desktop 2.1 audio concept: two midrange-focused near-field speakers, a separate deep-bass 10–12-inch subwoofer, optional active DSP, real-wood finishes and integration with the sound engine.

Status: **requirements captured / modular 2.1 simulation next**

See: [projects/diy-speakers](projects/diy-speakers/README.md) and [wired optical audio fabric](projects/diy-speakers/wired-audio-fabric/README.md)

### Shared Audio System
The player and earbuds share a dedicated digital radio link, audio-quality acceptance criteria, ANC timing requirements and joint validation gates.

See: [projects/audio-system](projects/audio-system/README.md), [format-specific audio paths](projects/audio-system/AUDIO-FORMAT-PATHS.md), [simulation plan](projects/audio-system/SIMULATION-AND-VALIDATION.md), and [audiophile reference study](projects/audio-system/REFERENCE-STUDY.md), plus the [executable packet-model test bench](projects/audio-system/validation/README.md)

### Local Audio Player
A compact but substantial metal-bodied offline audio player with owner-controlled embedded firmware, high-capacity digital music storage, wireless charging and a dedicated digital audio link.

Status: **concept / RF and transfer feasibility pending**

See: [projects/audio-player](projects/audio-player/README.md)

### Modular Wireless Earbuds
Small earbuds with removable cylindrical batteries, secure wet-weather fit, adjustable hybrid ANC/transparency and a custom local-player-to-earbud digital audio link.

Status: **concept / battery and RF feasibility pending**

See: [projects/earbuds](projects/earbuds/README.md)

### Acoustic Volumetric CAD
A future acoustic volumetric display/CAD interface based on levitated particles, RGB illumination, spatial tracking and mid-air haptics.

Status: **concept / deferred until budget allows**

See: [projects/acoustic-volumetric-cad](projects/acoustic-volumetric-cad/README.md)

### Shared Power, Protection & Cooling
Reusable low-voltage supply, protection, electrical-noise and thermal-management research across DIY projects. Includes a qualifications matrix; initial bench uses certified external AC/DC modules.

See: [projects/shared-power](projects/shared-power/README.md)

## Repository policy

Concept documents distinguish **owner requirements**, **implementation candidates** and **unvalidated claims**. Expensive metal fabrication follows bench validation, not the other way around.
