# Installation Guide - Finance AIGC Skills

完整的安装指南，适用于 Claude Code 和其他 AI 代码工具。

---

## Table of Contents

- [Quick Start](#quick-start)
- [Claude Code Native Marketplace](#claude-code-native-marketplace-recommended)
- [Universal Installer](#universal-installer)
- [Manual Installation](#manual-installation)
- [Verification & Testing](#verification--testing)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

---

## Quick Start

**Choose your installation method:**

### For Claude Code Users (Recommended)

```bash
# Add marketplace
/plugin marketplace add cyhzzz/finance_aigc_skills

# Install all skills
/plugin install all-skills@claude-code-skills
```

### For All Other Agents (Cursor, VS Code, etc.)

```bash
npx ai-agent-skills install cyhzzz/finance_aigc_skills
```

---

## Claude Code Native Marketplace (Recommended)

**Best for Claude Code users** - 原生集成，自动更新。

### Step 1: Add the Marketplace

```bash
/plugin marketplace add cyhzzz/finance_aigc_skills
```

### Step 2: Install Skills

#### Install All Skills

```bash
/plugin install all-skills@claude-code-skills
```

#### Install Individual Skills

```bash
# 金融投顾工具
/plugin install abundance-every-year@claude-code-skills

# 小红书创作工具
/plugin install xiaohongshu-creator@claude-code-skills
```

### Step 3: Verify Installation

```bash
# List installed skills
/plugin list

# Test a skill
# Start a conversation and use the skill
```

### Update Skills

```bash
# Update all installed plugins
/plugin update

# Update specific plugin
/plugin update abundance-every-year
```

### Remove Skills

```bash
# Remove specific plugin
/plugin remove xiaohongshu-creator

# Remove marketplace
/plugin marketplace remove cyhzzz/finance_aigc_skills
```

**Benefits:**
- ✅ Native Claude Code integration
- ✅ Automatic updates with `/plugin update`
- ✅ Version management with git tags
- ✅ Managed through Claude Code UI

---

## Universal Installer

通用安装器使用 [ai-agent-skills](https://github.com/skillcreatorai/Ai-Agent-Skills) 包，支持多平台同时安装。

### Install All Skills

```bash
# Install to all supported agents
npx ai-agent-skills install cyhzzz/finance_aigc_skills
```

**This installs to:**
- Claude Code → `~/.claude/skills/`
- Cursor → `.cursor/skills/`
- VS Code/Copilot → `.github/skills/`
- And more...

### Install to Specific Agent

```bash
# Claude Code only
npx ai-agent-skills install cyhzzz/finance_aigc_skills --agent claude

# Cursor only
npx ai-agent-skills install cyhzzz/finance_aigc_skills --agent cursor

# VS Code/Copilot only
npx ai-agent-skills install cyhzzz/finance_aigc_skills --agent vscode
```

### Install Individual Skills

```bash
# abundance-every-year
npx ai-agent-skills install cyhzzz/finance_aigc_skills/abundance-every-year

# xiaohongshu-creator
npx ai-agent-skills install cyhzzz/finance_aigc_skills/xiaohongshu-creator
```

### Preview Before Installing

```bash
# Dry run to see what will be installed
npx ai-agent-skills install cyhzzz/finance_aigc_skills --dry-run
```

---

## Manual Installation

用于开发、定制或离线使用。

### Prerequisites

- **Git**
- **Claude Code** (for using skills)
- **Python 3.7+** (for abundance-every-year scripts)

### Step 1: Clone Repository

```bash
git clone https://github.com/cyhzzz/finance_aigc_skills.git
cd finance_aigc_skills
```

### Step 2: Copy to Agent Directory

#### For Claude Code

```bash
# Copy all skills
cp -r abundance-every-year ~/.claude/skills/
cp -r xiaohongshu-creator ~/.claude/skills/

# Or copy single skill
cp -r xiaohongshu-creator ~/.claude/skills/
```

#### For Cursor

```bash
# Copy to project directory
mkdir -p .cursor/skills
cp -r xiaohongshu-creator .cursor/skills/
```

#### For VS Code/Copilot

```bash
# Copy to project directory
mkdir -p .github/skills
cp -r abundance-every-year .github/skills/
```

### Step 3: Install Python Dependencies (abundance-every-year)

```bash
pip install pandas>=1.3.0 akshare>=1.18.0
```

---

## Verification & Testing

### Verify Installation

```bash
# Check Claude Code installation
ls ~/.claude/skills/

# You should see:
# - abundance-every-year/
# - xiaohongshu-creator/
```

### Test Skill Usage

#### Test abundance-every-year

In Claude Code:
```
请使用 abundance-every-year 技能，分析今天的 A 股市场表现
```

#### Test xiaohongshu-creator

In Claude Code:
```
请使用 xiaohongshu-creator 技能，为"指数基金定投"创作小红书笔记
```

### Test Python Tools (abundance-every-year)

```bash
# Test data fetching
python ~/.claude/skills/abundance-every-year/scripts/fetch_market_data.py

# Test analysis
python ~/.claude/skills/abundance-every-year/scripts/analysis_tool.py
```

---

## Troubleshooting

### Issue: "Command not found: npx"

**Solution:** Install Node.js and npm

```bash
# macOS
brew install node

# Ubuntu/Debian
sudo apt-get install nodejs npm

# Windows
# Download from https://nodejs.org/
```

### Issue: "Skills not showing in Claude Code"

**Solution:** Verify installation and restart

```bash
# Check installation
ls -la ~/.claude/skills/

# Verify SKILL.md exists
cat ~/.claude/skills/xiaohongshu-creator/SKILL.md

# Restart Claude Code
```

### Issue: "Python module not found"

**Solution:** Install dependencies

```bash
pip install pandas akshare
```

### Issue: "Marketplace not found"

**Solution:** Check repository URL

```bash
# Verify repository exists
curl https://github.com/cyhzzz/finance_aigc_skills

# Try removing and re-adding
/plugin marketplace remove cyhzzz/finance_aigc_skills
/plugin marketplace add cyhzzz/finance_aigc_skills
```

---

## Uninstallation

### Claude Code Native Marketplace

```bash
# Remove specific skill
/plugin remove xiaohongshu-creator

# Remove marketplace
/plugin marketplace remove cyhzzz/finance_aigc_skills
```

### Universal Installer

```bash
# Remove from Claude Code
rm -rf ~/.claude/skills/abundance-every-year/
rm -rf ~/.claude/skills/xiaohongshu-creator/

# Remove from Cursor
rm -rf .cursor/skills/abundance-every-year/
rm -rf .cursor/skills/xiaohongshu-creator/

# Remove from VS Code
rm -rf .github/skills/abundance-every-year/
rm -rf .github/skills/xiaohongshu-creator/
```

### Manual Installation

```bash
# Remove cloned directory
rm -rf finance_aigc_skills/

# Remove copied skills
rm -rf ~/.claude/skills/abundance-every-year/
rm -rf ~/.claude/skills/xiaohongshu-creator/
```

---

## Advanced: Installation Locations Reference

| Agent | Default Location | Flag | Notes |
|-------|------------------|------|-------|
| **Claude Code** | `~/.claude/skills/` | `--agent claude` | User-level installation |
| **Cursor** | `.cursor/skills/` | `--agent cursor` | Project-level installation |
| **VS Code/Copilot** | `.github/skills/` | `--agent vscode` | Project-level installation |
| **Project** | `.skills/` | `--agent project` | Portable, project-specific |

---

## Support

**Installation Issues?**
- Check [Troubleshooting](#troubleshooting) section above
- Review [ai-agent-skills documentation](https://github.com/skillcreatorai/Ai-Agent-Skills)
- Open issue: https://github.com/cyhzzz/finance_aigc_skills/issues

**Feature Requests:**
- Submit via GitHub Issues with `enhancement` label

---

**Last Updated:** 2025-02-13
**Skills Version:** 1.0.0
**Universal Installer:** [ai-agent-skills](https://github.com/skillcreatorai/Ai-Agent-Skills)
