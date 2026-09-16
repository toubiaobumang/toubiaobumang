import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INIT = REPO / "scripts" / "initialize_kb.py"
VALIDATE = REPO / "scripts" / "validate_structure.py"


class TestV2Validator(unittest.TestCase):
    def test_construction_profile_validation_passes_after_profile_init(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "企业知识库"
            subprocess.run(
                [sys.executable, str(INIT), str(root), "--profile", "construction-bidding"],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [sys.executable, str(VALIDATE), str(root), "--profile", "construction-bidding"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("V2.0", result.stdout)

    def test_generic_init_fails_construction_profile_validation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "企业知识库"
            subprocess.run(
                [sys.executable, str(INIT), str(root)],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [sys.executable, str(VALIDATE), str(root), "--profile", "construction-bidding"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("投标事实索引.csv", result.stdout)


if __name__ == "__main__":
    unittest.main()
