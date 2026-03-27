# Phase 5：自测评循环

> 本文档为 Phase 5 的详细操作指南

---

## 目标

确保生成的Skill真正符合案例标准。采用 **LLM驱动 + Python辅助** 的自测评模式。

---

## 核心机制

### MD评估指南（LLM执行）

LLM按照 `references/self_eval.md` 的评估检查表逐Phase执行。

### Python辅助工具

`scripts/self_eval.py` 负责：
1. 特征提取：从样本和生成文章中提取7维度特征
2. 结构对比：计算各维度的匹配度得分
3. 格式校验：调用skill-creator规范或内置校验

---

## 自测评流程

```
初始生成
    ↓
Step 1: 随机选题（自动选择测试主题，如"今日收评"）
    ↓
Step 2: Skill执行（调用生成的Skill生成测试文章）
    ↓
Step 3: 格式校验 ← LLM按 self_eval.md 检查
    ↓
Step 4: 7维对比分析 ← Python辅助
    ↓
Step 5: 差距识别（输出结构差异清单）
    ↓
    ├── 达标（≥80%）→ 结束循环
    │
    └── 未达标 → 修复优化 → 循环（最多3轮）
```

---

## 达标标准

| 指标 | 标准 | 处理 |
|:---|:---|:---|
| 整体匹配度 | ≥80% | 通过 |
| 单维度匹配度 | ≥60% | 可接受 |
| 任何维度 | <50% | 必须修复 |
| 循环次数 | 最多3轮 | 2轮未达标输出警告 |

---

## 7维对比权重

| 维度 | 权重 | 说明 |
|:---|:---:|:---|
| 标题格式 | 20% | 符号规范、字数、结构 |
| 段落结构 | 20% | 段落数量、功能定位 |
| 分析逻辑 | 20% | 框架、因果、转折 |
| 句式特征 | 15% | 条件句、概率表达 |
| 特色词汇 | 15% | 比喻词、谨慎词 |
| 固定表达 | 10% | 开头语、品牌呼号 |

---

## 自测评执行方式

### 自动执行（格式校验 + 文件完整性）

这部分由 Python 脚本自动执行：

```bash
# 格式校验 + 文件完整性检查（自动）
python scripts/self_eval.py \
  --skill-path {生成的Skill路径} \
  --validate-format-only
```

### 手动执行（内容质量 + 风格对比）

这部分需要用户提供生成的测试文章：

```bash
# 1. 使用生成的Skill生成测试文章（用户手动执行）
# 调用生成的skill，传入测试主题，生成文章

# 2. 7维度风格对比（Python辅助 + LLM判断）
python scripts/self_eval.py \
  --skill-path {生成的Skill路径} \
  --reference-samples {案例路径} \
  --compare-style-only \
  --generated-article {用户生成的测试文章} \
  --output style_report.json
```

### 完整流程

```bash
# 完整自测评
python scripts/self_eval.py \
  --skill-path {生成的Skill路径} \
  --reference-samples {案例路径} \
  --test-topic "今日收评" \
  --generated-article {文章内容或文件路径} \
  --output eval_report.json
```

> **注意**：完整自测评需要用户提供生成的测试文章，因为自测评的目的是验证Skill在真实场景下能否正常工作。

---

## skill-creator 集成

如果 `skill-creator` 已安装，自测评的格式校验阶段会：
1. 自动调用 `skill-creator` 的格式校验接口
2. 使用 skill-creator 规范进行 frontmatter 和章节结构检查
3. 如果未安装，则使用内置校验逻辑（等效）

### 格式校验项

- [ ] YAML frontmatter 存在且包含 name、description、dependency
- [ ] name 字段使用小写字母、数字、连字符
- [ ] name 字段以 `-writer` 或 `-skill` 结尾
- [ ] description 不超过200字符
- [ ] 包含"任务目标"、"操作步骤"、"注意事项"章节
- [ ] 文件结构符合 Skill 标准布局

---

## 输出报告格式

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

---

## 完成后的操作

自测评完成后，**必须自动触发一次skill安装检查**：

```
✅ 自测评完成！

📁 生成目录：output/{文章类型}-writer/

🔔 是否安装生成的skill？
   运行：/install-skill output/{文章类型}-writer/
   或说："安装这个skill"
```

---

## 下一步

安装检查完成后，整个流程结束。
