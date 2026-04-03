# 微信HTML输出规范

> 本文档是多平台改写流程 Step 6.1 的详细操作手册
> 将 Markdown 转为微信可用的内联样式 HTML

---

## 微信HTML输出要求

### 格式要求

| 要求 | 说明 |
|-----|------|
| 内联样式 | 所有CSS必须内联在HTML标签的 `style` 属性中 |
| 无 `<style>` 标签 | 微信会剥离 `<style>` 标签 |
| 暗黑模式 | 注入 `data-darkmode-*` 属性 |
| 图片占位 | 用 `[封面图建议：描述]` 标注 |
| 外链处理 | 转为上标编号脚注，底部附参考链接 |

---

## HTML标签对应关系

### 标题

```html
<!-- H1 → 居中加粗大标题 -->
<h1 style="text-align: center; font-size: 22px; font-weight: bold; margin: 20px 0;">{标题}</h1>

<!-- H2 → 左对齐加粗次标题 -->
<h2 style="font-size: 18px; font-weight: bold; margin: 16px 0 12px;">{章节标题}</h2>

<!-- H3 → 加粗 -->
<h3 style="font-size: 16px; font-weight: bold; margin: 12px 0 8px;">{子标题}</h3>
```

### 段落

```html
<p style="font-size: 16px; line-height: 1.8; margin: 12px 0; text-indent: 2em;">
  {正文内容}
</p>
```

### 强调

```html
<!-- 加粗：标点移到 strong 外 -->
<p>这个问题很<strong style="font-weight: bold;">重要</strong>，不是说说而已。</p>

<!-- 斜体 -->
<em style="font-style: italic;">{斜体内容}</em>
```

### 列表

```html
<!-- 无序列表：圆点 -->
<ul style="margin: 12px 0; padding-left: 24px;">
  <li style="margin: 6px 0;">{列表项1}</li>
  <li style="margin: 6px 0;">{列表项2}</li>
</ul>

<!-- 有序列表：数字 -->
<ol style="margin: 12px 0; padding-left: 24px;">
  <li style="margin: 6px 0;">{列表项1}</li>
  <li style="margin: 6px 0;">{列表项2}</li>
</ol>
```

### 引用

```html
<blockquote style="margin: 12px 0; padding: 12px 16px; border-left: 3px solid #ddd; background: #f8f8f8; color: #666;">
  {引用内容}
</blockquote>
```

### 图片占位

```html
<!-- 封面图 -->
<div style="text-align: center; margin: 16px 0; color: #999; font-size: 12px;">
  [封面图建议：{描述}]
</div>

<!-- 内文图 -->
<div style="text-align: center; margin: 16px 0;">
  <p style="color: #999; font-size: 12px; margin: 4px 0;">[配图：{描述}]</p>
</div>
```

### 脚注

```html
<!-- 上标编号 -->
<p>这个问题很重要<sup style="color: #999;">[1]</sup></p>

<!-- 脚注区域 -->
<hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
<p style="font-size: 12px; color: #999;">[1] 参考：<a href="{url}" style="color: #999;">{标题}</a></p>
```

### 分割线

```html
<hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
```

---

## 暗黑模式处理

```html
<!-- 暗黑模式段落 -->
<p
  style="font-size: 16px; line-height: 1.8; margin: 12px 0;"
  data-darkmode-color="#cccccc"
  data-darkmode-bgcolor="#1a1a1a"
>
  {正文内容}
</p>
```

### 暗黑模式颜色映射

| 元素 | 亮色 | 暗黑 |
|-----|------|------|
| 背景 | #ffffff | #1a1a1a |
| 正文 | #333333 | #cccccc |
| 标题 | #000000 | #ffffff |
| 辅助文字 | #999999 | #888888 |
| 分割线 | #eeeeee | #333333 |
| 引用背景 | #f8f8f8 | #2a2a2a |
| 链接 | #576b95 | #6a9fd4 |

---

## 封面图规范

### 封面图位置

在文章标题后，正文开始前插入：

```html
<h1 style="text-align: center;">{标题}</h1>

<!-- 封面图 -->
<div style="text-align: center; margin: 20px 0;">
  <p style="color: #999; font-size: 12px; margin: 4px 0;">[封面图建议：{描述}]</p>
</div>

<p style="...">{正文开始}</p>
```

### 封面图提示词生成

封面图提示词应包含：
1. **画面主体**：核心视觉元素
2. **风格**：简约/科技感/温暖等
3. **配色**：主色调
4. **文字**：是否需要叠加标题文字

```
封面图提示词示例：
[封面图建议：画面主体为中国A股K线图叠加手掌接住金币的意象，风格简约金融感，配色以深蓝和金色为主，右下角留白用于叠加标题文字]
```

---

## 纯文本文件规范

### article.txt 要求

- 纯文本，无任何HTML标签
- 保留段落分隔（空行）
- 保留标题（H1/H2/H3 转为纯文本标题）
- 脚注区域保留，但转为普通文本格式

### article.txt 示例

```txt
{标题}

{正文段落1}

{正文段落2}

---

脚注：
[1] 参考：{标题} {链接}
[2] 参考：{标题} {链接}

---
风险提示：本内容仅供参考，不构成投资建议。投资者据此操作，风险自担。市场有风险，投资需谨慎。
```

---

## 风险提示规范

### 位置

文章最后一段之后，独立成区。

### 格式

```html
<hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
<p style="font-size: 14px; color: #999; line-height: 1.6;">
  本内容仅供参考，不构成投资建议。投资者据此操作，风险自担。<br>
  市场有风险，投资需谨慎。
</p>
```

---

## 完整HTML模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{标题}</title>
</head>
<body style="margin: 0; padding: 0; background: #fff;">

<!-- 标题 -->
<h1 style="text-align: center; font-size: 22px; font-weight: bold; margin: 20px 0; padding: 0 16px;">
  {标题}
</h1>

<!-- 封面图 -->
<div style="text-align: center; margin: 16px 0;">
  <p style="color: #999; font-size: 12px;">[封面图建议：{描述}]</p>
</div>

<!-- 摘要 -->
<p style="font-size: 14px; color: #666; margin: 0 16px 20px; text-align: center;">
  {摘要}
</p>

<!-- 正文 -->
<div style="padding: 0 16px;">
  <p style="font-size: 16px; line-height: 1.8; margin: 12px 0; text-indent: 2em;">
    {正文}
  </p>
  <!-- 更多段落... -->
</div>

<!-- 风险提示 -->
<hr style="border: none; border-top: 1px solid #eee; margin: 20px 16px;">
<p style="font-size: 14px; color: #999; line-height: 1.6; padding: 0 16px;">
  本内容仅供参考，不构成投资建议。投资者据此操作，风险自担。<br>
  市场有风险，投资需谨慎。
</p>

</body>
</html>
```

---

## 质量检查清单

- [ ] 所有CSS内联，无 `<style>` 标签
- [ ] 标题层级正确（H1/H2/H3）
- [ ] 段落缩进2em
- [ ] 加粗标点在 `</strong>` 外
- [ ] 封面图提示存在
- [ ] 风险提示完整
- [ ] 暗黑模式属性注入（如需要）
- [ ] 外链转为上标脚注
- [ ] article.txt 纯文本无乱码
