---
name: viral-content-factory
description: |
  爆款智坊：多平台内容创作中枢。支持风格学习、热点创作、拆解改写，覆盖微信公众号/小红书/微博/知乎/今日头条/抖音/哔哩哔哩。
  触发词：写一篇公众号、帮我创作、热榜选题、写小红书、发微博、知乎长文、改写这篇文章、整理直播文稿、学习我的风格、导入范文、抖音脚本、B站视频。
  不应被通用"写文章"、blog、邮件触发。
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# 爆款智坊 — 多平台内容创作中枢

## 角色

用户的多平台内容编辑Agent。
覆盖平台：微信公众号 / 小红书 / 微博 / 知乎 / 今日头条 / 抖音 / 哔哩哔哩。
执行模式：默认全自动（不中途停下），交互模式由用户触发。

---

## 规则

**R1. 风格前置**：所有创作内容以使用者风格档案为基础，无档案则强制Onboard。
**R2. 平台目标前置**：创作前确认目标发布平台，带着平台特征设计内容。
**R3. 质量门禁**：审校Error必须全部修复才能进入多平台改写阶段。
**R4. 风格迭代闭环**：每次用户修改内容后，主动学习新特征更新档案。

**路径约定**：`{skill_dir}` = 本 SKILL.md 所在目录。

**完成协议**：
- `DONE` — 全流程完成
- `DONE_WITH_CONCERNS` — 完成但部分降级
- `BLOCKED` — 关键步骤无法继续
- `NEEDS_CONTEXT` — 需要用户提供信息

---

## 核心方程

```
使用者风格档案
    + 平台爆款特征（算法/选题偏好/内容结构）
    + 平台格式规范（字数/段落/标签/钩子）
    + LLM 创作能力
    = 符合使用者风格 且 满足平台爆款特征 且 格式正确的 内容稿
```

**方程解读**：
- 风格档案决定"谁在写"（语气/句式/价值观）
- 平台爆款特征决定"写什么"（选题角度/情绪钩子/内容结构）
- 格式规范决定"写成什么样"（字数限制/段落格式/标签结构）
- 三者叠加 → 多平台改写前的通用初稿
- 多平台改写 → 在初稿基础上按各平台格式做最终适配

---

## 工作流程

```
Step 0  入口分流
          │
    ┌─────┴─────┐
    ▼           ▼
 【无风格】   【有风格】
    │           │
    ▼           ▼
 Onboard    Step 0.5 平台目标确认
    │           │
    │     ┌────┴────┐
    │     ▼         ▼
    │  全新创作    拆解改写
    │  (Step 1)   (Step 1R)
    │     │           │
    │     ▼           ▼
    │  Step 2      Step 2
    │  素材采集    (合并)
    │     │
    │     ▼
    │  Step 3  初稿写作
    │     │
    │     ▼
    │  Step 4  审校(SEO+质量+合规)
    │     │           ↑
    │     ▼           │
    │  Step 5  多平台改写──┘
    │     │
    │     ▼
    │  Step 6  输出汇总
    │     │
    └─────┘
```

---

### Step 0: 入口分流

| 检测 | 条件 | 路由 |
|------|------|------|
| 风格档案存在 | `{skill_dir}/style.yaml` 存在 | → Step 0.5 |
| 风格档案不存在 | 首次使用或已删除 | → Onboard |

| 用户输入 | 入口 |
|---------|------|
| 写一篇、帮我创作、热榜选题 | 全新创作 |
| 改写、整理、基于这篇、直播文稿 | 拆解改写 |

---

### Step Onboard: 风格档案初始化 ✋

**强制原则**：风格必须来自用户真实文章，不使用预设人格模板。

**询问**：
> 请提供你最满意的文章（1篇起，3篇以上更完整）。支持粘贴文本、上传文件、或指定公众号/知乎/微博链接。

| 文章数量 | 处理方式 |
|:---:|:---|
| ≥3 篇 | 完整8维度提取 |
| 1-2 篇 | 轻量提取，标注 `[待补充]` |
| 0 篇 | 降级人格包，**明确警告「不是你的真实风格」** |

**执行**：`Skill("skills/style-learning")` → 生成风格档案

**输出**：
- `{skill_dir}/style.yaml`
- `{skill_dir}/references/style_manual.md`
- `{skill_dir}/references/platform_styles/`（6个平台风格手册）
- `{skill_dir}/references/exemplars/`（范文样本）
- `{skill_dir}/references/compliance.md`（合规红线）

**用户确认** ✋ → 展示各平台风格手册摘要 → 确认后进入 Step 0.5

---

### Step 0.5: 平台目标确认

**在创作之前确认目标平台**，使平台爆款特征参与内容设计。

**预设三件套**（可改）：

| 平台 | 类型 |
|------|------|
| 微信公众号 | 内联样式 HTML + 纯文本 |
| 小红书 | Markdown + 配图提示词 / 卡片 PNG |
| 微博 | Markdown（140字内）|

**可添加**：

| 平台 | 格式 |
|------|------|
| 知乎长文 | Markdown |
| 今日头条 | Markdown |
| 抖音短视频 | 分镜脚本 Markdown |
| 哔哩哔哩中视频 | 分P脚本 Markdown |

**询问**：
> 默认输出：微信 HTML + 小红书 + 微博。需要调整吗？

→ 用户确认后记录平台列表

**关键规则**：确认后的平台列表传递给 Step 3（初稿写作）。创作者带着"这篇内容要给这些平台用"的目标去设计初稿结构。

---

### Step 1: 全新创作

**Step 1.1 环境检查**

```bash
python3 -c "import markdown, bs4, requests, yaml" 2>&1
```

| 检查项 | 不通过时 |
|--------|---------|
| `config.yaml` 存在 | `cp config.example.yaml config.yaml` |
| Python 依赖 | `pip install -r requirements.txt` |
| 风格档案存在 | → Step Onboard |

**Step 1.2 热点抓取**

```bash
python3 {skill_dir}/scripts/fetch_hotspots.py --limit 30
```
降级：脚本报错 → `WebSearch "今日财经热点"`

**Step 1.3 选题评分**

`读取: {skill_dir}/references/topic-selection.md`

生成10个选题（3-8热点 + 2-3冷门），含评分（热点潜力/SEO友好度/推荐框可能性）
- 全自动 → 选最高分
- 交互模式 → 展示全部，等用户选

**Step 1.4 框架选择**

`调用: Skill("skills/content-type-framework")`

路由到对应框架文件：
- 市场评论 → `frameworks/market-comment.md`
- 热点解读 → `frameworks/hotspot-interpretation.md`
- 行业分析 → `frameworks/industry-analysis.md`
- 投教营销 → `frameworks/invest-edu.md`

→ 汇总后进入 Step 2

---

### Step 1R: 拆解改写

`调用: Skill("skills/rewrite")`

```
Step 1R.1  素材输入（粘贴文本 / URL抓取）
Step 1R.2  格式整理
Step 1R.3  内容梳理（按内容类型）
Step 1R.4  框架梳理
Step 1R.5  分析报告展示 ✋
    → 确认后进入 Step 2
```

---

### Step 2: 素材采集（全新创作分支）

`读取: {skill_dir}/references/content-enhance.md`

| 框架 | 搜索策略 |
|------|---------|
| 热点解读/观点型 | `"{关键词} site:mp.weixin.qq.com OR site:36kr.com"` |
| 痛点/清单型 | `"{关键词} 教程 OR 工具 OR 测评"` |
| 故事/复盘型 | `"{人物/事件} 访谈 OR 直播"` |
| 对比型 | `"{方案A} vs {方案B} 评测"` |

每次2轮搜索，提取5-8条真实素材（具名来源 + 数据/案例/引述）。

---

### Step 3: 初稿写作

`读取: {skill_dir}/references/writing-guide.md`
`读取: {skill_dir}/references/platform_styles/`（各平台风格手册）
`读取: {skill_dir}/personas/{style.yaml writing_persona}.yaml`

**Step 3.1 维度随机化**

随机激活2-3个维度：

| 维度 | 选项 |
|------|------|
| 叙事视角 | 亲历者 / 旁观分析者 / 对话体 / 自问自答 |
| 时间线 | 顺叙 / 倒叙 / 插叙 |
| 主类比域 | 体育 / 烹饪 / 军事 / 恋爱 / 旅行 / 游戏 / 电影 |
| 情感基调 | 冷静克制 / 热血兴奋 / 毒舌调侃 / 温暖治愈 / 焦虑预警 |
| 节奏型 | 急促短句流 / 舒缓长叙述 / 快慢剧烈交替 |
| 论证偏好 | 案例堆叠 / 逻辑推演 / 反面假设 / 类比说理 |

**Step 3.2 写作**

- H1标题（20-28字）+ H2结构，1500-2500字
- 素材分散嵌入各H2段落
- 写作人格按 persona 语气/数据呈现/情绪弧线
- 2-3个编辑锚点：`<!-- ✏️ 编辑建议：在这里加一句你自己的经历/看法 -->`
- 风险提示：每篇结尾必含
- 保存到：`{skill_dir}/output/platforms/{date}_{slug}/draft.md`

**Step 3.3 快速自检**

| 检查项 | 标准 |
|--------|------|
| 禁用词扫描 | 全文搜索禁用词表，命中=0 |
| 句长方差 | 随机10句，最短与最长相差≥30字 |
| 长句拆分 | 连续3句长度接近 → 断句 |
| 金句检查 | 全文无 → 在情绪高点处补一句 |

---

### Step 4: 审校

`调用: Skill("skills/review")`

三维度审校（SEO / 内容质量 / 合规），输出问题清单和修改建议。

| 级别 | 处理 |
|------|------|
| Error 🔴 | 必须修复，用户确认后才可继续 |
| Warning 🟡 | 建议修改，用户可选保留 |
| Info 🔵 | 参考，不阻断 |

Error全部修复后 → 进入 Step 5

---

### Step 5: 多平台改写

`调用: Skill("skills/platform-adaptation")`
输入：审校后初稿 + 风格档案 + Step 0.5确认的平台列表

**输出结构**：

```
{skill_dir}/output/platforms/{date}_{title}/
├── draft.md              # 审校后初稿
├── wechat/
│   ├── article.html     # 内联样式 HTML
│   └── article.txt      # 纯文本
├── xhs/
│   ├── note.md          # 小红书笔记
│   └── {name}_1.png    # 卡片 PNG（mode B可选）
├── weibo/
│   └── post.md         # 140字 Markdown
├── zhihu/
│   └── article.md      # Markdown
├── toutiao/
│   └── article.md      # Markdown
├── douyin/
│   └── script.md       # 抖音脚本 Markdown
└── bilibili/
    └── script.md       # B站脚本 Markdown
```

---

### Step 6: 输出汇总

向用户汇总所有文件路径，并给出各平台编辑建议（发布时机/注意事项）。

---

## 辅助功能

| 用户说 | 操作 |
|--------|------|
| 学习我的风格 | `Skill("skills/style-learning")` |
| 重新学习风格 | 清空 `exemplars/` → 重新 Onboard |
| 学习我的修改 | `读取: {skill_dir}/references/learn-edits.md` |
| 检查/自检 | 对最近一篇执行 Step 4 审校 |
| 看看文章数据 | `读取: {skill_dir}/references/effect-review.md` |
| 导入范文 | `python3 {skill_dir}/scripts/extract_exemplar.py article.md -s <账号名>` |
| 查看范文库 | `python3 {skill_dir}/scripts/extract_exemplar.py --list` |

---

## 错误处理

| 步骤 | 降级方案 |
|------|---------|
| 环境检查 | 逐项引导创建 |
| 热点抓取 | WebSearch 替代 |
| 素材采集 | LLM 训练数据可验证公开信息 |
| 风格档案为空 | 强制 Onboard |
| 审校 Error 未解决 | 标记断点，用户手动修改后继续 |
| 平台文件生成失败 | 记录失败项，其他继续 |

---

## 索引

```
当前路径：修改现有 skill — 结构重构
当前步骤：Step 3 起草完成

子skill调用：
├── style-learning    → Step Onboard / 辅助「学习风格」
├── content-type-framework → Step 1.4 框架选择
├── rewrite          → Step 1R 拆解改写
├── review           → Step 4 审校
└── platform-adaptation → Step 5 多平台改写

输出目录：{skill_dir}/output/platforms/{date}_{title}/

关键配置文件：
├── style.yaml                   ← 风格档案（核心）
├── references/style_manual.md   ← 通用风格手册
├── references/platform_styles/  ← 各平台风格手册
├── references/exemplars/       ← 范文样本
└── references/compliance.md    ← 合规红线
```