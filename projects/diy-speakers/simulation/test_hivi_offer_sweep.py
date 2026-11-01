import json
import math
import unittest

from hivi_offer_sweep import DATA, compare, volume_at_qtc
from acoustic_baseline import SealedBox

CATALOG = json.loads(DATA.read_text(encoding="utf8"))


class OfferedHiViTests(unittest.TestCase):
    def test_known_models_and_user_observed_prices(self):
        p = {v["model"]: v["unit_price_rub_user_observed"] for v in CATALOG["candidates"]}
        self.assertEqual(p, {"HiVi F6N": 6729, "HiVi D6G": 7762, "HiVi M6N": 6439})

    def test_every_source_scenario_is_preserved(self):
        result = compare(CATALOG)
        r = result["comparison"]
        self.assertEqual(len(r), 4)
        self.assertEqual(sum(row["model"] == "HiVi F6N" for row in r), 2)
        self.assertEqual({row["scenario_id"] for row in r if row["model"] == "HiVi F6N"},
                         {"seller_spec", "other_published_f6n"})

    def test_qts_identity_with_spec_precision(self):
        for r in compare(CATALOG)["comparison"]:
            self.assertLess(r["source_internal_qts_difference"], 0.012)

    def test_butterworth_inverse_matches_forward(self):
        for c in CATALOG["candidates"]:
            for s in c["scenarios"]:
                v = volume_at_qtc(s["qts"], s["vas_l"])
                b = SealedBox(s["fs_hz"], s["qts"], s["vas_l"], v)
                self.assertAlmostEqual(b.qtc, 1 / math.sqrt(2), places=10)
                self.assertAlmostEqual(b.fc_hz, b.f3_hz(), places=8)

    def test_seller_f6n_and_alt_have_distinct_f3(self):
        rows = {r["scenario_id"]: r for r in compare(CATALOG)["comparison"]}
        self.assertAlmostEqual(rows["seller_spec"]["fixture_f3_hz"], 91.83, delta=.15)
        self.assertAlmostEqual(rows["other_published_f6n"]["fixture_f3_hz"], 79.92, delta=.15)
        self.assertGreater(abs(rows["seller_spec"]["fixture_f3_hz"] -
                               rows["other_published_f6n"]["fixture_f3_hz"]), 10)

    def test_invoice_price_is_two_seller_units(self):
        for r in compare(CATALOG)["comparison"]:
            self.assertEqual(r["seller_observed_price_rub_pair"], 2*r["seller_observed_price_rub_each"])

    def test_nonphysical_box_target_is_rejected(self):
        with self.assertRaises(ValueError):
            volume_at_qtc(.9, 30)
        with self.assertRaises(ValueError):
            compare(CATALOG, 0)

    def test_report_is_json_serializable(self):
        report = compare(CATALOG)
        self.assertIn("known_source_disagreement", json.loads(json.dumps(report)))


if __name__ == "__main__":
    unittest.main()
