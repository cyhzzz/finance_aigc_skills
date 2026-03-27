# 投顾写作Skill自评估指南

> 本文档为投顾写作Skill工厂的自评估检查表
> 由LLM驱动执行，用于验证生成的Skill是否符合质量标准

---

## 评估流程总览

```
Phase 1: 格式校验（skill-creator规范）
    ↓
Phase 2: 文件完整性检查
    ↓
Phase 3: 内容质量检查
    ↓
Phase 4: 7维度风格对比（≥80%通过）
    ↓
Phase 5: 综合判定与修复建议
    ↓
Phase 6: Skill安装检查（输出到output/ + 触发安装提示）
```

---

## Phase 1：格式校验（skill-creator规范）

> 使用 skill-creator 的格式标准检查生成的Skill

### 1.1 YAML Frontmatter 检查

验证 `SKILL.md` 开头是否包含正确的YAML frontmatter：

```markdown
---
name: {风格名}-writer
description: 基于{风格名}风格撰写{文章类型}...
dependency:
  python:
    - akshare>=1.18.0
    - pandas>=1.3.0
---
```

**检查项**：
- [ ] SKILL.md 以 `---` 开头
- [ ] frontmatter 包含 `name` 字段（小写字母、数字、连字符）
- [ ] frontmatter 包含 `description` 字段（不超过200字符）
- [ ] frontmatter 包含 `dependency` 字段（python依赖）
- [ ] name 字段以 `-writer` 或 `-skill` 结尾

### 1.2 章节结构检查

**检查项**：
- [ ] 包含"任务目标"或"## 任务目标"章节
- [ ] 包含"操作步骤"或"## 操作步骤"章节
- [ ] 包含"注意事项"或"## 注意事项"章节
- [ ] 包含质量检查清单

### 1.3 文件结构检查

**检查项**：
- [ ] `SKILL.md` 存在
- [ ] `scripts/` 目录存在
- [ ] `references/` 目录存在
- [ ] `scripts/fetch_market_data.py` 存在
- [ ] `references/step1.md` 存在
- [ ] `references/step2.md` 存在
- [ ] `references/step3.md` 存在
- [ ] `references/step4.md` 存在

---

## Phase 2：文件完整性检查

> 逐个检查每个文件的内容是否完整

### 2.1 SKILL.md 内容检查

**检查项**：
- [ ] frontmatter 完整（name, description, dependency）
- [ ] "任务目标"章节有明确描述
- [ ] "操作步骤"章节包含完整流程（Phase1→Phase4）
- [ ] "注意事项"章节有实质内容
- [ ] 质量检查清单完整

### 2.2 {风格名}创作风格.md 内容检查

**检查项**：
- [ ] 风格核心定义（500字以上）
- [ ] 标题格式说明（含示例）
- [ ] 6段式结构说明（含每段功能定位）
- [ ] 数据使用原则
- [ ] 每个段落类型的写作示例（100-200字，直接来自样本）
- [ ] 至少2个完整案例片段（包含亮点分析和片段参考）
- [ ] 常用表达方式（格局描述、概率性表达、动态描述）
- [ ] 行文节奏与篇幅控制说明
- [ ] 语言风格要求
- [ ] 思维模式说明
- [ ] 常见模仿误区（至少5个）
- [ ] 质量检查清单

### 2.3 {风格名}创作风格_微观特征.md 内容检查

**检查项**：
- [ ] 句式特征说明
- [ ] 条件判断句式示例（至少3个）
- [ ] 概率性表达句式示例（至少3个）
- [ ] 高频专业术语表（至少10个）
- [ ] 谨慎词使用表
- [ ] 特色比喻词表及含义（至少5个）
- [ ] 排比句式示例
- [ ] 转折句式示例
- [ ] 数据引导句式示例
- [ ] 润色检查清单（句式、词汇、标志性表达、情感语气）
- [ ] 正式度评估

### 2.4 step1-4.md 内容检查

**每个step文件检查项**：
- [ ] 包含章节标题（##）
- [ ] 目标说明清晰
- [ ] 具体操作步骤完整
- [ ] 输出格式说明
- [ ] 下一步预告

### 2.5 合规检查.md 内容检查

**检查项**：
- [ ] 禁止表达清单（市场预测类）
- [ ] 禁止表达清单（操作承诺类）
- [ ] 谨慎表达规则
- [ ] 风险提示格式
- [ ] 数据来源标注规范
- [ ] 合规检查清单

---

## Phase 3：内容质量检查

> 基于原始样本，检查生成Skill的内容质量

### 3.1 风格一致性检查

**对比原始样本**：
- [ ] 标题格式与样本一致
- [ ] 段落数量与样本一致
- [ ] 固定开头语全部提取
- [ ] 特色词汇全部纳入
- [ ] 分析逻辑框架正确

### 3.2 自洽性检查

- [ ] SKILL.md 中的格式要求与 创作风格.md 一致
- [ ] 微观特征.md 的检查项与 SKILL.md 的润色步骤一致
- [ ] step1-4 的流程与 SKILL.md 的操作步骤一致

---

## Phase 4：7维度风格对比

> 使用Python辅助工具提取特征，对比生成质量

### 4.1 运行特征提取

```bash
cd {生成的Skill路径}
python scripts/self_eval.py --extract-features --samples {样本路径}
```

### 4.2 维度评分

| 维度 | 权重 | 通过标准 | 得分 |
|:---|:---:|:---|:---:|
| 标题格式 | 20% | 格式完全一致 | /20 |
| 段落结构 | 20% | 数量和功能一致 | /20 |
| 分析逻辑 | 20% | 框架完整 | /20 |
| 句式特征 | 15% | 条件句/概率表达足够 | /15 |
| 特色词汇 | 15% | 比喻词/谨慎词齐全 | /15 |
| 固定表达 | 10% | 开头语/结尾格式一致 | /10 |

**整体匹配度 = Σ(各维度得分) / 100**

### 4.3 通过标准

- **整体匹配度 ≥ 80%** → 通过
- **单维度匹配度 ≥ 60%** → 可接受
- **任何维度 < 50%** → 必须修复
- **最大3轮循环**，2轮未达标输出警告

---

## Phase 5：综合判定与修复建议

### 5.1 格式校验结果

- [ ] 通过 → ✅ 格式正确
- [ ] 未通过 → ❌ 列出具体问题

### 5.2 文件完整性结果

- [ ] 通过 → ✅ 所有文件完整
- [ ] 未通过 → ❌ 列出缺失文件

### 5.3 内容质量结果

- [ ] 通过 → ✅ 内容质量达标
- [ ] 未通过 → ❌ 列出具体问题

### 5.4 风格对比结果

| 维度 | 得分 | 状态 |
|:---|:---:|:---:|
| 标题格式 | /20 | ✅/⚠️/❌ |
| 段落结构 | /20 | ✅/⚠️/❌ |
| 分析逻辑 | /20 | ✅/⚠️/❌ |
| 句式特征 | /15 | ✅/⚠️/❌ |
| 特色词汇 | /15 | ✅/⚠️/❌ |
| 固定表达 | /10 | ✅/⚠️/❌ |
| **整体** | **/100** | **✅/❌** |

### 5.5 最终判定

**综合结果**：
- ✅ **全部通过** → Skill可交付
- ⚠️ **部分通过** → 需要修复后重新评估
- ❌ **未通过** → 需要重大修改

### 5.6 修复建议

针对每个❌/⚠️项，给出具体修复建议：

```
【问题1】描述
修复建议：具体操作步骤

【问题2】描述
修复建议：具体操作步骤
```

---

## Phase 6：Skill安装检查

> 评估通过后，必须执行此步骤

### 6.1 确认输出目录

确认生成的Skill已输出到指定目录：

```
output/{文章类型}-writer/
```

### 6.2 触发安装检查

评估通过后，自动提示用户是否安装：

```
✅ Skill评估通过，已生成到 `output/{文章类型}-writer/`

🔔 是否安装生成的skill？
   运行：/install-skill output/{文章类型}-writer/
   或说："安装这个skill"
```

### 6.3 安装后验证

Skill安装后，验证：
- [ ] Skill可被 Skill 工具识别
- [ ] 执行一次试运行验证可用性

---

## 评估执行命令

### 完整评估

```bash
python scripts/self_eval.py \
    --skill-path {生成的Skill路径} \
    --reference-samples {样本路径} \
    --test-topic "今日收评" \
    --output eval_report.json
```

### 仅格式校验

```bash
python scripts/self_eval.py \
    --skill-path {生成的Skill路径} \
    --validate-format-only
```

### 仅风格对比

```bash
python scripts/self_eval.py \
    --skill-path {生成的Skill路径} \
    --reference-samples {样本路径} \
    --compare-style-only
```

---

## 输出报告格式

评估完成后，生成报告：

```json
{
  "timestamp": "ISO时间戳",
  "skill_path": "Skill路径",
  "overall_pass": true/false,
  "phases": {
    "format_validation": {
      "passed": true/false,
      "issues": []
    },
    "file_completeness": {
      "passed": true/false,
      "missing_files": []
    },
    "content_quality": {
      "passed": true/false,
      "issues": []
    },
    "style_comparison": {
      "passed": true/false,
      "overall_score": 0.85,
      "dimension_scores": {}
    }
  },
  "final_verdict": "PASS/NEED_FIX/FAIL",
  "recommendations": []
}
```
