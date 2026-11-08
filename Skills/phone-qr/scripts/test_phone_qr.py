"""Tests for phone_qr.py. Run: python -m unittest discover -s ~/.claude/scripts -p "test_phone_qr.py"."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phone_qr  # noqa: E402


class CandidateUrls(unittest.TestCase):
    def test_tailscale_first_then_home_wifi(self):
        got = phone_qr.candidate_urls(8765, "/", "100.64.0.10", "192.168.1.20")
        self.assertEqual(got, [
            ("Tailscale", "http://100.64.0.10:8765/"),
            ("Home Wi-Fi", "http://192.168.1.20:8765/"),
        ])

    def test_skips_missing_addresses(self):
        self.assertEqual(phone_qr.candidate_urls(3000, "/", None, "10.0.0.5"),
                         [("Home Wi-Fi", "http://10.0.0.5:3000/")])

    def test_path_is_normalised(self):
        got = phone_qr.candidate_urls(80, "app/today", "100.1.2.3", None)
        self.assertEqual(got, [("Tailscale", "http://100.1.2.3:80/app/today")])


class Classify(unittest.TestCase):
    CANDS = [("Tailscale", "http://100.1.2.3:8765/"), ("Home Wi-Fi", "http://192.168.1.2:8765/")]

    def test_ok_keeps_only_reachable(self):
        reach = {self.CANDS[0][1]: False, self.CANDS[1][1]: True}
        status, ok = phone_qr.classify(self.CANDS, reach, localhost_ok=True)
        self.assertEqual(status, "ok")
        self.assertEqual(ok, [self.CANDS[1]])

    def test_localhost_only(self):
        reach = {u: False for _, u in self.CANDS}
        self.assertEqual(phone_qr.classify(self.CANDS, reach, localhost_ok=True), ("localhost-only", []))

    def test_down(self):
        reach = {u: False for _, u in self.CANDS}
        self.assertEqual(phone_qr.classify(self.CANDS, reach, localhost_ok=False), ("down", []))

    def test_no_network_addresses(self):
        self.assertEqual(phone_qr.classify([], {}, localhost_ok=True), ("no-network", []))


class Svg(unittest.TestCase):
    def test_svg_has_one_code_per_url_with_labels(self):
        svg = phone_qr.qr_svg(TestData.TWO)
        self.assertTrue(svg.startswith("<svg"))
        self.assertEqual(svg.count('class="qr"'), 2)
        self.assertIn("Tailscale", svg)
        self.assertIn("http://192.168.1.2:8765/", svg)

    def test_svg_draws_dark_modules_on_white(self):
        svg = phone_qr.qr_svg(TestData.TWO[:1])
        self.assertIn('fill="#fff"', svg)
        self.assertIn('fill="#000"', svg)
        self.assertRegex(svg, r'<path class="qr" [^>]*d="M\d')

    def test_svg_escapes_text(self):
        svg = phone_qr.qr_svg([("A&B", "http://1.2.3.4:1/?a=1&b=2")])
        self.assertNotIn("A&B", svg)
        self.assertIn("A&amp;B", svg)


class TestData:
    TWO = [("Tailscale", "http://100.1.2.3:8765/"), ("Home Wi-Fi", "http://192.168.1.2:8765/")]


if __name__ == "__main__":
    unittest.main()
