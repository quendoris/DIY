import math
import unittest

from wavecor_phase_sensitivity import (
    BASELINE_DB, flattening_metric, investigate,
    physical_path_increment_us, responses_for
)
from wavecor_threeway_realdata import Curve


def flat_inputs():
    fs=[100,150,250,450,800,1100,2000,2500,3500,6000,9000,12000]
    return {name:Curve("spl",[(f,BASELINE_DB,0.) for f in fs])
            for name in ("LOW","MID","HIGH")}


class SensitivityTests(unittest.TestCase):
    def test_flat_drivers_ideal_filters_are_flat_if_delay_free(self):
        rows=responses_for(flat_inputs(),450,2500)
        self.assertLess(flattening_metric(rows),1e-9)

    def test_relative_delay_changes_ideal_summed_response(self):
        curves=flat_inputs()
        base=dict(responses_for(curves,450,2500))
        later=dict(responses_for(curves,450,2500,high_delay_us=100))
        self.assertLess(later[2500],base[2500]-.5)

    def test_ear_height_change_zero_at_baseline(self):
        for z in (-.15,0,.115):
            self.assertAlmostEqual(physical_path_increment_us(0,z),0.,places=9)

    def test_head_shift_has_opposite_signs_for_woofer_tweeter(self):
        low=physical_path_increment_us(.1,-.15)
        high=physical_path_increment_us(.1,.115)
        self.assertGreater(low,0)
        self.assertLess(high,0)

    def test_invalid_crossover_detected(self):
        with self.assertRaises(ValueError):
            responses_for(flat_inputs(),3000,1000)
        with self.assertRaises(ValueError):
            flattening_metric([])

    def test_genuine_uncertainty_is_not_overridden(self):
        rep=investigate(flat_inputs())
        self.assertFalse(rep["phase_origins_cross_driver_verified"])
        self.assertFalse(rep["measured_system"])
        self.assertFalse(rep["valid_for_component_selection"])
        self.assertGreater(len(rep["geometry_only_head_motion_scenarios"]),10)
        self.assertEqual(len(rep["relative_channel_delay_sensitivity"]),7)
        self.assertEqual(len(rep["crossover_hypothetical_ranking"]),10)

if __name__=="__main__":
    unittest.main()
