# D2-FRAME-01 — 2×1 m Desk, 50×50 mm Frame, 50 mm Solid-Wood Top

Date: 2026-11-01. Status: **OWNER GEOMETRY RECORDED, REAL STRUCTURAL LOAD PATH NOT QUALIFIED**.

This is an engineering continuation of [D2-MOUNT-01](D2-MOUNT-01-COPLANAR-STRUCTURAL-SAFETY.md) and the owner's *zero longitudinal speaker offset* preference, horizontal 3-way satellites directly above a scalable future triple-monitor array. Nominal satellite mass ~10kg each; demanded **minimum 50kgf working load and 100kgf proof/stress target PER satellite**, across the entire load chain. We preserve seven active analog audio channels (L/R LF+MID+HF, separate sub) and the final-enclosure-LAST sequence.

## New owner-supplied information (NOT guesses)

- Desk MAIN footprint: **2000×1000 mm**.
- Frame sections described as **50×50 mm profile**; the main tabletop **and upper shelf** attach to this table structure.
- MAIN tabletop planned: **50mm solid wood**.
- Owner plans **double-sided threaded screws** (`двусторонние винты`) to attach wood top to desk frame. This phrase does NOT establish diameter, steel grade, thread pitch, wood embedment, through-bolt versus blind dowel screw, quantity or whether clamping will allow wood movement.
- Upper shelf thickness/footprint and whether it is wood are NOT specified.

**Still unknown:** 50×50 profile metal (steel/aluminum/other), CLOSED TUBE vs extruded profile, thickness of walls, frame spans/legs/crossmembers, welded versus mechanical joints, locations of upper-shelf supporting rails and underside access, anchors' real design, solid-wood species, laminated-board grain direction, humidity range, and actual all-up loudspeaker centre of mass.

**Do not fill these missing fields with invented measurements.**

## Preliminary physical meaning

### 50 mm solid-wood main panel is substantial

Main tabletop gross wood volume: `2.0×1.0×0.050 = 0.100 m³`.

For hypothetical densities 450,550,650,750,850kg/m³, the standalone wood main top would mass **45,55,65,75,85kg** respectively — illustrative only. The real species, moisture and material voids are unknown; this EXCLUDES upper shelf, steel frame, three monitors, two satellites, audio hardware and any other equipment.

Tabletop weight can contribute to resistance against overall overturning only in a well-established support/floor load path; it does **not** automatically strengthen a local screw pull-out point, a frame joint, or a hinged cantilever.

### Frame 50×50 is not enough to compute real beam capacity

For a **hypothetical CLOSED SHARP-CORNER SQUARE STEEL TUBE** only, and wall thickness `t` mm:
- `I=(50^4-(50-2t)^4)/12 mm^4`;
- `W=I/(50/2) mm^3`;
- elastic *section stress illustration* `sigma=M/W` (convert Nm→Nmm);
- hypothetical steel modulus `E=200,000 N/mm²`.

| Hypothetical steel 50×50 closed wall | Ideal second moment I | Ideal elastic W | Stress due to 294.2 N·m about ideal pure bending axis |
|---:|---:|---:|---:|
| 1.5 mm | 114,193 mm⁴ | 4,568 mm³ | 64.4 MPa |
| 2.0 mm | 147,712 mm⁴ | 5,908 mm³ | 49.8 MPa |
| 2.5 mm | 179,115 mm⁴ | 7,165 mm³ | 41.1 MPa |
| 3.0 mm | 208,492 mm⁴ | 8,340 mm³ | 35.3 MPa |
| 4.0 mm | 261,525 mm⁴ | 10,461 mm³ | 28.1 MPa |

**Not a stress acceptance check:** this is the simplest ideal straight elastic beam, with rounded corners, tube manufacturing tolerances, real material grade, local flange/web buckling, hole weakening, wall bearing/tear-out, weld strength, column base torsion, global frame sway and fatigue all omitted. The `294.2Nm` case itself presumes a **100kgf load at a 300mm lever arm**, NOT a measured speaker centre of mass or a required steel member load combination. Do not divide a guessed yield strength by these numbers and call the whole desk "approved".

A deliberately independent simple midspan model (one isolated simply supported 50×50×2mm steel beam, point force 100kgf, E=200GPa):
- ideal 0.5m support span: **~0.0865mm** deflection;
- ideal 1.0m support span: **~0.6915mm** deflection;
- ideal 2.0m support span: **~5.532mm** deflection.

Deflection scales with `L³` in this simple beam model. In the real **2m×1m FRAME**, the number/location of corner legs and crossmembers and their joint rigidity determine effective spans and load sharing. The supporting upper-shelf frame could be used as a second steel tie-in point IF continuous and properly engineered; merely having a wooden upper shelf does not make it a reliable structural brace.

**External engineering reference:** [AISC introduction to hollow structural sections](https://www.aisc.org/aisc/solutions-center/hss/) and [HSS specification guidance](https://www.aisc.org/globalassets/aisc/manual/15th-ed-ref-list/specification-for-the-design-of-steel-hollow-structural-sections.pdf), which distinguish nominal outer profile size from actual design thickness/material/geometry.

### Solid timber + rigid steel: attachment must allow seasonal wood movement

A 2m-long glued-up solid tabletop is anisotropic: dimensional movement ALONG grain is much smaller than ACROSS grain. Full-metal rigid fastening at multiple spread-out locations across the width can stress/check/warp the top during humidity cycles. **Double-ended threaded fasteners do not automatically solve this**. Design wood support separately from the suspended speaker support:
- Choose one or a small number of main **locating datum** positions, if compatible with timber grain and joint mechanics.
- At other tabletop fix points, use appropriate elongated holes / metal clips / sliding joint architecture allowing expected *across-grain* travel, with suitable captive washers, maintained hold-down strength and no unsafe looseness. Slot length must come from measured species, board construction and climate, not guessed here.
- Don't permanently restrain the 1m solid top in both dimensions or install a welded bracket in ways that prevent swelling.
- Avoid turning fastener holes into moisture traps/crack initiators in a thick expensive timber top; preserve enough remaining wood section and edge distance, to be designed from fastener/vendor data.
- If `двусторонние винты` means wood-to-metal HANGER BOLTS with one end threaded into wood and the other into steel: those might suit timber-to-frame fixation provided seasonal motion is accommodated, **but they should NOT be the lone structural connection holding a 10kg overhead audio cabinet**.

Woodworking supporting references:
- [Fine Woodworking: attaching solid wood tops while permitting seasonal movement](https://www.finewoodworking.com/2003/06/01/how-to-attach-a-tabletop)
- [Woodcraft: appropriate figure-eight / Z-clip / button fasteners](https://www.woodcraft.com/blogs/cabinetry-furniture-making/tabletop-fasteners)
- [Fine Woodworking: solid wood top fastening methods](https://www.finewoodworking.com/project-guides/tables-and-desks/attaching-solid-wood-tabletops)

## Preferred structural architecture: table is two cooperating subsystems

**Loudspeaker (10kg) → stiff dedicated cabinet skeleton/hardpoints → double-sided captured tilt yoke + positive mechanical lock → upright steel/engineered metal column → REINFORCED metal frame joint or direct secondary load path to legs → floor.**

**50mm solid-wood top → independently fastened to metal frame, with wood grain seasonal movement allowed, and NO reliance on blind-wood screw pullout to catch the speaker.**

One physical surface can conceal both mechanisms, and a steel receiver sleeve/bolted flange can emerge through a **deliberately oversized wood clearance opening with decorative escutcheon**. The wood and mount do not have to share the same threaded anchor, which reduces acoustic vibration coupling to the top and avoids placing the critical tilt load into a moving timber panel. This is a CONCEPT, not fabrication dimensions or a built/rated receiver.

Potential frame-to-upright variants to evaluate after actual desk drawing:
1. At a short span near an actual 50×50 frame junction / load-bearing leg: reinforced steel mounting socket or two-sided bolted steel plates that carry bending and torsion in the metal. Note hidden hollow tube wall crushing at through-bolts; plan internal sleeve/doubler as needed.
2. Where upper-shelf rails have actual **steel** columns continuous to the lower frame: two vertically separated frame connections may reduce local joint demand. Verify exact members/welds; cannot call the upper shelf itself a structural tie-in without proof.
3. Independent floor-connected safety support as backup if desk/frame analysis reveals excessive top-rail torque or desk overturning. Do not confuse a second tether attached to the exact same failing element with independent redundancy.

**No bolt diameter, plate thickness, tie-rod count, weld size or drilling pattern is approved** at this evidence level. High lever moment from 50/100kgf demand must be checked for EACH primary/secondary actual load path, including simultaneous L/R use where required, cable pulls, user bumps, vibration and creep, with professional structural verification when mounting heavy speakers over people/screens.

## Safety, reliability and test gates

1. Identify profile steel/aluminum and closed wall thickness, with supplier drawings / actual wall measurement. Check straightness and corner radii.
2. Sketch desk structure: locations of 2m×1m supports/legs, horizontal 50×50 rails, crosspieces, shelf frame and fasteners/welds. Mark proposed COLUMN BASE mounting coordinates.
3. Distinguish timber-to-frame fasteners from loudspeaker-to-frame fasteners. Confirm solid timber grain/board lamination/species/moisture allowance before designing wood attachment.
4. Define actual final speaker estimated mass INCLUDING stiff frame, driver baskets, amp/DAC, cables, fixings; calculate 3D CoM envelope at ALL tilt/yaw settings and dynamic moments.
5. Verify support stiffness, column buckling, localized hollow profile bearing/tear-out, welds / frame connections, tabletop wood slot motion, tip/overturning and floor leg reactions.
6. Design and independently prove the protective secondary retention against independent structure, with accessible inspection and no loose slip-angle joints.
7. Perform controlled instrumented tests **on a protected test fixture away from people/monitors** with documented force/moment path and no destructive improvised overload above the user. Work/proof targets must be tied to an actual applicable design standard and qualified test procedure.
8. Only then physically fit to the desk, inspect after full multi-monitor installation, and recheck after replacing screens or cabinet mass.

## Reproducible machine-readable evidence

- [threeway_desk_frame_structural.py](simulation/threeway_desk_frame_structural.py) — measured 2×1m /50×50 /50mm input, 0.1m³, hypothesis steel tube 1.5–4mm, illustrative simple beam span 0.5/1/2m and per-speaker 10/50/100kgf base moments.
- [test_threeway_desk_frame_structural.py](simulation/test_threeway_desk_frame_structural.py) — 12 tests catch dimension errors, stiffness vs span, fake profile grade/wall/wood species, load-target conflation, and wood fastener ≠ speaker rigging.
- [threeway-desk-frame-study.yml](../../.github/workflows/threeway-desk-frame-study.yml) — source CI with archived report artifact: https://github.com/quendoris/DIY/actions/runs/41329862943

**Acceptance state:** frame dimension USER_CONFIRMED; main top thickness and material USER_PLANNED; wood-to-frame double-sided fastener USER_PLANNED_UNSPECIFIED; tube material/wall/frame topology UNKNOWN; stand load path PRELIMINARY_HYPOTHESIS; real structural safety / certification NOT_TESTED.
