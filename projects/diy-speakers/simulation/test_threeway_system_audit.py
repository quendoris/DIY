import json
import unittest

from threeway_system_audit import CATALOG, evaluate

DATA=json.loads(CATALOG.read_text(encoding="utf-8"))


class ThreeWaySystemTests(unittest.TestCase):
    def setUp(self):
        self.result=evaluate(DATA)
        self.systems={x["system_id"]:x for x in self.result["system_comparisons"]}
        self.subs={x["id"]:x for x in self.result["subwoofer_displacement_comparison"]}

    def test_three_way_stereo_plus_sub_requires_seven_channels(self):
        self.assertEqual(self.systems["three_way_hivi_wavecor"]["digital_amp_output_channels"],7)
        self.assertEqual(self.systems["three_way_all_wavecor"]["digital_amp_output_channels"],7)

    def test_two_way_plus_sub_requires_five_channels(self):
        self.assertEqual(self.systems["two_way_hivi"]["digital_amp_output_channels"],5)

    def test_all_published_sample_boms_reproduce(self):
        self.assertEqual(self.systems["three_way_hivi_wavecor"]["drivers_only_rub"],87978)
        self.assertEqual(self.systems["three_way_all_wavecor"]["drivers_only_rub"],92300)
        self.assertEqual(self.systems["two_way_hivi"]["drivers_only_rub"],63978)

    def test_2way_3way_difference_is_more_than_0(self):
        self.assertEqual(
            self.systems["three_way_hivi_wavecor"]["drivers_only_rub"] -
            self.systems["two_way_hivi"]["drivers_only_rub"],24000
        )

    def test_sub_displacement_geometric_units(self):
        self.assertAlmostEqual(self.subs["Wavecor SW280WA01"]["vd_cm3"],201)
        self.assertAlmostEqual(self.subs["Wavecor SW312WA05"]["vd_cm3"],561.2)
        self.assertAlmostEqual(self.subs["Dayton RSS315HF-4"]["vd_cm3"],736)

    def test_no_unverified_sub_spl(self):
        self.assertTrue(all(x["measured_bass_at_25hz"] is None for x in self.subs.values()))

    def test_deprecated_parts_not_in_boms(self):
        disabled={x["id"] for x in DATA["rejected"]}
        for system in DATA["sample_systems"]:
            self.assertFalse(set(system["per_satellite"]) & disabled)
            self.assertNotIn(system["sub"],disabled)

    def test_source_and_currency_flags(self):
        for name in ("midranges","tweeters","bass_satellites","subwoofers"):
            for item in DATA[name]:
                self.assertTrue(item["maker"].startswith("https://"))
                if item.get("price_rub_unit") is not None:
                    self.assertGreater(item["price_rub_unit"],0)
        self.assertEqual(self.systems["three_way_hivi_wavecor"]["sub_ohm"],4)


if __name__=="__main__":
    unittest.main()
