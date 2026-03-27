# 小红书创作Skill工厂 - 快速开始

## 触发语

对我说：
- "帮我建一个小红书创作skill"
- "训练一个专属小红书风格"
- "提取我的小红书风格"

## 输入要求

3-5篇你满意的小红书笔记，每篇包含：
- **图片**：封面图 + 内页图（越多越全越好）
- **文案**：完整的正文文字（标题+正文+话题标签）

## 流程概览

```
Step 1: 内容提取 → Step 2: 分析归纳 → Step 3: Skill组装 → Step 4: 双维审核
```

## 输出

一个以你账号名命名的专属Skill目录，直接可用于创作新笔记。

## 核心原则

- 笔记质量决定Skill质量
- 同风格笔记效果更好
- 图片+文案越完整，提取越准确
- 有爆款数据更佳

## 文件结构

```
xhs-writer-factory/
├── SKILL.md                    # 主流程文件（详细执行见references/phase-guides.md）
├── README.md                   # 本文件
├── assets/
│   └── prompt_templates.md     # 提示词模板（固化资源）
└── references/
    ├── phase-guides.md        # 详细执行手册
    ├── compliance.md           # 合规红线（固化资源）
    ├── creativity_rules.md    # 爆款规律库（固化资源）
    └── image_styles.md        # 6种图片风格预设（固化资源）
```
