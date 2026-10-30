# DIY KVM / Matrix Switch — Concept

Status: **feasibility and architecture**, not a frozen BOM or build-ready schematic.

## Original user proposal

- A desktop rectangular low-profile switch appliance, not a rack chassis.
- **Ten HDMI connectors**, arranged five on one edge and five on another.
- HDMI goal **4K at 240 Hz**, with source/display feature compatibility verified per use case.
- As many sensible additional USB-A and USB-C ports as the architecture and packaging allow, with a **top-tier USB performance goal** (investigate USB4 80 Gbit/s, but do not silently equate every Type-C receptacle with USB4).
- A dedicated STM32-class management MCU with ample performance margin and fully controlled, open-source management firmware.
- A separate hardware authorization token for sensitive switching functions.
- Separate auxiliary power to keep the control plane running independently of source PCs.
- Independent **Management / Video / USB** boards, with possible replaceable daughtercards and future protocol upgrades.

**Important ambiguity:** ten HDMI connectors do not by themselves define a topology. The provisional interpretation is **five HDMI sources + five HDMI sinks**; determine whether the user needs (A) one-to-one arbitrary assignments (a 5x5 permutation matrix), (B) outputs freely duplicating one source (multicast), or (C) only one selected host to one selected monitor. Architecture, power, EDID/HDCP complexity and cost differ greatly.

The project is feasible in principle. The risk is **high-speed PHY, routing topology and host-link semantics**, not MCU computation alone.

## Proposed board hierarchy

```text
                   [ AUTH TOKEN ]
                          |
                 [ Management Board ]
                 STM32H5-class / policy
                  |     |      |
        control/status  |  USB debug
                  |     |
       +----------+     +----------------+
       |                                 |
  [Video Board]                    [USB Board]
  HDMI FRL routing                 USB2/HID virtualization
  EDID/HPD/DDC/SCDC                USB3 hub / host switching
  optional retiming                USB-C CC / PD
  independent outputs              USB4-specific router/path
       |                                 |
  5× HDMI IN / 5× HDMI OUT         host/device USB ports
```

Boards share only fully specified power, management and service interfaces. **Three PCBs do not remove the need for high-speed signal-integrity design**: any high-rate mezzanine, flex or cable between boards becomes part of the measured insertion-loss/reflection budget.

## Why this architecture matters

The management MCU is the **control plane**, never a 48-Gbit/s HDMI serializer or 80-Gbit/s USB4 PHY. Purpose-built PHY/mux/retimer/router devices carry the data path. Replaceable RF/high-speed boards give the project real upgradeability instead of a single complicated PCB.

The goal is to preserve useful device identity and desktop layout where technically possible, while explicitly recording when the source OS must retrain video or re-enumerate USB. No promise of "zero disconnect" on every transport.

## Development rule

Begin with protocol/route simulation, state machines, link budget, vendor datasheets and electrical feasibility; then validate independent HDMI and USB experimental channels. Only after measurements justify the topology should a full ten-port PCB be fabricated.

Read:
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [REVIEW-OF-INITIAL-PROPOSAL.md](REVIEW-OF-INITIAL-PROPOSAL.md)
- [VALIDATION.md](VALIDATION.md)
