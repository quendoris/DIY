"""Adversarial, assumption-specific checks for D2-WAVE-01.

These tests validate mathematical approximations and prevent inflated claims.
They do not measure any physical loudspeaker, desktop, baffle diffraction
or proof of industry audio quality.
"""
import math
import unittest

from threeway_baffle_geometry import (
  REF_EAR_M, default_layouts, panel_dimensions
)
from threeway_wave_desk_model import (
  HEAD_HEIGHT_ABOVE_DESK_M, PISTON, desk_comb_db,
  desk_reflection_geometry, edge_path_proxies, jinc2,
  piston_directivity, piston_radius_m, placement_for_ear_height,
  pressure, relative_window_db, report, window_score
)


class D2WaveDeskTests(unittest.TestCase):
    def setUp(self):
        layouts={x.name:x for x in default_layouts()}
        self.vertical=layouts["A_minimum_practical_vertical"]
        self.side=layouts["F_side_LOW_left"]

    def test_bessel_jinc_analytical_known_values(self):
        self.assertEqual(jinc2(0),1)
        # J1 values and jinc2 normalized values; no SciPy at runtime.
        self.assertAlmostEqual(jinc2(1),0.880101171489867,places=12)
        self.assertAlmostEqual(jinc2(2),0.576724807756873,places=12)
        self.assertAlmostEqual(jinc2(3),0.226039305,places=8)
        self.assertAlmostEqual(jinc2(3.8317059702075125),0,delta=1e-9)

    def test_bessel_is_bounded_only_validated_interval(self):
        for v in (-1,16,float("nan"),float("inf")):
            with self.assertRaises(ValueError):
                jinc2(v)

    def test_effective_area_not_basket_diameter(self):
        rlow=piston_radius_m("LOW")
        rmid=piston_radius_m("MID")
        self.assertAlmostEqual(math.pi*rlow**2,131*1e-4,places=12)
        self.assertAlmostEqual(math.pi*rmid**2,50*1e-4,places=12)
        self.assertAlmostEqual(piston_radius_m("HIGH"),.015,places=12)
        self.assertLess(rlow,.168/2)
        self.assertLess(rmid,.120/2)

    def test_piston_on_axis_unity_and_realizable_high_frequency_narrowing(self):
        for name in PISTON:
            for f in (300,1000,2500,5000):
                self.assertAlmostEqual(piston_directivity(name,f,0),1,places=12)
        self.assertLess(
            abs(piston_directivity("LOW",2500,60)),
            abs(piston_directivity("MID",2500,60))
        )
        self.assertLess(
            abs(piston_directivity("MID",2500,60)),
            abs(piston_directivity("HIGH",2500,60))
        )

    def test_reference_is_calibrated_only_in_model(self):
        for f in (400,450,1000,2500,4000):
            for layout in (self.vertical,self.side):
                self.assertAlmostEqual(abs(pressure(layout,f,REF_EAR_M,True)),1,places=9)
                self.assertAlmostEqual(relative_window_db(layout,f,REF_EAR_M,True),0,places=9)

    def test_moving_head_changes_response_even_with_reference_calibration(self):
        for layout in (self.vertical,self.side):
            x=relative_window_db(layout,2500,(.08,.10,.6),True)
            self.assertTrue(math.isfinite(x))
            self.assertGreater(abs(x),.05)

    def test_geometric_edge_paths_are_strictly_nonnegative_and_not_spl(self):
        for layout in (self.vertical,self.side):
            edges=edge_path_proxies(layout)
            self.assertEqual(set(edges),{"LOW","MID","HIGH"})
            for driver,rows in edges.items():
                self.assertEqual(len(rows),4)
                self.assertEqual({r["edge"] for r in rows},
                                 {"left","right","bottom","top"})
                self.assertTrue(all(x["extra_via_edge_path_mm"]>=0 for x in rows))

    def test_mirrored_side_woofer_shifts_unequal_edge_distances(self):
        e=edge_path_proxies(self.side)["LOW"]
        source_to_edge={r["edge"]:r["speaker_to_nearest_edge_mm"] for r in e}
        self.assertNotEqual(source_to_edge["left"],source_to_edge["right"])

    def test_exact_same_ear_projection_for_mid_high_but_woofer_height_differs(self):
        v=placement_for_ear_height(self.vertical,.35)
        s=placement_for_ear_height(self.side,.35)
        self.assertAlmostEqual(v["panel_bottom_height_above_table_mm"],39.5,places=6)
        self.assertAlmostEqual(s["panel_bottom_height_above_table_mm"],189.0,places=6)
        self.assertEqual(v["driver_acoustic_center_heights_above_table_mm"]["MID"],
                         s["driver_acoustic_center_heights_above_table_mm"]["MID"])
        self.assertEqual(v["driver_acoustic_center_heights_above_table_mm"]["HIGH"],
                         s["driver_acoustic_center_heights_above_table_mm"]["HIGH"])
        self.assertAlmostEqual(
          s["driver_acoustic_center_heights_above_table_mm"]["LOW"]-
          v["driver_acoustic_center_heights_above_table_mm"]["LOW"],
          149,places=6)

    def test_tall_baffle_not_possible_at_low_ear_height_on_desktop(self):
        r=placement_for_ear_height(self.vertical,.25)
        self.assertFalse(r["panel_bottom_is_above_table"])
        self.assertTrue(placement_for_ear_height(self.side,.25)["panel_bottom_is_above_table"])

    def test_image_source_desk_paths_have_correct_limits(self):
        g=desk_reflection_geometry(.15,.35,.7)
        self.assertGreater(g["image_reflected_path_m"],g["direct_path_m"])
        self.assertGreater(g["extra_path_m"],0)
        self.assertGreater(g["reflection_point_from_speaker_m"],0)
        self.assertLess(g["reflection_point_from_speaker_m"],.7)
        self.assertAlmostEqual(g["first_halfcycle_interference_hz"],
          343/(2*g["extra_path_m"]),places=9)

    def test_zero_reflection_has_exact_zero_effect_and_nonzero_reflection_not_zero(self):
        self.assertAlmostEqual(desk_comb_db(450,.15,.35,.7,0),0,places=10)
        self.assertNotAlmostEqual(desk_comb_db(450,.15,.35,.7,.6),0,places=3)

    def test_half_cycle_frequency_is_a_dip_with_positive_reflection(self):
        g=desk_reflection_geometry(.3,.35,.7)
        dip=desk_comb_db(g["first_halfcycle_interference_hz"],.3,.35,.7,.6)
        self.assertLess(dip,0)
        self.assertGreater(desk_comb_db(1,.3,.35,.7,.6),0)

    def test_floor_reflection_woofer_changes_across_two_panels(self):
        v=placement_for_ear_height(self.vertical,.35)
        s=placement_for_ear_height(self.side,.35)
        hv=v["driver_acoustic_center_heights_above_table_mm"]["LOW"]/1000.
        hs=s["driver_acoustic_center_heights_above_table_mm"]["LOW"]/1000.
        fv=desk_reflection_geometry(hv,.35,.7)["first_halfcycle_interference_hz"]
        fs=desk_reflection_geometry(hs,.35,.7)["first_halfcycle_interference_hz"]
        self.assertGreater(fv,fs) # proximity to table shifts geometric interference scale

    def test_report_distinguishes_actual_and_ideal_datasets(self):
        r=report()
        self.assertEqual(r["study"],"D2-WAVE-01")
        for k in ("actual_speaker_measurements","wave_eq_finite_baffle_diffraction_solved",
                  "desk_reflection_measured","manufacturer_angular_response_measured"):
            self.assertFalse(r[k])
        self.assertEqual(len(r["layout_hypotheses"]),6) # D: too-tight rejected
        self.assertTrue(r["piston_model_does_not_use_manufacturer_angular_data"])
        self.assertTrue(any(x["layout"]=="F_side_LOW_left" for x in r["layout_hypotheses"]))
        self.assertTrue(all(x["ideal_piston_head_window"]["n_points"]==585
                            for x in r["layout_hypotheses"]))


if __name__=="__main__":
    unittest.main()
