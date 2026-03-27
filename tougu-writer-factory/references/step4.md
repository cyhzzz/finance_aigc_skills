# Step 4：HTML可视化输出

> **本文档为具体Skill（如"收评writer"）的操作Phase 4**
> 当具体Skill执行时，按此步骤使用HTML模板生成可视化海报
> 元skill生成具体Skill时，将此步骤复制到生成物的 `references/step4.md`

---

## 目标

将润色后的文章内容填充到HTML模板中，生成可分享的视觉化海报。

---

## HTML模板

模板文件：`references/{风格名}html海报模板.html`

模板使用 [Tailwind CSS](https://tailwindcss.com/) 构建，无需额外安装。

---

## 模板变量说明

### 必填变量

| 变量名 | 说明 | 示例 |
|:---|:---|:---|
| `{{BRAND_NAME}}` | 品牌/栏目名称 | 年年有鱼 |
| `{{AUTHOR_NAME}}` | 作者姓名 | 于晴于理 |
| `{{ARTICLE_TYPE}}` | 文章类型 | 收评/早评 |
| `{{HEADLINE}}` | 主标题 | 节前收官在即，鱼群高低切换待春归 |
| `{{SUBTITLE}}` | 副标题（——本栏目为...） | ——本栏目为"于晴于理"观点收评 |
| `{{PUBLISH_DATE}}` | 发布日期 | 2026年3月25日 |
| `{{RISK_DISCLOSURE}}` | 风险提示文字 | 本内容仅供参考，不构成投资建议... |
| `{{SUBSCRIPTION_CTA}}` | 签约引导语 | 解锁更多内容 |

### 内容区变量（根据文章段落）

| 变量名 | 对应段落 |
|:---|:---|
| `{{MARKET_SUMMARY}}` | 第1段：市场概述 |
| `{{EVENT_ANALYSIS}}` | 第2段：事件分析 |
| `{{PERIPHERY_MARKET}}` | 第3段：外围市场 |
| `{{TECH_ANALYSIS}}` | 第4段：技术分析 |
| `{{FUND_FLOW}}` | 第5段：资金板块 |
| `{{OPERATION_SUGGESTION}}` | 第6段：操作建议 |

### 数据卡片变量

| 变量名 | 说明 | 示例 |
|:---|:---|:---|
| `{{INDEX_DATA}}` | 指数数据JSON | 见下方格式 |
| `{{FUND_DATA}}` | 资金流向数据 | 见下方格式 |

---

## 数据卡片格式

### 指数数据

```html
<div class="data-card bg-rice-paper rounded-lg p-3 border border-light-gray">
    <div class="flex justify-between items-center mb-1">
        <span class="text-xs text-silver-gray">上证指数</span>
        <span class="text-xs text-silver-gray">2月6日</span>
    </div>
    <div class="font-mono text-2xl font-bold text-daiqing">4065</div>
    <div class="text-xs text-silver-gray mt-1">震荡延续</div>
</div>
```

### JSON格式数据

如果使用JavaScript动态渲染：

```javascript
const indexData = [
    { name: "上证指数", value: "4065", change: "+0.09%", date: "2月6日", status: "震荡" },
    { name: "深证成指", value: "11500", change: "-0.35%", date: "2月6日", status: "分化" },
    { name: "两市成交额", value: "2.15", unit: "万亿", subtext: "-300亿", trend: "↓缩量" }
];
```

---

## 操作流程

### 方式一：手动替换

1. 打开 `references/{风格名}html海报模板.html`
2. 搜索 `{{VARIABLE_NAME}}`
3. 替换为实际内容
4. 保存为新文件（如 `output_20260325.html`）

### 方式二：脚本渲染

如果项目包含 `render_html.py`：

```bash
python scripts/render_html.py \
    --template references/{风格名}html海报模板.html \
    --data ./market_data_20260325.json \
    --article ./article_final.md \
    --output ./poster_20260325.html
```

---

## 生成后检查

- [ ] 所有 `{{VARIABLE_NAME}}` 已被替换（无遗留）
- [ ] 标题显示正确
- [ ] 风险提示完整
- [ ] 品牌信息正确
- [ ] 日期正确
- [ ] 整体布局正常

---

## 输出

生成完成后，可：

1. **直接打开**：在浏览器中查看效果
2. **截图分享**：使用浏览器截图工具
3. **打印PDF**：浏览器打印功能导出

---

## 完整流程结束

恭喜！文章从数据获取到可视化输出已完成。

最终输出物：
- `article_final.md` — 文章终稿（Markdown）
- `poster_YYYYMMDD.html` — 可视化海报（HTML）
