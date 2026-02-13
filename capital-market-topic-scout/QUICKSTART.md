# 资本市场热点抓取 - 快速开始

## 5 分钟上手

### 1. 安装依赖

```bash
pip install requests
```

### 2. 运行脚本

```bash
cd D:\project\skills\capital-market-topic-scout\scripts
python fetch_newsnow_topics.py
```

### 3. 查看结果

输出文件位置：
```
D:\project\skills\capital-market-topic-scout\output\finance_topics_YYYYMMDD_HHMMSS.json
```

## 核心功能

### 支持的平台

| 平台 | 状态 | 说明 |
|------|------|------|
| 财联社热门 | ✓ 正常 | 92.3% 财经相关 |
| 华尔街见闻 | ✓ 正常 | 80.0% 财经相关 |

### 自动过滤

脚本会自动匹配 105 个财经关键词，只保留相关热点：
- 股市：A股、港股、美股、涨停、跌停...
- 宏观：GDP、CPI、央行、降息...
- 金融：基金、债券、理财、保险...

## 输出示例

### 控制台输出

```
============================================================
抓取结果摘要
============================================================
平台数量: 2
总热点数: 23
财经相关: 20
财经占比: 87.0%

各平台详情:
------------------------------------------------------------
  财联社热门       :  13 条热点,  12 条财经相关 ( 92.3%)
  华尔街见闻       :  10 条热点,   8 条财经相关 ( 80.0%)
============================================================
```

### JSON 数据

```json
{
  "timestamp": "2026-02-13T16:21:30",
  "platforms": {
    "cls-hot": {
      "name": "财联社热门",
      "items": [
        {
          "rank": 1,
          "title": "【早报】深夜跳水！美股、黄金、白银、原油集体大跌",
          "url": "https://www.cls.cn/detail/2289071",
          "matched_keywords": ["美股", "黄金", "原油", "跳水"]
        }
      ]
    }
  }
}
```

## 常见问题

### Q: 如何添加新平台？

编辑 `scripts/fetch_newsnow_topics.py`:

```python
FINANCE_PLATFORMS = [
    ("cls-hot", "财联社热门"),
    ("your-platform-id", "你的平台"),  # 添加这一行
]
```

### Q: 如何自定义关键词？

编辑 `FINANCE_KEYWORDS` 列表：

```python
FINANCE_KEYWORDS = [
    "A股",
    "你的关键词",
    # ...
]
```

### Q: 定时运行怎么办？

**Windows**:
```powershell
schtasks /create /tn "财经热点" /tr "python D:\path\to\fetch_newsnow_topics.py" /sc hourly
```

**Linux**:
```bash
0 * * * * cd /path/to/scripts && python fetch_newsnow_topics.py
```

## 文档索引

- **详细使用说明**: `scripts/README_NEWSNOW.md`
- **源码分析报告**: `docs/NEWSNOW_ANALYSIS_REPORT.md`
- **API 测试工具**: `scripts/test_newsnow_api.py`

## 技术支持

遇到问题？
1. 查看 `scripts/README_NEWSNOW.md` 常见问题章节
2. 运行 `python test_newsnow_api.py` 测试 API 连接
3. 检查网络连接和防火墙设置

---

**最后更新**: 2026-02-13
**脚本版本**: 1.0.0
