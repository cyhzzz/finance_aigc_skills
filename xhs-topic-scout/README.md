# xhs-topic-scout

小红书财经选题调研工具

## 功能

为证券/基金/理财账号提供小红书选题参考，输出5-10个可执行的选题。

## 核心工作流

```
Phase 1: 热点采集（财联社 + 新浪财经 + 东方财富）
Phase 2: 选题发散（提取候选话题）
Phase 3: 小红书市场调研（CDP真实检索）
Phase 4: 选题分析（评估框架 + 避坑指南）
Phase 5: 输出选题报告
```

## 快速开始

1. 确保 CDP Proxy 运行中：
```bash
node ~/.claude/skills/web-access/scripts/cdp-proxy.mjs
```

2. 执行 Python 脚本抓取热点：
```bash
cd D:/project/skills/xhs-topic-scout/scripts
python fetch_hot_topics.py
```

3. 根据 SKILL.md 引导进行小红书调研

## 文件结构

```
xhs-topic-scout/
├── SKILL.md                    # 主技能文件
├── README.md                   # 说明文件
├── scripts/
│   └── fetch_hot_topics.py    # 热点抓取脚本
└── references/
    └── 选题方法论.md          # 选题方法论参考
```

## 输出

选题报告保存到：`./output/选题调研报告_{YYYYMMDD}.md`（相对路径）
