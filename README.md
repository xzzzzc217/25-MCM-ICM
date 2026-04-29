# 25 美赛 / MCM-ICM 资料库

本仓库收录了准备 2025 年美国大学生数学建模竞赛（MCM/ICM）期间整理的资料、历年题目、代码与论文，以及参赛 2025 C 题的完整工作过程。

## 目录结构

```
25美赛/
├── 2023/                       # 2023 年 MCM/ICM 各题（A–F）题面、O 奖论文、评委评论
├── 2024/                       # 2024 年 MCM/ICM 各题（A–F）题面、O 奖论文、评委评论
├── 2025_MCM-ICM_Problems/      # 2025 年官方题目与数据集
│   ├── 2025_MCM_Problem_A/E/F.pdf
│   ├── 2025_Problem_C_Data/    # C 题：奥运会奖牌预测数据（运动员、奖牌等）
│   └── 2025_Problem_D_Data.zip # D 题数据
├── 22c/                        # 2022 C 题练习（含原始数据、处理后数据、伪代码、复现代码）
├── 24d/                        # 2024 D 题练习
├── 25c/                        # 【参赛】2025 C 题的完整解题过程（详见 25c/README.md）
│   ├── 02_代码/                    # 第一问代码包
│   ├── 03_处理后数据/              # CSV/XLSX 中间产物与最终输出
│   ├── 04_模型分析文档/            # 各子模型的 Word 说明
│   ├── 05_可视化/                  # 思维框图与结果图
│   └── 06_论文/                    # 最终论文 PDF
├── 2023美赛LaTeX模板.txt        # 美赛 LaTeX 模板说明
├── main.tex                    # 论文主 tex 文件
├── 2519836.pdf                 # 一篇优秀范文
├── 美赛.pdf                     # 备赛参考文档
├── 美赛实例.zip                 # 实例资料
└── 代码汇总.docx                # 常用代码汇总
```

## 2025 C 题（25c/）研究主题

题目方向：基于历届夏季奥运会数据预测 2028 年奖牌数。25c 文件夹中保留了完整的工作流：

- **数据预处理**：`processed_athletes.csv`、`olympic_data.csv`、`athlete_num_by_year_sex.csv`
- **模型建立**：线性关系验证（验证 Y 与 xi 存在线性关系.docx）、首次获奖国家专项分析、教练效应建模
- **预测与验证**：`effective_ratio_prediction_by_year.csv`、`prediction_diff.csv`、`omega_results.csv`、敏感性分析
- **可视化**：教练效应前后对比图、Pearson 相关系数热力图

## 历年题目说明

`2023/` 与 `2024/` 收录了 6 个赛道（A 连续型、B 离散型、C 数据分析、D 运筹/网络科学、E 环境科学、F 政策）的题面、官方评委评论（JC/AC/PC）以及多篇 Outstanding 论文，便于研读思路与表述。

## 使用建议

- 论文写作模板见 `main.tex` 与 `2023美赛LaTeX模板.txt`
- 学习思路时优先看官方 Judges Commentary（`*_JC.pdf`），再读 O 奖论文
- 25c 中 `.drawio` 文件可用 [draw.io](https://app.diagrams.net/) 打开

## 致谢与免责

仓库中的官方题面、数据、Outstanding 论文与评委评论版权归 [COMAP](https://www.comap.com/) 所有，仅供学习交流，请勿用于商业用途。25c 中的代码与文档为参赛过程产出。
