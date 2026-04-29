# 25c — 2025 MCM Problem C 完整解题过程

题目方向:基于历届夏季奥运会数据预测 2028 年奖牌数(包括金牌、奖牌总数,并对首次获奖国家与教练效应建模)。

## 目录结构

```
25c/
├── README.md                  # 本文件
├── 02_代码/
│   └── C题第一问第一小问代码/    # 第一问代码包(自包含,可直接运行)
│       ├── Q1-code1.ipynb
│       ├── 2025_MCM_Problem_C.docx
│       ├── data_dictionary.xlsx
│       ├── summerOly_medal_counts.csv
│       ├── 项目与金牌合并数据.xlsx
│       └── data/              # notebook 依赖的原始数据子目录
│           ├── data_dictionary.csv
│           ├── summerOly_athletes.csv
│           ├── summerOly_hosts.csv
│           ├── summerOly_medal_counts.csv
│           ├── summerOly_programs.csv
│           └── 历年项目数据整理.xlsx
├── 03_处理后数据/              # 中间产物与最终输出表
├── 04_模型分析文档/            # 各子模型的 Word 说明
├── 05_可视化/                 # 思维框图(.drawio)与结果图(.png/.jpg)
└── 06_论文/
    └── 上午五点.pdf            # 最终论文
```

## 03_处理后数据 索引

| 文件 | 说明 |
|---|---|
| `processed_athletes.csv` | 清洗后的运动员主表(含历届参赛记录) |
| `athlete_num_by_year_sex.csv` | 按年份/性别统计的运动员数 |
| `olympic_data.csv` | 奥运会基础数据汇总 |
| `data_total.csv` | 综合数据表 |
| `gold_medal_summary.csv` / `gold_medal_table.csv` | 金牌汇总/对照表 |
| `total_medal_summary.csv` / `total_medal_table.csv` | 总奖牌汇总/对照表 |
| `summary_medals.csv` / `total_and_gold_medals_by_year.csv` | 按年份汇总 |
| `medals_with_rate_rlk.csv` | 含率与排名的奖牌表 |
| `effective_ratio_prediction_by_year.csv` | 有效比率年度预测 |
| `prediction_diff.csv` | 预测差值 |
| `omega_results.csv` | Omega 模型结果 |
| `GBRswimming.xlsx` | 英国游泳项目专项数据 |
| `筛选运动员.xls` | 筛选后的运动员表 |
| `1.xlsx` / `1(1).xlsx` | 临时工作表(两个版本,内容不同) |

## 04_模型分析文档 索引

| 文件 | 说明 |
|---|---|
| `验证Y与xi存在线性关系.docx` | 验证因变量与解释变量的线性关系 |
| `验证教练效应存在.docx` | 教练效应存在性的统计检验 |
| `针对首次获奖国家的数据.docx` | 首次获奖国家的专项分析 |
| `预测模型的敏感性分析.docx` | 模型敏感性分析 |
| `优缺点.doc` | 模型优缺点讨论 |
| `sammary.docx` / `sammary(1).docx` | 摘要(两个版本,内容不同,待合并/取舍) |
| `todolist(1).docx` | 任务清单 |

## 05_可视化 索引

| 文件 | 说明 |
|---|---|
| `思维框图.drawio` | 整体建模思路框图(用 [draw.io](https://app.diagrams.net/) 打开) |
| `未命名绘图.drawio` | 备用框图 |
| `pearson.png` | Pearson 相关系数热力图 |
| `教练效应1.png` / `教练效应2.png` | 教练效应前后对比 |
| `Figure_1.png` | 模型输出图 |
| `hd.jpg` | 大图素材 |

## 备注

- `02_代码/C题第一问第一小问代码/` 内部结构未拆分,因 notebook 中有相对路径依赖
- `(1)` 后缀的文件经哈希比对**与原文件内容不同**,是不同版本,留待人工取舍
