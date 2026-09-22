#!/usr/bin/env python3
"""校验企业知识库 V2.0.1 标准骨架及关键表头。"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

KB_VERSION = "V2.0.1"

REQUIRED_DIRS = [
    "00_待整理入口",
    "01_企业原始资料库",
    "02_AI企业知识库",
    "03_结构化索引与台账",
    "04_当前项目工作区",
    "05_知识库维护与审计",
    "99_待识别与异常资料",
]

REQUIRED_FILES = [
    "知识库使用说明.md",
    "02_AI企业知识库/00_企业总览.md",
    "03_结构化索引与台账/企业资料总索引.csv",
    "03_结构化索引与台账/人员台账.csv",
    "03_结构化索引与台账/项目案例台账.csv",
    "03_结构化索引与台账/资质证照台账.csv",
    "05_知识库维护与审计/知识库更新日志.md",
    "05_知识库维护与审计/待补资料清单.csv",
    "05_知识库维护与审计/待人工核验.csv",
]

CONSTRUCTION_BIDDING_REQUIRED_FILES = [
    "02_AI企业知识库/08_专题知识/投标知识库使用说明.md",
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

CONSTRUCTION_BIDDING_REQUIRED_COLUMNS = {
    "03_结构化索引与台账/投标事实索引.csv": {
        "事实ID", "对象ID", "对象类型", "对象名称", "属性", "标准值", "原始值", "单位",
        "事实状态", "证据等级", "来源文件", "正式归档路径", "来源定位", "最后核验日期",
        "是否可用于投标匹配",
    },
    "03_结构化索引与台账/企业业绩台账.csv": {
        "合同金额", "金额单位", "建筑面积", "建筑面积单位", "长度", "长度单位",
        "高度", "高度单位", "跨度", "跨度单位", "容量", "容量单位",
        "证据完整度", "事实状态", "最后核验日期", "是否可用于投标匹配",
    },
    "03_结构化索引与台账/个人业绩台账.csv": {
        "合同金额", "金额单位", "建筑面积", "建筑面积单位", "长度", "长度单位",
        "高度", "高度单位", "跨度", "跨度单位", "容量", "容量单位",
        "证明材料路径", "证据完整度", "事实状态", "最后核验日期", "是否可用于投标匹配",
    },
}


def read_csv_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return next(csv.reader(f), [])


def main() -> int:
    p = argparse.ArgumentParser(description=f"校验企业知识库 {KB_VERSION} 结构")
    p.add_argument("root")
    p.add_argument(
        "--profile",
        choices=["generic", "construction-bidding"],
        default="generic",
    )
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()

    problems: list[str] = []
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            problems.append(f"目录缺失  {rel}")

    required_files = list(REQUIRED_FILES)
    if args.profile == "construction-bidding":
        required_files.extend(CONSTRUCTION_BIDDING_REQUIRED_FILES)

    for rel in required_files:
        if not (root / rel).is_file():
            problems.append(f"文件缺失  {rel}")

    if args.profile == "construction-bidding":
        for rel, required_columns in CONSTRUCTION_BIDDING_REQUIRED_COLUMNS.items():
            path = root / rel
            if not path.is_file():
                continue
            try:
                header = set(read_csv_header(path))
            except (OSError, UnicodeError, csv.Error) as exc:
                problems.append(f"表头无法读取  {rel}：{exc}")
                continue
            missing_columns = sorted(required_columns - header)
            if missing_columns:
                problems.append(f"表头缺字段  {rel}：{', '.join(missing_columns)}")

    if problems:
        print(f"FAIL：企业知识库 {KB_VERSION} [{args.profile}] 结构或关键表头不完整")
        for item in problems:
            print(f"- {item}")
        return 1

    print(f"PASS：企业知识库 {KB_VERSION} [{args.profile}] 标准骨架与关键表头完整")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
