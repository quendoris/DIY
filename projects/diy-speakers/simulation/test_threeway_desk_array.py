import math
import unittest
from threeway_baffle_geometry import default_layouts
from threeway_wave_desk_model import pressure
from threeway_desk_array import integrated_pressure, reference_relative_db, scenarios

L={x.name:x for x in default_layouts()}


class DeskArrayTests(unittest.TestCase):
    def test_no_desk_is_identical_to_calibrated_original_piston_array(self):
        for name in ("A_minimum_practical_vertical","F_side_LOW_left","G_side_LOW_right"):
            l=L[name]
            for freq in (450,1000,2500,3500):
                for ear in ((0,0,.7),(.08,.1,.6),(-.06,-.05,.8)):
                    new=integrated_pressure(l,freq,*ear,reflection_coefficient=0.)
                    old=pressure(l,freq,ear,piston=True)
                    self.assertAlmostEqual(abs(new-old),0,delta=1e-10)

    def test_reference_direct_only_is_allpass_unity(self):
        for name in ("A_minimum_practical_vertical","F_side_LOW_left"):
            for f in (450,2500):
                self.assertAlmostEqual(abs(integrated_pressure(L[name],f,0,0,.7)),1,places=9)

    def test_nonzero_reflection_is_not_a_magic_global_correction(self):
        l=L["A_minimum_practical_vertical"]
        self.assertEqual(reference_relative_db(l,2500,0,None),0)
        self.assertNotAlmostEqual(reference_relative_db(l,2500,.6,None),0,delta=.01)

    def test_zero_table_extent_disables_all_specular_paths(self):
        l=L["F_side_LOW_left"]
        for f in (450,2500):
            self.assertAlmostEqual(reference_relative_db(l,f,.6,0),0,places=12)

    def test_finite_table_changes_response_relative_to_infinite_model(self):
        l=L["A_minimum_practical_vertical"]
        infinite=reference_relative_db(l,2500,.6,None)
        truncated=reference_relative_db(l,2500,.6,.2)
        self.assertGreater(abs(infinite-truncated),.01)

    def test_head_movement_is_not_recalibrated(self):
        l=L["F_side_LOW_left"]
        a=reference_relative_db(l,2500,.6,.45,(0,0))
        b=reference_relative_db(l,2500,.6,.45,(0,.1))
        self.assertGreater(abs(a-b),.01)

    def test_invalid_user_inputs_refused(self):
        l=L["A_minimum_practical_vertical"]
        for k in (-.1,1.1):
            with self.assertRaises(ValueError):
                integrated_pressure(l,2500,0,0,.7,k)
        with self.assertRaises(ValueError):
            integrated_pressure(l,2500,0,0,.7,.3,-.1)
        with self.assertRaises(ValueError):
            integrated_pressure(l,2500,0,-.4,.7,.3)

    def test_stress_layout_below_table_is_not_accepted(self):
        l=L["E_wide_gaps_vertical"]
        with self.assertRaisesRegex(ValueError,"intersects table"):
            integrated_pressure(l,450,0,0,.7,.6)

    def test_scenarios_preserve_nonmeasured_status(self):
        r=scenarios()
        self.assertEqual(r["study"],"D2-WAVE-02")
        self.assertFalse(r["real_desktop_dimensions_known"])
        self.assertFalse(r["component_phase_time_zero_verified"])
        self.assertFalse(r["actual_output_Spl_measured"])
        self.assertEqual(len(r["results"]),3)
        self.assertTrue(all(len(row["scenarios"])==12 for row in r["results"]))


if __name__=="__main__":
    unittest.main()
