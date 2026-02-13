# 小红书笔记图预览卡片 - Vital Geometry 设计规范

## 设计哲学

Vital Geometry 是一种动态几何美学，通过精确的几何形式与充满活力的装饰元素相结合，创造出既严谨又生动的视觉语言。

**核心理念：**
- 几何精确性：所有元素基于网格和对齐系统
- 动态装饰：通过点、线、圆等几何元素创造视觉活力
- 控制的活力：在严格的结构框架内注入动态能量
- 工匠精神：每个细节都经过精心雕琢，体现专业水准

---

## 1. 卡片基础结构

### 1.1 卡片容器

```css
.note-card {
    width: 100%;
    height: 100%;
    padding: 36px 28px;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    background: #fafaf8;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}
```

**设计要点：**
- 宽高比：3:4（标准小红书笔记比例）
- 统一背景色：#fafaf8（米白色）
- 内边距：上下 36px，左右 28px
- 圆角：12px
- 多层阴影增强立体感
- position: relative 支持装饰元素的绝对定位

### 1.2 顶部彩色边框

```css
.note-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 14px;
    background: linear-gradient(90deg, #1a1a1a 0%, #3a3a3a 100%);
}
```

**设计要点：**
- 高度：14px
- 渐变：从深灰到中灰
- 位置：顶部，横跨整个卡片宽度
- 作用：视觉锚点，定义卡片顶部边界

---

## 2. 卡片内容层级

### 2.1 卡片编号（.card-number）

```css
.card-number {
    font-size: 11px;
    color: #999;
    font-family: "Courier New", monospace;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
```

**设计要点：**
- 字号：11px（超小，不抢视觉焦点）
- 颜色：#999（浅灰，低调）
- 字体：等宽字体（营造技术感）
- 字间距：1px（增强可读性）
- 位置：内容区的第一个元素

**示例：**
```
COVER · 01
CHAPTER · 02
PROMO · 07
```

### 2.2 卡片标题（.card-title）

```css
.card-title {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
    position: relative;
}

.card-title::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -8px;
    width: 30px;
    height: 3px;
    background: #ff6b6b;
    border-radius: 2px;
}
```

**设计要点：**
- 字号：24px（大而醒目）
- 字重：700（粗体强调）
- 颜色：#1a1a1a（近黑，高对比）
- **红色装饰线**：
  - 宽度：30px
  - 高度：3px
  - 颜色：#ff6b6b（珊瑚红）
  - 圆角：2px
  - 位置：标题下方 8px

### 2.3 卡片副标题（.card-subtitle）

```css
.card-subtitle {
    font-size: 16px;
    color: #666;
    margin-bottom: 16px;
    margin-top: 8px;
}
```

**设计要点：**
- 字号：16px（中等）
- 颜色：#666（中灰）
- 位置：标题下方，与标题保持 8px 间距
- 用途：补充说明或第二标题

---

## 3. 分隔元素

### 3.1 动态分隔线（.card-divider）

```css
.card-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 16px 0;
}

.card-divider::before,
.card-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #ddd, transparent);
}

.card-divider-dot {
    width: 6px;
    height: 6px;
    background: #ddd;
    border-radius: 50%;
}
```

**设计要点：**
- 两侧渐变虚线（透明 → 灰 → 透明）
- 中心圆点：6px 直径
- 整体间距：12px
- 上下边距：16px
- 作用：视觉分隔，引导视线向下

---

## 4. 强调元素

### 4.1 高亮文字（.card-highlight）

```css
.card-highlight {
    font-size: 36px;
    font-weight: 300;
    color: #1a1a1a;
    margin: 20px 0;
    letter-spacing: -1px;
    line-height: 1.2;
    position: relative;
}

.card-highlight span {
    font-weight: 700;
    color: #ff6b6b;
}
```

**设计要点：**
- 字号：36px（超大，视觉焦点）
- 主字重：300（细体，优雅）
- 颜色：#1a1a1a
- **关键词强调**：
  - 字重：700（粗体）
  - 颜色：#ff6b6b（珊瑚红）
- 负字间距：-1px（紧凑感）
- 行高：1.2（紧密排列）

**示例：**
```html
<div class="card-highlight">
    从0到<span>380万</span>
</div>
```

### 4.2 高亮圆点组（.highlight-dots）

```css
.highlight-dots {
    display: flex;
    gap: 4px;
    margin-top: 8px;
}

.highlight-dots .dot {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #ffc107;
}
```

**设计要点：**
- 圆点数量：3-4 个
- 圆点大小：4px
- 间距：4px
- 颜色：#ffc107（琥珀黄）
- 用途：装饰性强调，点缀在关键信息附近

---

## 5. 内容容器

### 5.1 强调框（.card-accent-box）

```css
.card-accent-box {
    background: #f8f8f6;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
}

.card-accent-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: radial-gradient(circle, rgba(0,0,0,0.03) 1px, transparent 1px);
    background-size: 8px 8px;
    opacity: 0.5;
    pointer-events: none;
}
```

**设计要点：**
- 背景：#f8f8f6（极浅灰）
- 边框：1px，透明度 0.06
- 圆角：8px
- 内边距：16px
- **点阵纹理**：
  - 圆点：1px，透明度 0.03
  - 间距：8px
  - 作用：增加质感，避免单调

### 5.2 数据框（.data-box）

```css
.data-box {
    background: #f8f8f6;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
}

.data-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, transparent 50%, rgba(255, 193, 7, 0.05) 50%);
    pointer-events: none;
}

.data-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid rgba(0,0,0,0.04);
    font-size: 13px;
}

.data-row:last-child {
    border-bottom: none;
}

.data-label {
    color: #666;
}

.data-value {
    color: #1a1a1a;
    font-weight: 600;
}
```

**设计要点：**
- **右上角渐变装饰**：
  - 尺寸：60px × 60px
  - 渐变：透明 → 淡琥珀黄
  - 位置：左上角
- **数据行**：
  - 两侧对齐（标签 | 值）
  - 下边框分割（最后一行无边框）
  - 字号：13px
  - 值字重：600（半粗）

**示例结构：**
```html
<div class="data-box">
    <div class="data-row">
        <span class="data-label">现在拥有</span>
        <span class="data-value">¥10,000</span>
    </div>
    <div class="data-row">
        <span class="data-label">实际购买力</span>
        <span class="data-value" style="color: #ff6b6b;">¥7,400</span>
    </div>
</div>
```

---

## 6. 列表系统

### 6.1 动态列表（.card-list）

```css
.card-list {
    margin: 16px 0;
}

.card-list-item {
    padding: 12px 0;
    font-size: 13px;
    color: #333;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    display: flex;
    align-items: flex-start;
    position: relative;
    padding-left: 20px;
}

.card-list-item::before {
    content: '';
    position: absolute;
    left: 0;
    top: 16px;
    width: 8px;
    height: 8px;
    background: #ff6b6b;
    border-radius: 50%;
}

.card-list-item:last-child {
    border-bottom: none;
}
```

**设计要点：**
- **红色圆点装饰**：
  - 大小：8px
  - 颜色：#ff6b6b
  - 位置：左侧，垂直居中
- 内边距：左 20px（为圆点留空间），上下 12px
- 下边框：透明度 0.05
- 字号：13px
- 最后一项无边框

**示例：**
```html
<div class="card-list">
    <div class="card-list-item"><strong>门槛低</strong> · 几百块就能开始</div>
    <div class="card-list-item"><strong>风险分散</strong> · 包含几十上百只股票</div>
    <div class="card-list-item"><strong>操作简单</strong> · 不需要专业选股能力</div>
    <div class="card-list-item"><strong>长期收益</strong> · 年化8-12%</div>
</div>
```

---

## 7. 正文文字

### 7.1 内容文本（.card-content-text）

```css
.card-content-text {
    font-size: 13px;
    color: #555;
    line-height: 1.8;
    margin-bottom: auto;
}
```

**设计要点：**
- 字号：13px
- 颜色：#555（中灰）
- 行高：1.8（舒适阅读）
- margin-bottom: auto（将页脚推到底部）

---

## 8. 页脚区域

### 8.1 页脚容器（.card-footer）

```css
.card-footer {
    margin-top: auto;
    padding-top: 16px;
}

.card-footer-text {
    font-size: 11px;
    color: #ccc;
    letter-spacing: 0.5px;
}

.card-tag {
    display: inline-block;
    padding: 6px 12px;
    background: #f0f0f0;
    color: #999;
    border-radius: 6px;
    font-size: 10px;
    letter-spacing: 0.5px;
}
```

**设计要点：**
- **页脚文字**：
  - 字号：11px
  - 颜色：#ccc（浅灰）
  - 字间距：0.5px
- **标签样式**：
  - 背景：#f0f0f0
  - 圆角：6px
  - 字号：10px
  - 内边距：6px 12px

---

## 9. 装饰元素系统

### 9.1 点阵网格（.dot-grid）

```css
.dynamic-shape.dot-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
}

.dot-grid .dot {
    width: 6px;
    height: 6px;
    background: #ddd;
    border-radius: 50%;
}
```

**设计要点：**
- 网格布局：5 列
- 圆点大小：6px
- 间距：6px
- 颜色：#ddd（默认）
- **使用位置**：绝对定位在卡片的装饰位置
- **透明度变化**：0.2-0.3，不抢主内容

**示例用法：**
```html
<div class="dynamic-shape dot-grid"
     style="position: absolute; top: 60px; right: 40px; opacity: 0.2;">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
    <!-- ... 共 25 个点 (5×5) -->
</div>
```

### 9.2 波浪线（.wave-line）

```css
.dynamic-shape.wave-line {
    height: 2px;
    background: repeating-linear-gradient(
        90deg,
        transparent,
        transparent 4px,
        rgba(0, 0, 0, 0.03) 4px,
        rgba(0, 0, 0, 0.03) 8px
    );
}
```

**设计要点：**
- 高度：2px
- 模式：4px 透明 + 4px 实线（重复）
- 颜色：rgba(0, 0, 0, 0.03)（极淡）
- 用途：装饰性分隔线，增加视觉节奏

### 9.3 同心圆装饰（.circle-dots）

```html
<div class="card-decoration circle-dots">
    <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(0,0,0,0.03)" stroke-width="1"/>
        <circle cx="60" cy="60" r="35" fill="none" stroke="rgba(0,0,0,0.04)" stroke-width="1"/>
        <circle cx="60" cy="60" r="20" fill="none" stroke="rgba(0,0,0,0.05)" stroke-width="1"/>
    </svg>
</div>
```

**设计要点：**
- SVG 实现
- 3-4 层同心圆
- 半径递减：50px → 35px → 20px
- 透明度递增：0.03 → 0.04 → 0.05
- 位置：绝对定位，通常在卡片四角

### 9.4 主圆装饰（.circle-main）

```css
.card-decoration.circle-main {
    position: absolute;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 1px solid rgba(0,0,0,0.02);
    top: -50px;
    right: -50px;
    pointer-events: none;
}
```

**设计要点：**
- 大型圆形：200px × 200px
- 边框：1px，极淡透明度
- 位置：部分超出卡片边界，创造开放感
- 交互：pointer-events: none（不影响点击）

### 9.5 背景光晕

在 `.carousel-section::before` 中定义：

```css
.carousel-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
        radial-gradient(circle at 20% 30%, rgba(255, 107, 107, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(255, 193, 7, 0.02) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}
```

**设计要点：**
- 多层径向渐变叠加
- 珊瑚红光晕：rgba(255, 107, 107, 0.03)
- 琥珀黄光晕：rgba(255, 193, 7, 0.02)
- 位置：分散布局（20% 30%, 80% 70%）
- 作用：增加氛围感，不干扰主内容

---

## 10. 特殊卡片类型

### 10.1 封面卡片（.card-cover）

```css
.card-cover {
    background: #fafaf8;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.card-cover .card-title {
    font-size: 26px;
    margin-bottom: 8px;
}

.card-cover .card-title::after {
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
}

.card-cover .card-highlight {
    font-size: 52px;
    margin: 32px 0;
}
```

**设计要点：**
- 居中对齐所有内容
- 标题字号更大：26px
- 标题装饰线居中：left: 50%, transform: translateX(-50%)
- 装饰线宽度：40px
- 高亮文字字号：52px（超大）

### 10.2 推广卡片（.card-promo）

```css
.card-promo {
    background: #fafaf8;
}

.card-promo::before {
    background: linear-gradient(90deg, #ff6b6b 0%, #ffc107 100%);
    height: 16px;
}

.card-promo .card-number {
    color: #999;
}

.card-promo .card-title::after {
    background: #ff6b6b;
}

.card-promo .card-list-item::before {
    background: #ff6b6b;
}

.card-promo .card-accent-box {
    background: linear-gradient(135deg, rgba(255, 107, 107, 0.08) 0%, rgba(255, 193, 7, 0.08) 100%);
    border-color: rgba(255, 107, 107, 0.15);
}
```

**设计要点：**
- 顶部彩条：红黄渐变，高度 16px
- 强调框：红黄渐变背景
- 保持整体视觉风格统一

---

## 11. 内容编排原则

### 11.1 垂直节奏

- 标题区域：编号(8px) → 标题(4px) → 装饰线(8px) → 副标题(16px)
- 内容区域：分隔线(16px) → 内容(12-16px)
- 列表区域：每个项目 12px 间距
- 页脚区域：自动边距将页脚推到底部

### 11.2 视觉层级

1. **第一层级**：高亮数字（36px）、封面标题（52px）
2. **第二层级**：卡片标题（24px）、封面标题（26px）
3. **第三层级**：副标题（16px）、正文（13-14px）
4. **第四层级**：编号、页脚文字（11px）

### 11.3 装饰密度

- **少即是多**：每张卡片 2-3 个装饰元素
- **平衡分布**：装饰元素分布在卡片不同区域
- **透明度控制**：所有装饰元素透明度 ≤ 0.3
- **不抢焦点**：装饰元素永远服务于内容

---

## 12. 使用场景

### 12.1 封面卡片

**必需元素：**
- 卡片编号（COVER · 01）
- 主标题（大字号，居中）
- 副标题（可选）
- 高亮数字（超大，视觉焦点）
- 装饰元素：点阵网格、同心圆

**布局：** 居中对齐，纵向分布

### 12.2 内容卡片

**必需元素：**
- 卡片编号（CHAPTER · XX）
- 标题（带红色装饰线）
- 分隔线
- 内容框/列表/高亮文字
- 页脚（页码）

**布局：** 左对齐，纵向流式

### 12.3 推广卡片

**必需元素：**
- 卡片编号（PROMO · XX）
- 标题 + 副标题
- 分隔线
- 列表（福利内容）
- 强调框（资料包等）
- 页脚（品牌标识）

**布局：** 左对齐，红黄渐变顶部

---

## 13. 响应式适配

```css
@media (max-width: 600px) {
    .note-card {
        padding: 28px 20px;
    }

    .card-title {
        font-size: 20px;
    }

    .card-highlight {
        font-size: 28px;
    }

    .card-cover .card-title {
        font-size: 22px;
    }

    .card-cover .card-highlight {
        font-size: 44px;
    }
}
```

---

## 14. 最佳实践

### 14.1 装饰元素使用

1. **不要过度装饰**：每张卡片最多 2-3 个装饰元素
2. **保持平衡**：装饰元素应分布在不同区域
3. **透明度优先**：所有装饰使用低透明度
4. **服务于内容**：装饰不应干扰信息传达

### 14.2 颜色使用

1. **主色**：#1a1a1a（文字）、#fafaf8（背景）
2. **强调色**：#ff6b6b（珊瑚红，用于强调）、#ffc107（琥珀黄，用于点缀）
3. **中性色**：#999、#666、#555（灰度文字）
4. **边界色**：#ddd、#e8e8e8（边框、分隔）

### 14.3 排版建议

1. **留白充足**：元素之间保持足够间距
2. **呼吸感**：使用 padding 而非 margin 创建内部空间
3. **视觉引导**：用装饰线和分隔线引导视线
4. **焦点明确**：每张卡片只有一个主要视觉焦点

---

**版本：** v1.0
**设计风格：** Vital Geometry
**最后更新：** 2025-01-23
**维护者：** 爆款智坊项目组
