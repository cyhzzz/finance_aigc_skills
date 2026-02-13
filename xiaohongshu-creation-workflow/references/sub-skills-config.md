# 子Skill路径配置

本文档用于配置三个子skill的路径。工作流会优先通过**skill名称**自动调用，如果需要自定义路径，请按以下说明配置。

---

## 配置方式

### 方式1：自动查找（推荐）

工作流会自动通过skill名称查找已安装的skill。确保以下四个skill已安装在您的Claude Code skills目录中：

1. `content-creation-framework`
2. `xiaohongshu-finance-writer`
3. `baoyu-xhs-images`
4. `xiaohongshu-viral-analyzer`（爆款分析器）

**Skills目录位置**：
- Windows: `C:\Users\<用户名>\.claude\skills\`
- macOS/Linux: `~/.claude/skills/`

---

### 方式2：自定义路径（可选）

如果skill未安装在标准位置，或者需要使用特定版本，可以在本文件中配置自定义路径。

#### 配置格式

在下方"路径配置"部分，将默认的 `{auto-detect}` 替换为实际的绝对路径。

---

## 路径配置

### 1. content-creation-framework（内容创作框架）

**Skill名称**：`content-creation-framework`

**默认行为**：`{auto-detect}` - 自动查找skills目录

**自定义路径**（可选）：
```yaml
path: <在此处填写实际路径，例如：/path/to/skill/SKILL.md>
```

**集成位置**（本skill包内）：
- 目录：`skills/content-creation-framework/`
- 文件：`SKILL-257f83c5c0.md`

---

### 2. xiaohongshu-finance-writer（小红书财经笔记）

**Skill名称**：`xiaohongshu-finance-writer`

**默认行为**：`{auto-detect}` - 自动查找skills目录

**自定义路径**（可选）：
```yaml
path: <在此处填写实际路径，例如：/path/to/skill/SKILL.md>
```

**集成位置**（本skill包内）：
- 目录：`skills/xiaohongshu-finance-writer/`
- 文件：`SKILL.md`

**原始位置参考**：
- 目录：`xiaohongshu-finance-writer`
- 文件：`SKILL.md`

---

### 3. baoyu-xhs-images（小红书图文生成器）

**Skill名称**：`baoyu-xhs-images`

**默认行为**：`{auto-detect}` - 优先使用本地集成版本

**自定义路径**（可选）：
```yaml
path: <在此处填写实际路径，例如：/path/to/skill/SKILL.md>
```

**集成位置**（本skill包内）：
- 目录：`skills/baoyu-xhs-images/`
- 文件：`SKILL.md`

**全局位置**（备用）：
- Windows: `C:\Users\<用户名>\.claude\skills\baoyu-xhs-images\`
- macOS/Linux: `~/.claude/skills/baoyu-xhs-images/`

**功能**：生成小红书图文系列，支持10种视觉风格和8种布局方式

---

### 4. xiaohongshu-viral-analyzer（小红书爆款分析器）

**Skill名称**：`xiaohongshu-viral-analyzer`

**默认行为**：`{auto-detect}` - 自动查找skills目录

**自定义路径**（可选）：
```yaml
path: <在此处填写实际路径，例如：/path/to/skill/SKILL.md>
```

**集成位置**（本skill包内）：
- 目录：`skills/xiaohongshu-viral-analyzer/`
- 文件：`SKILL.md`

**功能**：基于流量黑客视角评估笔记爆款潜力。从四维结构（极致对标/情绪放大/算法迎合/工业结构）分析内容质量，提供评分（0-100分）和优化建议（≤100字）

**调用时机**：Phase 2完成后，Phase 3开始前

**原始位置参考**：
- 目录：`仿写-罗网灯下黑\小红书笔记\`
- 文件：`小红书爆款解析提示词.txt`

---

## 使用说明

### 如何激活自定义路径

1. 打开本文件：`references/sub-skills-config.md`
2. 找到需要配置的skill
3. 将 `{auto-detect}` 替换为实际的绝对路径
4. 保存文件

示例：
```yaml
# 修改前
path: {auto-detect}

# 修改后
path: /your-custom-path/skill/SKILL.md
```

### 路径格式要求

- **Windows**：使用反斜杠或正斜杠均可
  - ✅ 使用绝对路径或相对路径
  - 推荐使用相对于skill根目录的路径

- **macOS/Linux**：使用正斜杠
  - ✅ 使用绝对路径或相对路径
  - 推荐使用相对于skill根目录的路径

---

## 验证配置

配置完成后，可以通过以下方式验证：

1. **检查skill是否可访问**：确保路径指向的文件存在
2. **测试工作流**：运行一个小红书笔记创作任务
3. **查看错误信息**：如果skill无法访问，工作流会显示错误提示

---

## 常见问题

### Q1: 我应该使用哪种配置方式？

**A**：
- 如果skill已安装在标准skills目录：使用**方式1（自动查找）**
- 如果skill在其他位置或需要特定版本：使用**方式2（自定义路径）**

### Q2: 如何找到skill的路径？

**A**：使用以下方法之一：
- 在文件管理器中搜索skill的SKILL.md文件
- 使用命令行搜索：
  - Windows: `dir /s /b SKILL.md`
  - macOS/Linux: `find ~ -name "SKILL.md"`

### Q3: 配置后不生效怎么办？

**A**：检查以下几点：
- 路径是否正确（文件是否存在）
- 路径格式是否符合要求
- 是否保存了配置文件
- 尝试重启Claude Code

### Q4: 可以混合使用两种方式吗？

**A**：可以。部分skill使用自动查找，部分skill使用自定义路径。

---

## 技术说明

### 查找优先级

工作流按以下优先级查找skill：

1. **自定义路径**（如果配置了非 `{auto-detect}` 的路径）
2. **全局skills目录**（`~/.claude/skills/`）
3. **相对路径查找**（从当前工作目录）

### 错误处理

如果skill无法找到或访问：
- 工作流会显示错误信息
- 指出哪个skill无法访问
- 提供建议的解决方案
- 不会继续执行后续步骤（确保质量）

---

## 更新日志

- **2026-01-22**：初始版本，支持自动查找和自定义路径配置

---

## 联系与反馈

如遇到配置问题或有改进建议，请通过以下方式反馈：
- 在使用工作流时直接描述问题
- 提供错误信息和配置内容
- 说明期望的配置方式
