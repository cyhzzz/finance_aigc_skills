# 小红书笔记预览模板 - 页面布局设计规范

## 1. 整体容器规范

### 1.1 主容器（.preview-container）

```css
.preview-container {
    width: 100%;
    max-width: 420px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    overflow: hidden;
}
```

**设计要点：**
- 容器宽度最大 420px，模拟移动端屏幕宽度
- 白色背景 (#fff)
- 圆角 16px，营造柔和的卡片感
- 轻微阴影增强层次感
- overflow: hidden 确保内容不会溢出圆角

### 1.2 页面结构

采用三段式布局结构：

```
┌─────────────────────────────┐
│   Section 1: 标题候选区域    │
├─────────────────────────────┤
│   Section 2: 笔记图轮播区域  │
├─────────────────────────────┤
│   Section 3: 正文内容区域    │
└─────────────────────────────┘
```

**Section 间分隔：**
- 使用 `border-bottom: 1px solid #f0f0f0` 创建轻微分隔
- 保持视觉连续性的同时明确区分不同功能区

---

## 2. Section 1: 标题候选列表

### 2.1 容器样式

```css
.title-section {
    background: #fff;
    padding: 24px 20px;
    border-bottom: 1px solid #f0f0f0;
}
```

**设计要点：**
- 内边距：上下 24px，左右 20px
- 白色背景，保持清爽

### 2.2 Section 标签

```css
.section-label {
    font-size: 11px;
    color: #999;
    margin-bottom: 12px;
    font-weight: 500;
    letter-spacing: 0.5px;
}
```

**设计要点：**
- 超小字号 11px，营造精致感
- 灰色文字，不抢主内容的视觉焦点
- 字间距 0.5px，增强可读性

### 2.3 标题列表项

#### 默认状态

```css
.title-item {
    padding: 12px 14px;
    margin-bottom: 8px;
    background: #fafafa;
    border-radius: 8px;
    font-size: 13px;
    line-height: 1.5;
    cursor: pointer;
    transition: all 0.2s;
    border: 1.5px solid transparent;
}
```

**设计要点：**
- 浅灰背景 (#fafafa) 区别于白色主背景
- 圆角 8px，与主容器圆角呼应
- 1.5 行高确保多行标题可读性
- 0.2s 过渡动画，提供流畅交互反馈

#### 悬停状态

```css
.title-item:hover {
    background: #f5f5f5;
}
```

#### 选中状态

```css
.title-item.selected {
    background: #fff;
    border-color: #e8e8e8;
    color: #1a1a1a;
}

.title-item.selected::after {
    content: '✓';
    position: absolute;
    right: 14px;
    top: 50%;
    transform: translateY(-50%);
    color: #1a1a1a;
    font-size: 14px;
    font-weight: bold;
}
```

**设计要点：**
- 选中项使用白色背景 + 灰色边框，突出显示
- 右侧 ✓ 标记，清晰表明选中状态
- 相对定位确保标记不影响内容布局

### 2.4 标题序号

```css
.title-number {
    display: inline-block;
    width: 18px;
    height: 18px;
    background: #e0e0e0;
    color: #666;
    border-radius: 50%;
    text-align: center;
    line-height: 18px;
    font-size: 10px;
    margin-right: 8px;
}

.title-item.selected .title-number {
    background: #1a1a1a;
    color: #fff;
}
```

**设计要点：**
- 圆形序号设计，视觉友好
- 选中时反色，增强对比

---

## 3. Section 2: 笔记图片轮播区域

### 3.1 容器样式

```css
.carousel-section {
    background: #f5f3f0;
    padding: 24px 20px;
    position: relative;
}
```

**设计要点：**
- 暖灰色背景 (#f5f3f0)，与白色 Section 形成对比
- 使用 position: relative 支持装饰元素的绝对定位

### 3.2 轮播视口

```css
.carousel-viewport {
    position: relative;
    width: 100%;
    aspect-ratio: 3 / 4;
    overflow: hidden;
    border-radius: 12px;
    box-shadow:
        0 4px 12px rgba(0, 0, 0, 0.08),
        0 8px 24px rgba(0, 0, 0, 0.04);
}
```

**设计要点：**
- **3:4 宽高比**：标准小红书笔记图片比例
- 多层阴影营造深度感
- 圆角 12px，略小于主容器的 16px

### 3.3 轮播轨道

```css
.carousel-track {
    display: flex;
    transition: transform 0.3s ease;
    height: 100%;
}
```

**设计要点：**
- Flexbox 布局实现横向排列
- 0.3s ease 过渡动画，流畅自然

### 3.4 单张卡片

```css
.carousel-slide {
    flex: 0 0 100%;
    width: 100%;
    height: 100%;
}
```

---

## 4. Section 3: 正文内容区域

### 4.1 容器样式

```css
.content-section {
    background: #fff;
    padding: 24px 20px;
}
```

**设计要点：**
- 与 Section 1 保持一致的内边距
- 白色背景，保持整体协调

### 4.2 正文内容

```css
.note-content {
    font-size: 14px;
    line-height: 1.8;
    color: #333;
    margin-bottom: 20px;
}
```

**设计要点：**
- 14px 字号，1.8 行高，保证舒适阅读体验
- 左对齐，及时换行
- 深灰色文字 (#333) 降低视觉疲劳

### 4.3 风险提示框

```css
.risk-warning {
    background: #fff3cd;
    border: 1px solid #ffc107;
    padding: 15px;
    margin: 20px 0;
    border-radius: 8px;
    font-size: 13px;
    color: #856404;
}
```

**设计要点：**
- 浅黄背景 + 黄色边框，警示色但不过于强烈
- 圆角 8px 与整体风格统一

### 4.4 标签云

```css
.tags {
    padding-top: 16px;
}

.tag {
    display: inline-block;
    background: #667eea;
    color: white;
    padding: 6px 12px;
    border-radius: 16px;
    margin: 4px 4px 0 0;
    font-size: 12px;
}
```

**设计要点：**
- 胶囊形状设计（圆角 16px）
- 蓝紫色 (#667eea) 与整体配色协调
- 小间距排列，形成云状效果

---

## 5. 响应式规范

### 5.1 移动端适配

```css
@media (max-width: 600px) {
    body {
        padding: 0;
    }

    .preview-container {
        max-width: 100%;
        border-radius: 0;
    }

    .note-card {
        padding: 28px 20px;
    }

    .card-title {
        font-size: 20px;
    }
}
```

**设计要点：**
- 移动端去除容器边距和圆角，全屏显示
- 卡片内边距适当缩小
- 字号按比例缩小

---

## 6. 间距系统

### 6.1 基础间距单位

基于 4px 网格系统：
- 超小间距：4px
- 小间距：8px
- 中间距：12px
- 大间距：16px
- 超大间距：20px, 24px

### 6.2 应用场景

| 场景 | 间距值 |
|------|--------|
| Section 内边距 | 24px 20px |
| 列表项间距 | 8px |
| 元素组间距 | 12px-16px |
| 边框粗细 | 1px-1.5px |

---

## 7. 圆角系统

| 元素 | 圆角值 |
|------|--------|
| 主容器 | 16px |
| 轮播视口 | 12px |
| 按钮/标签 | 8px-16px |
| 小元素 | 4px-8px |

---

## 8. 阴影系统

### 8.1 阴影层级

**轻微阴影（卡片）：**
```css
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
```

**中度阴影（悬浮）：**
```css
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
```

**强调阴影（强调）：**
```css
box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
```

---

## 9. 字体系统

### 9.1 字体族

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
             "PingFang SC", "Hiragino Sans GB",
             "Microsoft YaHei", sans-serif;
```

**设计要点：**
- 优先使用系统字体，确保加载速度和原生体验
- 中文环境优先显示 PingFang SC

### 9.2 字号层级

| 用途 | 字号 | 字重 |
|------|------|------|
| Section 标签 | 11px | 500 |
| 辅助文字 | 12px-13px | 400 |
| 正文内容 | 14px | 400 |
| 卡片标题 | 24px | 700 |
| 强调数字 | 36px | 700/300 |

---

## 10. 过渡动画

### 10.1 标准过渡

```css
transition: all 0.2s ease;
```

### 10.2 轮播过渡

```css
transition: transform 0.3s ease;
```

**设计要点：**
- 交互元素使用 0.2s 快速响应
- 轮播切换使用 0.3s 平滑过渡
- 统一使用 ease 缓动函数

---

## 11. 可访问性

### 11.1 颜色对比

确保文字与背景对比度符合 WCAG AA 标准：
- 正文文字 (#333) vs 白色背景：对比度 > 7:1
- 次要文字 (#999) vs 白色背景：对比度 > 4.5:1

### 11.2 交互反馈

所有可交互元素提供清晰的视觉反馈：
- 悬停状态
- 选中状态
- 禁用状态（如适用）

---

## 12. 性能优化

### 12.1 CSS 优化

- 使用 transform 而非 position 属性实现动画
- 使用 will-change 提示浏览器优化
- 避免过度使用 box-shadow（最多 2-3 层）

### 12.2 图片优化

- 轮播图片使用懒加载
- 适当压缩图片质量
- 使用 WebP 格式（如浏览器支持）

---

**版本：** v1.0
**最后更新：** 2025-01-23
**维护者：** 爆款智坊项目组
