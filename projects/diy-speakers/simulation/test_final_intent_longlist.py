"""Consistency audits for serious end-system acoustic candidate research.

Only validates records and nominal voltage-power normalizations, NOT actual
transducer distortion, crossover or quality.
"""
import json
import math
import unittest
from pathlib import Path

FILE=Path(__file__).with_name("final_intent_longlist_2026-11.json")
CATALOG=json.loads(FILE.read_text(encoding="utf-8"))
C={c["id"]:c for c in CATALOG["candidates"]}


def nominal_db_at_1w(sensitivity_db_2v83m, impedance_ohm):
    """Nominal load only; measured impedance and averaging band vary."""
    if impedance_ohm <= 0:
        raise ValueError("invalid impedance")
    return sensitivity_db_2v83m - 10*math.log10(2.83**2/impedance_ohm)


class FinalIntentResearchTests(unittest.TestCase):
    def test_all_records_preserve_provenance(self):
        for c in CATALOG["candidates"]:
            self.assertTrue(c["id"])
            self.assertTrue(c["primary_url"].startswith("https://"))
            self.assertTrue(c["source_level"])
            self.assertTrue(c["status"])

    def test_no_duplicate_models_or_unknown_price_exchange(self):
        self.assertEqual(len(CATALOG["candidates"]),len(C))
        for c in CATALOG["candidates"]:
            if c["price"] is not None:
                currencies=[x for x in ("rub","eur","dkk") if x in c["price"]]
                self.assertEqual(len(currencies),1)
                self.assertTrue(c["price"]["each"])

    def test_final_intent_does_not_mean_measured_proof(self):
        self.assertIn("No competitive winner",CATALOG["warning"])
        for key in ("HIVI-M6N","WAVECOR-WF152BD14","SB-SB17NBAC35-4"):
            self.assertIn("final_intent",C[key]["status"])

    def test_wavecor_russian_price_not_aspirational(self):
        expected={"WAVECOR-WF168WA02":9200,"WAVECOR-WF168WA06":8600,"WAVECOR-WF152BD14":14000}
        for key,price in expected.items():
            self.assertEqual(C[key]["price"]["rub"],price)
            self.assertTrue(C[key]["retailer_url"].startswith("https://"))

    def test_discrepancies_remain_visible(self):
        self.assertIsNone(C["HIVI-F6N"]["fs_hz"])
        self.assertIn("seller",C["WAVECOR-WF168WA06"]["note"])
        self.assertEqual(C["SB-SB17NBAC35-8"]["ohm"], 8)
        self.assertIn("4-ohm tested variant", C["SB-SB17NBAC35-8"]["note"])
        self.assertEqual(C["SB-SB17NBAC35-4"]["ohm"],4)

    def test_four_ohm_sensitivity_requires_power_normalization(self):
        scan=C["SCAN-SPEAK-18W-4434G00"]
        actual=nominal_db_at_1w(scan["sens_db_2v83m"],scan["ohm"])
        self.assertAlmostEqual(actual,88.4897,delta=.01)
        hivi=C["HIVI-M6N"]
        self.assertAlmostEqual(nominal_db_at_1w(hivi["sens_db_2v83m"],8),89,delta=.01)

    def test_missing_data_not_invented(self):
        for k in ("SEAS-U18RNX-P","HIVI-L6-4R"):
            self.assertIsNone(C[k]["qts"])
            self.assertIsNone(C[k]["sens_db_2v83m"])
        self.assertTrue(C["PURIFI-PTT6.5X04-NFA-06"]["price"]["dkk"]>0)


if __name__=="__main__":
    unittest.main()
