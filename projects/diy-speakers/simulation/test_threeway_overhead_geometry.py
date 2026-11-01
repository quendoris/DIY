"""D2-OVERHEAD-01 tests: exact rigid-body geometry and honest caveats.

No physical over-the-monitor speaker or safe stand measured.
"""
import math
import unittest
from pathlib import Path
from threeway_overhead_geometry import (
  Setup, Screen, tilt_deg, unit_vectors, sources, distance, projected_baffle_extents,
  crossing, visibility, angle_to_normal, band_pressure, compare_window,
  stand_height_for_acoustic_center, scenarios
)
from threeway_baffle_geometry import default_layouts, ideal_filters

LAYOUTS={x.name:x for x in default_layouts()}
VERT="A_minimum_practical_vertical"
SIDE="F_side_LOW_left"

class OverheadGeometryTests(unittest.TestCase):
    def setUp(self):
        self.s=Setup("stand",VERT,0,.45,.20)
        self.roll=Setup("rotated",VERT,90,.45,.20)

    def test_down_tilt_is_real_with_user_proposed_height_difference(self):
        self.assertAlmostEqual(tilt_deg(self.s),math.degrees(math.atan(.25/.7)),places=10)
        self.assertGreater(tilt_deg(self.s),15)
        self.assertAlmostEqual(tilt_deg(Setup("modest",VERT,0,.5,.35)),
                               math.degrees(math.atan(.15/.7)),places=10)

    def test_baffle_basis_is_orthonormal_and_aims_at_reference_ear(self):
        for roll in (0,45,90,-45):
            st=Setup("t",VERT,roll,.45,.20)
            u,v,n=unit_vectors(st)
            self.assertAlmostEqual(sum(x*x for x in n),1,places=12)
            self.assertAlmostEqual(sum(x*x for x in u),1,places=12)
            self.assertAlmostEqual(sum(x*x for x in v),1,places=12)
            for a,b in ((u,v),(u,n),(v,n)):
                self.assertAlmostEqual(sum(x*y for x,y in zip(a,b)),0,places=12)
            toward=(0,.20-.45,-.7)
            self.assertAlmostEqual(angle_to_normal(n,toward),0,places=6)

    def test_roll_preserves_inter_driver_center_distances(self):
        baseline=sources(self.s)
        for angle in (45,90):
            arr=sources(Setup("rot",VERT,angle,.45,.20))
            for a,b in (("LOW","MID"),("MID","HIGH"),("LOW","HIGH")):
                self.assertAlmostEqual(distance(arr[a],arr[b]),
                                       distance(baseline[a],baseline[b]),places=12)

    def test_roll_converts_mid_high_vertical_separation_into_horizontal(self):
        base=sources(self.s)
        horizontal=sources(self.roll)
        dy=base["HIGH"][1]-base["MID"][1]
        dx=horizontal["HIGH"][0]-horizontal["MID"][0]
        self.assertAlmostEqual(abs(dx),.117,places=12)
        self.assertAlmostEqual(dy,.117*math.cos(math.atan(.25/.7)),places=12)
        self.assertAlmostEqual(horizontal["HIGH"][1],horizontal["MID"][1],places=12)

    def test_monitor_occlusion_is_ray_between_actual_driver_and_ear(self):
        low_screen=Screen(.35,.35,.3)
        wide_screen=Screen(.35,.45,.3)
        a=visibility(self.s,low_screen)
        self.assertTrue(any(row["blocked"] for row in a.values()))
        self.assertTrue(all("top_margin_m" in row for row in a.values()))
        self.assertGreaterEqual(len([x for x in visibility(self.s,wide_screen).values()
                                     if x["blocked"]]),1)

    def test_rising_speaker_does_not_always_clear_screen(self):
        tall=Setup("over",VERT,0,.65,.35)
        short=Setup("at",VERT,90,.65,.35)
        screen=Screen(.35,.45,.3)
        vertical=visibility(tall,screen)
        horizontal=visibility(short,screen)
        self.assertTrue(vertical["LOW"]["blocked"])
        self.assertFalse(horizontal["LOW"]["blocked"])

    def test_aperture_clearance_is_stricter_than_center_ray(self):
        high=Setup("over",VERT,90,.65,.35)
        screen=Screen(.35,.45,.3)
        rows=visibility(high,screen)
        self.assertFalse(any(v["blocked"] for v in rows.values()))
        for r in rows.values():
            self.assertIn("projected_flange_bound_radius_m",r)
            self.assertGreater(r["projected_flange_bound_radius_m"],0)
            if r["conservative_full_flange_clear_above"]:
                self.assertGreater(r["full_flange_top_clearance_m"],0)
        self.assertTrue(all(r["conservative_full_flange_clear"] for r in rows.values()))

    def test_openscad_scene_has_matching_geometry_axes_and_roll_modes(self):
        scad=Path(__file__).with_name("threeway_overhead_scene.scad").read_text()
        self.assertIn("roll_deg=90",scad)
        self.assertIn("acoustic_axis_height_m=.65",scad)
        self.assertIn("ear_height_m=.35",scad)
        self.assertIn("rotate([90+pitch_deg,0,0])",scad)
        self.assertIn("rotate([0,0,roll_deg])",scad)
        self.assertIn("show_placeholder_stand=false",scad)
        for v in ("low_xy","mid_xy","high_xy","screen_top_height_m"):
            self.assertIn(v,scad)

    def test_acoustic_axis_and_platform_height_are_not_synonyms(self):
        st=stand_height_for_acoustic_center(self.s)
        self.assertGreater(st["difference_axis_to_lower_flange_m"],.15)
        self.assertLess(st["hypothetical_lower_flange_envelope_m"],.45)
        self.assertGreater(st["legacy_panel_axis_from_bottom_mm"],.3*1000)

    def test_reference_allpass_acoustical_crossover_after_aiming_and_roll(self):
        for st in (self.s,self.roll,Setup("diagonal",SIDE,45,.65,.35)):
            for freq in (450,2500,4000):
                ear=(0,st.ear_height_m,0)
                p=band_pressure(st,freq,ear,reflection_coeff=0)
                self.assertAlmostEqual(abs(p),1,places=9)

    def test_piston_head_window_moves_and_not_magically_reoptimized(self):
        for st in (self.s,self.roll):
            k=compare_window(st)
            self.assertEqual(k["grid_samples"],450)
            self.assertGreater(k["p95_abs_db"],0)
            self.assertGreater(k["worst_abs_db"],k["p95_abs_db"]-.001)

    def test_nonzero_table_reflection_changes_result_even_if_aimed(self):
        ear=(0,self.s.ear_height_m,0)
        base=band_pressure(self.s,2500,ear,0)
        reflected=band_pressure(self.s,2500,ear,.6)
        self.assertGreater(abs(base-reflected),.005)
        self.assertEqual(band_pressure(self.s,2500,ear,0,.20),base)

    def test_corner_screen_does_not_block_if_outside_horizontal_width(self):
        st=Setup("stand",VERT,0,.45,.20)
        sc=Screen(.35,.35,.2,center_x_m=.5)
        self.assertFalse(any(z["blocked"] for z in visibility(st,sc).values()))

    def test_degenerate_and_unsafe_geometries_rejected(self):
        with self.assertRaises(ValueError):
            tilt_deg(Setup("invalid",VERT,0,.45,-.2))
        with self.assertRaises(ValueError):
            sources(Setup("invalid","NO_SUCH_LAYOUT",0,.45,.2))
        with self.assertRaises(ValueError):
            band_pressure(self.s,2500,(0,.2,0),reflection_coeff=1.2)
        with self.assertRaises(ValueError):
            band_pressure(self.s,2500,(0,.2,0),table_forward_extent_m=-.1)

    def test_report_has_no_physical_winner_or_false_certification(self):
        j=scenarios()
        self.assertEqual(len(j["scenarios"]),18)
        self.assertFalse(j["real_monitor_geometry_known"])
        self.assertFalse(j["real_ear_height_known"])
        self.assertFalse(j["real_stationary_hardware_mounting_tested"])
        self.assertFalse(j["true_wavecor_angular_phase_known"])
        self.assertFalse(j["real_baffle_diffraction_calculated"])
        for c in j["scenarios"]:
            self.assertFalse(c["stand_mechanics_qualified"])
            self.assertFalse(c["true_angular_array_measured"])
            self.assertEqual(len(c["monitor_occlusion_proxies"]),3)


if __name__=="__main__":
    unittest.main()
