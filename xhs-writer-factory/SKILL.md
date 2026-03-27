---
name: xhs-writer-factory
description: 小红书创作Skill工厂。接收用户1-5篇满意笔记，通过4步流程提取风格特征，训练出专属小红书创作Skill。触发：用户说"帮我建一个小红书创作skill"、"训练一个专属小红书风格"、"提取我的小红书风格"
---

# 小红书创作Skill工厂

> 从1-5篇满意笔记中提取风格特征，训练出专属小红书创作Skill的元技能
> 核心原则：所有分析工作由LLM驱动，不依赖代码执行

---

## 核心定位

本Skill是一个"工厂"——接收用户的1-5篇满意小红书笔记（图片+文案），通过4步流程输出一个专属创作Skill。

**成品形态**：
```
用户输入 → 选题模块 → 分析模块 → 撰写模块 → 绘画提示词模块
```

**输出目录**：`/tmp/output/{品牌名}-xhs/`

---

## 4步流程总览

```
Step 1: 内容提取（/tmp/extracted_notes/）
Step 2: 分析归纳（/tmp/analysis/）
Step 3: Skill组装（/tmp/output/{品牌名}-xhs/）
Step 4: 双维审核 + 输出确认
```

---

## Step 1: 内容提取

**任务**：对每篇笔记逐一提取全部内容要素，输出到 `/tmp/extracted_notes/` 目录

**详细执行手册**：见 `references/phase-guides.md#step-1`

**目录结构**：
```
/tmp/extracted_notes/
  note_1/
    - title.md
    - image_1_analysis.md
    - image_2_analysis.md
    - ...
    - copy_structure.md
    - image_prompts.md
  note_2/
  ...
```

**执行内容**：
1. 标题提取：结构类型、字数、悬念手法、核心要素
2. 图片7模块分析：每张图用途判断+文案倒推
3. 正文结构：段落功能、开头钩子、结尾CTA
4. 绘画提示词反推：每张图完整7模块提示词

> ✋ **确认点**：Step 1全部完成后，展示每篇笔记的提取结果摘要，请用户确认是否准确

---

## Step 2: 分析归纳

**输入**：`/tmp/extracted_notes/` 全部内容

**输出到 `/tmp/analysis/` 目录**：
```
/tmp/analysis/
  - style_guide.md        # 写作风格指南
  - topic_analysis.md     # 选题分析指南
  - image_style.md        # 绘画风格指南
```

**详细执行手册**：见 `references/phase-guides.md#step-2`

**执行内容**：
1. **写作风格归纳**（11维度）：品牌信息/标题风格/正文结构/**段落强制开头语**/比喻体系/语体特征/固定结尾/话题标签/禁止清单/图片偏好/封面尾页结构
2. **选题分析**：热点类型/切入角度/关键词库/公式模板
3. **绘画风格**：视觉类型/配色体系/构图规律/元素符号库/图片用途类型/数量组合规律

> ⚠️ **品牌名、品牌口号、固定结尾模板**是本步骤的**最高优先级提取项**

> ✋ **确认点**：Step 2全部完成后，展示三份归纳文档，重点确认"品牌信息"是否准确

---

## Step 3: Skill组装

**输入**：`/tmp/analysis/` 三份归纳文档 + Step 2提取的"品牌信息"

**输出目录**：`/tmp/output/{品牌名}-xhs/`

**详细执行手册**：见 `references/phase-guides.md#step-3`

**固定输出结构**：
```
/tmp/output/{品牌名}-xhs/
  ├── SKILL.md
  ├── references/
  │   ├── style_guide.md          # 写作风格指南（个性化提取）
  │   ├── topic_analysis.md        # 选题分析指南（个性化提取）
  │   ├── image_style.md           # 绘画风格指南（个性化提取）
  │   ├── 固化模块.md              # 合规红线（固化资源）
  │   ├── creativity_rules.md      # 爆款规律库（固化资源）
  │   └── image_styles.md          # 图片风格预设（固化资源）
  └── assets/
      └── prompt_templates.md      # 提示词模板
```

**执行内容**：
1. 生成SKILL.md主文件（品牌名最高优先级）
2. 生成references/下3个归纳文件
3. 生成assets/prompt_templates.md
4. **固化资源复制**（必须执行）：
   - `D:/project/skills/xhs-writer-factory/references/compliance.md` → 合规红线
   - `D:/project/skills/xhs-writer-factory/references/creativity_rules.md` → 爆款规律库
   - `D:/project/skills/xhs-writer-factory/references/image_styles.md` → 图片风格预设
5. 图片风格预设选择（用户提供图片→风格提取锚定；无图片→6选1）

> ✋ **确认点**：Step 3完成后，列出生成的文件结构，请用户确认是否满意

---

## Step 4: 双维审核 + 输出确认

**任务**：审核成品Skill的质量

**详细执行手册**：见 `references/phase-guides.md#step-4`

### 4.1 文件结构完整性检查

| 文件 | 最低行数 | 必须存在 |
|:---|:---:|:---:|
| SKILL.md | 200行 | 必须 |
| references/style_guide.md | 100行 | 必须 |
| references/topic_analysis.md | 50行 | 必须 |
| references/image_style.md | 50行 | 必须 |
| assets/prompt_templates.md | 30行 | 必须 |

**品牌名一致性检查**：SKILL.md的name字段 + 所有文件中品牌名是否一致

### 4.2 格式评审

- [ ] SKILL.md存在frontmatter（name + description）
- [ ] 流程清晰（用户输入→各Phase→输出）
- [ ] 无未替换占位符（所有{}变量均有实际内容）
- [ ] references目录被引用（在正文中）
- [ ] 段落强制开头语被写入写作模块
- [ ] 比喻体系被写入写作模块
- [ ] 禁止清单被写入写作模块

### 4.3 内容测试

1. 从原始输入案例中随机选1篇
2. 倒推该案例的选题主题
3. 用该主题调用成品Skill生成
4. 对比输出与原始案例（品牌名/完整性/标题风格/正文结构/段落开头语/比喻体系/画风一致性）

**通过标准**：≥80%，最多3轮循环

### 4.4 输出确认

1. 询问用户成品Skill输出目录（默认：`/tmp/output/{品牌名}-xhs/`）
2. 检查目标目录是否已存在同名Skill → 询问覆盖或重命名
3. 完成最终交付

> ✋ **最终确认点**：双维审核通过后，确认输出目录和安装方式，完成交付。

---

## 版本历史

| 版本 | 日期 | 优化内容 |
|:---|:---|:---|
| v1.0 | - | 初始版本 |
| v9.0 | 2026-03-26 | 确立4步流程 |
| v10.0 | 2026-03-26 | 新增8维提取、固化资源复制、文件结构检查、输出目录确认 |
| v11.0 | 2026-03-27 | 重构三层加载架构，SKILL.md压缩至~300行，删除冗余文件 |
