# Finance AIGC Skills

金融与内容创作 AIGC 专业技能集，适用于 Claude Code。

## 📦 包含技能

### 1. abundance-every-year-market-notes
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

**安装**：
```bash
/plugin install abundance-every-year@claude-code-skills
```

---

### 2. xiaohongshu-creation-workflow
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

**安装**：
```bash
/plugin install xiaohongshu-creator@claude-code-skills
```

---

## 🚀 快速开始

### 方式 1：Claude Code 原生 Marketplace（推荐）

```bash
# 添加 Marketplace
/plugin marketplace add cyhzzz/finance_aigc_skills

# 安装所有技能
/plugin install all-skills@claude-code-skills

# 或安装单个技能
/plugin install abundance-every-year@claude-code-skills
/plugin install xiaohongshu-creator@claude-code-skills
```

### 方式 2：通用安装器（多平台支持）

```bash
# 安装所有技能
npx ai-agent-skills install cyhzzz/finance_aigc_skills

# 仅安装到 Claude Code
npx ai-agent-skills install cyhzzz/finance_aigc_skills --agent claude

# 安装单个技能
npx ai-agent-skills install cyhzzz/finance_aigc_skills/xiaohongshu-creator
```

---

## 📖 使用指南

### abundance-every-year 使用示例

```
请使用 abundance-every-year 技能生成今天的 A 股收评
```

### xiaohongshu-creator 使用示例

```
请使用 xiaohongshu-creator 为以下话题创作小红书笔记：
"如何选择合适的指数基金进行定投"
```

---

## 🔄 更新技能

```bash
# Claude Code 原生方式
/plugin update

# 通用安装器方式
npx ai-agent-skills update cyhzzz/finance_aigc_skills
```

---

## 🛠️ 开发

### 添加新技能

1. 在仓库中创建技能目录
2. 添加 `SKILL.md`（必需的 YAML frontmatter）
3. 更新 `MARKETPLACE.md`
4. 创建新的 git tag

### 本地测试

```bash
# 克隆仓库
git clone https://github.com/cyhzzz/finance_aigc_skills.git

# 复制到 skills 目录
cp -r finance_aigc_skills/xiaohongshu-creator ~/.claude/skills/
```

---

## 📋 版本历史

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
