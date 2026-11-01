"""Adversarial D2-MOUNT-01 support-load + coplanar stereo geometry tests.

Must never pass nominal demand off as certified real installed safety.
"""
import math
import unittest
from threeway_coplanar_mount_mechanics import (
    G, OWNER_SATELLITE_DESIGN_MASS_KG, OWNER_REQUESTED_MIN_WORKING_EQUIV_KG,
    OWNER_REQUESTED_PROOF_EQUIV_KG, BOLT_ROW_SPACING_M,
    load_equivalent_kgf_to_newtons, structural_demands,
    certification_envelope, transformed_baffle_envelope, screen_top_clearance,
    coplanar_stereo, report
)
from threeway_stereo_multimonitor import Satellite, true_equilateral_3d_lateral_x

class SupportLoadsAndScreenPlaneTests(unittest.TestCase):
    def test_10kg_static_is_not_50kgf_working_capacity(self):
        self.assertEqual(OWNER_SATELLITE_DESIGN_MASS_KG,10.)
        self.assertEqual(OWNER_REQUESTED_MIN_WORKING_EQUIV_KG,50.)
        self.assertEqual(OWNER_REQUESTED_PROOF_EQUIV_KG,100.)
        self.assertAlmostEqual(load_equivalent_kgf_to_newtons(10),98.0665,places=5)
        self.assertAlmostEqual(load_equivalent_kgf_to_newtons(50),490.3325,places=5)
        self.assertAlmostEqual(load_equivalent_kgf_to_newtons(100),980.665,places=5)

    def test_load_rating_must_include_offset_lever_arm(self):
        d=structural_demands(100,.30,.08)
        self.assertAlmostEqual(d["moment_Nm"],294.1995,places=4)
        self.assertAlmostEqual(d["ideal_two_row_force_couple_N"],3677.4938,places=3)
        self.assertTrue(d["ideal_two_row_force_is_not_validated_bolt_tension"])
        self.assertGreater(
            structural_demands(10,.3,.08)["moment_Nm"],
            structural_demands(10,.03,.08)["moment_Nm"]*9)

    def test_wide_arm_doubles_bending_moment(self):
        a=structural_demands(50,.2,.08)["moment_Nm"]
        b=structural_demands(50,.4,.08)["moment_Nm"]
        self.assertAlmostEqual(b/a,2,places=10)

    def test_bolt_spacing_changes_tension_couple_not_gravity(self):
        small=structural_demands(50,.3,.06)
        wide=structural_demands(50,.3,.12)
        self.assertEqual(small["force_N"],wide["force_N"])
        self.assertEqual(small["moment_Nm"],wide["moment_Nm"])
        self.assertAlmostEqual(small["ideal_two_row_force_couple_N"]/
                               wide["ideal_two_row_force_couple_N"],2.,places=4)

    def test_invalid_mass_lever_and_row_spacing_rejected(self):
        for a,b,c in [(0,.3,.08),(10,0,.08),(10,.3,0),(-1,.1,.1)]:
            with self.assertRaises(ValueError):
                structural_demands(a,b,c)
        with self.assertRaises(ValueError):
            load_equivalent_kgf_to_newtons(-100)

    def test_lateral_axis_rotation_does_not_erase_baffle_margins(self):
        half=true_equilateral_3d_lateral_x(.35,.90)
        speaker=Satellite("L",-half,.90,.35,90.)
        e=transformed_baffle_envelope(speaker)
        self.assertLess(e["min_baffle_front_plane_y_m"],.90)
        self.assertLess(e["lowest_front_plane_y_m"],.90)
        self.assertFalse(e["full_cabinet_depth_checked"])
        self.assertFalse(e["mounting_hardware_clearances_checked"])

    def test_actual_front_panel_clearance_stronger_than_center_height_only(self):
        sx=true_equilateral_3d_lateral_x(.35,.90)
        speaker=Satellite("L",-sx,.90,.35,90.)
        clear=screen_top_clearance(speaker,.80)
        self.assertLess(clear["idealized_front_plane_min_gap_m"],.10)
        self.assertFalse(clear["solid_cabinet_above_screen_certified"])
        self.assertIn("FRONT panel",clear["note"])

    def test_at_zero_depth_speaker_axis_does_not_imply_all_six_rays_clear(self):
        x=coplanar_stereo(.35,.90,.80,True,90)
        self.assertTrue(x["both_reference_acoustic_axes_coplanar_with_monitor_surface"])
        self.assertFalse(x["cabinet_mechanics_and_solid_collision_tested"])
        self.assertLessEqual(x["source_to_listener_screen_ray_grid"]
                             ["two_speaker_all_six_faceplates_clear_count"],27)
        self.assertTrue(x["screen_sizes_and_spatial_offsets_are_hypotheses"])

    def test_both_plan_stereo_and_true_equilateral_are_explicit(self):
        a=coplanar_stereo(.35,.925,.80,False)
        b=coplanar_stereo(.35,.925,.80,True)
        self.assertLess(abs(a["source_horizontal_positions_m"][0]),
                        abs(b["source_horizontal_positions_m"][0]))
        self.assertEqual(a["speaker_center_depth_m"],.35)
        self.assertEqual(b["speaker_center_depth_m"],.35)

    def test_coplanar_report_is_not_mechanical_certificate(self):
        x=report()
        self.assertEqual(x["study"],"D2-MOUNT-01")
        self.assertEqual(x["owner_measured"]["head_above_table_m"],.60)
        self.assertEqual(x["owner_requested"]["speaker_depth_relative_to_screen_plane_m"],0)
        self.assertFalse(x["load_rating_claimed_for_real_joint"])
        self.assertFalse(x["preinstallation_passed"])
        self.assertEqual(len(x["force_and_moment_demands"]),21)
        self.assertEqual(len(x["coplanar_speaker_position_scenarios"]),20)
        self.assertIsNone(x["screen_and_ear_unknowns"]["actual_ear_canal_above_table_m"])
        self.assertTrue(x["source_plane_is_not_full_cabinet_envelope"])

    def test_100kgf_is_proof_target_not_inferred_from_50kgf(self):
        for r in certification_envelope():
            self.assertGreater(r["proof_target_100kgf_demand"]["moment_Nm"],
                               r["working_target_50kgf_demand"]["moment_Nm"])
            self.assertFalse(not r["not_certified_for_overhead_use"])

if __name__=="__main__":
    unittest.main()
