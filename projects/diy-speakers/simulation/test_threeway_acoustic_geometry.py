import math
import unittest
from threeway_acoustic_geometry import (
    ResponsePoint, complex_from_point, delayed_pair_sum_db, lr4_pair,
    parse_phase_frd, pair_path_difference_us, projected_mid_high_geometry
)


class ThreewayGeometryProofOfConcept(unittest.TestCase):
    def test_ideal_lr4_single_pair_is_magnitude_allpass(self):
        for f in (50,200,400,800,1500,2500,5000,15000):
            lo,hi=lr4_pair(f,2500)
            self.assertAlmostEqual(abs(lo+hi),1,places=10)

    def test_crossover_both_paths_are_minus_6dB(self):
        lo,hi=lr4_pair(2500,2500)
        self.assertAlmostEqual(abs(lo),.5,places=10)
        self.assertAlmostEqual(abs(hi),.5,places=10)
        self.assertAlmostEqual(delayed_pair_sum_db(2500,0),0,places=10)

    def test_delay_mismatch_is_not_free(self):
        self.assertAlmostEqual(delayed_pair_sum_db(2500,100),-3.0103,places=3)
        self.assertLess(delayed_pair_sum_db(2500,50),0)

    def test_center_spacing_changes_vertical_listening_response(self):
        center=pair_path_difference_us(.115,.7,0)
        raised=pair_path_difference_us(.115,.7,.1)
        self.assertAlmostEqual(center,0,places=9)
        self.assertGreater(raised,40)
        self.assertLess(raised,60)

    def test_frd_requires_phase(self):
        with self.assertRaisesRegex(ValueError,"three columns"):
            parse_phase_frd("100 85\n200 86\n")
        with self.assertRaisesRegex(ValueError,"increase"):
            parse_phase_frd("200 85 0\n100 86 0")

    def test_frd_nonfinite_and_short_series_not_allowed(self):
        with self.assertRaises(ValueError):
            parse_phase_frd("200 90 nan\n300 91 0")
        with self.assertRaises(ValueError):
            parse_phase_frd("100 88 0")

    def test_frd_complex_response_reconstruction(self):
        d=parse_phase_frd("# valid\n1000 -6.0205999 -180\n2000 -6.0205999 180\n")
        self.assertAlmostEqual(abs(complex_from_point(d[0])),.5,places=7)

    def test_report_marks_ideal_not_measured(self):
        d=projected_mid_high_geometry()
        self.assertFalse(d["measured_driver_phase_imported"])
        self.assertFalse(d["derived_production_crossover"])
        self.assertFalse(d["baffle_and_reflection_modeled"])
        self.assertEqual(len(d["head_movement_window"]),9)


if __name__=="__main__":
    unittest.main()
