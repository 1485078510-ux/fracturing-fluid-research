# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

个人学术研究工作区，包含两个子项目：

### 1. 荧光压裂液（硕士开题报告）
- 论文题目：用于压裂裂缝监测的荧光压裂液体系构建与性能研究
- 学校：成都理工大学，能源学院，石油与天然气工程专业
- 导师：李娜
- 核心内容：稀土铝酸盐荧光粉表面改性 + 胍胶压裂液体系构建 + 裂缝壁面吸附机制
- 遵循标准：SY/T 6376-2008《压裂液通用技术条件》、SY/T 5107-2016《水基压裂液性能评价方法》

### 2. 四氧化三铁环氧树脂拟合
- 示踪剂溶质运移模型拟合
- 分段光滑过渡模型（tanh blending）：
  - 上升相：ADE脉冲解（高斯分量）
  - 下降相：erfc(-z)拖尾（不动水/传质限制）
- 拟合算法：`scipy.optimize.differential_evolution` + `minimize`（L-BFGS-B精修）
- Python 3，依赖：numpy, scipy, matplotlib
- 输出中文图表需设置字体：`Microsoft YaHei` 或 `SimHei`

## 常用操作

- 读取 .doc 文件：使用 PowerShell Word COM 自动化：
  ```powershell
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $doc = $word.Documents.Open("path/to/file.doc")
  $text = $doc.Content.Text
  $doc.Close(); $word.Quit()
  ```
- 运行拟合脚本：`python "c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\fit_solute.py"`
- 运行物理解释脚本：`python "c:\Users\郝\Desktop\claude\四氧化三铁环氧树脂拟合\physical_analysis.py"`

## 文献要求

所有参考文献必须为真实可查的文献。本工作区涉及的核心文献领域：
- 水力压裂裂缝监测（Maxwell 2014, Molenaar 2012, Jin & Roy 2017）
- 荧光示踪技术（Takeuchi/Ishida 2025, Guryanov 2019）
- 稀土铝酸盐荧光粉（Matsuzawa 1996, Van den Eeckhout 2010）
- 压裂液标准（SY/T 6376-2008, SY/T 5107-2016）