# Finance AIGC Skills

金融与内容创作 AIGC 专业技能集，适用于 Claude Code。

## 📦 包含技能

### 1. capital-market-topic-scout
**资本市场热点选题挖掘工具**

从资本市场热点中挖掘抖音/公众号/小红书爆款选题。

**功能**：
- 集成 NewsNow API 抓取实时财经热点
- 基于直男财经、半佛仙人等实战案例的黄金案例分析
- 二维评分体系（行业关注度 + 社会热度）
- 平台特定公式（抖音、小红书、公众号）
- 105个财经关键词自动过滤

**特点**：
- 聚焦投资关联性和传播潜力
- 基于"从实践中学习"的方法论
- 输出可执行的话题方案

**依赖**：
- Python 3.7+
- requests >= 2.22.0
- NewsNow API

---

### 2. hot-topics-selector
**财经热点选题工具**

从财经热点中智能筛选适合引导投资理财的优质选题。

**功能**：
- 实时抓取5个平台热点（133个标题）
- 智能筛选5个可关联投资的选题
- 抓取新闻详细内容
- 生成完整选题方案（概要、理由、引导策略）

**特点**：
- 聚焦投资关联性（证券开户/基金投资）
- Python 数据抓取 + Agent 智能筛选
- 固定输出5个高质量选题
- 每个选题都有明确的引导策略

**依赖**：
- Python 3.7+
- requests >= 2.22.0
- pytz >= 2021.1

---

### 3. abundance-every-year-market-notes
**年年有鱼投顾评论撰写技能**

基于真实交易数据生成 A 股收评文章。

**功能**：
- 自动获取市场数据（akshare）
- 智能分析市场表现
- 生成专业收评文章
- 包含合规风险提示

**依赖**：
- Python 3.7+
- pandas >= 1.3.0
- akshare >= 1.18.0

---

### 4. xiaohongshu-creation-workflow
**小红书图文笔记创作工作流**

专为财经证券领域设计的小红书笔记创作工具，支持"一切主题转向投资"的软性营销引流。

**功能**：
- 智能模式判断（创作/改写）
- 两阶段创作（内容创作 + 风格适配）
- 多账号风格支持（6种 IP 风格）
- 爆款潜力评分
- 双模式信息图生成（AI 手绘图 / HTML 预览）

**内置子技能**：
- baoyu-xhs-images（小红书图文生成器）
- content-creation-framework（内容创作框架）

---

## 🚀 快速开始

### 安装所有技能

```bash
npx skills add cyhzzz/finance_aigc_skills
```

### 安装单个技能

```bash
# 金融投顾工具
npx skills add cyhzzz/finance_aigc_skills/abundance-every-year

# 小红书创作工具
npx skills add cyhzzz/finance_aigc_skills/xiaohongshu-creator
```

### 更新技能

```bash
npx skills update cyhzzz/finance_aigc_skills
```

---

## 📖 使用指南

### capital-market-topic-scout 使用示例

```
请使用 capital-market-topic-scout 技能挖掘适合短视频创作的资本市场热点选题
```

**工作流**：
1. 抓取 NewsNow 财经热点
2. 二维评分筛选（行业关注度 + 社会热度）
3. 输出可执行的话题方案

---

### hot-topics-selector 使用示例

```
请使用 hot-topics-selector 技能筛选适合引导开户的财经热点选题
```

**工作流**：
1. 抓取133个新闻标题
2. 筛选出5个可关联投资的选题
3. 抓取5篇新闻详细内容
4. 生成5个完整选题方案

---

### abundance-every-year 使用示例

```
请使用 abundance-every-year 技能生成今天的 A 股收评
```

---

### xiaohongshu-creator 使用示例

```
请使用 xiaohongshu-creator 为以下话题创作小红书笔记：
"如何选择合适的指数基金进行定投"
```

---

## 📋 版本历史

- **v1.2.0** (2026-02-24)
  - 新增 capital-market-topic-scout 资本市场热点选题挖掘工具
  - 集成 NewsNow API 实时财经热点抓取
  - 二维评分体系（行业关注度 + 社会热度）

- **v1.1.0** (2026-02-13)
  - 新增 hot-topics-selector 财经热点选题工具
  - 重构为 Python 数据 + Agent 智能的混合架构
  - 提示词迁移到 Markdown，更易维护
  - 新增内容抓取功能

- **v1.0.0** (2025-02-13)
  - 初始发布
  - 包含 abundance-every-year 和 xiaohongshu-creator

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

## 🔗 相关资源

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Claude Skills 社区](https://github.com/anthropics/skills)
- [akshare 文档](https://akshare.akfamily.xyz/)

---

**Made with ❤️ for Finance & Content Creation**
