# 热点抓取脚本使用说明

## 📡 脚本说明

`fetch_hot_topics.py` 是一个轻量级的热点抓取脚本，用于获取今日资本市场热点。

---

## 🚀 快速开始

### 方式 1：直接运行（使用示例数据）

```bash
cd D:\project\skills\capital-market-topic-scout\scripts
python fetch_hot_topics.py
```

**输出示例**：
```
📊 资本市场热点 - 2025-02-13
============================================================

【财联社】
  1. A股三大股指集体大跌，创业板指跌超4%
  2. 北向资金全天净流出超120亿元
  3. 证监会：暂停转融券业务

【华尔街见闻】
  1. 美联储暗示可能推迟降息
  2. 美股科技股集体下挫
  3. 原油价格突破80美元

【微博】
  1. 基金亏损上热搜
  2. A股

【知乎】
  1. 如何看待近期A股大跌？
  2. 2025年适合定投吗？

============================================================
共 10 条热点
✅ 数据已保存到: .../hot_topics_20250213_143052.json
```

---

## 🔌 方式 2：集成 TrendRadar（推荐）

TrendRadar 有完整的热点抓取功能，可以直接使用：

### Step 1: 安装依赖

```bash
cd D:\project\skills\TrendRadar
pip install -r requirements.txt
```

### Step 2: 运行 TrendRadar

```bash
# Windows
start-http.bat

# macOS/Linux
./start-http.sh
```

### Step 3: 查看热点

访问本地 Web 界面（通常是 `http://localhost:8000`）

---

## 📊 数据源说明

### 当前脚本使用的数据源

**模拟数据**（演示用）：
- 财联社：A股相关热点
- 华尔街见闻：美股、宏观热点
- 微博热搜：社会关注话题
- 知乎热榜：讨论热点

### 可扩展的真实数据源

如果您想使用真实数据源，可以修改 `fetch_hot_topics.py`：

#### 1. newsnow API

TrendRadar 使用的 API：
```python
import requests

def fetch_from_newsnow():
    url = "https://inshorts.com/api/en/search/news"
    params = {"category": "business"}
    response = requests.get(url, params=params)
    return response.json()
```

#### 2. 微博热搜 API

```python
def fetch_weibo_hot():
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://weibo.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()
```

#### 3. 知乎热榜 API

```python
def fetch_zhihu_hot():
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    return response.json()
```

---

## 📁 输出格式

### 文本输出

控制台打印格式化的热点列表，按平台分组。

### JSON 输出

保存到 `output/hot_topics_YYYYMMDD_HHMMSS.json`：

```json
{
  "fetch_time": "2025-02-13T14:30:52",
  "total_count": 10,
  "topics": [
    {
      "title": "A股三大股指集体大跌，创业板指跌超4%",
      "source": "财联社",
      "rank": 1,
      "platform": "财联社"
    }
  ]
}
```

---

## 🔧 自定义配置

### 修改关键词过滤

编辑 `fetch_financial_hotwords()` 函数：

```python
def fetch_financial_hotwords():
    keywords = [
        "你的关键词1",
        "你的关键词2",
        # 添加更多...
    ]
    return keywords
```

### 添加新平台

1. 在 `fetch_sample_hot_topics()` 中添加新平台数据
2. 或者创建新的 fetch 函数：

```python
def fetch_your_platform():
    """你的平台数据源"""
    return [
        {"title": "热点标题", "source": "来源", "rank": 1, "platform": "你的平台"},
    ]
```

然后在 `main()` 中调用：

```python
def main():
    topics = fetch_sample_hot_topics()
    your_topics = fetch_your_platform()
    topics.extend(your_topics)
    # ...
```

---

## 🚀 与 Skill 集成

### 在 Claude Code 中使用

运行脚本后，可以这样使用 skill：

```
请使用 capital-market-topic-scout 分析以下热点：
A股三大股指集体大跌，创业板指跌超4%
北向资金全天净流出超120亿元
```

### 自动化工作流

创建一个批处理脚本：

```bash
# fetch_and_analyze.bat
@echo off
echo 正在抓取热点...
python scripts\fetch_hot_topics.py > hot_topics.txt

echo.
echo 正在分析选题...
echo 请使用 capital-market-topic-scout 分析以下热点：
type hot_topics.txt
```

---

## 📝 开发计划

### v1.1 计划功能

- [ ] 集成真实 API（微博、知乎）
- [ ] 支持命令行参数（选择平台）
- [ ] 增加历史数据对比
- [ ] 自动去重和排序

### v2.0 计划功能

- [ ] Web 界面
- [ ] 定时任务（每小时抓取）
- [ ] 数据库存储
- [ ] 热点趋势分析

---

## 🆚 TrendRadar vs 独立脚本

| 特性 | TrendRadar | 独立脚本 |
|------|------------|----------|
| **功能完整性** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **部署难度** | 需要配置 | 开箱即用 |
| **数据源** | 11个平台 | 4个平台（示例） |
| **推送功能** | ✅ 支持 | ❌ 不支持 |
| **适用场景** | 长期使用 | 快速测试 |

**推荐**：
- 开发测试：使用独立脚本
- 生产环境：使用 TrendRadar

---

## 📞 问题反馈

如有问题或建议，请提交 Issue：
https://github.com/cyhzzz/finance_aigc_skills/issues
