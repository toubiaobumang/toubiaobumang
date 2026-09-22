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
            self.assertIn("V2.0.1", result.stdout)


    def test_construction_validation_fails_when_metric_unit_columns_are_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "企业知识库"
            subprocess.run(
                [sys.executable, str(INIT), str(root), "--profile", "construction-bidding"],
                check=True,
                capture_output=True,
                text=True,
            )
            target = root / "03_结构化索引与台账/企业业绩台账.csv"
            target.write_text(
                "业绩ID,项目名称,合同金额,金额单位,建筑面积,长度,高度,跨度,容量,规模单位,证据完整度,事实状态,最后核验日期,是否可用于投标匹配\n",
                encoding="utf-8-sig",
            )
            result = subprocess.run(
                [sys.executable, str(VALIDATE), str(root), "--profile", "construction-bidding"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("建筑面积单位", result.stdout)
            self.assertIn("跨度单位", result.stdout)

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
