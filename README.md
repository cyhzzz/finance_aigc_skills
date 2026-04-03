# Finance AIGC Skills

金融与内容创作 AIGC 专业技能集，适用于 Claude Code / OpenClaw / WorkBuddy 等 AI Agent 工具。

## 🌟 核心技能

### 1. 爆款智坊 (viral-content-factory) ⭐ 主打技能
**多平台新媒体内容创作套件**

一句话创作，自动生成适配微信公众号 / 小红书 / 微博 / 知乎 / 头条 / 短视频脚本的多平台内容。

**两大入口**：
- **全新创作**：热点抓取 → 选题评分 → 框架选择 → 素材采集 → 初稿生成
- **拆解改写**：URL/粘贴 → 格式整理 → 内容梳理 → 框架梳理 → 改写

**核心功能**：
- 🎯 风格学习：录入你的文章，AI学习你的写作风格，越用越像你
- 📊 合规内嵌：个股检查、风险提示、表述规范自动处理
- 🎨 16+主题：professional-clean / minimal / newspaper / tech-modern / sspai / github / bauhaus 等
- 📱 多平台适配：自动改写成6大平台格式

**适用场景**：
- 每日市场解读 → 一键生成多平台版本
- 直播回放 → 自动转文稿，改写成多平台内容
- 转发同行好稿 → 快速改写成自己的风格

**依赖**：
- Python 3.7+
- markdown, bs4, requests, yaml

**触发词**：
- "写一篇公众号文章"
- "写小红书"
- "改写这篇文章"
- "整理直播文稿"
- "学习我的风格"

---

## 📦 其他技能

### 2. capital-market-topic-scout
**资本市场热点选题挖掘工具**

从资本市场热点中挖掘抖音/公众号/小红书爆款选题。

**功能**：
- 集成 NewsNow API 抓取实时财经热点
- 基于直男财经、半佛仙人等实战案例的黄金案例分析
- 二维评分体系（行业关注度 + 社会热度）
- 平台特定公式（抖音、小红书、公众号）
- 105个财经关键词自动过滤

---

### 3. hot-topics-selector
**财经热点选题工具**

从财经热点中智能筛选适合引导投资理财的优质选题。

**功能**：
- 实时抓取5个平台热点（133个标题）
- 智能筛选5个可关联投资的选题
- 抓取新闻详细内容
- 生成完整选题方案（概要、理由、引导策略）

---

### 4. abundance-every-year-market-notes
**年年有鱼投顾评论撰写技能**

基于真实交易数据生成 A 股收评文章。

**功能**：
- 自动获取市场数据（akshare）
- 智能分析市场表现
- 生成专业收评文章
- 包含合规风险提示

---

### 5. xiaohongshu-creation-workflow
**小红书图文笔记创作工作流**

专为财经证券领域设计的小红书笔记创作工具，支持"一切主题转向投资"的软性营销引流。

**功能**：
- 智能模式判断（创作/改写）
- 两阶段创作（内容创作 + 风格适配）
- 多账号风格支持（6种 IP 风格）
- 爆款潜力评分
- 双模式信息图生成（AI 手绘图 / HTML 预览）

---

### 6. xhs-topic-scout
**小红书财经选题调研工具**

通过5-phase工作流采集热点、分析小红书市场、输出可执行选题。

**功能**：
- CDP真实采集财联社/新浪/东财热点
- 小红书市场调研获取真实竞争数据
- 动态关键词检索，非预设
- 双维度评分框架
- 输出5-10个可执行选题

---

### 7. xhs-writer-factory
**小红书写作Skill工厂**

从小红书创作者提交的3-5篇满意文章中，使用8维深度提取分析法，训练出专属写作Skill。

---

### 8. tougu-writer-factory
**投顾写作Skill工厂**

从投顾提交的3-5篇满意文章中，使用8维深度提取分析法，训练出专属写作Skill。

---

## 🚀 快速开始

### 安装所有技能

```bash
npx skills add cyhzzz/finance_aigc_skills
```

### 安装单个技能

```bash
# 爆款智坊（推荐）
npx skills add cyhzzz/finance_aigc_skills/viral-content-factory

# 金融投顾工具
npx skills add cyhzzz/finance_aigc_skills/abundance-every-year

# 小红书创作工具
npx skills add cyhzzz/finance_aigc_skills/xiaohongshu-creator

# 小红书选题调研
npx skills add cyhzzz/finance_aigc_skills/xhs-topic-scout
```

### 更新技能

```bash
npx skills update cyhzzz/finance_aigc_skills
```

---

## 📖 使用指南

### 爆款智坊 使用示例

**全新创作**：
```
写一篇公众号文章，主题是最近AI Agent很火
```

**拆解改写**：
```
改写这篇文章：https://mp.weixin.qq.com/s/xxx
```

**学习风格**：
```
导入我的文章，学习我的写作风格
```

**整理直播文稿**：
```
整理这段直播文稿，改写成公众号和小红书
```

---

## 📋 版本历史

- **v2.0.0** (2026-04-04)
  - 🌟 新增爆款智坊 (wewrite-main) 作为主打技能
  - 支持多平台内容创作（微信/小红书/微博/知乎/头条/短视频）
  - 风格学习：AI越用越像你
  - 合规内嵌：投顾场景自动处理

- **v1.2.0** (2026-03-27)
  - 新增 xhs-writer-factory 小红书写作Skill工厂
  - 新增 tougu-writer-factory 投顾写作Skill工厂

- **v1.1.0** (2026-03-23)
  - 新增 xhs-topic-scout 小红书财经选题调研工具

- **v1.0.0** (2025-02-13)
  - 初始发布

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 联系方式

- **GitHub**: https://github.com/cyhzzz/finance_aigc_skills
- **Issues**: https://github.com/cyhzzz/finance_aigc_skills/issues

---

**Made with ❤️ for Finance & Content Creation**
