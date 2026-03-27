# Claude Skills Marketplace

## Marketplace Metadata

**Name**: Finance AIGC Skills
**Description**: 金融投顾与小红书营销专业工具集
**Version**: 1.0.0
**Author**: cyhzzz
**License**: MIT
**Repository**: https://github.com/cyhzzz/finance_aigc_skills

---

## Available Skills

### Finance & Investment

#### abundance-every-year

**Path**: `abundance-every-year/`
**Description**: A股收评自动生成工具，基于 akshare 数据分析，生成专业投顾评论文章
**Version**: 1.0.0
**Dependencies**: Python 3.7+, pandas>=1.3.0, akshare>=1.18.0
**Install**: `/plugin install abundance-every-year@claude-code-skills`

**Features**:
- 自动获取市场数据（上证、深证、创业板）
- 北向资金流向分析
- 板块表现统计
- 智能生成收评文章
- 完整合规风险提示

### Marketing & Content Creation

#### xiaohongshu-creator

**Path**: `xiaohongshu-creator/`
**Description**: 小红书图文笔记创作工作流，支持多账号风格，智能投资转向
**Version**: 1.0.0
**Dependencies**: baoyu-xhs-images (bundled), content-creation-framework (bundled)
**Install**: `/plugin install xiaohongshu-creator@claude-code-skills`

**Features**:
- 智能模式判断（创作/改写）
- 两阶段创作流程
- 6种 IP 风格配置
- 爆款潜力评分
- 双模式信息图生成
- 完整合规内容模板

**Bundled Sub-Skills**:
- `baoyu-xhs-images`: 10种视觉风格，8种布局方式
- `content-creation-framework`: 通用内容创作方法论

### Social Media Topic Research

#### xhs-topic-scout

**Path**: `xhs-topic-scout/`
**Description**: 小红书财经选题调研工具，5-phase工作流获取可执行选题
**Version**: 1.0.0
**Dependencies**: web-access skill (CDP浏览器操控)
**Install**: `/plugin install xhs-topic-scout@claude-code-skills`

**Features**:
- CDP真实采集财联社/新浪/东财热点
- 小红书市场调研获取真实竞争数据
- 动态关键词检索，非预设
- 双维度评分框架（新闻热度+小红书机会）
- 输出5-10个可执行选题

### Skill Factory (Meta-Skills)

#### xhs-writer-factory

**Path**: `xhs-writer-factory/`
**Description**: 小红书写作Skill工厂，从3-5篇满意文章训练专属写作Skill
**Version**: 1.0.0
**Dependencies**: Python 3.7+, markdown, akshare>=1.18.0, pandas>=1.3.0
**Install**: `/plugin install xhs-writer-factory@claude-code-skills`

**Features**:
- 8维深度提取分析法
- 风格画像自动生成
- 自测评循环确保质量
- 完整Skill输出

**Trigger**: "帮我建一个小红书写作skill" / "训练一个专属写作模板"

#### tougu-writer-factory

**Path**: `tougu-writer-factory/`
**Description**: 投顾写作Skill工厂，从3-5篇满意文章训练专属写作Skill
**Version**: 1.0.0
**Dependencies**: Python 3.7+, markdown, akshare>=1.18.0, pandas>=1.3.0
**Install**: `/plugin install tougu-writer-factory@claude-code-skills`

**Features**:
- 8维深度提取分析法
- 固化模块（市场数据+合规红线）
- 自测评循环确保质量
- 完整Skill输出

**Trigger**: "帮我建一个投顾写作skill" / "训练一个专属写市场评论的模板"

---

## Installation

### Install All Skills

```bash
# Add marketplace
/plugin marketplace add cyhzzz/finance_aigc_skills

# Install all skills
/plugin install all-skills@claude-code-skills
```

### Install Individual Skills

```bash
# 金融投顾工具
/plugin install abundance-every-year@claude-code-skills

# 小红书创作工具
/plugin install xiaohongshu-creator@claude-code-skills

# 小红书选题调研
/plugin install xhs-topic-scout@claude-code-skills

# 小红书写作工厂
/plugin install xhs-writer-factory@claude-code-skills

# 投顾写作工厂
/plugin install tougu-writer-factory@claude-code-skills
```

---

## Version Management

Skills use git tags for versioning:

| Version | Date | Changes |
|---------|------|---------|
| `v1.2.0` | 2026-03-27 | 新增 xhs-writer-factory 和 tougu-writer-factory |
| `v1.1.0` | 2026-03-23 | 新增 xhs-topic-scout 小红书财经选题调研工具 |
| `v1.0.0` | 2025-02-13 | Initial release |

Update all installed skills:
```bash
/plugin update
```

Update specific skill:
```bash
/plugin update abundance-every-year
```

---

## Quick Reference

| Skill | Command | Use Case |
|-------|---------|----------|
| **abundance-every-year** | 生成A股收评 | 每日市场评论 |
| **xiaohongshu-creator** | 创作小红书笔记 | 财经内容营销 |
| **xhs-topic-scout** | 小红书选题调研 | 获取可执行选题 |
| **xhs-writer-factory** | 训练写作Skill | 从样本学习风格 |
| **tougu-writer-factory** | 训练写作Skill | 投顾专属风格 |

---

## Development

### Adding New Skills

1. Create skill directory following the structure
2. Add `SKILL.md` with proper frontmatter
3. Update this `MARKETPLACE.md`
4. Create a new git tag

### Skill Structure Template

```
skill-name/
├── SKILL.md              # Required: Skill definition with YAML frontmatter
├── CLAUDE.md             # Required: Project instructions
├── README.md             # Optional: Skill documentation
├── references/           # Optional: Reference materials
└── scripts/              # Optional: Python/tool scripts
```

### SKILL.md Frontmatter Template

```yaml
---
name: skill-name
description: 简短描述（<50字符）
dependency: 依赖项说明
version: 1.0.0
author: cyhzzz
---
```

---

## Dependencies

### Python Dependencies

For `abundance-every-year`, `xhs-writer-factory`, `tougu-writer-factory`:
```bash
pip install pandas>=1.3.0 akshare>=1.18.0 markdown
```

### Sub-Skills

`xiaohongshu-creator` includes bundled sub-skills:
- `baoyu-xhs-images` - Visual content generation
- `content-creation-framework` - Writing methodology

No additional installation required.

---

## Support

- **Issues**: https://github.com/cyhzzz/finance_aigc_skills/issues
- **Discussions**: https://github.com/cyhzzz/finance_aigc_skills/discussions
- **Documentation**: See individual skill README files

---

## License

MIT License - See [LICENSE](LICENSE) file for details

---

**Last Updated**: 2026-03-27
**Skills Version**: 1.2.0
**Total Skills**: 5
