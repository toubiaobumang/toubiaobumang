#!/usr/bin/env python3
"""校验企业知识库 V2.0 标准骨架及可选投标专业档案。"""
from __future__ import annotations

import argparse
from pathlib import Path

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


def main() -> int:
    p = argparse.ArgumentParser(description="校验企业知识库 V2.0 结构")
    p.add_argument("root")
    p.add_argument(
        "--profile",
        choices=["generic", "construction-bidding"],
        default="generic",
    )
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()

    missing: list[str] = []
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            missing.append(f"目录  {rel}")

    required_files = list(REQUIRED_FILES)
    if args.profile == "construction-bidding":
        required_files.extend(CONSTRUCTION_BIDDING_REQUIRED_FILES)

    for rel in required_files:
        if not (root / rel).is_file():
            missing.append(f"文件  {rel}")

    if missing:
        print(f"FAIL：企业知识库 V2.0 [{args.profile}] 结构不完整")
        for item in missing:
            print(f"- {item}")
        return 1

    print(f"PASS：企业知识库 V2.0 [{args.profile}] 标准骨架完整")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
