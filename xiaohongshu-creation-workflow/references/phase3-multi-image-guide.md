# Phase 3: 多页信息图生成指南

**目标**：为小红书笔记的每一页生成对应的图像提示词（AI绘图提示词，不直接出图）

> **重要说明**：本指南输出的是**图像生成提示词**，不直接调用画图工具。用户收到提示词后，可自行粘贴到 Midjourney / DALL·E / Stable Diffusion / 即梦 / 可灵等 AI 绘图工具中生成图像。
>
> 每页提供**三种风格**的提示词供选择：
> 1. **[视觉风格A]格**：莫兰迪色系、手绘线条感、适合小红书风格
> 2. **Mondo 大师海报风格**：极简主义、高饱和度、丝网印刷美学，视觉冲击力强
> 3. **手账手绘信息图风格**：手账日记感、莫兰迪三色严格固定、虚线连接、几何角色插图、8K超清、36种信息图类型智能匹配

---

## 执行流程

### Step 1: 读取笔记图结构

从Phase 2的输出中读取笔记图部分：
- 封面页（1页）
- 内容页（N页，通常4-6页）
- 尾页（1页）

**总页数**：通常6-8页

### Step 2: 为每一页规划图像

#### 封面页图像设计

**目标**：吸引点击，体现核心价值

**设计要素**：
- **主标题**：醒目的标题（手写字体）
- **核心观点金句**：1-2句话总结核心价值
- **视觉元素**：简单的图标或插图
- **吸引元素**：问号、数字、关键词高亮

**布局建议**：
```
┌─────────────────────┐
│  [主标题]           │
│  （大号手写字体）    │
│                     │
│  [核心观点金句]     │
│  （中号字体，重点）  │
│                     │
│  [简单图标/插图]    │
│  （底部装饰）        │
└─────────────────────┘
```

**信息图类型选择**：
- 优先：中心辐射图（突出核心主题）
- 或：大标题+要点列表

---

#### 内容页图像设计

**目标**：清晰展示该页的知识要点

**设计要素**：
- **页面标题**：该页的主题
- **要点清单**：该页的3-5个要点
- **视觉层次**：用框线、箭头、虚线连接
- **数据/案例**：关键数据或案例的可视化

**布局建议**：
```
┌─────────────────────┐
│  [页面标题]         │
├─────────────────────┤
│  ● 要点1            │
│     （简短解释）     │
│                     │
│  ● 要点2            │
│     （简短解释）     │
│                     │
│  ● 要点3            │
│     （简短解释）     │
│                     │
│  [数据/案例框]      │
└─────────────────────┘
```

**信息图类型选择**：
- 列表式内容：清单图、步骤图
- 对比内容：对比表、天平图
- 流程内容：流程图、循环图
- 分析内容：四象限图、桥梁图

---

#### 尾页图像设计

**目标**：明确引导行动，强化品牌印象

**设计要素**：
- **引导语**：开户/咨询的行动召唤
- **权益亮点**：新客专属权益（3-5个要点）
- **品牌标识**：[券商名称]品牌元素
- **联系方式**：私信、企业微信等

**布局建议**：
```
┌─────────────────────┐
│  [行动召唤]         │
│  "开户[券商名称]"     │
├─────────────────────┤
│  新客专属权益：     │
│  ● 8.18%理财        │
│  ● Level-2行情      │
│  ● 投顾服务         │
│  ● 增值指标         │
├─────────────────────┤
│  求赞收藏关注       │
│  私信领资料包       │
│                     │
│  @[券商名称]证券      │
└─────────────────────┘
```

**信息图类型选择**：
- 优先：清单图（突出权益要点）
- 或：中心辐射图（品牌在中心）

---

### Step 2.5: ★ 确定全套视觉规格（必须在生成任何提示词之前完成）

> **这是保证跨页风格统一的核心机制。** 生成任何单页提示词之前，必须先确定以下"全套视觉规格锚点"，并在后续每一页提示词中**原封不动复用**这些参数，不得每页重新决策。

```
【全套视觉规格锚点】（生成后锁定，所有页共享）

■ [视觉风格A]格
  背景色：___________（如 #FAF9F6，全套统一）
  主色调：___________（如 #9FA8DA + #A5D6A7 + #EF9A9A，全套统一）
  文字色：___________（如 #424242，全套统一）
  线条规格：___________（如 2.5px，85%透明度，全套统一）
  字体风格：___________（如 手写风格，左对齐，全套统一）
  装饰主题：___________（如 简洁几何+金融图标，全套统一）

■ Mondo 大师海报风格
  选定流派：___________（如 Reid Miles 爵士排版风，全套统一）
  背景主色：___________（如 深海军蓝 #1B2A4A，全套统一）
  主强调色：___________（如 金色 #F2C744，全套统一）
  辅助色：___________（如 奶白 #FAF5E4，全套统一）
  字体指令：___________（如 bold geometric sans-serif，全套统一）
  图形风格：___________（如 flat vector icons，全套统一）

■ 手账手绘信息图风格（参数固定，无需决策，直接锁定以下值）
  背景色：#FAF9F6（Warm Ivory，禁止变更）
  主色调：#9FA8DA（莫兰迪蓝）+ #A5D6A7（莫兰迪绿）+ #EF9A9A（莫兰迪粉），透明度20-30%（禁止变更）
  强调色：#424242（Deep Charcoal，禁止变更）
  线条颜色：#757575（Medium Gray，禁止变更）
  线条宽度：2.5px，虚线：8px实线+6px空白（禁止变更）
  字体：手写风格，左对齐，轻度抖动（禁止变更）
  角色插图：简化几何风，仅3种动作（思考/指向/展示），模块右上角（禁止变更）
  信息图类型：___________（每页根据内容独立选择，共36种可选，见下方类型表）
```

**规则**：
1. 根据主题类型（金融/科普/生活等）自动选择初始配色，填入上方锚点
2. 锚点一旦确定，后续每一页的 `[风格参数]` / `[Color Palette]` **直接引用锚点值**，不得重新决策颜色
3. 唯一允许变化的是：各页的**内容设计**（主标题/要点/数据）和**布局**（图示类型），不改变任何视觉参数
4. **手账手绘信息图风格**的视觉参数全部固定，无需决策；每页唯一需要决策的是"信息图类型"（从36种中选择最匹配当页内容的类型）

---

### Step 3: 生成每页的图像提示词（三风格输出）

> **每页均输出三组提示词**：① [视觉风格A]格  ② Mondo 大师海报风格  ③ 手账手绘信息图风格
> 用户可根据喜好选择其中一组提示词，粘贴到 AI 绘图工具中使用。

#### 手账手绘信息图风格：信息图类型速查表（按内容特性选择）

| 内容特性 | 推荐类型 |
|---------|---------|
| 分析原因 | 鱼骨图（15）、冰山模型（03） |
| 制定策略 | 四象限图（18）、桥梁图（25） |
| 展示流程 | 线性流程图（08）、循环图（12） |
| 比较优劣 | 天平图（20）、对比表（21） |
| 解释概念 | 汉堡图（24）、洋葱图（05） |
| 层级结构 | 金字塔图（04）、组织结构图（02） |
| 成长进阶 | 阶梯图（28）、路线图（11） |
| 主题概述/封面 | 中心辐射图=思维导图（01）、靶心图（29） |
| 行动引导/尾页 | 清单图=线性流程图（08）、阶梯图（28） |

---

#### 风格一：[视觉风格A]格提示词

**风格说明**：[视觉风格A]系列是为小红书深度优化的手绘风格体系，由**视觉风格（Style）× 信息布局（Layout）**两个维度自由组合，共 10 种风格 × 8 种布局 = 80+ 种组合效果。所有风格统一使用手绘线条，不使用写实或计算机生成字体。

---

**视觉风格（Style）完整库 × 布局（Layout）完整库**

##### 10种视觉风格对照表

| 风格名 | 核心特征 | 配色 | 适用内容 |
|-------|---------|------|---------|
| `notion`（默认知识类）| 极简线稿、大留白、stick figure、黑白+柔色点缀 | 黑/深灰 + 纯白 + 粉蓝/粉黄点缀 | 金融知识科普、投资概念、SaaS工具 |
| `minimal`（高端极简）| 单一焦点、细线条、优雅留白 | 黑白为主，单色点缀（内容派生色）| 专业分析、高端品牌感 |
| `warm`（温暖生活）| 圆润手写、暖色系、温馨装饰（云朵/星星）| 暖橙/金黄/奶油底 | 生活理财、个人分享、情感引导 |
| `cute`（小红书爆款）| 甜美手绘、粉彩系、贴纸/爱心/星星 | 粉/桃/薄荷/薰衣草 | 美妆生活类引流、萌系封面 |
| `fresh`（清新自然）| 植物/云朵/水滴装饰、留白舒展、清爽感 | 薄荷绿/天蓝/鹅黄 | 健康理财、生活品质、养生投资 |
| `bold`（冲击力强）| 强对比、粗字体、感叹号/箭头/警告图形 | 黑底+亮红/橙/黄 | 热点话题、"必看"类内容、风险提示 |
| `retro`（复古vintage）| 做旧纹理、半色调点、胶带感、老报纸色调 | 做旧米黄/赭石/褪色红/复古金 | 历史行情回顾、"那年那月"类 |
| `pop`（活力流行）| 高饱和、气泡感、漫画效果、confetti | 鲜红/亮黄/电蓝/霓虹粉 | 年轻受众、热点引流、趣味科普 |
| `chalkboard`（黑板粉笔）| 黑板纹理底、彩色粉笔线条、粉笔尘效果 | 黑/墨绿底 + 粉笔白/黄/粉/蓝/绿 | 教学类科普、投资入门知识 |
| `study-notes`（学霸笔记）| 真实拍照感、蓝黑圆珠笔、红笔圈注、黄色荧光 | 白色横线纸底 + 蓝/黑/红/黄荧光 | 金融知识整理、"学渣变学霸"类 |

##### 8种信息布局对照表

| 布局名 | 结构描述 | 密度 | 要点数 | 最适合 |
|-------|---------|------|-------|-------|
| `sparse`（默认封面）| 单一视觉焦点，大量留白 | 低 | 1-2 | 封面、金句、冲击性陈述 |
| `balanced`（标准内容）| 标题+均等分布内容 | 中 | 3-4 | 通用内容页、教程 |
| `dense`（知识卡片）| 多区块紧凑，structured grid | 高 | 5-8 | 知识点合集、速查表 |
| `list`（清单排行）| 竖向枚举+编号，左对齐 | 中高 | 4-7 | 权益清单、步骤指南、排行榜 |
| `comparison`（对比分析）| 左右分屏，鲜明视觉对比 | 中 | 2区块 | 之前/之后、优缺点、A vs B |
| `flow`（流程时序）| 箭头连接节点，方向性布局 | 中 | 3-6步 | 开户流程、投资步骤、时间线 |
| `mindmap`（中心辐射）| 中心主题向外发散 | 中高 | 4-8分支 | 话题全景、框架梳理、封面概述 |
| `quadrant`（四象限）| 2×2方格，坐标轴划分 | 中 | 4区块 | SWOT、优先级矩阵、风险评估 |

##### 风格×布局自动选择规则

| 内容类型信号 | 推荐风格 | 推荐布局 |
|------------|---------|---------|
| 金融知识、投资概念、SaaS工具 | `notion` | `dense` / `list` |
| 开户引导、权益展示、专业品牌 | `minimal` | `sparse` / `balanced` |
| 生活理财、个人分享、情感 | `warm` | `balanced` / `flow` |
| 美妆/生活/年轻女性受众 | `cute` | `sparse` / `balanced` |
| 健康投资、自然生活 | `fresh` | `balanced` / `flow` |
| 风险提示、必看内容、热点 | `bold` | `list` / `comparison` |
| 历史行情、复古回顾 | `retro` | `balanced` / `list` |
| 趣味科普、年轻热点 | `pop` | `sparse` / `list` |
| 教学科普、知识入门 | `chalkboard` | `balanced` / `dense` |
| 笔记感、知识整理 | `study-notes` | `dense` / `list` / `mindmap` |

---

##### 排版元素系统（花字/标签/装饰）

**花字（标题文字特效）选择**：
- `gradient`（渐变色填充）→ 现代感标题
- `stroke-text`（描边字）→ 封面大标题，高可见性
- `shadow-3d`（3D阴影）→ 关键词突出
- `highlight`（荧光笔效果）→ 关键信息划重点
- `handwritten`（手写感）→ 亲切随意，适合温暖类风格
- `bubble`（气泡圆润字）→ cute/pop 风格

**内容标签选择**：
- `black-white`（黑底白字）→ 品牌名/价格/分类
- `pill`（圆角药丸）→ 话题标签，notion/minimal 常用
- `bubble`（对话气泡）→ 备注/标注/Q&A
- `ribbon`（丝带横幅）→ 特别说明，warm/cute 常用
- `stamp`（印章感）→ 推荐认证，retro 常用

**强调标记选择**：
- `red-arrow`（红箭头）→ 指向重点
- `circle-mark`（圆圈标注）→ 框选细节
- `star-burst`（爆炸星）→ 特别优惠/重要发现
- `checkmark`（勾选）→ 已完成/优点清单
- `numbering`（圆形编号）→ 步骤/排名

**背景类型选择**：
- `solid-pastel`（柔和纯色）→ cute/warm/fresh 默认
- `paper-texture`（纸张纹理）→ retro/study-notes
- `chalkboard`（黑板纹理）→ chalkboard 专用
- `grid`（网格底纹）→ notion/minimal 轻量版

---

##### 封面页提示词模板

```
Create a Xiaohongshu (Little Red Book) style infographic:

## Image Specifications
- Type: Infographic, Cover
- Orientation: Portrait (vertical), 3:4 aspect ratio
- Resolution: 8K (1242×1660 optimized display)
- Style: Hand-drawn illustration

## Core Principles
- Hand-drawn quality throughout — NO realistic or photographic elements
- ALL text MUST be hand-drawn style, NO computer-generated fonts
- Use ample whitespace (≥ 50% for cover) for visual impact
- Single focal point with maximum visual punch

## Style: {从10种风格中选择，如 notion / warm / bold...}
[Color Palette]
- Primary: {对应风格的主色，如 notion→黑/#1A1A1A、warm→暖橙/#ED8936}
- Background: {对应背景色，如 notion→纯白/#FFFFFF、warm→奶油/#FFFAF0}
- Accents: {对应点缀色，如 notion→粉蓝#A8D4F0/粉黄#F9E79F}

[Visual Elements]
- {对应风格的装饰元素，如 notion→简单线稿+stick figure、cute→爱心/星星/贴纸}
- {字体类型，如 notion→clean hand-drawn lettering、cute→rounded bubbly手写}

## Layout: sparse（封面默认）
- Single focal point centered
- Title: prominent top-left or center, hand-drawn style, large
- Core visual occupies 60-70% of canvas
- Breathing room on all sides

## Content
- Main Title: "{标题}"（大号手写字体，醒目突出）
- Core Hook/Tagline: "{金句或副标题}"（中号，置于标题下方或视觉中心）
- Decorative Icons: {1-2个与主题相关的简单图标，底部或右侧点缀}
- Visual Theme: {整体画面隐喻描述，如"上升的折线+金币构成画面焦点"}

## Typography
- Title: {花字类型，如 stroke-text 描边 / highlight 荧光划重点 / handwritten 手写}
- Accent Tags: {标签类型，如 pill圆角标签 / stamp印章}

## Emphasis Elements
- {强调标记，如 star-burst 爆炸星标注关键词 / red-arrow 指向核心数据}
```

##### 内容页提示词模板

```
Create a Xiaohongshu (Little Red Book) style infographic:

## Image Specifications
- Type: Infographic, Content Page {N}
- Orientation: Portrait (vertical), 3:4 aspect ratio
- Resolution: 8K
- Style: Hand-drawn illustration

## Core Principles
- Hand-drawn quality throughout — NO realistic or photographic elements
- ALL text MUST be hand-drawn style, NO computer-generated fonts
- Maintain clear visual hierarchy (title > section > body > caption)
- Consistent style with cover page

## Style: {与封面一致}
[Color Palette — 与封面完全相同，不得变更色系]
- Primary: {同封面}
- Background: {同封面}
- Accents: {同封面}

[Visual Elements — 与封面一致]
- {同风格的装饰元素}

## Layout: {根据内容选择}
- `balanced`（3-4要点通用）/ `dense`（5-8知识卡片）/ `list`（清单权益）/ `flow`（流程步骤）/ `comparison`（对比分析）/ `mindmap`（主题辐射）/ `quadrant`（四象限）

[布局参数]
- 标题区域：画布上部 15%，左对齐
- 要点区域：画布中部 70%，垂直排列
- 数据/案例区：画布下部 15%（如有）
- 要点间距：5%
- 整体留白：40-50%（balanced）/ 20-30%（dense）

## Content
- Page Title: "{本页标题}"（中号手写字体，左对齐，顶部）
- Key Points（按所选布局排列）:
  {① 要点1：简短解释（≤15字）}
  {② 要点2：简短解释（≤15字）}
  {③ 要点3：简短解释（≤15字，如有）}
  {④ 要点4：简短解释（≤15字，如有）}
- Data/Case Box: {关键数据或案例，如有，放置于底部数据框}
- Page Number: {当前页}/{总页数}（小号，右下角）

## Typography
- Section Headers: highlight（荧光划重点）或 handwritten 手写
- Body Points: 简洁手写，每点前配 {圆圈编号numbering 或 checkmark勾选}
- Key Numbers/Data: shadow-3d 突出显示

## Decorations
- Background: {对应风格，如 solid-pastel / paper-texture / grid}
- Doodles: {对应装饰，如 notion→hand-drawn-lines+arrows-curvy、warm→clouds+stars}
- Emphasis: {红箭头red-arrow 或 圆圈标注circle-mark，指向最重要的数据}
- Dividers: {分隔线类型，如 line-dashed虚线 / line-wavy波浪线}
```

##### 尾页提示词模板

```
Create a Xiaohongshu (Little Red Book) style infographic:

## Image Specifications
- Type: Infographic, Ending/CTA Page
- Orientation: Portrait (vertical), 3:4 aspect ratio
- Resolution: 8K
- Style: Hand-drawn illustration

## Core Principles
- Hand-drawn quality throughout — NO realistic or photographic elements
- ALL text MUST be hand-drawn style
- Clear action-oriented hierarchy: CTA headline → Benefits → Brand
- Warm, inviting, not hard-sell

## Style: {与全套一致}
[Color Palette — 与封面完全相同]
- Primary: {同封面}
- Background: {同封面，尾页可在品牌区域局部用[券商名称]品牌色强化}
- Accents: {同封面}

## Layout: list（尾页默认，突出权益清单）
- CTA区域：画布上部 25%，大号手写字体
- 权益清单区域：画布中部 50%，左对齐，list布局
- 引导语+品牌区：画布下部 25%，居中或左对齐

## Content
- Main CTA: "开户[券商名称]证券"（大号手写字体，配向上箭头图标）
- Benefits List（每条配手绘小图标）:
  ● 新客理财 8.18% 预期收益率（配金币/图表图标）
  ● Level-2 高速行情 90 天免费（配折线图/雷达图标）
  ● 专业投顾一对一服务（配人物/握手图标）
  ● 增值量化指标工具礼包（配工具/齿轮图标）
- Guide Text: "求赞收藏关注 · 私信领资料包"（小号，倒数第二行）
- Brand: "@[券商名称]证券财富管理"（最底部，手写风格）

## Typography
- CTA Title: stroke-text描边 或 shadow-3d，大号，高可见性
- Benefits: highlight（荧光划线），左对齐
- Brand: handwritten手写，温暖亲切

## Decorations
- Benefit Icons: hand-drawn line icons（金币、折线图、人物、工具），medium gray，2px
- CTA Area: star-burst爆炸星 点缀于标题旁
- Background: {同风格，如 solid-pastel / paper-texture}
- Doodles: {与全套一致的装饰元素}
- Frames: {如用cute/warm风格，可用tape-corners胶带角装饰}
```

---

#### 风格二：Mondo 大师海报风格提示词

**风格说明**：Mondo 风格源于专业演出海报设计，核心特征是极简主义象征、丝网印刷美学（silkscreen）、有限色彩平面色块（2-5色）、大胆配色与强烈对比。无渐变、无阴影、无3D效果。AI 根据内容主题和情感基调，从33+位传奇设计师中智能选择最匹配的流派。

---

**设计师流派完整库（三层选择机制）**

> **选择逻辑**：先判断内容类型（第一层），再判断情感基调（第二层），最终落地到具体设计师（第三层）。

##### 第一层：内容类型 → 设计师大类

| 内容类型 | 推荐设计师大类 | 说明 |
|---------|-------------|------|
| 金融/投资/财富 | 专辑封面派（Blue Note/Verve 爵士路线）| 理性权威 + 极简优雅 |
| 市场热点/趋势 | 电影海报派（Saul Bass / Kilian Eng）| 视觉冲击 + 象征力量 |
| 知识科普/教育 | 书籍封面派（Chip Kidd / 王志弘）| 概念清晰 + 克制优雅 |
| 生活理财/个人 | 社交媒体风格派（日系/文艺风）| 亲切温暖 + 易读传播 |
| 开户推广/品牌 | 电影海报派（Drew Struzan 史诗风）| 仪式感 + 品牌权威 |

##### 第二层：情感基调 → 具体风格流派

**A. 理性权威类（金融/专业/数据）**

| 设计师 | 流派特征 | 配色偏好 | 适用场景 |
|--------|---------|---------|---------|
| Reid Miles（Blue Note Records）| 爵士黄金时代，高对比度网格排版，几何无衬线字体主导 | 深蓝/黑底 + 奶白 + 单强调色 | 金融数据页、专业分析 |
| David Stone Martin（Verve Records）| 极简水墨线条，手绘感强，留白大量 | 米色/纸感底 + 黑色线条 + 金棕点缀 | 知识梳理、流程图 |
| 王志弘（东亚书籍设计）| 克制优雅，东方美学，字体即视觉 | 米白底 + 深炭灰 + 单色点缀 | 科普知识、深度解读 |

**B. 视觉冲击类（热点/趋势/引流）**

| 设计师 | 流派特征 | 配色偏好 | 适用场景 |
|--------|---------|---------|---------|
| Saul Bass | 极简几何象征，用最少元素传达最强概念，圆形+线+箭头构成 | 深底（海军蓝/炭黑）+ 高饱和强调色（金/橙/红）| 开户封面、热点话题封面 |
| Olly Moss | 负空间视觉双关，图形中藏图形，需要"第二眼发现"的惊喜 | 有限双色（2-3色）+ 强烈剪影 | 反转型内容、有悬念的封面 |
| Kilian Eng | 几何未来主义，宇宙感光效，像素化光晕，科幻氛围 | 深宇宙蓝/紫底 + 霓虹蓝/青/品红 | 科技投资、AI/量化内容 |

**C. 史诗仪式类（品牌/开户引导/权益）**

| 设计师 | 流派特征 | 配色偏好 | 适用场景 |
|--------|---------|---------|---------|
| Drew Struzan | 《星球大战》《夺宝奇兵》御用，手绘插画+史诗感构图，人物居中放射光芒 | 金色/橙红/深棕 + 史诗光晕 | 尾页权益展示、开户引导 |
| Peter Saville（Factory Records）| 极简主义 + 工业冷感，Joy Division 封面级别的去装饰感，字体即设计 | 深色底 + 单色文字 + 大量留白 | 高端品牌感页面 |

**D. 知性书卷类（科普/教育/深度）**

| 设计师 | 流派特征 | 配色偏好 | 适用场景 |
|--------|---------|---------|---------|
| Chip Kidd（Random House）| 概念派视觉隐喻，用物体/图形讲述抽象概念，"看一眼就懂主题" | 明亮对比色 或 高度克制双色 | 知识科普封面、概念解释页 |
| Coralie Bickford-Smith（Penguin Clothbound）| 经典纹样 + 精致装帧感，布面质感，重复图案构成背景 | 深底（深绿/深红/深蓝）+ 金色压纹感 | 系列感套图、长知识页 |

**E. 社交传播类（生活/轻松/日常理财）**

| 风格 | 特征 | 配色偏好 | 适用场景 |
|-----|------|---------|---------|
| 文艺风（小红书文艺派）| 柔和大留白，诗意排版，文字与极简图形共舞 | 米色/莫兰迪底 + 低饱和单色 | 生活理财、软性引导 |
| 日系风（胶片感）| 温暖自然光感，柔化处理，像在胶片相纸上印刷 | 暖黄/米白底 + 棕色/深红系 | 亲近生活的内容 |
| 韩系风（梦幻粉彩）| 清新渐变感（例外：Mondo通常无渐变，此风格可用极浅渐变）、奶fufu配色 | 粉白/薰衣草底 + 深色文字 | 年轻受众、活泼内容 |
| 国潮风 | 传统纹样现代演绎，水墨/印章感，红金配色 | 朱红/金色 + 米白/宣纸色 | 文化类投资、节日内容 |

---

**配色智能适配规则（内容类型 → 设计师 → 色板三联映射）**

| 内容类型 | 推荐设计师 | 背景色 | 主强调色 | 辅助色 | 情感定位 |
|---------|----------|-------|---------|-------|---------|
| 金融数据/专业分析 | Reid Miles（Blue Note）| 深海军蓝 #1B2A4A | 金色 #F2C744 | 奶白 #FAF5E4 | 专业权威 |
| 知识科普/概念解释 | Chip Kidd / 王志弘 | 米色 #F5F0E8 | 深炭灰 #1A1A1A | 单色点缀（赭石/深红）| 知性清晰 |
| 市场热点/爆款选题 | Saul Bass（极简几何）| 炭黑 #1A1A1A | 火焰橙 #E85D04 | 暖白 #FFF8F0 | 冲击力 |
| 科技/量化/AI投资 | Kilian Eng（未来主义）| 深宇宙蓝 #0D1B2A | 霓虹青 #00E5FF | 品红 #FF006E | 未来感 |
| 生活理财/软性引导 | 日系风 / 文艺风 | 暖奶白 #FFFAF0 | 深棕 #5D4037 | 赭石 #8D6E63 | 亲切温暖 |
| 开户推广/权益展示 | Drew Struzan / Peter Saville | 深海军蓝 #1B2A4A | 金色 #F2C744 | 奶白 #FAF5E4 | 仪式权威 |
| 系列套图/精读封面 | Coralie Bickford-Smith | 深绿 #1B4332 或 深蓝 #1A3A5C | 金色 #D4AF37 | 米白 #FAF5E4 | 精装书感 |
| 节日/文化类 | 国潮风 | 宣纸米 #F5ECD7 | 朱红 #C0392B | 金色 #D4AF37 | 文化仪式 |

---

##### 封面页提示词模板

```
Mondo poster design style, vertical 3:4 ratio, 8K resolution

[Visual Concept]
主题："{核心主题关键词}"
概念化提炼：将主题转化为一个强烈的视觉象征符号（如：投资→公牛+上升曲线; 理财→天平+金币; 趋势→箭头+几何波形）

[Designer Style Selection - 根据内容类型自动选择以下之一]
① 金融/专业类 → Reid Miles 爵士排版风：高对比度网格，几何无衬线字体主导，数字与符号即设计
② 热点/冲击类 → Saul Bass 极简几何风：最少元素传达最强概念，圆形+剪影+箭头构成核心画面
③ 科技/量化类 → Kilian Eng 未来主义：几何光效，宇宙感背景，像素化光晕，霓虹色点缀
④ 知识/科普类 → Chip Kidd 概念隐喻风：用一个物体或图形讲述抽象概念，"看一眼就懂主题"
⑤ 生活/温暖类 → 日系文艺风：胶片感，柔化光，温暖排版，文字诗意留白

[Design Directives]
- 风格：[从上方选定流派，此处填入设计师名称]
- 丝网印刷美学：仅使用3种颜色的平面色块，无渐变（日系风格例外，可用极浅渐变）
- 主视觉：一个代表核心主题的极简象征符号，占画面60-70%
- 标题字体：手绘复古装饰风格，"{标题文字}"，置于视觉下方1/3区域
- 副标题/品牌名：极小号，底部区域，奶白色

[Color Palette - 按上方配色三联映射填入]
- 背景色：{按内容类型选定，如：深海军蓝 #1B2A4A}
- 主强调色：{如：金色 #F2C744}
- 辅助留白色：{如：奶白 #FAF5E4}

[Layout Principles]
- 极简构图：主视觉居中，占据画面60-70%
- 强烈的明暗对比（明度差 > 80%）
- 手绘装饰风格标题字，居于视觉下方1/3区域
- 整体留白 ≥ 40%，营造高级感
- 禁止使用渐变（日系除外）、阴影、3D效果

[Technical]
flat graphic design, screen printing silkscreen effect, limited 3-color palette, no gradients,
high contrast, iconic minimalism, hand-lettered decorative title, vintage poster texture,
8K resolution, 3:4 portrait ratio
```

##### 内容页提示词模板

```
Mondo informational poster, vertical 3:4 ratio, 8K resolution

[Visual Concept]
主题："{本页章节标题}"
视觉化：将内容要点提炼为图示（图标+编号+极简文字的排版构图）

[Designer Style - 与封面保持一致，从以下选一]
① Reid Miles 风格（金融/专业）：高对比度网格排版，章节标题大号几何无衬线体，要点用编号+图标，底部页码标注
② Chip Kidd / 王志弘 风格（科普/知识）：概念化版式，每个要点配一个微型象征图形，克制留白
③ Peter Saville 风格（品牌/高端）：极简工业感，字体即排版，大量留白，去装饰化
④ Kilian Eng 风格（科技/量化）：几何图形网络化，光效点缀，要点以节点形式呈现
⑤ 日系/文艺风格（生活/温暖）：温暖排版，手写感字体，每点配温暖小图标

[Design Directives]
- 以视觉化图示为主（图标+连接线+数字编号），辅以极简文字
- 章节标题：大号几何字体，占顶部20%
- 要点展示（每个要点 ≤ 8字，配对应图标）：
  ① {要点1} + 图标
  ② {要点2} + 图标
  ③ {要点3} + 图标
- 底部加入页码标注："{当前页} / {总页数}"

[Color Palette - 与封面一致]
- 背景：{与封面相同的深色底或浅色底}
- 要点图标与编号：使用主强调色
- 正文文字：奶白色 #FAF5E4（深色底）或 深炭灰 #1A1A1A（浅色底）
- 分隔线/辅助线：主强调色 30% 透明度

[Technical]
flat graphic design, bold typography, iconographic elements, numbered list visual,
screen printing silkscreen style, no gradients, vintage poster aesthetic,
high legibility, consistent with cover color scheme, 8K resolution, 3:4 portrait ratio
```

##### 尾页提示词模板

```
Mondo promotional poster, vertical 3:4 ratio, 8K resolution

[Visual Concept]
主题："开户引导 - [券商名称]证券"
核心象征：向上增长的箭头 + 品牌圆形徽章 + 光芒放射（Drew Struzan 史诗感）

[Designer Style]
Drew Struzan 史诗感 + Peter Saville 极简主义混合：
- 顶部：大号几何象征图形（品牌感symbol），光芒放射，占画面上方40%
- 中部：权益清单，极简图标+一行字，左对齐，图标使用主强调色
- 底部：强烈CTA行动召唤文字，大号装饰字体

[Content]
权益清单（每条配极简手绘图标）：
  ● 新客理财 8.18% 预期收益率（配金币/图表图标）
  ● Level-2 高速行情 90 天免费（配折线/雷达图标）
  ● 专业投顾一对一服务（配人物/握手图标）
  ● 增值量化指标工具礼包（配工具/齿轮图标）
行动召唤：「立即开户 · [券商名称]证券」（大号手绘装饰字体）
引导语：「求赞收藏关注 · 私信领资料包」（小号，倒数第二行）
品牌标识：@[券商名称]证券财富管理（最底部）

[Color Palette]
- 背景：深海军蓝 #1B2A4A（专业权威感，与封面呼应）
- 顶部象征图形与CTA文字：金色 #F2C744（财富感）
- 权益清单文字与图标：奶白 #FAF5E4
- 辅助分隔线：金色 #F2C744，30% 透明度

[Layout Principles]
- 上方大号品牌象征（40%高度）
- 中部清单区（40%高度），左对齐，条目间距均等
- 底部CTA区（20%高度），大号醒目
- 整体留白 ≥ 30%

[Technical]
flat graphic design, brand identity poster, screen printing silkscreen style,
bold CTA typography, iconic brand symbol, limited 3-color palette,
vintage poster texture, high contrast, 8K resolution, 3:4 portrait ratio
```

---

#### 风格三：手账手绘信息图风格提示词

**风格说明**：手账日记感 + 莫兰迪三色系 + 虚线连接 + 几何卡通角色。所有视觉参数严格固定（参见全套视觉规格锚点），每页唯一的变量是**信息图类型**和**内容**。风格高度一致，适合需要"统一系列感"的笔记套图。

---

**固定参数完整清单（16项，全部禁止变更）**

| 参数 | 固定值 | 说明 |
|-----|-------|------|
| 背景色 | #FAF9F6（Warm Ivory）| 禁止渐变/图案/纹理 |
| 主色调 | #9FA8DA 莫兰迪蓝 + #A5D6A7 莫兰迪绿 + #EF9A9A 莫兰迪粉 | 模块填充，透明度20-30% |
| 强调色 | #424242（Deep Charcoal）| 标题文字/关键数字/重要边框 |
| 线条颜色 | #757575（Medium Gray）| |
| 线条宽度 | 2.5px，透明度85%，抖动15%振幅 | 禁止粗线(>4px)、彩色线 |
| 虚线样式 | 8px实线 + 6px空白，2px宽，圆角端点 | 所有模块连接必须用此样式 |
| 框线 | 2px，#757575，透明度90%，不规则圆角5-8px，**20%缺口**（手绘感）| 禁止完全闭合边框 |
| 标题字体 | 手写风格，#424242，画布高度6%，左对齐，轻度抖动5-8% | 固定位置：顶部左对齐，距上边缘8% |
| 正文字体 | 手写风格，#424242，画布高度2.5%，左对齐，行距1.8x，抖动3-5% | 模块内距左边缘15%，距上边缘12% |
| 标注字体 | 手写风格，#424242，画布高度1.8%，细体，抖动3-5% | 靠近元素右下角或下方 |
| 角色插图 | 圆形头+几何身体，#757575线条，莫兰迪色填充30-40%，模块高度20-25%，**仅3种动作**（思考/指向/展示）| 位置固定：模块右上角 |
| 道具/图标 | #757575线条，2px，莫兰迪色填充25-35%，模块高度15-20%，左侧固定位置 | 禁止彩色填充图标 |
| 模块间距 | 画布高度5%（垂直）| 垂直排列，禁止横向排列 |
| 模块尺寸 | 高度：画布高度15-18%；宽度：画布宽度70% | |
| 留白 | 整体30%；左右边缘12%；上边缘8%；下边缘10% | |
| 分辨率/比例 | 8K (7680×5760)，3:4竖版 | |

**应用场景对应主色调选择（唯一允许的差异化）**：
- 金融知识科普 → 莫兰迪蓝 #9FA8DA 为主色
- 商业报告/策略 → 莫兰迪绿 #A5D6A7 为主色
- 生活指导/个人 → 莫兰迪粉 #EF9A9A 为主色

---

> ⚠️ **重要提示**：提示词中所有颜色代码（#FAF9F6 等）和百分比数值仅为 AI 生成的内部参数，**切勿渲染为图像中可见文字**。

##### 封面页提示词模板

```
CRITICAL INSTRUCTIONS:
1. All color codes (e.g., #FAF9F6, #9FA8DA, #424242, #757575) are internal parameters ONLY - DO NOT render them as visible text in the image
2. All percentage/pixel values are internal parameters ONLY - DO NOT render them as visible text in the image
3. Color codes specify the colors to USE when generating, NOT text to display
4. Generate a hand-drawn style infographic with proper visual elements, NOT text listings of color codes or numbers

Generate a hand-drawn journal-style infographic, vertical 3:4 ratio, 8K resolution (7680×5760), ultra high definition, sharp focus, photorealistic render quality, print quality

[Content Design]
- Infographic Type: Mind Map (Center Radial) — center node: "{核心主题}", radiate 3-5 key sub-themes outward
- Main Title: "{标题}" (large handwritten font, top-left, 8% from top edge)
- Core Quote: "{金句}" (medium size, inside center circle/oval)
- Sub-theme Nodes: {子主题1} / {子主题2} / {子主题3} (connected from center with dashed lines)

[Fixed Visual Parameters - DO NOT change ANY of these]
BACKGROUND: Solid warm ivory (no gradient, no pattern, no texture)

COLOR SYSTEM (3 Morandi colors + 1 accent, nothing else):
- Module fills: soft Morandi blue / soft Morandi green / soft Morandi pink — each at 20-30% opacity
- Text & borders: deep charcoal color (titles, body, outlines)
- Lines: medium gray color

TYPOGRAPHY (strictly proportional):
- Title: handwritten style, large (6% of canvas height), left-aligned, slight jitter 5-8%, positioned top-left at 8% from top
- Body text: handwritten style, medium (2.5% of canvas height), left-aligned, line-height 1.8x, jitter 3-5%
- Caption/annotation: handwritten style, small (1.8% of canvas height), light weight, jitter 3-5%, placed near element's bottom-right

LINES: medium gray, 2.5px width, 85% opacity, 15% amplitude jitter (never perfectly straight, never colorful)

DASHED CONNECTORS: 8px solid + 6px gap pattern, 2px width, rounded ends, medium gray (all connections use this style, no solid lines)

MODULE BORDERS: 2px width, medium gray, 90% opacity, irregular rounded corners 5-8px, 20% corner gap retained (hand-drawn feel, NOT fully closed borders)

CHARACTER ILLUSTRATION: Simple geometric cartoon (circle head + geometric body shapes), placed top-right of central module, THINKING POSE (hand on chin), filled with Morandi colors at 30-40% opacity, size = 20-25% of module height

MODULE SIZES: each module height = 15-18% of canvas height; each module width = 70% of canvas width

SPACING: module-to-module vertical gap = 5% canvas height; title-to-first-module gap = 6% canvas height

WHITESPACE: 30% overall; left/right margins = 12% canvas width; top = 8%; bottom = 10%

READING FLOW: top-left to bottom-right; connection arrows point downward at 45°; vertical arrangement only (no horizontal layout)

STYLE: hand-drawn journal style with consistent jitter effect, no gradients, no mixed styles, no photorealistic elements

[Technical]
hand-drawn journal style, consistent jitter effect, no gradients, no color codes as visible text,
no percentages as visible text, Morandi color palette, dashed line connections, geometric cartoon character,
irregular corner gaps in module borders, 8K resolution, 3:4 aspect ratio, photorealistic render quality, print quality typography
```

##### 内容页提示词模板

```
CRITICAL INSTRUCTIONS:
1. All color codes (e.g., #FAF9F6, #9FA8DA, #424242, #757575) and percentage/pixel values are internal parameters ONLY - DO NOT render as visible text in the image
2. Color codes specify colors to USE when generating, NOT text to display
3. Generate a hand-drawn style infographic with proper visual elements, NOT text listings of color codes or numbers

Generate a hand-drawn journal-style infographic, vertical 3:4 ratio, 8K resolution (7680×5760), ultra high definition, sharp focus, photorealistic render quality, print quality

[Content Design]
- Infographic Type: {选择与内容最匹配的类型，从36种中选一，如清单图/流程图/四象限图/鱼骨图/汉堡图...} — see infographic type selection table
- Page Title: "{标题}" (medium handwritten font, top-left, 12% from top)
- Key Points (arranged according to selected infographic type):
  ① {要点1} — {简短解释}
  ② {要点2} — {简短解释}
  ③ {要点3} — {简短解释，如需要}
  ④ {要点4} — {简短解释，如需要}
- Data/Case: {关键数据或案例，如有} — place in data box at bottom if present
- Character Illustration: geometric cartoon character, pose = {根据内容选择：POINTING POSE（手指指向）或 SHOWING POSE（双手展示）}, positioned top-right of relevant module

[Fixed Visual Parameters - DO NOT change ANY of these]
BACKGROUND: Solid warm ivory color (no gradient, no pattern, no texture)

COLOR SYSTEM (3 Morandi colors + 1 accent, nothing else):
- Module fills: soft Morandi blue OR soft Morandi green OR soft Morandi pink (each module uses ONE color) — at 20-30% opacity
- Text & borders: deep charcoal color
- Lines: medium gray color

TYPOGRAPHY (strictly proportional):
- Title: handwritten style, medium (2.5% of canvas height), left-aligned, slight jitter 3-5%, positioned top-left at 12% from top edge
- Body text: handwritten style, regular (1.8% of canvas height for body; variable for points), left-aligned, line-height 1.8x, jitter 3-5%
- Numbers/bullets: medium gray, 2px width, positioned left of each point

LINES: medium gray, 2.5px width, 85% opacity, 15% amplitude jitter (never perfectly straight)

DASHED CONNECTORS BETWEEN MODULES: 8px solid + 6px gap pattern, 2px width, rounded ends, medium gray (all inter-module connections use this style, no solid lines)

MODULE BORDERS: 2px width, medium gray, 90% opacity, irregular rounded corners 5-8px, 20% corner gap retained (hand-drawn feel, NOT fully closed borders)

CHARACTER ILLUSTRATION: Simple geometric cartoon (circle head + geometric body shapes), placed top-right of relevant module, POINTING POSE or SHOWING POSE, filled with Morandi colors at 30-40% opacity, size = 20-25% of module height

PROPS/ICONS: Simple line icons only, medium gray lines 2px width, Morandi color fills at 25-35% opacity, size = 12-15% of module height, positioned left of related text (禁止彩色填充图标)

MODULE SIZES: each module height = 15-18% of canvas height; each module width = 70% of canvas width

SPACING: module-to-module vertical gap = 5% canvas height; text-to-module-border gap = 2% canvas height

WHITESPACE: 30% overall; left/right margins = 12% canvas width; top = 12%; bottom = 10%

READING FLOW: top-left to bottom-right; connection arrows point downward at 45°; vertical arrangement only (no horizontal layout)

LAYOUT: vertical arrangement, modules stacked top to bottom with consistent spacing

STYLE: hand-drawn journal style with consistent jitter effect, no gradients, no mixed styles, no photorealistic elements

[Technical]
hand-drawn journal style, dashed line connections, Morandi color palette, geometric cartoon character,
simple line icons (no colored fills), irregular corner gaps in module borders, no gradients,
no color codes as visible text, 8K resolution, 3:4 aspect ratio, photorealistic render quality,
print quality typography, consistent jitter effect, proportional font sizing
```

##### 尾页提示词模板

```
CRITICAL INSTRUCTIONS:
1. All color codes (e.g., #FAF9F6, #9FA8DA, #424242, #757575) and percentage/pixel values are internal parameters ONLY - DO NOT render as visible text in the image
2. Color codes specify colors to USE when generating, NOT text to display
3. Generate a hand-drawn style infographic with proper visual elements, NOT text listings of color codes or numbers

Generate a hand-drawn journal-style infographic, vertical 3:4 ratio, 8K resolution (7680×5760), ultra high definition, sharp focus, photorealistic render quality, print quality

[Content Design]
- Infographic Type: Checklist (list format) — highlight benefit items with dashed connectors
- Main CTA: "开户[券商名称]证券" (large handwritten font, top section, paired with upward arrow icon)
- Benefits List (each item with simple hand-drawn line icon):
  ① 新客理财 8.18% 预期收益率 (配金币/图表图标)
  ② Level-2 高速行情 90 天免费 (配折线图/雷达图标)
  ③ 专业投顾一对一服务 (配人物/握手图标)
  ④ 增值量化指标工具礼包 (配工具/齿轮图标)
- Guide Text: "求赞收藏关注 · 私信领资料包" (small font, second-to-last section from bottom)
- Brand Identity: "@[券商名称]证券财富管理" (very bottom, handwritten font)
- Character Illustration: geometric cartoon character, SHOWING POSE (both hands presenting), positioned right of CTA section

[Fixed Visual Parameters - DO NOT change ANY of these]
BACKGROUND: Solid warm ivory color (no gradient, no pattern, no texture)

COLOR SYSTEM (3 Morandi colors + 1 accent, nothing else):
- CTA header module fill: soft Morandi pink (for brand emphasis)
- Benefit list module fill: soft Morandi blue
- Footer module fill: soft Morandi green
- Text & borders: deep charcoal color
- Lines: medium gray color

TYPOGRAPHY (strictly proportional):
- CTA Title: handwritten style, large (8% of canvas height), bold, left-aligned, jitter 5-8%, positioned top section at 8% from top edge
- Benefits list items: handwritten style, medium (2% of canvas height), left-aligned, line-height 1.8x, jitter 3-5%
- Guide Text: handwritten style, small (1.5% of canvas height), left-aligned, jitter 3-5%
- Brand: handwritten style, small (1.5% of canvas height), centered or left-aligned, jitter 3-5%

LINES: medium gray, 2.5px width, 85% opacity, 15% amplitude jitter (never perfectly straight, never colorful)

DASHED CONNECTORS BETWEEN BENEFIT ITEMS: 8px solid + 6px gap pattern, 2px width, rounded ends, medium gray (connect benefit items vertically, no solid lines)

MODULE BORDERS: 2px width, medium gray, 90% opacity, irregular rounded corners 5-8px, 20% corner gap retained (hand-drawn feel, NOT fully closed borders)

CHARACTER ILLUSTRATION: Simple geometric cartoon (circle head + geometric body shapes), SHOWING POSE (both hands presenting gesture), placed right of CTA title section, filled with Morandi colors at 30-40% opacity, size = 20-25% of module height

BENEFIT ITEM ICONS: Simple hand-drawn line icons (coins, chart line, person, tools), medium gray lines 2px width, NO color fills, positioned left of each benefit text, size = 10-12% of module height

MODULE SIZES: CTA section = 25% of canvas height; Benefits list = 50%; Guide + Brand = 25%

SPACING: vertical gap between modules = 5% canvas height; text-to-border gap = 2% canvas height; gap between benefit items = 3%

WHITESPACE: 30% overall; left/right margins = 12% canvas width; top = 8%; bottom = 10%

READING FLOW: top-left to bottom-right; CTA → Benefits → Guide → Brand; downward flow with 45° arrows if needed; vertical arrangement only (no horizontal layout)

STYLE: hand-drawn journal style with consistent jitter effect, no gradients, no mixed styles, no photorealistic elements, simple line icons (no colored fills for icons)

[Technical]
hand-drawn journal style, checklist layout, Morandi color palette, hand-drawn line icons (no colored fills),
dashed connectors, geometric cartoon character, no gradients, irregular corner gaps in module borders,
no color codes as visible text, 8K resolution, 3:4 aspect ratio, photorealistic render quality,
print quality typography, consistent jitter effect, proportional font sizing
```

[Fixed Visual Parameters - DO NOT change any of these]
- Background: solid warm ivory color
- Module fills: Morandi pink for CTA header, Morandi blue for benefit list, Morandi green for footer
- All text: deep charcoal color, handwritten style, left-aligned
- Lines & dashed connectors: medium gray, 2.5px / 2px, consistent pattern
- Benefit item icons: hand-drawn line icons, medium gray, 2px width
- Character: geometric cartoon, showing pose, Morandi colors 30-40% opacity
- Overall whitespace: 30%

[Technical]
hand-drawn journal style, checklist layout, Morandi color palette, hand-drawn icons,
dashed connectors, geometric cartoon character, no gradients, no color codes as visible text,
8K resolution, 3:4 aspect ratio, photorealistic render quality, print quality
```

---
1. 以上提示词为英文核心指令，可直接粘贴到 Midjourney（在末尾加 `--ar 3:4 --style raw`）
2. 如使用中文绘图工具（即梦、可灵），可将 `[Technical]` 部分翻译为中文后使用
3. 每页三种风格提示词，建议**封面页三种都生成**后对比选择一种风格，其余各页沿用同一风格以保持视觉统一
4. **手账手绘信息图风格**特别适合即梦/可灵，参数明确、风格固定，生成效果最稳定

---

### Step 4: 输出全套提示词

**输出顺序**：
1. 封面页：[视觉风格A]风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词
2. 内容页1：[视觉风格A]风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词
3. 内容页2：[视觉风格A]风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词
4. 内容页3：[视觉风格A]风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词
5. ...（根据实际页数）
6. 尾页：[视觉风格A]风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词

**输出要求**：
- 每页三种风格的提示词都要完整输出
- 提示词中的 {变量} 全部替换为实际内容（不保留占位符）
- Mondo 风格按内容主题自动选择最适合的色彩方案
- **手账手绘信息图风格**：视觉参数不变，只替换内容变量和信息图类型
- 在最后添加使用说明（如何在不同绘图工具中使用）

---

## 输出格式

### Phase 3输出示例

```markdown
## Phase 3: 多页信息图提示词生成结果

### 笔记图总览
**总页数**：7页
- 封面页：1张
- 内容页：5张
- 尾页：1张

---

### 第1张：封面页图像提示词

**对应内容**：[Phase 2的封面页文字]

**设计说明（[视觉风格A]风格）**：莫兰迪色系手绘，中心辐射图
**设计说明（Mondo风格）**：Saul Bass极简几何，深蓝+金色
**设计说明（手账手绘信息图风格）**：思维导图，莫兰迪三色，几何角色插图思考状

---

#### 🖌️ 风格一：[视觉风格A]格

[填入完整的[视觉风格A]封面页提示词，变量全部替换为实际内容]

---

#### 🎨 风格二：Mondo 大师海报风格

[填入完整的Mondo封面页提示词，变量全部替换为实际内容]

---

#### 📓 风格三：手账手绘信息图风格

[填入完整的手账手绘信息图封面页提示词，变量全部替换为实际内容，信息图类型填入：思维导图（中心辐射图）]

---

### 第2张：笔记页一图像提示词

**对应内容**：[Phase 2的笔记页一文字]

**设计说明（[视觉风格A]风格）**：清单图，列出3个要点
**设计说明（Mondo风格）**：Reid Miles排版风格，高对比度图示
**设计说明（手账手绘信息图风格）**：[根据内容选择最匹配的类型，如：线性流程图 / 四象限图 / 阶梯图]

---

#### 🖌️ 风格一：[视觉风格A]格

[填入完整的[视觉风格A]内容页提示词，变量全部替换为实际内容]

---

#### 🎨 风格二：Mondo 大师海报风格

[填入完整的Mondo内容页提示词，变量全部替换为实际内容]

---

#### 📓 风格三：手账手绘信息图风格

[填入完整的手账手绘信息图内容页提示词，变量全部替换为实际内容，信息图类型填入选定类型]

---

[以此类推...]

---

### 第7张：尾页图像提示词

**对应内容**：[Phase 2的尾页文字]

**设计说明（[视觉风格A]风格）**：清单图，突出新客权益
**设计说明（Mondo风格）**：Peter Saville极简品牌风格
**设计说明（手账手绘信息图风格）**：清单图，莫兰迪粉色CTA区，角色展示状

---

#### 🖌️ 风格一：[视觉风格A]格

[填入完整的[视觉风格A]尾页提示词]

---

#### 🎨 风格二：Mondo 大师海报风格

[填入完整的Mondo尾页提示词]

---

#### 📓 风格三：手账手绘信息图风格

[填入完整的手账手绘信息图尾页提示词]

---

### 使用说明

**选择风格建议**：
- [视觉风格A]格：亲切自然，适合知识科普类、生活类笔记
- Mondo 海报风格：视觉冲击力强，适合热点类、开户推广类笔记
- 手账手绘信息图风格：系列感最强、参数最固定，适合需要"高度统一套图"的金融科普类笔记；支持36种信息图类型智能适配，适合内容结构多样的多页笔记
- **建议**：先生成封面三种风格对比，选定一种后全套沿用同一风格

**如何使用提示词**：
- **Midjourney**：复制提示词，末尾加 `--ar 3:4 --style raw --v 6`
- **DALL·E 3**：直接粘贴（中英混合提示词均可）
- **即梦 / 可灵（字节/快手）**：将英文 [Technical] 部分翻译为中文后使用
- **Stable Diffusion**：使用 [Technical] 部分作为正向提示词

**保存建议**：
- 保存所有提示词文件以便后续调整
- 文件名格式：`笔记标题_页码_风格.md`
- 生成图片后按页码顺序命名便于查找
```

---

## 提示词质量检查

生成提示词后检查以下项目：

**内容完整性**：
- [ ] 所有 {变量} 已替换为实际内容（封面/内容/尾页）
- [ ] 每页均提供了三种风格的提示词
- [ ] Mondo 风格已根据主题选择了合适色彩方案
- [ ] 手账手绘信息图风格每页已选定信息图类型（从36种中选择）
- [ ] 尾页的[券商名称]品牌信息准确无误

**提示词质量**：
- [ ] [视觉风格A]风格：包含背景色、主色调、文字色、线条参数
- [ ] Mondo 风格：包含风格流派、色板、设计指令、Technical 标签
- [ ] 手账手绘信息图风格：包含 CRITICAL INSTRUCTIONS、Fixed Visual Parameters、Technical 标签
- [ ] 每页提示词有明确的内容设计和布局说明

**一致性**：
- [ ] 同套笔记的各页 Mondo 风格使用了相同的色彩方案
- [ ] 各页 [视觉风格A]风格使用了相同的色系
- [ ] 手账手绘信息图风格各页视觉参数完全一致（只有内容和信息图类型不同）
- [ ] 所有提示词标注了 3:4 竖版比例和 8K 分辨率

### 根据内容类型选择

| 内容类型 | 推荐的信息图类型 | 适用页面 |
|---------|----------------|---------|
| 主题概述 | 中心辐射图、大标题图 | 封面页 |
| 要点列表 | 清单图、步骤图 | 内容页 |
| 对比分析 | 对比表、天平图 | 内容页 |
| 流程说明 | 流程图、循环图 | 内容页 |
| 策略方法 | 四象限图、桥梁图 | 内容页 |
| 原因分析 | 鱼骨图、冰山图 | 内容页 |
| 概念解释 | 汉堡图、洋葱图 | 内容页 |
| 行动引导 | 清单图、中心辐射图 | 尾页 |

---

## 优化技巧

### 提升视觉吸引力

1. **封面页**：
   - 使用大号字体突出标题
   - 核心观点用不同颜色高亮
   - 添加简单但醒目的图标

2. **内容页**：
   - 每个要点用不同颜色的框区分
   - 使用虚线或箭头展示关联
   - 数据用大号字体突出显示

3. **尾页**：
   - 行动召唤使用大号醒目字体
   - 权益要点用图标+文字
   - 品牌标识放在显眼位置

### 保持风格一致

1. **统一配色**：所有页使用相同的配色方案
2. **统一字体**：所有页使用相同的手写字体风格
3. **统一布局**：保持标题、内容、装饰的区域比例一致
4. **统一线条**：线条宽度、虚线样式完全一致

---

## 常见问题处理

### Q: 某页内容太多，一页图放不下怎么办？

**A**：
- 提炼最核心的3-5个要点
- 删减次要细节
- 将详细内容放在笔记正文
- 图像只起概括和吸引作用

### Q: 某页内容太少，图像太空怎么办？

**A**：
- 增加装饰性图标
- 放大字体增加视觉分量
- 增加留白营造高级感
- 添加数据可视化元素

### Q: 如何确保所有图像风格统一？

**A**：
- 严格遵守固定风格参数
- 使用相同的提示词模板
- 生成后检查风格一致性
- 如不一致，调整参数重新生成

---

## 更新日志

- **2026-01-22**：初始版本，建立多页信息图生成指南
