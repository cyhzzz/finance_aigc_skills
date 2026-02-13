# 资本市场热点抓取脚本使用说明

## 概述

基于 **NewsNow API** 的真实资本市场热点抓取工具，支持多个财经平台的自动化数据采集和关键词分析。

## 核心特性

### 1. 真实数据源
- **API 地址**: `https://newsnow.busiyi.world/api/s`
- **响应格式**: JSON
- **数据状态**:
  - `success`: 最新抓取的数据
  - `cache`: 缓存的数据

### 2. 支持的财经平台

| 平台 ID | 平台名称 | 状态 |
|---------|----------|------|
| `cls-hot` | 财联社热门 | ✓ 正常 |
| `wallstreetcn-hot` | 华尔街见闻 | ✓ 正常 |
| `sina-finance` | 新浪财经 | ⚠ API 故障 (500) |

**注意**: 平台可用性取决于 NewsNow 服务，部分平台可能偶尔返回错误。

### 3. 核心功能

- **自动重试机制**: 请求失败时自动重试（默认 2 次）
- **智能延迟**: 每次请求间隔 1 秒 ± 0.2 秒随机扰动
- **关键词过滤**: 105+ 财经关键词自动匹配
- **中文编码支持**: Windows 控制台完美兼容
- **结构化输出**: JSON 格式，UTF-8 编码

## 安装依赖

```bash
pip install requests
```

## 使用方法

### 基本用法

```bash
cd D:\project\skills\capital-market-topic-scout\scripts
python fetch_newsnow_topics.py
```

### 输出示例

```
============================================================
资本市场热点抓取工具
============================================================
时间: 2026-02-13 16:21:16
平台数量: 3
关键词数量: 105
============================================================

正在获取: 财联社热门 (cls-hot)
------------------------------------------------------------
[OK] 获取 cls-hot 成功 (缓存数据)
  提取到 13 条热点
  等待 1.2 秒...

正在获取: 华尔街见闻 (wallstreetcn-hot)
------------------------------------------------------------
[OK] 获取 wallstreetcn-hot 成功 (最新数据)
  提取到 10 条热点

正在分析数据...

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

## 输出文件

### 文件位置

```
D:\project\skills\capital-market-topic-scout\output\
└── finance_topics_YYYYMMDD_HHMMSS.json
```

### JSON 结构

```json
{
  "timestamp": "2026-02-13T16:21:30.413787",
  "platforms": {
    "cls-hot": {
      "name": "财联社热门",
      "total_items": 13,
      "finance_items": 12,
      "items": [
        {
          "rank": 1,
          "title": "【早报】深夜跳水！美股、黄金、白银、原油集体大跌",
          "url": "https://www.cls.cn/detail/2289071",
          "mobile_url": "",
          "matched_keywords": ["美股", "黄金", "原油", "跳水"]
        }
      ]
    }
  },
  "summary": {
    "total_platforms": 2,
    "total_items": 23,
    "finance_items": 20
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `rank` | int | 热点排名 |
| `title` | str | 热点标题 |
| `url` | str | 文章链接 |
| `mobile_url` | str | 移动端链接（可能为空） |
| `matched_keywords` | list | 匹配到的财经关键词 |

## 财经关键词列表

### 股市相关
`A股`, `港股`, `美股`, `股市`, `上证`, `深证`, `创业板`, `科创板`, `股票`, `涨停`, `跌停`, `大盘`, `指数`, `个股`, `板块`

### 宏观经济
`GDP`, `CPI`, `PPI`, `PMI`, `通胀`, `通缩`, `央行`, `降息`, `加息`, `货币政策`, `财政政策`, `宏观经济`

### 金融产品
`基金`, `债券`, `理财`, `信托`, `保险`, `银行`, `证券`, `期货`, `期权`, `外汇`, `汇率`, `黄金`, `原油`

### 投资相关
`投资`, `融资`, `IPO`, `上市`, `退市`, `并购`, `重组`, `定增`, `减持`, `增持`, `回购`, `分红`

### 行业概念
`新能源`, `半导体`, `芯片`, `人工智能`, `AI`, `医药`, `消费`, `地产`, `房地产`, `基建`

### 市场情绪
`利好`, `利空`, `暴涨`, `暴跌`, `震荡`, `反弹`, `回调`, `突破`, `跳水`, `飙升`

### 政策相关
`政策`, `监管`, `法规`, `税务`, `税率`, `补贴`, `优惠`

### 企业相关
`财报`, `业绩`, `营收`, `利润`, `亏损`, `盈利`

> 完整列表（105 个）见脚本源码 `FINANCE_KEYWORDS` 变量。

## 自定义配置

### 添加新平台

编辑 `fetch_newsnow_topics.py`:

```python
FINANCE_PLATFORMS = [
    ("cls-hot", "财联社热门"),
    ("wallstreetcn-hot", "华尔街见闻"),
    ("sina-finance", "新浪财经"),
    ("your-platform-id", "你的平台名称"),  # 添加这一行
]
```

**如何找到平台 ID**:
1. 访问 [NewsNow 分类页面](https://newsnow.busiyi.world/)
2. 找到想要的平台
3. 查看网络请求中的 `id` 参数

### 调整关键词

编辑 `FINANCE_KEYWORDS` 列表，添加或删除关键词：

```python
FINANCE_KEYWORDS = [
    "A股",
    "你的关键词",
    # ...
]
```

### 修改请求参数

```python
# 重试次数
max_retries=2

# 等待时间（秒）
min_wait=3
max_wait=5

# 请求间隔（秒）
request_interval=1.0
```

## TrendRadar 源码分析

### 1. API 调用方式

**源文件**: `TrendRadar/trendradar/crawler/fetcher.py`

核心代码：
```python
url = f"{api_url}?id={platform_id}&latest"

response = requests.get(
    url,
    headers=DEFAULT_HEADERS,
    timeout=10,
)
```

**关键参数**:
- `id`: 平台唯一标识
- `latest`: 强制获取最新数据（否则可能返回缓存）

### 2. 响应格式

```json
{
  "status": "success",  // 或 "cache"
  "items": [
    {
      "title": "标题",
      "url": "https://...",
      "mobileUrl": "https://..."
    }
  ]
}
```

### 3. 重试机制

TrendRadar 采用指数退避策略：

```python
base_wait = random.uniform(min_retry_wait, max_retry_wait)
additional_wait = (retries - 1) * random.uniform(1, 2)
wait_time = base_wait + additional_wait
```

- 第 1 次重试: 3-5 秒
- 第 2 次重试: 4-7 秒
- 第 3 次重试: 5-9 秒

### 4. 请求间隔

批量爬取时的间隔控制：

```python
actual_interval = request_interval + random.randint(-10, 20)
actual_interval = max(50, actual_interval)  # 最小 50ms
time.sleep(actual_interval / 1000)
```

## 常见问题

### Q1: 为什么新浪财经返回 500 错误？

**A**: NewsNow API 的某些平台可能暂时不可用，原因包括：
- 平台源网站结构变化
- API 后端爬虫故障
- 平台反爬虫限制

**解决方案**:
- 从 `FINANCE_PLATFORMS` 中移除该平台
- 等待 NewsNow 修复
- 联系 NewsNow 维护者

### Q2: Windows 控制台显示乱码

**A**: 脚本已包含编码修复代码：

```python
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

如果仍有问题，尝试：
```bash
chcp 65001
python fetch_newsnow_topics.py
```

### Q3: 如何增加更多平台？

**步骤**:
1. 访问 https://newsnow.busiyi.world/
2. 浏览分类，找到目标平台
3. 打开浏览器开发者工具 (F12)
4. 切换到 Network 标签
5. 点击平台，查看请求中的 `id` 参数
6. 添加到 `FINANCE_PLATFORMS`

### Q4: 可以用于生产环境吗？

**建议**:
- 添加日志记录（logging 模块）
- 增加错误监控（如 Sentry）
- 实现数据持久化（数据库）
- 添加速率限制（避免被封）
- 考虑使用代理池

## 性能基准

### 测试环境
- 时间: 2026-02-13 16:21:16
- 平台: 财联社、华尔街见闻
- 网络: 中国大陆

### 结果
- 总耗时: ~15 秒（含延迟）
- 成功率: 2/3 (66.7%)
- 数据质量: 财经相关占比 87%

## 扩展建议

### 1. 定时任务
使用 Windows 任务计划程序：

```bash
# 每小时运行一次
schtasks /create /tn "财经热点抓取" /tr "python D:\path\to\fetch_newsnow_topics.py" /sc hourly
```

### 2. 数据分析
基于抓取数据生成趋势报告：
- 热点词频统计
- 时间序列分析
- 情感分析

### 3. 消息推送
集成推送服务：
- 飞书机器人
- 企业微信
- 钉钉
- Telegram Bot

## 许可证

本脚本基于 TrendRadar (MIT License) 改编。

## 相关资源

- [NewsNow API](https://newsnow.busiyi.world/)
- [TrendRadar 项目](https://github.com/sansan0/TrendRadar)
- [requests 文档](https://docs.python-requests.org/)

---

**最后更新**: 2026-02-13
**脚本版本**: 1.0.0
