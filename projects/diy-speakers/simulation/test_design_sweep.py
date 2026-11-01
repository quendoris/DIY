import json
import math
import unittest
from pathlib import Path

from design_sweep import compare, volume_for_qtc
from acoustic_baseline import SealedBox

CATALOG = json.loads((Path(__file__).resolve().parent / "candidates.json").read_text(encoding="utf-8"))


class InverseBoxTests(unittest.TestCase):
    def test_inverse_qtc_relation_matches_forward(self):
        for fs, qts, vas in ((39, .37, 17.7), (36.5, .42, 27), (46, .39, 21.9)):
            vol = volume_for_qtc(qts, vas, .707)
            self.assertAlmostEqual(SealedBox(fs, qts, vas, vol).qtc, .707, places=8)

    def test_box_size_trends(self):
        self.assertGreater(volume_for_qtc(.37, 17.7, .65),
                           volume_for_qtc(.37, 17.7, .707))
        self.assertGreater(volume_for_qtc(.37, 17.7, .707),
                           volume_for_qtc(.37, 17.7, .8))

    def test_impossible_target_is_explicit(self):
        with self.assertRaises(ValueError):
            volume_for_qtc(.8, 30, .7)

    def test_midwoofer_volumes_at_qtc_707(self):
        result = compare(CATALOG, .707)
        rows = {v["id"]: v for v in result["midwoofers"]}
        self.assertAlmostEqual(rows["SB15MFC30-8"]["net_box_l"], 6.68, delta=.03)
        self.assertAlmostEqual(rows["SB17NRX2C35-8"]["net_box_l"], 14.73, delta=.03)
        self.assertAlmostEqual(rows["HiVi-M6N-B"]["net_box_l"], 9.58, delta=.03)
        self.assertAlmostEqual(rows["SB15MFC30-8"]["fc_hz"],
                               rows["SB15MFC30-8"]["f3_hz"], places=2)

    def test_unrealistically_low_target_is_not_silently_clipped(self):
        result = compare(CATALOG, .3)
        self.assertTrue(all(v["status"] == "NO_FINITE_POSITIVE_BOX"
                            for v in result["midwoofers"]))

    def test_json_output_can_be_serialized(self):
        self.assertIn('"midwoofers"', json.dumps(compare(CATALOG)))


if __name__ == "__main__":
    unittest.main()
