import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from simple_eval import flags, load_json, render_report, summarize, validate_scorecard


class SimpleScorecardTests(unittest.TestCase):
    def setUp(self):
        self.data = load_json(ROOT / "evals/SIMPLE_SCORECARD.json")

    def test_scorecard_references_published_responses(self):
        self.assertEqual(validate_scorecard(self.data, ROOT), [])

    def test_summary_is_easy_to_check(self):
        summary = summarize(self.data)
        self.assertEqual(summary["cases"], 8)
        self.assertEqual(summary["arms"]["baseline"]["counts"]["experiment"], 3)
        self.assertEqual(summary["arms"]["skill"]["counts"]["experiment"], 7)
        self.assertEqual(summary["arms"]["baseline"]["counts"]["all_three"], 3)
        self.assertEqual(summary["arms"]["skill"]["counts"]["all_three"], 6)

    def test_flags_use_the_documented_rules(self):
        self.assertEqual(
            flags({"evidence": 2, "uncertainty": 2, "experiment": 2, "founder_fit": 2, "decision": 2}),
            {"evidence": True, "experiment": True, "decision": True},
        )
        self.assertEqual(
            flags({"evidence": 2, "uncertainty": 2, "experiment": 1, "founder_fit": 2, "decision": 1}),
            {"evidence": True, "experiment": False, "decision": False},
        )

    def test_rendered_report_contains_plain_language_result(self):
        report = render_report(self.data)
        self.assertIn("strong, founder-fit experiment from **3/8** to **7/8**", report)
        self.assertIn("All three in the same answer", report)
        self.assertIn("unblinded qualitative AI review", report)

    def test_committed_report_matches_the_scorecard(self):
        self.assertEqual(
            (ROOT / "evals/SIMPLE_REPORT.md").read_text(encoding="utf-8"),
            render_report(self.data),
        )

    def test_invalid_score_is_rejected(self):
        broken = json.loads(json.dumps(self.data))
        broken["cases"][0]["skill"]["experiment"] = 3
        self.assertTrue(any("must be 0, 1, or 2" in error for error in validate_scorecard(broken, ROOT)))


if __name__ == "__main__":
    unittest.main()
