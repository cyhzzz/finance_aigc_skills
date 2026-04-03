---
name: platform-adaptation
description: |
  多平台改写子技能：将审校后的初稿改写为各平台适配版本。
  输入：初稿 + 风格档案 + 平台列表
  输出：6个平台的文件（微信HTML/小红书/微博/知乎/头条/短视频）
  由主管道 Step 6 调用。
---

# 多平台改写流程

## 核心定位

将审校后的初稿，按各平台的格式规范、风格偏好进行改写，输出6个平台的独立文件。

---

## 输入

```
审校后初稿：{skill_dir}/output/platforms/{date}_{title}/draft.md
风格档案：{skill_dir}/references/style_manual.md
         {skill_dir}/references/platform_styles/
平台列表：[微信HTML, 小红书, 微博, 知乎, 头条, 短视频]
```

---

## 输出结构

```
{skill_dir}/output/platforms/{date}_{title}/
├── draft.md                      # 审校后初稿
├── wechat/
│   ├── article.html              # 内联样式 HTML
│   └── article.txt               # 纯文本
├── xhs/
│   ├── note.md                   # 标题 + 正文 + 配图提示词
│   └── cards.html                # 小红书卡片 HTML（可选）
├── weibo/
│   └── post.md                   # 140字 Markdown
├── zhihu/
│   └── article.md                # Markdown
├── toutiao/
│   └── article.md                # Markdown
└── video/
    └── script.md                 # 短视频脚本 Markdown
```

---

## 平台改写调用顺序

```
Step 6.1  微信长文（HTML + TXT）
Step 6.2  小红书笔记
Step 6.3  微博短文案
Step 6.4  知乎长文
Step 6.5  今日头条
Step 6.6  短视频脚本
```

---

## Step 6.1 微信长文

### 调用规范

```
读取: skills/platform-adaptation/references/wechat-html.md
```

### 输出文件

- `wechat/article.html` — 内联样式 HTML
- `wechat/article.txt` — 纯文本

### 核心要求

- 内联所有 CSS 样式（不依赖 `<style>` 标签）
- 封面图提示：`[封面图建议：{描述}]`
- 脚注：外链转为上标编号，底部附参考链接
- 支持暗黑模式（注入 `data-darkmode-*` 属性）
- 风险提示完整（见 compliance.md）

---

## Step 6.2 小红书笔记

### 调用规范

```
读取: skills/platform-adaptation/references/xhs-card.md
```

### 渲染模式选择

询问用户：「配图想要 AI 绘图提示词，还是直接生成卡片 PNG？」

| 用户选择 | 执行方式 | 输出文件 |
|:---:|:---|:---|
| AI 绘图提示词（默认） | 生成 `xhs/note.md` + 配图提示词 | `xhs/note.md` |
| 卡片 PNG | 调用 `render_poster()` | `xhs/{name}_1.png` 等 |

### 模式 A：AI 绘图提示词

输出文件：
- `xhs/note.md` — 标题 + emoji + 正文 + 标签 + 配图提示词

核心要求：
- 标题：吸引眼球型，含悬念/数字/情绪词
- 正文：短段落 + 大量 emoji + 空行分隔
- 标签：5-8个话题标签（#开头）
- 配图提示词：3:4 竖版，3-6张，逐张描述

### 模式 B：HTML → PNG 卡片渲染

触发条件：用户选择「卡片 PNG」

调用方式：
```bash
python3 {skill_dir}/toolkit/cli.py render-poster {xhs_content.md} \
    --output {output_dir}/xhs/ \
    --title "{文章标题}" \
    --name {slug}
```

前置准备：将小红书笔记正文保存为临时 Markdown 文件，供 `render_poster()` 处理。

输出文件：
- `xhs/{name}_1.png` — 第1张卡片（1080×1440）
- `xhs/{name}_2.png` — 第2张卡片（如有）
- …

技术说明：
- 依赖：`node` + `playwright`（`npx playwright install chromium`）
- 模板：`toolkit/assets/poster_template.html`
- 截图：`toolkit/assets/capture.js`
- 字体：KingHwa_OldSong（备选 Noto Serif SC）
- 色调：自动根据内容气质匹配（技术蓝/文学暖/科学绿）
- 多卡：自动贪心切分，每卡约 380 字符视觉重量

---

## Step 6.3 微博短文案

### 调用规范

```
读取: skills/platform-adaptation/references/weibo-short.md
```

### 输出文件

- `weibo/post.md` — 140字 Markdown

### 核心要求

- ≤140字（含话题标签）
- 1句话核心观点 + 1-2句补充 + 话题标签
- 互动引导语（"你怎么看？"等）
- 可附原文链接

---

## Step 6.4 知乎长文

### 调用规范

```
读取: skills/platform-adaptation/references/zhihu-long.md
```

### 输出文件

- `zhihu/article.md` — Markdown

### 核心要求

- 标题层级：H1 + H2 + H3 结构完整
- 论证式行文：观点 → 论据 → 论证
- 参考文献脚注（引用格式规范）
- 可添加"编辑推荐"类引导语

---

## Step 6.5 今日头条

### 调用规范

```
读取: skills/platform-adaptation/references/toutiao.md
```

### 输出文件

- `toutiao/article.md` — Markdown

### 核心要求

- 短段落（每段 ≤ 3句）
- 关键词前置（前3段出现核心关键词）
- 情绪化标题（与原标题不同）
- 算法友好：密度高、信息量大

---

## Step 6.6 短视频脚本

### 调用规范

```
读取: skills/platform-adaptation/references/video-script.md
```

### 输出文件

- `video/script.md` — Markdown

### 核心要求

- 开场钩子：3秒内抓住注意力
- 分镜式正文：镜头编号 + 画面描述 + 配音稿
- 结尾引导：关注/评论/点赞引导
- 时长估算：1分钟脚本 ≈ 180字

---

## 改写原则

### 通用原则（所有平台）

1. **内容一致性**：所有平台版本的核心信息必须一致
2. **风格适配**：按平台风格手册调整语气/结构
3. **信息裁剪**：长文→短文时，裁剪次要信息，保留核心
4. **格式适配**： Markdown / HTML / 纯文本 按平台选择
5. **风险提示**：各平台合规风险提示必须包含

### 平台差异原则

| 平台 | 信息策略 | 核心原则 |
|------|---------|---------|
| 微信 | 全量信息 | 深度完整 |
| 小红书 | 核心观点+视觉 | 情绪共鸣+可操作 |
| 微博 | 1句话+标签 | 即时传播 |
| 知乎 | 论证+引用 | 专业深度 |
| 头条 | 短段落+关键词 | 算法友好 |
| 短视频 | 分镜+钩子 | 3秒注意力 |

---

## 质量检查

完成所有平台改写后，逐项核对：

- [ ] 微信HTML内联样式完整，无 `<style>` 依赖
- [ ] 微信TXT纯文本无乱码
- [ ] 小红书 mode A：笔记含配图提示词；mode B：PNG 卡片 1080×1440，多卡页码正确（1/N）
- [ ] 微博≤140字
- [ ] 知乎有引用脚注
- [ ] 头条标题与原标题不同（情绪化版本）
- [ ] 短视频脚本有开场钩子
- [ ] 所有平台风险提示完整
- [ ] 各平台文件均在正确目录
