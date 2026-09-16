import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INIT = REPO / "scripts" / "initialize_kb.py"


class TestV2ConstructionBiddingInitialization(unittest.TestCase):
    def run_init(self, root: Path):
        return subprocess.run(
            [sys.executable, str(INIT), str(root), "--profile", "construction-bidding"],
            cwd=REPO,
            text=True,
            capture_output=True,
        )

    def test_construction_profile_creates_bid_ready_registers(self):
        expected = [
            "03_结构化索引与台账/投标事实索引.csv",
            "03_结构化索引与台账/企业资质台账.csv",
            "03_结构化索引与台账/投标人员台账.csv",
            "03_结构化索引与台账/企业业绩台账.csv",
            "03_结构化索引与台账/个人业绩台账.csv",
            "03_结构化索引与台账/信用奖项台账.csv",
            "03_结构化索引与台账/财务税务保险台账.csv",
            "03_结构化索引与台账/设备资源台账.csv",
            "03_结构化索引与台账/技术方案索引.csv",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "企业知识库"
            result = self.run_init(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            for rel in expected:
                self.assertTrue((root / rel).exists(), rel)

    def test_bid_fact_index_is_atomic_and_traceable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "企业知识库"
            result = self.run_init(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            p = root / "03_结构化索引与台账/投标事实索引.csv"
            with p.open("r", encoding="utf-8-sig", newline="") as f:
                header = next(csv.reader(f))
            required = {
                "事实ID", "对象ID", "对象类型", "属性", "标准值", "单位",
                "事实状态", "证据等级", "来源文件", "来源定位", "最后核验日期"
            }
            self.assertTrue(required.issubset(set(header)), header)

    def test_performance_register_contains_bid_filter_fields(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "企业知识库"
            result = self.run_init(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            p = root / "03_结构化索引与台账/企业业绩台账.csv"
            with p.open("r", encoding="utf-8-sig", newline="") as f:
                header = next(csv.reader(f))
            required = {
                "工程类别", "项目标签", "合同金额", "建筑面积", "长度", "高度", "跨度", "容量",
                "中标日期", "合同日期", "竣工日期", "项目经理", "技术负责人",
                "中标通知书路径", "合同路径", "验收材料路径", "官方查询证明路径", "证据完整度"
            }
            self.assertTrue(required.issubset(set(header)), header)

    def test_existing_files_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "企业知识库"
            target = root / "03_结构化索引与台账/企业业绩台账.csv"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("DO_NOT_OVERWRITE\n", encoding="utf-8")
            result = self.run_init(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "DO_NOT_OVERWRITE\n")

    def test_bid_matching_contract_reference_exists(self):
        self.assertTrue((REPO / "references/bid-matching-contract.md").exists())


if __name__ == "__main__":
    unittest.main()
