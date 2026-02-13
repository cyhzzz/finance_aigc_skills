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
```

---

## Version Management

Skills use git tags for versioning:

| Version | Date | Changes |
|---------|------|---------|
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

For `abundance-every-year`:
```bash
pip install pandas>=1.3.0 akshare>=1.18.0
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

**Last Updated**: 2025-02-13
**Skills Version**: 1.0.0
**Total Skills**: 2
