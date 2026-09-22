import csv
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]


class TestReleaseConsistency(unittest.TestCase):
    def test_repository_and_skill_versions_are_release_versions(self):
        self.assertEqual((REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip(), "1.0.1")
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('version: "2.0.1"', skill_text)
        evals_text = (SKILL_ROOT / "evals" / "evals.json").read_text(encoding="utf-8")
        self.assertIn('"version": "2.0.1"', evals_text)

    def test_bid_requirement_contract_matches_template_time_and_logic_fields(self):
        schema = SKILL_ROOT / "templates" / "bid-requirement-schema.csv"
        with schema.open("r", encoding="utf-8-sig", newline="") as f:
            header = next(csv.reader(f))
        required = {"time_start", "time_end", "parent_group", "logic"}
        self.assertTrue(required.issubset(set(header)), header)
        self.assertNotIn("time_window", header)

        contract = (SKILL_ROOT / "references" / "bid-matching-contract.md").read_text(encoding="utf-8")
        for field in required:
            self.assertIn(f"| {field} |", contract)
        self.assertNotIn("| time_window |", contract)

    def test_fact_status_vocabulary_has_no_legacy_combined_terms(self):
        paths = [
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "references" / "evidence-rules.md",
            SKILL_ROOT / "references" / "entity-model.md",
            SKILL_ROOT / "references" / "bid-matching-contract.md",
            SKILL_ROOT / "templates" / "wiki-page.md",
        ]
        merged = "\n".join(p.read_text(encoding="utf-8") for p in paths)
        self.assertNotIn("历史或失效", merged)
        self.assertNotIn("`历史/失效`", merged)
        for term in ["已确认", "待核验", "历史", "失效", "版本冲突", "缺失", "不适用"]:
            self.assertIn(term, merged)


if __name__ == "__main__":
    unittest.main()
