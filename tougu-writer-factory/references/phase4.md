# Phase 4：Skill组装

> 本文档为 Phase 4 的详细操作指南

---

## 目标

将风格画像和固化模块组装成完整的、可直接使用的写作Skill。

---

## 组装流程

### Step 1：创建输出目录

```python
import os
from pathlib import Path

# 跨平台兼容的输出目录（使用相对路径）
OUTPUT_BASE = Path("output")  # 不用 /output/，兼容Windows/Mac/Linux
output_dir = OUTPUT_BASE / f"{文章类型}-writer"
output_dir.mkdir(parents=True, exist_ok=True)
```

### Step 2：生成SKILL.md

**必须包含的内容**：

```markdown
---
name: {风格名}-writer
description: 基于{风格名}风格撰写{文章类型}，包含{核心能力描述}
dependency:
  python:
    - akshare>=1.18.0
    - pandas>=1.3.0
---

# {风格名}{文章类型}撰写

## 任务目标
- 本Skill用于：{具体描述}
- 能力包含：{列出核心能力}
- 触发条件：{具体触发场景}

## 前置准备
- 依赖说明：akshare>=1.18.0, pandas>=1.3.0, requests>=2.22.0

## 操作步骤

### 标准流程

1. **获取市场数据**
   - 调用 scripts/fetch_market_data.py 获取指定日期的A股市场数据
   - 支持默认获取上一个交易日数据

2. **撰写{文章类型}（初稿）**
   - 严格遵循"{风格名}"创作风格
   - 必须包含完整的标题格式
   - 采用{段落数量}段式结构
   - 数据使用要求：精确数值、数据对比、来源标注

3. **文案润色**
   - 严格按照微观特征.md进行润色
   - 句式特征检查、核心词汇检查、标志性表达检查

4. **合规检查**
   - 调用合规检查.md进行合规检查

5. **输出终稿**
   - 保存为Markdown格式
   - 可选：使用HTML模板渲染可视化输出

## 注意事项
- 标题格式：{具体格式要求}
- 固定表达：{从样本提取的开头语、结尾格式}
- 概率性表达：使用{谨慎词列表}
```

### Step 3：复制固化模块

固化模块是通用模块，直接复制即可：

| 源文件 | 目标文件 |
|:---|:---|
| 固化模块/compliance.md | output/{类型}-writer/固化模块/compliance.md |
| 固化模块/market_data.py | output/{类型}-writer/固化模块/market_data.py |
| 固化模块/market_data.py | output/{类型}-writer/scripts/fetch_market_data.py |

### Step 4：复制风格文档

| 源文件 | 目标文件 |
|:---|:---|
| {风格名}创作风格.md | output/{类型}-writer/references/{风格名}创作风格.md |
| {风格名}创作风格_微观特征.md | output/{类型}-writer/references/{风格名}创作风格_微观特征.md |

### Step 5：生成step文件

复制step模板到目标skill的references/目录：

```
references/
├── step1.md  →  output/{类型}-writer/references/step1.md
├── step2.md  →  output/{类型}-writer/references/step2.md
├── step3.md  →  output/{类型}-writer/references/step3.md
├── step4.md  →  output/{类型}-writer/references/step4.md
└── self_eval.md →  output/{类型}-writer/references/self_eval.md
```

### Step 6：生成HTML模板

从 `assets/html_template.html` 复制并定制化：

```
assets/html_template.html → output/{类型}-writer/references/{风格名}html海报模板.html
```

### Step 7：生成合规检查

从 `固化模块/compliance.md` 定制化：

```
固化模块/compliance.md → output/{类型}-writer/references/{风格名}合规检查.md
```

---

## 最终输出结构

```
output/{文章类型}-writer/
├── SKILL.md                      # 可直接使用的写作Skill
├── 固化模块/
│   ├── compliance.md             # 合规红线
│   └── market_data.py           # 市场数据脚本
├── scripts/
│   ├── fetch_market_data.py     # 可执行脚本
│   └── market_data.md           # LLM数据获取驱动指南
└── references/
    ├── {风格名}创作风格.md
    ├── {风格名}创作风格_微观特征.md
    ├── {风格名}html海报模板.html
    ├── {风格名}合规检查.md
    ├── step1.md
    ├── step2.md
    ├── step3.md
    ├── step4.md
    └── self_eval.md
```

---

## 完整性检查

组装完成后，验证以下文件是否存在：

- [ ] SKILL.md
- [ ] 固化模块/compliance.md
- [ ] 固化模块/market_data.py
- [ ] scripts/fetch_market_data.py
- [ ] scripts/market_data.md
- [ ] references/step1.md
- [ ] references/step2.md
- [ ] references/step3.md
- [ ] references/step4.md
- [ ] references/self_eval.md
- [ ] references/{风格名}创作风格.md
- [ ] references/{风格名}创作风格_微观特征.md
- [ ] references/{风格名}html海报模板.html
- [ ] references/{风格名}合规检查.md

---

## 下一步

组装完成后，自动进入 [Phase 5：自测评循环](./phase5.md)
