import json
import unittest
from pathlib import Path
from compare_candidates import compare_catalog

CATALOG = json.loads((Path(__file__).resolve().parent / "candidates.json").read_text(encoding="utf-8"))


class CandidateComparisonTests(unittest.TestCase):
    def test_all_candidates_have_verifiable_sources(self):
        for group in ("midwoofers", "subwoofers", "tweeters"):
            self.assertTrue(CATALOG[group])
            for c in CATALOG[group]:
                self.assertTrue(c["source"].startswith("https://"))
                self.assertTrue(c["id"])

    def test_unique_ids_within_each_group(self):
        for group in ("midwoofers", "subwoofers", "tweeters"):
            ids = [c["id"] for c in CATALOG[group]]
            self.assertEqual(len(ids), len(set(ids)))

    def test_calculated_vd_for_dayton_is_consistent_with_reported_data(self):
        report = compare_catalog(CATALOG)
        rows = {v["id"]: v for v in report["groups"]["subwoofers"]}
        self.assertAlmostEqual(rows["DCS255-4"]["vd_cm3_if_xmax_defined"], 287.51, delta=.1)
        self.assertAlmostEqual(rows["RSS265HO-4"]["vd_cm3_if_xmax_defined"], 430.13, delta=.1)
        self.assertAlmostEqual(rows["RSS315HF-4"]["vd_cm3_if_xmax_defined"], 736.02, delta=.1)

    def test_unspecified_xmax_never_invented(self):
        report = compare_catalog(CATALOG)
        rows = {v["id"]: v for v in report["groups"]["subwoofers"]}
        self.assertIsNone(rows["SB29SWNRX-S75-6"]["vd_cm3_if_xmax_defined"])
        self.assertIsNone(rows["SB34SWNRX-S75-6"]["vd_cm3_if_xmax_defined"])

    def test_known_sealed_box_example(self):
        report = compare_catalog(CATALOG)
        rows = {v["id"]: v for v in report["groups"]["midwoofers"]}
        self.assertAlmostEqual(rows["SB15MFC30-8"]["sealed_f3_hz"], 74.8, delta=.3)
        self.assertAlmostEqual(rows["SB17NRX2C35-8"]["sealed_f3_hz"], 61.7, delta=.3)

    def test_results_are_json_serializable(self):
        self.assertIn('"midwoofers"', json.dumps(compare_catalog(CATALOG)))


if __name__ == "__main__":
    unittest.main()
