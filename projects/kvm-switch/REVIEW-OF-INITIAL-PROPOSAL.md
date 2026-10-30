# Review of Initial Qwen Conversation (2026-10-30)

User supplied a dialogue describing a rectangular KVM with ten HDMI connectors, a high-performance USB/Type-C subsystem, a local STM32 management MCU, external power and an authorization token.

We preserve its worthwhile architecture without treating all prior assistant claims as established.

| Claim in original dialogue | Engineering correction / classification |
|---|---|
| HDMI 2.1 high-speed muxes are nearly impossible to obtain | **Incorrect as stated:** Diodes PI3WVR14412 explicitly supports HDMI 2.1 4-lane 2:1/1:2 mux/demux at up to 20 Gbit/s/channel. It does not provide a complete 5×5 matrix or retiming. |
| 4K240 HDMI 2.1 video | **Possible** with matching source/sink capabilities and usually DSC for full RGB on 48-Gbit/s FRL. HDMI 2.1 feature labels do not guarantee 48G/DSC. |
| HDMI 2.1 necessarily requires HDCP 2.3 | **Incorrect:** HDCP applies to protected-content paths and must be handled when required, but is not a condition of carrying arbitrary unprotected HDMI video. |
| Holding EDID and HPD high hides switching completely | **Incomplete:** caching may preserve an OS display object; FRL/SCDC state, actual termination, HDCP and source/sink retraining are separate. |
| STM32 can coordinate video/USB link changes | **Correct at the control-plane level.** The MCU neither serializes HDMI FRL nor implements USB4 PHY by itself. |
| A three-board split fixes 90% of high-speed issues | **Unsupported:** improves serviceability and functional isolation but introduces possible mezzanine loss; link budget remains mandatory. |
| ASM2464PD is a generic USB4 hub | **Incorrect:** vendor calls it USB4-to-PCIe/NVMe device/endpoint controller. |
| MegaChips MCDP6000 is a 48-Gbit/s HDMI 2.1 crosspoint | **Incorrect:** MCDP6000 datasheet identifies a USB Type-C DisplayPort Alt-Mode switching retimer; it is not an HDMI 2.1 5×5 crosspoint. |
| VIA VL830 is a plug-and-play multi-host USB4 router | **Incorrect for the proposed job:** vendor describes USB4 endpoint functionality with integrated USB3.2 hub and DP. |
| TUSB546 supports USB4/DP tunneling | **Incorrect:** TI specifies USB 3.1 Gen1 up to 5G and DP Alt Mode. |
| STUSB4500 handles any Type-C source/sink role | **Incorrect:** STUSB4500 is sink-only. |
| Standard switched USB hub stays enumerated on every host | **Incorrect:** a conventional hub upstream handoff typically forces re-enumeration. Separate per-host HID emulation is a different design with its own trust model. |
| One authorization token provides bank-HSM-grade security | **Overclaim:** token auth can substantially improve authorization but depends on key provisioning, threat model, firmware, session rules, recovery and physical access. |
| PCB pricing $150–300 per 5×5 HDMI+USB4 iteration | **Not substantiated:** no layout, stackup, fabrication quote, connector specification, specific retimers, assembly/validation instrumentation or yield assumptions were shown. Treat every given total as illustrative at best. |
| 5 mil length matching or mandatory Rogers for every path | **Overgeneralized:** topology-specific impedance, insertion/return loss, skew budget, vias, stackup and simulation determine requirements. |
| 1k stars in year one | **Unfounded commercial/social prediction:** not a technical requirement. |

## Confirmed MCDP6000 source

The public MCDP6000 PDF is titled *USB Type-C DP Alt-Mode Switching Retimer*, not an HDMI FRL 48-Gbit/s matrix: https://media.digikey.com/pdf/Data%20Sheets/MegaChips%20PDFs/MCDP6000_DS.pdf

## Additional modern standards point

In 2026, the HDMI 2.2 specification already provides a path to up to 96-Gbit/s links, including demanding uncompressed modes. That is **not a requirement for first hardware**. It strengthens the case for a swappable video board instead of rebuilding the management firmware whenever the video standard evolves.

## Current risk ranking

1. **Topology:** one-to-one routing vs source multicast dictates whether a true multi-output HDMI repeater/duplicator is needed.
2. **USB4 host domains:** multi-host switching is a router/PD/link-management problem, not just copper mux routing.
3. **Full-channel signal integrity** across all ports/cables/connectors.
4. **HPD/EDID/SCDC/FRL behavior** and OS display persistence across route changes.
5. **Protected-content/HDCP compatibility** without proprietary or non-distributable design assumptions.
6. **Actual availability, documentation and total BOM** for multiport high-rate PHY parts.
7. **Fault isolation and safe power switching.**

## Bottom line

This is a challenging but worthwhile research/manufacturing project. The proposed MCU-management partition is sound; the previously claimed particular USB4 parts and cost estimates do not support a finished high-end matrix.

Build a topology-specific simulation and parts feasibility matrix before freezing the boards.
