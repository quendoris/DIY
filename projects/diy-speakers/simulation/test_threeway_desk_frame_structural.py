import unittest
from threeway_desk_frame_structural import (
    G, PROFILE_OUTER_MM, TOP_SOLID_WOOD_THICKNESS_MM, MEASURED_PLAN_MM,
    desktop_volume_m3, indicative_wood_mass, ideal_square_hollow_section_mm,
    hypothetical_local_section_bending_stress_MPa, theoretical_beam_response,
    base_joint_couple_N, report, gravity_N
)

class DeskStructuralTests(unittest.TestCase):
    def test_user_exact_desk_values(self):
        self.assertEqual(MEASURED_PLAN_MM,[2000,1000])
        self.assertEqual(PROFILE_OUTER_MM,[50,50])
        self.assertEqual(TOP_SOLID_WOOD_THICKNESS_MM,50)
        self.assertAlmostEqual(desktop_volume_m3(),.1,places=12)

    def test_main_top_mass_not_assumed_constant(self):
        self.assertAlmostEqual(indicative_wood_mass(450),45,places=9)
        self.assertAlmostEqual(indicative_wood_mass(650),65,places=9)
        self.assertAlmostEqual(indicative_wood_mass(850),85,places=9)

    def test_square_hollow_tube_exact_ideal_derived_modulus(self):
        s=ideal_square_hollow_section_mm(50,2)
        I=(50**4-46**4)/12
        self.assertAlmostEqual(s["ideal_I_mm4"],I,places=8)
        self.assertAlmostEqual(s["ideal_elastic_section_modulus_mm3"],I/25,places=8)
        self.assertTrue(s["actual_profile_section_unknown"])

    def test_wider_wall_increases_ideal_stiffness_not_proof(self):
        a=ideal_square_hollow_section_mm(50,2)
        b=ideal_square_hollow_section_mm(50,3)
        self.assertGreater(b["ideal_I_mm4"],a["ideal_I_mm4"])
        self.assertGreater(b["ideal_elastic_section_modulus_mm3"],
                           a["ideal_elastic_section_modulus_mm3"])

    def test_100kgf_x_30cm_uses_true_moment_not_mass_to_strength_guess(self):
        moment=gravity_N(100)*.3
        self.assertAlmostEqual(moment,294.1995,places=4)
        s=ideal_square_hollow_section_mm(50,2)
        self.assertAlmostEqual(
            hypothetical_local_section_bending_stress_MPa(
                moment,s["ideal_elastic_section_modulus_mm3"]),49.8,delta=.15)

    def test_full_frame_cannot_be_approved_by_one_beam_deflection(self):
        s=ideal_square_hollow_section_mm(50,2)
        d1=theoretical_beam_response(gravity_N(100),1000,s["ideal_I_mm4"])
        d2=theoretical_beam_response(gravity_N(100),2000,s["ideal_I_mm4"])
        self.assertAlmostEqual(d2["ideal_midspan_deflection_mm"]/
                               d1["ideal_midspan_deflection_mm"],8,places=10)
        self.assertFalse(d1["reflects_real_desk_frame"])
        self.assertAlmostEqual(d1["ideal_midspan_deflection_mm"],.6916,delta=.005)

    def test_load_couple_for_recessed_anchor_is_not_bolt_capacity(self):
        c=base_joint_couple_N(100,300,80)
        self.assertAlmostEqual(c,3677.49375,places=4)
        self.assertAlmostEqual(base_joint_couple_N(100,300,160),c/2,places=6)

    def test_zero_and_negative_cases_rejected(self):
        with self.assertRaises(ValueError):desktop_volume_m3(2000,-1000,50)
        with self.assertRaises(ValueError):indicative_wood_mass(0)
        with self.assertRaises(ValueError):ideal_square_hollow_section_mm(50,25)
        with self.assertRaises(ValueError):ideal_square_hollow_section_mm(50,0)
        with self.assertRaises(ValueError):base_joint_couple_N(100,300,0)
        with self.assertRaises(ValueError):theoretical_beam_response(10,1,-20)

    def test_user_did_not_claim_stainless_tube_wall_or_wood_species(self):
        x=report()
        self.assertIsNone(x["unknown_requirements"]["frame_profile_material"])
        self.assertIsNone(x["unknown_requirements"]["tube_wall_mm"])
        self.assertIsNone(x["unknown_requirements"]["solid_wood_species"])
        self.assertIsNone(x["unknown_requirements"]["grain_direction"])
        self.assertIsNone(x["unknown_requirements"]["wood_to_metal_fastener_detail"])
        self.assertIsNone(x["unknown_requirements"]["upper_shelf_dimensions_mass_and_loads"])
        self.assertTrue(x["owner_measured_geometry"]["upper_shelf_present"])

    def test_speaker_loads_are_still_only_targets(self):
        x=report()
        self.assertEqual(x["speaker_load_target"]["total_estimated_satellite_mass_kg"],20)
        self.assertEqual(x["speaker_load_target"]["both_nominal_speaker_gravity_N"],2*10*G)
        self.assertIsNone(x["speaker_load_target"]["both_simultaneous_proof_is_required_by_owner"])
        self.assertFalse(x["real_structural_capacity_certified"])
        self.assertFalse(x["real_fastener_load_rated"])
        self.assertFalse(x["beam_model_equivalent_to_frame"])
        self.assertTrue(x["architecture_preference"]["not_qualified"])

    def test_incorrectly_equating_double_ended_wood_screw_with_overhead_rigging_is_forbidden(self):
        x=report()
        self.assertIn("wood-movement-compatible",x["architecture_preference"]["tabletop_attachment"])
        self.assertIn("metal frame",x["architecture_preference"]["primary_load_path"])
        self.assertIn("independent",x["architecture_preference"]["redundancy"])

    def test_parameter_sweep_has_tube_and_span_without_fabricated_material(self):
        x=report()
        self.assertEqual(len(x["illustrative_tube_sections"]),5)
        self.assertEqual(len(x["illustrative_tube_span_model"]),6)
        self.assertEqual(len(x["load_case_moments"]),4)
        self.assertEqual(len(x["main_solid_wood_mass_scenarios_not_actual"]),5)
        self.assertEqual(x["main_desktop_volume_m3"],.1)

if __name__=="__main__":
    unittest.main()
