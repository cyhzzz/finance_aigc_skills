# Phase 3: 多页信息图生成指南

**目标**：为小红书笔记的每一页生成对应的图像提示词（AI绘图提示词，不直接出图）

> **重要说明**：本指南输出的是**图像生成提示词**，不直接调用画图工具。用户收到提示词后，可自行粘贴到 Midjourney / DALL·E / Stable Diffusion / 即梦 / 可灵等 AI 绘图工具中生成图像。
>
> 每页提供**三种风格**的提示词供选择：
> 1. **baoyu 手绘风格**：莫兰迪色系、手绘线条感、适合小红书风格
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
- **品牌标识**：申万宏源品牌元素
- **联系方式**：私信、企业微信等

**布局建议**：
```
┌─────────────────────┐
│  [行动召唤]         │
│  "开户申万宏源"     │
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
│  @申万宏源证券      │
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

■ baoyu 手绘风格
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

> **每页均输出三组提示词**：① baoyu 手绘风格  ② Mondo 大师海报风格  ③ 手账手绘信息图风格
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

#### 风格一：baoyu 手绘风格提示词

##### 封面页提示词模板

```
手绘风格竖版信息图，3:4比例，8K分辨率

[内容设计]
- 主标题："{标题}"（大号手写字体，顶部居中偏左）
- 核心观点："{金句}"（中号字体，中部突出显示）
- 装饰元素：简单的投资/理财相关图标（底部）

[风格参数]
- 背景色：#FAF9F6
- 主色调：#9FA8DA、#A5D6A7、#EF9A9A
- 文字色：#424242
- 线条：2.5像素，85%透明度
- 字体：手写风格，左对齐

[布局]
- 标题区域：占画布上部20%
- 核心观点区域：占画布中部50%
- 装饰区域：占画布下部30%
- 整体留白30%
```

##### 内容页提示词模板

```
手绘风格竖版信息图，3:4比例，8K分辨率

[内容设计]
- 页面标题："{标题}"（中号手写字体）
- 要点清单：
  ● {要点1} - {简短解释}
  ● {要点2} - {简短解释}
  ● {要点3} - {简短解释}
- 数据/案例框：{关键数据或案例}（如有）

[风格参数]
- 背景色：#FAF9F6
- 主色调：#9FA8DA、#A5D6A7、#EF9A9A
- 文字色：#424242
- 线条：2.5像素，85%透明度
- 虚线连接：8像素实线+6像素空白

[布局]
- 标题区域：占画布上部15%
- 要点区域：占画布中部70%（垂直排列）
- 数据区域：占画布下部15%（如有）
- 每个要点之间间距：5%
```

##### 尾页提示词模板

```
手绘风格竖版信息图，3:4比例，8K分辨率

[内容设计]
- 行动召唤："开户申万宏源证券"（大号手写字体）
- 权益清单：
  ● 新客理财8.18%收益率
  ● Level-2高速行情90天
  ● 专业投顾服务
  ● 增值指标工具
- 引导语：求赞收藏关注，私信领资料包
- 品牌：@申万宏源证券财富管理

[风格参数]
- 背景色：#FAF9F6
- 主色调：使用申万宏源品牌色（可调整）
- 文字色：#424242
- 线条：2.5像素，85%透明度

[布局]
- 行动召唤区域：占画布上部25%
- 权益清单区域：占画布中部50%
- 引导语区域：占画布下部15%
- 品牌标识区域：占画布底部10%
```

---

#### 风格二：Mondo 大师海报风格提示词

**风格说明**：Mondo 风格源于专业演出海报设计，核心特征是极简主义象征、丝网印刷美学、有限色彩平面色块（2-5色）、大胆配色与强烈对比。AI 会根据内容主题自动选择最合适的设计师流派（Saul Bass 极简几何 / Olly Moss 负空间 / Kilian Eng 未来主义等）。

**配色智能适配规则**：
- 金融/投资内容 → 深蓝 + 金色 + 白色（专业权威感）
- 科普/教育内容 → 米色 + 深红 + 黑（经典知性感）
- 热点/趋势内容 → 赛博蓝 + 霓虹黄（现代冲击感）
- 生活理财内容 → 暖黄 + 橙红 + 米白（亲近生活感）

##### 封面页提示词模板

```
Mondo poster design style, vertical 3:4 ratio, 8K resolution

[Visual Concept]
主题："{核心主题关键词}"
概念化提炼：将主题转化为一个强烈的视觉象征符号

[Design Directives]
- 风格流派：Saul Bass极简几何风格 OR Olly Moss负空间双关设计（根据主题自动选择）
- 丝网印刷美学：仅使用3种颜色的平面色块，无渐变
- 主视觉：一个代表核心主题的极简象征符号（如：投资→上升箭头+圆形构成的公牛图形）
- 标题字体：手绘复古装饰风格，"{标题文字}"
- 副标题：极小号，底部区域

[Color Palette - 根据主题智能选择]
- 深色底：深海军蓝 #1B2A4A 或 炭黑 #1A1A1A
- 主强调色：金色 #F2C744 或 火焰橙 #E85D04
- 留白色：奶白 #FAF5E4

[Layout Principles]
- 极简构图：主视觉占据画面60-70%
- 强烈的明暗对比（明度差 > 80%）
- 手绘字体标题，居于视觉下方1/3区域
- 整体留白 ≥ 40%，营造高级感
- 禁止使用渐变、阴影、3D效果

[Technical]
flat graphic design, screen printing effect, limited color palette, no gradients,
high contrast, iconic minimalism, hand-lettered title, vintage poster texture
```

##### 内容页提示词模板

```
Mondo informational poster, vertical 3:4 ratio, 8K resolution

[Visual Concept]
主题："{本页章节标题}"
视觉化：将"{要点1}/{要点2}/{要点3}"提炼为图示

[Design Directives]
- 风格：Reid Miles爵士乐海报风格（高对比度网格排版）
- 以视觉化图示为主（图标+连接线+数字编号），辅以极简文字
- 章节标题使用大号几何无衬线字体，占顶部20%
- 要点用图标+短文字展现（每个要点 ≤ 8字）
- 底部加入页码标注："{当前页} / {总页数}"

[要点内容]
  ① {要点1}
  ② {要点2}
  ③ {要点3}

[Color Palette]
- 背景：深色底（同封面主色调保持一致）
- 要点图标：使用主强调色
- 文字：奶白色 #FAF5E4
- 分隔线：主强调色 30% 透明度

[Technical]
flat graphic design, bold typography, iconographic elements, numbered list visual,
screen printing style, no gradients, vintage poster aesthetic, high legibility
```

##### 尾页提示词模板

```
Mondo promotional poster, vertical 3:4 ratio, 8K resolution

[Visual Concept]
主题："开户引导 - 申万宏源证券"
核心象征：向上增长的箭头 + 品牌圆形徽章

[Design Directives]
- 风格：Peter Saville极简主义 + Factory Records风格
- 顶部大号几何图形（品牌感symbol）
- 中部：权益清单，用极简图标+一行字排列
  ● 新客理财 8.18% 收益率
  ● Level-2 行情 90天
  ● 专业投顾服务
  ● 增值指标工具
- 底部：强烈的行动召唤文字 "立即开户 · 申万宏源证券"
- 品牌色系：深蓝 #1B2A4A + 金色 #F2C744

[Color Palette]
- 背景：深海军蓝 #1B2A4A
- 主文字与图标：金色 #F2C744
- 辅助文字：奶白 #FAF5E4

[Technical]
flat graphic design, brand identity poster, screen printing style, bold CTA typography,
iconic brand symbol, limited color palette, vintage poster texture, high contrast
```

---

#### 风格三：手账手绘信息图风格提示词

**风格说明**：手账日记感 + 莫兰迪三色系 + 虚线连接 + 几何卡通角色。所有视觉参数严格固定（参见全套视觉规格锚点），每页唯一的变量是**信息图类型**和**内容**。风格高度一致，适合需要"统一系列感"的笔记套图。

> ⚠️ **重要提示**：提示词中所有颜色代码（#FAF9F6 等）和百分比数值仅为 AI 生成的内部参数，**切勿渲染为图像中可见文字**。

##### 封面页提示词模板

```
CRITICAL INSTRUCTIONS:
1. All color codes (e.g., #FAF9F6, #9FA8DA, #424242) are internal parameters ONLY - DO NOT render them as visible text in the image
2. All percentage/pixel values are internal parameters ONLY - DO NOT render them as visible text in the image
3. Generate a hand-drawn style infographic with proper visual elements, NOT text listings of color codes

Generate a hand-drawn journal-style infographic, vertical 3:4 ratio, 8K resolution (7680×5760), ultra high definition, sharp focus

[内容设计]
- 信息图类型：思维导图（中心辐射图）—— 中心放"{核心主题}"，向外辐射3-5个关键子主题
- 主标题："{标题}"（大号手写字体，左对齐，顶部距上边缘8%）
- 核心金句："{金句}"（中号，中心圆形框内显示）
- 子主题节点：{子主题1} / {子主题2} / {子主题3}（用虚线从中心向外连接）

[Fixed Visual Parameters - DO NOT change any of these]
- Background: solid warm ivory color (no gradient, no pattern, no texture)
- Module fills: soft Morandi blue, soft Morandi green, soft Morandi pink — opacity 20-30%
- All text: deep charcoal color, handwritten style, left-aligned, slight jitter 5-8%
- Lines: medium gray, 2.5px width, 85% opacity, slight jitter effect (15% amplitude)
- Dashed connectors: 8px solid + 6px gap, 2px width, medium gray, rounded ends
- Module borders: 2px, medium gray, 90% opacity, irregular rounded corners, 20% corner gap
- Character illustration: simple geometric cartoon (circle head + geometric body), placed top-right of central module, "thinking pose" (hand on chin), filled with Morandi colors at 30-40% opacity
- Title position: top-left, 8% from top edge
- Overall whitespace: 30%, left/right margins 12%, top 8%, bottom 10%
- Module size: each module height 15-18% of canvas, width 70% of canvas

[Technical]
hand-drawn journal style, consistent jitter effect, no gradients, no color codes as visible text,
no percentages as visible text, Morandi color palette, dashed line connections, geometric cartoon character,
8K resolution, 3:4 aspect ratio, photorealistic render quality, print quality
```

##### 内容页提示词模板

```
CRITICAL INSTRUCTIONS:
1. All color codes and percentage values are internal parameters ONLY - DO NOT render as visible text
2. Generate visual infographic content, NOT technical parameter listings

Generate a hand-drawn journal-style infographic, vertical 3:4 ratio, 8K resolution (7680×5760), ultra high definition, sharp focus

[内容设计]
- 信息图类型：{根据内容特性从36种中选择，参见类型速查表}（例：清单图 / 流程图 / 四象限图…）
- 页面标题："{标题}"（中号手写字体，左对齐，顶部）
- 要点内容（按所选图示类型布局）：
  ① {要点1} - {简短解释}
  ② {要点2} - {简短解释}
  ③ {要点3} - {简短解释（如有）}
- 数据/案例：{关键数据或案例（如有）}
- 角色插图：几何卡通人物，放于{根据内容选择：指向状 / 展示状}，置于模块右上角

[Fixed Visual Parameters - DO NOT change any of these]
- Background: solid warm ivory color (no gradient, no pattern)
- Module fills: soft Morandi blue / green / pink — opacity 20-30%, each module uses one color
- All text: deep charcoal color, handwritten style, left-aligned
- Lines: medium gray, 2.5px, 85% opacity, 15% jitter
- Dashed connectors between modules: 8px+6px pattern, 2px, rounded ends
- Module borders: 2px, medium gray, slight corner gap for hand-drawn feel
- Character illustration: geometric cartoon, 3 fixed poses (thinking/pointing/showing), Morandi filled 30-40%
- Layout: vertical arrangement, modules stacked top to bottom
- Each module height: 15-18% canvas height; module width: 70% canvas width
- Module vertical spacing: 5% canvas height
- Overall whitespace: 30%

[Technical]
hand-drawn journal style, dashed line connections, Morandi color palette, geometric cartoon character,
no gradients, no color codes as visible text, 8K resolution, 3:4 aspect ratio,
photorealistic render quality, print quality typography, consistent jitter effect
```

##### 尾页提示词模板

```
CRITICAL INSTRUCTIONS:
1. All color codes and percentage values are internal parameters ONLY - DO NOT render as visible text
2. Generate visual infographic content, NOT technical parameter listings

Generate a hand-drawn journal-style infographic, vertical 3:4 ratio, 8K resolution (7680×5760), ultra high definition, sharp focus

[内容设计]
- 信息图类型：清单图（列表式）—— 突出权益要点，用虚线连接各权益条目
- 主行动召唤："开户申万宏源证券"（大号手写字体，顶部，配向上箭头图标）
- 权益清单（每条加手绘图标）：
  ① 新客理财 8.18% 预期收益率（配金币图标）
  ② Level-2 高速行情 90 天免费（配折线图图标）
  ③ 专业投顾一对一服务（配人物图标）
  ④ 增值量化指标工具礼包（配工具图标）
- 引导语："求赞收藏关注 · 私信领资料包"（小号，底部倒数第二区域）
- 品牌标识："@申万宏源证券财富管理"（最底部，手写字体）
- 角色插图：几何卡通人物，展示状（双手展示），置于标题区域右侧

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
1. 封面页：baoyu 风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词
2. 内容页1：baoyu 风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词
3. 内容页2：baoyu 风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词
4. 内容页3：baoyu 风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词
5. ...（根据实际页数）
6. 尾页：baoyu 风格提示词 + Mondo 风格提示词 + 手账手绘信息图风格提示词

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

**设计说明（baoyu风格）**：莫兰迪色系手绘，中心辐射图
**设计说明（Mondo风格）**：Saul Bass极简几何，深蓝+金色
**设计说明（手账手绘信息图风格）**：思维导图，莫兰迪三色，几何角色插图思考状

---

#### 🖌️ 风格一：baoyu 手绘风格

[填入完整的baoyu封面页提示词，变量全部替换为实际内容]

---

#### 🎨 风格二：Mondo 大师海报风格

[填入完整的Mondo封面页提示词，变量全部替换为实际内容]

---

#### 📓 风格三：手账手绘信息图风格

[填入完整的手账手绘信息图封面页提示词，变量全部替换为实际内容，信息图类型填入：思维导图（中心辐射图）]

---

### 第2张：笔记页一图像提示词

**对应内容**：[Phase 2的笔记页一文字]

**设计说明（baoyu风格）**：清单图，列出3个要点
**设计说明（Mondo风格）**：Reid Miles排版风格，高对比度图示
**设计说明（手账手绘信息图风格）**：[根据内容选择最匹配的类型，如：线性流程图 / 四象限图 / 阶梯图]

---

#### 🖌️ 风格一：baoyu 手绘风格

[填入完整的baoyu内容页提示词，变量全部替换为实际内容]

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

**设计说明（baoyu风格）**：清单图，突出新客权益
**设计说明（Mondo风格）**：Peter Saville极简品牌风格
**设计说明（手账手绘信息图风格）**：清单图，莫兰迪粉色CTA区，角色展示状

---

#### 🖌️ 风格一：baoyu 手绘风格

[填入完整的baoyu尾页提示词]

---

#### 🎨 风格二：Mondo 大师海报风格

[填入完整的Mondo尾页提示词]

---

#### 📓 风格三：手账手绘信息图风格

[填入完整的手账手绘信息图尾页提示词]

---

### 使用说明

**选择风格建议**：
- baoyu 手绘风格：亲切自然，适合知识科普类、生活类笔记
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
- [ ] 尾页的申万宏源品牌信息准确无误

**提示词质量**：
- [ ] baoyu 风格：包含背景色、主色调、文字色、线条参数
- [ ] Mondo 风格：包含风格流派、色板、设计指令、Technical 标签
- [ ] 手账手绘信息图风格：包含 CRITICAL INSTRUCTIONS、Fixed Visual Parameters、Technical 标签
- [ ] 每页提示词有明确的内容设计和布局说明

**一致性**：
- [ ] 同套笔记的各页 Mondo 风格使用了相同的色彩方案
- [ ] 各页 baoyu 风格使用了相同的色系
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
