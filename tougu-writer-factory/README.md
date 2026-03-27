# 投顾写作Skill工厂

> 从3-5篇满意文章中训练专属投顾八股文写作Skill的完整元技能

---

## 📦 完整结构

```
tougu-writer-factory/
├── SKILL.md                              # 主Skill文件
├── AGENTS.md                             # 快速开始指南
├── README.md                             # 本文件
│
├── 固化模块/                              # 通用固化模块（直接复制）
│   ├── compliance.md                     # 合规红线
│   └── market_data.py                   # 市场数据获取脚本
│
├── assets/                               # 资产文件
│   ├── compliance.md                     # 合规红线源文件
│   ├── market_data.py                   # 市场数据获取源文件
│   └── html_template.html               # HTML海报模板
│
├── scripts/                              # 工具脚本
│   ├── self_eval.py                     # 自测评脚本
│   └── market_data.md                   # LLM数据获取驱动指南
│
└── references/                          # 参考模板
    ├── phase1.md ~ phase5.md            # 各Phase详细指南
    ├── step1.md ~ step4.md              # 操作步骤模板
    ├── self_eval.md                     # 自评估检查表
    ├── analysis_logic.md                 # 分析逻辑框架
    ├── style_profile.md                 # 风格画像模板
    └── format_guide.md                  # 格式指南
```

---

## 🚀 快速开始

### 触发方式

对助手说：
- "帮我建一个收评skill"
- "训练一个专属写作模板"
- "提取我的写作风格建个skill"

### 操作流程

1. **提交材料**：发送3-5篇满意的投顾文章
2. **自动执行**：
   - 8维深度提取
   - 风格画像整合
   - 组装专属Skill（含固化模块）
   - 自测评循环确保质量
3. **获得输出**：可直接使用的专属写作Skill

---

## ✨ 核心能力

| 能力 | 说明 |
|:---|:---|
| 8维提取 | 标题/段落/句式/词汇/分析逻辑/数据/固定表达/数据需求 |
| 固化模块 | 市场数据获取 + 合规红线（通用，不用提取） |
| 自测评循环 | LLM驱动+Python辅助，格式校验（skill-creator规范）+ 7维度对比 |
| 完整输出 | SKILL.md + 6个references + 固化模块 + 自测评指南 |
| skill-creator集成 | 生成Skill的格式校验依赖skill-creator规范 |

---

## 📊 自测评机制

```
初始生成
    ↓
随机选题测试
    ↓
7维对比分析
    ↓
差距识别
    ↓
修复优化
    ↓
循环直到达标（≥80%）或达3轮上限
```

---

## 📝 输出示例

生成的专属Skill输出到 `output/` 目录：

```
output/收评writer/
├── SKILL.md (详细版)
├── 固化模块/
│   ├── compliance.md         # 合规红线
│   └── market_data.py      # 市场数据脚本
├── scripts/
│   ├── fetch_market_data.py # 可执行脚本
│   └── market_data.md      # LLM数据获取指南
└── references/
    ├── 收评创作风格.md
    ├── 收评创作风格_微观特征.md
    ├── 收评html海报模板.html
    ├── 收评合规检查.md
    ├── step1.md ~ step4.md
    └── self_eval.md
```

**生成后**：自动提示是否安装生成的skill

---

## ⚙️ 技术要求

- Python 3
- markdown解析能力
- 文件系统操作
- skill-creator（可选，用于格式校验）

---

## 📌 注意事项

1. **文章质量决定Skill质量**——提交你最满意的版本
2. **同类型文章**——收评就都选收评，不要混搭
3. **固化模块是通用的**——市场数据和合规不需要提取
4. **自测评自动进行**——不需要人工介入

---

