import math
import unittest
from acoustic_baseline import SealedBox, gain_db, lr4, report


class SealedBoxTests(unittest.TestCase):
    def test_free_air_limit_as_volume_grows(self):
        d = SealedBox(fs_hz=40, qts=0.4, vas_l=20, net_volume_l=1e12)
        self.assertAlmostEqual(d.fc_hz, 40, places=7)
        self.assertAlmostEqual(d.qtc, 0.4, places=7)

    def test_decreasing_volume_raises_system_resonance(self):
        big = SealedBox(40, 0.4, 20, 40)
        small = SealedBox(40, 0.4, 20, 10)
        self.assertGreater(small.fc_hz, big.fc_hz)
        self.assertGreater(small.qtc, big.qtc)

    def test_f3_at_fc_for_butterworth_qtc(self):
        target_qtc = 1 / math.sqrt(2)
        box = SealedBox(40, target_qtc / math.sqrt(2), 20, 20)
        self.assertAlmostEqual(box.f3_hz(), box.fc_hz, places=5)

    def test_zero_frequency_is_blocked(self):
        self.assertEqual(SealedBox(42, .38, 18, 12).response(0), 0j)

    def test_rejects_invalid_thiele_small_inputs(self):
        with self.assertRaises(ValueError):
            SealedBox(42, .38, 18, 0).f3_hz()


class CrossoverTests(unittest.TestCase):
    def test_lr4_each_is_six_db_down_at_crossover(self):
        low, high = lr4(80, 80)
        self.assertAlmostEqual(abs(low), 0.5, places=9)
        self.assertAlmostEqual(abs(high), 0.5, places=9)

    def test_ideal_aligned_sum_has_unity_magnitude(self):
        for f in (0, 10, 20, 40, 80, 120, 500, 1000):
            low, high = lr4(f, 80)
            self.assertAlmostEqual(abs(low + high), 1.0, places=9)

    def test_lr4_rejects_invalid_freq(self):
        with self.assertRaises(ValueError):
            lr4(-1, 80)

    def test_json_serializable_report(self):
        r = report(SealedBox(42, .38, 18, 12))
        self.assertEqual(len(r["sweep"]), 8)
        self.assertAlmostEqual(r["speaker_distance_m"]["min"], .6)
        self.assertGreater(r["sealed_f3_hz"], 0)


if __name__ == "__main__":
    unittest.main()
