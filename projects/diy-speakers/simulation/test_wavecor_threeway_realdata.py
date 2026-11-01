import math
import unittest
from wavecor_threeway_realdata import Curve, parse_wavecor, make_report, SOURCES

def fixture(kind, base):
    header="Freq\tdB\tPhase" if kind=="spl" else "Freq\tOhm\tDeg"
    return parse_wavecor(header+"\n" +
      "\n".join(f"{f} {base+(i%3)} {-90+i*10}" for i,f in enumerate([100,200,400,1000,2000,4000,8000,12000])),kind)

class RealDataParsingTests(unittest.TestCase):
    def test_spl_with_actual_manufacturer_header(self):
        c=fixture("spl",86)
        self.assertEqual(c.kind,"spl")
        self.assertAlmostEqual(c.at(400)[0],88)
        self.assertAlmostEqual(abs(c.complex_at(400)),10**(88/20),places=8)

    def test_impedance_with_actual_header(self):
        c=fixture("impedance",7)
        self.assertAlmostEqual(c.at(1000)[0],7)

    def test_explicit_outside_dataset_rejected(self):
        c=fixture("spl",86)
        with self.assertRaisesRegex(ValueError,"outside"):
            c.at(15000)

    def test_missing_phase_column_rejected(self):
        with self.assertRaisesRegex(ValueError,"header"):
            parse_wavecor("Freq dB\n100 85\n200 85","spl")

    def test_bad_impedance_rejected(self):
        with self.assertRaises(ValueError):
            parse_wavecor("Freq Ohm Deg\n100 8 0\n200 -2 0\n300 9 0","impedance")

    def test_duplicate_frequency_rejected(self):
        with self.assertRaises(ValueError):
            parse_wavecor("Freq dB Phase\n100 80 0\n200 80 0\n200 80 0","spl")

    def test_phase_unwrap_is_continuous(self):
        c=parse_wavecor("Freq dB Phase\n100 86 170\n200 86 179\n400 86 -179\n800 86 -170","spl")
        self.assertAlmostEqual(math.degrees(c.at(400)[1]),181,places=5)

    def test_report_does_not_claim_reconstructed_system(self):
        curves={name:{"spl":fixture("spl",{"LOW":87,"MID":86,"HIGH":91}[name]),
                      "impedance":fixture("impedance",8)} for name in SOURCES}
        metadata={name:{kind:{"sha256":"0"*64,"size_bytes":700,"url":src[kind]}
                        for kind in ("spl","impedance")} for name,src in SOURCES.items()}
        rep=make_report(curves,metadata)
        self.assertFalse(rep["measured_three_way_phase_aligned"])
        self.assertFalse(rep["measured_finite_baffle"])
        self.assertEqual(len(rep["illustrative_responses"]),11)
        self.assertTrue(all(r["same_time_reference_as_other_drivers"] is False
                            for r in rep["drivers"].values()))
        self.assertTrue(all(r["phase_column_present"] for r in rep["drivers"].values()))

    def test_source_has_six_explicit_manufacturer_paths(self):
        self.assertEqual(len(SOURCES),3)
        self.assertEqual(len({s["spl"] for s in SOURCES.values()}),3)
        self.assertTrue(all(url.startswith("https://www.wavecor.com/Driver%20measurements")
                  for s in SOURCES.values() for url in (s["spl"],s["impedance"])))

if __name__=="__main__":
    unittest.main()
