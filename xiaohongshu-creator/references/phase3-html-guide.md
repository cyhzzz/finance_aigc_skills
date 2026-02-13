# Phase 3 HTML模式详细指南

## 概述

本指南详细说明Phase 3的HTML代码模式（模式B），该模式基于预制的HTML模板生成小红书笔记预览页面，采用Vital Geometry设计风格。

---

## 模式选择时机

**选择HTML模式的场景**：
- 需要快速生成可预览的笔记页面
- 需要查看笔记的整体视觉效果
- 需要支持响应式设计的输出
- 需要后续编辑和调整灵活性
- 需要直接部署到网页服务器
- 不需要AI生成手绘图片

**选择AI绘图模式的场景**：
- 需要手绘风格的信息图
- 追求视觉创意和独特性
- 需要符合小红书图片笔记形式
- 不需要响应式网页设计

---

## HTML模板说明

### 模板位置

**主模板**：`references/xiaohongshu-preview-template.html`

**设计风格**：Vital Geometry（动态几何美学）

### 设计规范文档

完整的设计规范请参考以下文档：

1. **页面布局规范**：`references/xiaohongshu-preview-layout-spec.md`
   - 整体容器结构
   - 三段式布局（标题候选 + 笔记图轮播 + 正文内容）
   - 响应式规范
   - 间距和圆角系统

2. **卡片设计规范**：`references/xiaohongshu-preview-card-spec.md`
   - Vital Geometry 设计哲学
   - 卡片内容层级
   - 装饰元素系统（点阵、波浪线、同心圆）
   - 特殊卡片类型（封面、内容、推广）

3. **配色方案**：`references/xiaohongshu-preview-color-spec.md`
   - 完整色板定义
   - 强调色使用规则
   - 装饰元素配色
   - 最佳实践

### 模板特点

**1. Vital Geometry 设计风格**
- 动态几何装饰元素（点阵、波浪线、同心圆）
- 温暖的米色中性基底（#fafaf8）
- 精心选择的强调色（珊瑚红 #ff6b6b、琥珀黄 #ffc107）
- 控制的活力：在严格结构框架内注入动态能量

**2. 三段式布局**
- **Section 1**：标题候选列表（10个标题供选择）
- **Section 2**：笔记图卡片轮播（3:4比例，模拟小红书笔记）
- **Section 3**：正文内容区域（完整笔记稿 + 标签）

**3. 响应式设计**
- 移动端优先设计
- 最大宽度420px（模拟手机屏幕）
- 支持桌面端居中显示

**4. 交互元素**
- 标题选择交互（点击选中，✓标记）
- 卡片轮播（左右切换，圆点指示器）
- 悬停效果（标题项、按钮）

---

## 模板结构详解

### 整体结构

```html
<div class="preview-container">
    <!-- Section 1: 标题候选列表 -->
    <div class="title-section">...</div>

    <!-- Section 2: 笔记图轮播 -->
    <div class="carousel-section">
        <div class="carousel-viewport">
            <div class="carousel-track">
                <!-- 卡片1-7：封面 + 内容5张 + 推广 -->
            </div>
        </div>
        <div class="dots-indicator">...</div>
    </div>

    <!-- Section 3: 正文内容 -->
    <div class="content-section">...</div>
</div>
```

### Section 1: 标题候选列表

**功能**：展示10个标题候选，用户可点击选择

**HTML结构**：
```html
<div class="title-section">
    <div class="section-label">TITLE CANDIDATES · 标题候选</div>
    <ul class="title-list">
        <li class="title-item">
            <span class="title-number">1</span>
            标题文字
        </li>
        <!-- ... 重复10个 -->
    </ul>
</div>
```

**样式要点**：
- 未选中：浅灰背景 (#fafafa)，圆形编号
- 选中：白色背景 + 灰色边框 (#e8e8e8) + ✓ 标记
- 悬停：更浅灰背景 (#f5f5f5)

### Section 2: 笔记图卡片轮播

**功能**：横向轮播展示7张笔记图卡片（3:4比例）

**卡片类型**：

#### 1. 封面卡片（.card-cover）

```html
<div class="note-card card-cover">
    <div class="card-number">COVER · 01</div>
    <div class="card-title">主标题</div>
    <div class="card-subtitle">副标题</div>
    <div class="card-divider">...</div>
    <div class="card-highlight">从0到<span>380万</span></div>
    <div class="highlight-dots">...</div>
</div>
```

**特点**：
- 内容居中对齐
- 标题装饰线居中
- 超大高亮数字（52px）

#### 2. 内容卡片（标准卡片）

```html
<div class="note-card">
    <div class="card-number">CHAPTER · 02</div>
    <div class="card-title">标题</div>
    <div class="card-divider">...</div>

    <!-- 可选：强调框 -->
    <div class="card-accent-box">
        内容...
    </div>

    <!-- 可选：列表 -->
    <div class="card-list">
        <div class="card-list-item">项目1</div>
        <div class="card-list-item">项目2</div>
    </div>

    <!-- 可选：数据框 -->
    <div class="data-box">
        <div class="data-row">
            <span class="data-label">标签</span>
            <span class="data-value">值</span>
        </div>
    </div>

    <div class="card-footer">
        <div class="card-footer-text">02 / 07</div>
    </div>
</div>
```

**特点**：
- 左对齐内容
- 红色标题装饰线（30px × 3px）
- 页码标记

#### 3. 推广卡片（.card-promo）

```html
<div class="note-card card-promo">
    <div class="card-number">PROMO · 07</div>
    <div class="card-title">标题</div>
    <div class="card-subtitle">副标题</div>
    <div class="card-divider">...</div>
    <div class="card-list">...</div>
    <div class="card-accent-box">...</div>
    <div class="card-footer">
        <div class="card-tag">品牌标识</div>
    </div>
</div>
```

**特点**：
- 红黄渐变顶部彩条（16px高）
- 强调框使用红黄渐变背景
- 保持整体视觉风格统一

### Section 3: 正文内容区域

```html
<div class="content-section">
    <div class="section-label">CONTENT · 正文内容</div>
    <div class="note-content">
        完整笔记稿内容...
    </div>
    <div class="risk-warning">
        ⚠️ 风险提示...
    </div>
    <div class="tags">
        <span class="tag">#标签1</span>
        <span class="tag">#标签2</span>
    </div>
</div>
```

---

## 操作流程

### 步骤1：读取模板

```markdown
读取文件：references/xiaohongshu-preview-template.html
```

### 步骤2：分析笔记结构

从Phase 2输出的小红书笔记稿中提取：

1. **标题版本**（10个候选）
2. **笔记图内容**（封面页 + 内容页N页 + 尾页）
3. **正文引导语**
4. **风险提示**
5. **标签列表**

### 步骤3：确定卡片数量和类型

**标准配置**：7张卡片
- 封面页 × 1
- 内容页 × 5
- 推广页 × 1

**自定义配置**：
- 根据笔记内容页数调整
- 建议：3-9张卡片
- 保持：封面 + N张内容 + 推广页

### 步骤4：填充模板内容

#### 填充Section 1：标题候选列表

```html
<ul class="title-list">
    <li class="title-item selected">
        <span class="title-number">1</span>
        {标题1 - 最优标题}
    </li>
    <li class="title-item">
        <span class="title-number">2</span>
        {标题2}
    </li>
    <!-- ... 共10个标题 -->
</ul>
```

**规则**：
- 第一个设置为 `.selected`（默认选中）
- 提供10个标题供选择
- 从Phase 2输出的标题列表中选择

#### 填充Section 2：笔记图卡片

**卡片1：封面页**

```html
<div class="note-card card-cover">
    <div class="card-decoration circle-main"></div>
    <div class="dynamic-shape dot-grid">
        <!-- 5×5 点阵网格 -->
    </div>
    <div class="card-content">
        <div class="card-number">COVER · 01</div>
        <div class="card-title">{笔记主标题}</div>
        <div class="card-subtitle">{副标题}</div>
        <div class="card-divider">
            <div class="card-divider-dot"></div>
        </div>
        <div class="card-highlight">{核心观点}</div>
        <div class="highlight-dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
        <div class="card-content-text">{说明文字}</div>
        <div class="card-footer">
            <div class="card-footer-text">FINANCIAL GUIDE · 2025</div>
        </div>
    </div>
</div>
```

**卡片2-6：内容页**

根据内容类型选择合适的布局：

**类型A：文字内容**
```html
<div class="note-card">
    <div class="card-decoration circle-dots">
        <svg><!-- 同心圆 --></svg>
    </div>
    <div class="card-content">
        <div class="card-number">CHAPTER · XX</div>
        <div class="card-title">{章节标题}</div>
        <div class="card-divider">...</div>
        <div class="card-accent-box">
            {主要内容}
        </div>
        <div class="dynamic-shape wave-line"></div>
        <div class="card-content-text">
            {补充说明}
        </div>
        <div class="card-footer">
            <div class="card-footer-text">XX / 07</div>
        </div>
    </div>
</div>
```

**类型B：数据展示**
```html
<div class="note-card">
    <div class="card-content">
        <div class="card-number">CHAPTER · XX</div>
        <div class="card-title">{章节标题}</div>
        <div class="card-divider">...</div>
        <div class="card-highlight">{核心数据}<span>{强调数字}</span></div>
        <div class="data-box">
            <div class="data-row">
                <span class="data-label">{标签}</span>
                <span class="data-value">{值}</span>
            </div>
            <!-- 更多数据行 -->
        </div>
        <div class="card-content-text">{说明}</div>
        <div class="card-footer">
            <div class="card-footer-text">XX / 07</div>
        </div>
    </div>
</div>
```

**类型C：列表内容**
```html
<div class="note-card">
    <div class="card-content">
        <div class="card-number">CHAPTER · XX</div>
        <div class="card-title">{章节标题}</div>
        <div class="card-divider">...</div>
        <div class="card-list">
            <div class="card-list-item"><strong>{项目1}</strong> · {说明}</div>
            <div class="card-list-item"><strong>{项目2}</strong> · {说明}</div>
            <!-- 最多4-5项 -->
        </div>
        <div class="dynamic-shape wave-line"></div>
        <div class="card-content-text">{提示文字}</div>
        <div class="card-footer">
            <div class="card-footer-text">XX / 07</div>
        </div>
    </div>
</div>
```

**卡片7：推广页**

```html
<div class="note-card card-promo">
    <div class="card-decoration circle-main"></div>
    <div class="dynamic-shape dot-grid">
        <!-- 装饰点阵 -->
    </div>
    <div class="card-content">
        <div class="card-number">PROMO · 07</div>
        <div class="card-title">{推广标题}</div>
        <div class="card-subtitle">{推广副标题}</div>
        <div class="card-divider">...</div>
        <div class="card-list">
            <div class="card-list-item">{福利1}</div>
            <div class="card-list-item">{福利2}</div>
            <div class="card-list-item">{福利3}</div>
        </div>
        <div class="dynamic-shape wave-line"></div>
        <div class="card-accent-box">
            <strong>📚 {资料包标题}</strong><br>
            <span>{资料包说明}</span>
        </div>
        <div class="highlight-dots">
            <div class="dot" style="background: #ffc107;"></div>
            <div class="dot" style="background: #ffc107;"></div>
            <div class="dot" style="background: #ffc107;"></div>
        </div>
        <div class="card-footer">
            <div class="card-tag">{品牌标识}</div>
        </div>
    </div>
</div>
```

#### 填充Section 3：正文内容

```html
<div class="content-section">
    <div class="section-label">CONTENT · 正文内容</div>
    <div class="note-content">
        {完整笔记稿内容，保留段落和换行}
    </div>
    <div class="risk-warning">
        ⚠️ <strong>风险提示</strong>：{风险提示内容}
    </div>
    <div class="tags">
        <span class="tag">#标签1</span>
        <span class="tag">#标签2</span>
        <!-- 5-8个标签 -->
    </div>
</div>
```

### 步骤5：生成HTML文件

**文件命名**：
```
小红书笔记预览-{YYYY-MM-DD}.html
```

**输出位置**：
```
当前工作目录/
```

### 步骤6：质量检查

生成后检查以下项目：

**内容完整性**：
- [ ] 所有10个标题已填充
- [ ] 默认选中第一个标题
- [ ] 7张卡片内容完整
- [ ] 正文内容完整
- [ ] 标签数量合理（5-8个）

**视觉一致性**：
- [ ] 所有卡片背景色统一（#fafaf8）
- [ ] 标题装饰线颜色一致（#ff6b6b）
- [ ] 装饰元素不抢主内容
- [ ] 页码连续且正确

**功能性**：
- [ ] 标题选择可点击
- [ ] 卡片轮播可切换
- [ ] 浏览器中正常显示
- [ ] 移动端显示正常

---

## 使用示例

### 示例：职场新人理财指南

**输入**（Phase 2笔记稿）：
```
标题候选：
1. 22岁职场新人必看！ETF定投3步走
2. 从0到380万，职场新人理财指南
...

笔记图内容：
- 封面：22岁职场新人必看，ETF定投3步走
- 内容1：宝子们的理财困境
- 内容2：为什么要理财？（通胀偷走钱）
- 内容3：为什么选择ETF定投？
- 内容4：3步开启定投之旅
- 内容5：长期主义的力量（复利数据）
- 推广：申万宏源证券福利

正文：完整笔记稿...
标签：#理财小白 #投资入门 #ETF #定投
```

**输出**（HTML预览页面）：
- Section 1：10个标题候选，第1个选中
- Section 2：7张卡片轮播
  - 卡片1：封面（大标题 + "从0到380万"）
  - 卡片2-6：5个内容页
  - 卡片7：推广页（申万宏源福利）
- Section 3：正文 + 风险提示 + 标签

---

## 装饰元素使用指南

Vital Geometry风格的核心在于恰到好处的装饰元素。

### 点阵网格（.dot-grid）

**用途**：背景装饰，增加质感

**位置**：卡片四角，绝对定位

**配置**：
```html
<div class="dynamic-shape dot-grid"
     style="position: absolute; top: 60px; right: 40px; opacity: 0.2;">
    <!-- 5×5 = 25个点 -->
    <div class="dot"></div>
    <!-- ... 重复25次 -->
</div>
```

**使用原则**：
- 每张卡片最多1-2个点阵
- 透明度：0.2-0.3
- 位置：不遮挡内容

### 波浪线（.wave-line）

**用途**：装饰性分隔线

**位置**：内容块之间

**配置**：
```html
<div class="dynamic-shape wave-line" style="margin: 12px 0;"></div>
```

**使用原则**：
- 每张卡片最多1-2条
- 上下边距：12px-16px
- 作为视觉引导

### 同心圆（.circle-dots）

**用途**：背景装饰，增加层次感

**位置**：卡片角落

**配置**：
```html
<div class="card-decoration circle-dots">
    <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(0,0,0,0.03)"/>
        <circle cx="60" cy="60" r="35" fill="none" stroke="rgba(0,0,0,0.04)"/>
        <circle cx="60" cy="60" r="20" fill="none" stroke="rgba(0,0,0,0.05)"/>
    </svg>
</div>
```

**使用原则**：
- 每张卡片最多1组
- 3层圆圈，透明度递增
- 不干扰主内容

### 高亮圆点组（.highlight-dots）

**用途**：强调关键信息

**位置**：重要文字附近

**配置**：
```html
<div class="highlight-dots" style="margin-top: 8px;">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
</div>
```

**使用原则**：
- 3-4个圆点
- 黄色（#ffc107）或红色（#ff6b6b）
- 用于高亮数字或标题

### 主圆装饰（.circle-main）

**用途**：大型背景圆圈

**位置**：卡片边缘

**配置**：
```html
<div class="card-decoration circle-main"></div>
```

**使用原则**：
- 每张卡片最多1个
- 200px × 200px
- 部分超出卡片边界

---

## 配色使用指南

### 主色系统

**背景色**：
- 卡片背景：`#fafaf8`（所有卡片统一）
- Section背景：`#f5f3f0`（轮播区域）
- 内容框背景：`#f8f8f6`（强调框、数据框）

**文字色**：
- 标题：`#1a1a1a`（近黑）
- 正文：`#555`（中灰）
- 辅助：`#999`（浅灰）

### 强调色系统

**珊瑚红（#ff6b6b）**：
- 标题装饰线
- 列表项圆点
- 强调文字
- 数据框数值

**琥珀黄（#ffc107）**：
- 高亮圆点
- 数据框角装饰
- 背景光晕

**使用原则**：
- 每张卡片珊瑚红 ≤ 3处
- 每张卡片琥珀黄 ≤ 2处
- 避免过度使用

---

## 常见问题

### Q1: 如何调整卡片数量？

**A**: 修改 `.carousel-track` 中的 `.carousel-slide` 数量：
- 增加：复制 `.carousel-slide` 块
- 减少：删除 `.carousel-slide` 块
- 更新：JavaScript中的 `totalPages` 变量

### Q2: 如何修改卡片尺寸？

**A**: 修改 `.carousel-viewport` 的 `aspect-ratio`：
```css
.carousel-viewport {
    aspect-ratio: 3 / 4;  /* 3:4 比例 */
}
```

### Q3: 如何导出为PDF？

**A**:
1. 在浏览器中打开HTML文件
2. 使用"打印"功能（Ctrl+P）
3. 选择"另存为PDF"
4. 调整页面设置（建议纵向、A4纸张）

### Q4: 能否直接在小红书使用HTML？

**A**: 不能。小红书不支持HTML发布。HTML模式主要用于：
- 网页预览和展示
- 本地存档和分享
- PDF导出打印
- 内容审阅和调整

如需发布到小红书，请使用AI绘图模式（模式A）。

### Q5: 如何自定义品牌色？

**A**: 修改CSS变量：
```css
:root {
    /* 强调色 */
    --accent-red: #ff6b6b;
    --accent-yellow: #ffc107;

    /* 修改为品牌色 */
    --accent-red: #YOUR_BRAND_COLOR;
}
```

---

## 高级技巧

### 1. 添加交互效果

模板已包含：
- 标题选择（点击切换选中状态）
- 卡片轮播（左右箭头 + 圆点指示器）
- 悬停效果（标题项、按钮）

### 2. 调整动画速度

修改CSS：
```css
.carousel-track {
    transition: transform 0.3s ease;  /* 修改0.3s */
}
```

### 3. 添加自定义字体

在HTML `<head>` 中添加：
```html
<link href="https://fonts.googleapis.com/css2?family=Your+Font&display=swap" rel="stylesheet">
```

然后在CSS中使用：
```css
body {
    font-family: 'Your Font', -apple-system, sans-serif;
}
```

---

## 相关文档

- **页面布局规范**：`references/xiaohongshu-preview-layout-spec.md`
- **卡片设计规范**：`references/xiaohongshu-preview-card-spec.md`
- **配色方案**：`references/xiaohongshu-preview-color-spec.md`
- **Phase 3完整指南**：`references/phase-guides.md#phase-3`

---

## 版本历史

**v1.0** (2025-01-23)
- 初始版本
- 采用Vital Geometry设计风格
- 三段式布局（标题候选 + 卡片轮播 + 正文内容）
- 7张卡片标准配置

---

**维护者**：爆款智坊项目组
**最后更新**：2025-01-23
