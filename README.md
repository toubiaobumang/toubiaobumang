# 投标不盲｜AI 投标 Skills 与工具

“投标不盲”公开项目仓库。

## 当前公开项目

### 企业投标知识库

用于将企业资质、人员、业绩、奖项、财务、设备、技术资料等投标相关资料进行结构化整理，建立可检索、可追溯、可持续更新，并可供招标条件反查的企业投标知识库。

目录：[`skills/building-enterprise-knowledge-bases/`](skills/building-enterprise-knowledge-bases/)

详细使用规则：[`SKILL.md`](skills/building-enterprise-knowledge-bases/SKILL.md)

## 快速开始

将 `skills/building-enterprise-knowledge-bases/` 整个目录安装或复制到支持 Agent Skills 的客户端或授权工作空间中使用。

如需用脚本初始化建筑、工程、施工或招投标企业知识库，可在 Skill 目录执行：

```bash
python scripts/initialize_kb.py "<企业知识库根目录>" --profile construction-bidding
```

脚本只创建缺失目录和空表，不覆盖已有业务文件。

## 版本

- 仓库版本：`1.0.0`
- 企业投标知识库 Skill：`2.0.0`

## 使用许可

本仓库适用《投标不盲公开免费使用许可协议 V1.0》。

简要规则：

- 个人及企业内部可免费使用
- 可免费分享未经修改的官方版本
- 未经授权不得商业转售、收费分发、冒充原创或将本项目本身商业产品化

完整条款见 [`LICENSE`](LICENSE)。如本摘要与 LICENSE 不一致，以 LICENSE 为准。

## 官方来源

https://github.com/toubiaobumang/toubiaobumang

## 使用提示

AI 输出、结构化结果和投标匹配结论应结合原始资料、具体招标文件及最新适用规则进行人工复核。
