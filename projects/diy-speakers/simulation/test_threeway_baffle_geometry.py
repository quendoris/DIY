"""D2-GEO-01 adversarial geometry/ideal acoustic-window tests.

No measured actual speaker; checks dimensions, mounting collisions,
point-source phase and reference calibration only.
"""
import cmath
import math
import unittest
from threeway_baffle_geometry import (
  DRIVERS, ORDER, HEAD_X_M, HEAD_Y_M, TEST_DISTANCES_M, TEST_FREQUENCIES_HZ,
  REF_EAR_M, clearance_mm, default_layouts, distance_to_source_m,
  hypothetical_complex_pressure, ideal_filters, layout_score,
  panel_dimensions, relative_db, report, sidewoofer_layout, validate_layout, vertical_layout
)

class ThreewayBaffleTests(unittest.TestCase):
    def setUp(self):
        self.compact=vertical_layout("compact",5,5,0)
        self.spread=vertical_layout("spread",15,20,0)
        self.offset=vertical_layout("offset",5,5,40)

    def test_nominal_dimensions_from_exact_manufacturer_drawings(self):
        self.assertEqual([DRIVERS[k].outer_diameter_mm for k in ORDER],
                         [168,120,104])
        self.assertEqual([DRIVERS[k].rear_max_diameter_mm for k in ORDER],
                         [143,98,80])
        self.assertEqual([DRIVERS[k].mounting_circle_diameter_mm for k in ORDER],
                         [159,110,92])
        self.assertEqual([DRIVERS[k].nominal_mounting_depth_mm for k in ORDER],
                         [73,64,30])
        self.assertTrue(all(x.drawing.startswith("https://www.wavecor.com/")
                            for x in DRIVERS.values()))

    def test_clearance_exactly_five_mm_rounded_flange_conservative(self):
        self.assertAlmostEqual(clearance_mm(self.compact,"LOW","MID"),5)
        self.assertAlmostEqual(clearance_mm(self.compact,"MID","HIGH"),5)
        validate_layout(self.compact,5)

    def test_too_tight_variant_explicitly_fails(self):
        very_tight=vertical_layout("tight",2,2)
        with self.assertRaisesRegex(ValueError,"clearance"):
            validate_layout(very_tight,5)

    def test_panel_rounded_dimensions_and_coordinates(self):
        panel=panel_dimensions(self.compact)
        self.assertEqual(panel["required_flat_panel_width_mm"],205)
        self.assertEqual(panel["required_flat_panel_height_mm"],440)
        # Nominal locations from LOWER LEFT corner, millimeters
        self.assertAlmostEqual(panel["center_xy_from_lower_left_mm"]["LOW"][1],102.5,delta=1)
        self.assertAlmostEqual(panel["center_xy_from_lower_left_mm"]["MID"][1],251.5,delta=1)
        self.assertAlmostEqual(panel["center_xy_from_lower_left_mm"]["HIGH"][1],368.5,delta=1)
        self.assertFalse(panel["cutouts_and_screw_template_production_ready"])

    def test_trimmed_mid_has_other_geometry_and_cannot_be_substituted(self):
        self.assertIn("MR120BD02",DRIVERS["MID"].name)
        self.assertNotIn("BD04",DRIVERS["MID"].name)
        self.assertIn("2 L",DRIVERS["MID"].note)

    def test_three_way_ideal_filters_complex_sum_is_allpass(self):
        for f in TEST_FREQUENCIES_HZ:
            fs=ideal_filters(f)
            self.assertAlmostEqual(abs(sum(fs.values())),1,places=11)

    def test_calibration_exact_at_reference_for_each_frequency(self):
        for f in TEST_FREQUENCIES_HZ:
            self.assertAlmostEqual(
                abs(hypothetical_complex_pressure(self.compact,f,REF_EAR_M)),
                1,places=10)
            self.assertAlmostEqual(relative_db(self.compact,f,REF_EAR_M),0,places=10)

    def test_geometry_shift_cannot_be_undone_at_all_positions_by_single_calibration(self):
        pos=math.fsum(abs(relative_db(self.compact,f,(0,.1,.7)))
                      for f in (2000,2500,3000))
        self.assertGreater(pos,.2)

    def test_phase_wavelength_and_earth_distance_units(self):
        self.assertAlmostEqual(distance_to_source_m((0,0,.7),(0,0)),.7,places=10)
        with self.assertRaises(ValueError):
            distance_to_source_m((0,0,0),(0,0))
        self.assertGreater(abs(relative_db(self.compact,2500,(0,.1,.7))),.3)

    def test_lateral_offset_preserves_absolute_rim_clearance(self):
        validate_layout(self.offset)
        self.assertAlmostEqual(clearance_mm(self.offset,"MID","HIGH"),5)
        self.assertGreater(panel_dimensions(self.offset)["required_flat_panel_width_mm"],205)

    def test_compact_ideal_model_more_stable_than_spread_as_study_hypothesis(self):
        a=layout_score(self.compact)
        b=layout_score(self.spread)
        self.assertLess(a["worst_case"]["abs_delta_db"],
                        b["worst_case"]["abs_delta_db"])
        self.assertEqual(a["total_checked_points"],
                         len(TEST_DISTANCES_M)*len(HEAD_X_M)*len(HEAD_Y_M)*len(TEST_FREQUENCIES_HZ))
        self.assertEqual(b["total_checked_points"],a["total_checked_points"])

    def test_report_cannot_claim_acoustic_measurement_or_final_cabinet(self):
        r=report()
        self.assertFalse(r["measured_acoustic_head_window"])
        self.assertFalse(r["baffle_diffraction_measured_or_modeled"])
        self.assertFalse(r["angular_directivity_measured_or_modeled"])
        self.assertFalse(r["common_manufacturer_phase_time_zero_proven"])
        self.assertFalse(r["real_speaker_crossover_qualified"])
        self.assertEqual(len(r["layouts"]),7)
        self.assertEqual(sum(bool(v["physical_rim_clearance_pass"])
                             for v in r["layouts"]),6)
        self.assertIn("removable",r["physical_build_decision"])
        self.assertIn(r["conditionally_most_robust_layout_id"],
                      {x["id"] for x in r["layouts"] if x["physical_rim_clearance_pass"]})

    def test_left_and_right_woofer_layouts_fit_shorter_wider_panels(self):
        left=sidewoofer_layout("side_left",-1)
        right=sidewoofer_layout("side_right",1)
        for layout in (left,right):
            validate_layout(layout)
            p=panel_dimensions(layout)
            self.assertGreater(p["required_flat_panel_width_mm"],300)
            self.assertLess(p["required_flat_panel_height_mm"],310)
            self.assertAlmostEqual(clearance_mm(layout,"LOW","MID"),5)
            self.assertAlmostEqual(clearance_mm(layout,"MID","HIGH"),5)
        self.assertAlmostEqual(layout_score(left)["rms_abs_db"],
                               layout_score(right)["rms_abs_db"],delta=1e-5)

    def test_no_unphysical_input_or_fake_yield(self):

        with self.assertRaises(ValueError):
            vertical_layout("bad",5,5,200)
        with self.assertRaises(ValueError):
            panel_dimensions(self.compact,edge_margin_mm=-1)
        with self.assertRaises(ValueError):
            hypothetical_complex_pressure(self.compact,-100,REF_EAR_M)


if __name__=="__main__":
    unittest.main()
