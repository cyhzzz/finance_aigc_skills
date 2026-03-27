# 市场数据获取固化模块

> 本模块为投顾写作Skill工厂的固化模块
> 提供A股市场数据获取的标准接口和LLM驱动指南
> 生成具体Skill时，本模块内容将复制到对应 `scripts/market_data.md`

---

## 功能定位

投顾文章需要准确的市场数据作为撰写基础。本模块定义：
1. **必需数据**：撰写文章必须获取的数据类型
2. **API接口**：akshare数据获取接口映射
3. **容错策略**：多数据源fallback机制
4. **输出格式**：标准化JSON输出格式

---

## 必需数据类型

撰写市场评论前，必须获取以下数据：

| 数据类型 | 用途 | 优先级 |
|:---|:---|:---:|
| 三大指数行情 | 市场概述段（涨跌幅、点位、成交额） | 必需 |
| 两市成交额 | 判断资金活跃度 | 必需 |
| 板块表现 | 鱼群/资金流向段 | 推荐 |
| 北向资金 | 资金流向参考（如可用） | 可选 |
| 热点资讯 | 事件分析段素材 | 推荐 |

---

## akshare API 映射

### 指数行情

```python
# 上证指数
ak.index_zh_a_hist(symbol="000001", period="daily", start_date=date, end_date=date)
# 返回字段：收盘、开盘、最高、最低、成交量、成交额、涨跌幅

# 深证成指
ak.index_zh_a_hist(symbol="399001", period="daily", start_date=date, end_date=date)

# 创业板指
ak.index_zh_a_hist(symbol="399006", period="daily", start_date=date, end_date=date)
```

**关键字段**：
- `收盘` / `close` - 收盘点位
- `涨跌幅` / `change_pct` - 涨跌幅百分比
- `成交额` / `amount` - 成交额（元）

### 北向资金

```python
ak.stock_hsgt_north_net_flow_in_em(symbol="北向", start_date=date, end_date=date)
```

**重要限制**：东方财富北向资金API通常仅支持获取当日或近期数据，查询历史日期可能返回空值。

**处理规则**：
- 若北向资金数据为null、0或unavailable，**直接忽略**该部分内容
- **不虚构**北向资金数据
- 可用其他资金流向数据（如融资融券余额）作为替代

### 板块数据

```python
# 行业板块涨跌排行
ak.stock_board_industry_name_em()
# 返回字段：板块名称、涨跌幅、成交额、上涨家数、下跌家数
```

### 市场统计

```python
# 个股涨跌统计
ak.stock_zh_a_spot_em()
# 可计算：涨停家数、跌停家数、上涨家数、下跌家数
```

---

## 多数据源容错策略

当主数据源失败时，按以下顺序 fallback：

### 指数数据 fallback 链

```
东方财富EM (stock_zh_index_daily_em)
    ↓ 失败
腾讯股票API (stock_zh_index_daily_tx)
    ↓ 失败
中证指数 (index_zh_a_hist)
    ↓ 失败
返回 error 状态，文章中标注"数据获取失败"
```

### 北向资金 fallback 链

```
东方财富EM (stock_hsgt_north_net_flow_in_em)
    ↓ 失败/无历史数据
返回 null，文章中直接忽略北向资金相关内容
```

---

## 标准化输出格式

### 指数行情输出

```json
{
  "indices": [
    {
      "code": "000001",
      "name": "上证指数",
      "date": "2026-03-25",
      "close": 4065.0,
      "change": 3.65,
      "change_pct": 0.09,
      "amount": 2500000000000,
      "amount_str": "2.50万亿",
      "status": "success"
    },
    {
      "code": "399001",
      "name": "深证成指",
      "close": 11500.0,
      "change": -40.25,
      "change_pct": -0.35,
      "amount": 3200000000000,
      "amount_str": "3.20万亿",
      "status": "success"
    },
    {
      "code": "399006",
      "name": "创业板指",
      "close": 2300.0,
      "change": -25.08,
      "change_pct": -1.08,
      "amount": 1500000000000,
      "amount_str": "1.50万亿",
      "status": "success"
    }
  ],
  "market_summary": {
    "rise_count": 1,
    "fall_count": 2,
    "market_type": "分化",
    "total_amount": 7.2,
    "total_amount_str": "7.20万亿",
    "status": "success"
  }
}
```

### 板块表现输出

```json
{
  "sectors": {
    "top_risers": [
      {"name": "银行", "change_pct": 0.85, "amount": 320000000000},
      {"name": "石油", "change_pct": 0.72, "amount": 180000000000}
    ],
    "top_fallers": [
      {"name": "科技", "change_pct": -2.15, "amount": 450000000000},
      {"name": "新能源", "change_pct": -1.88, "amount": 380000000000}
    ]
  },
  "status": "success"
}
```

### 资金流向输出

```json
{
  "north_bound": {
    "net_flow": 5000000000,
    "net_flow_str": "净流入50亿元",
    "status": "success|unavailable|null"
  },
  "status": "success"
}
```

---

## LLM 驱动模式

当 akshare 不可用或需要快速获取数据时，LLM 可通过搜索获取数据：

### 搜索获取策略

1. **指数行情**：搜索"上证指数 2026-03-25 收盘"
2. **板块排行**：搜索"A股板块 2026-03-25 涨幅排行"
3. **资讯事件**：搜索"2026年3月25日 A股重大消息"

### 搜索结果使用规范

- 搜索结果作为**补充参考**，优先使用 akshare 获取的精确数据
- 搜索获取的数据需**标注来源**（如"根据东方财富数据显示"）
- 搜索结果可能存在延迟，重要数据需**多源交叉验证**

---

## 数据质量检查

获取数据后，撰写前必须验证：

1. **完整性**：三大指数数据是否全部获取
2. **有效性**：涨跌幅是否为有效数值（非NaN）
3. **一致性**：指数点位与涨跌幅方向是否匹配（涨→点位上升）
4. **时效性**：数据日期是否为指定交易日

### 异常处理

| 异常情况 | 处理方式 |
|:---|:---|
| 指数数据缺失 | 标注"数据获取失败"，避免涉及该指数 |
| 涨跌幅为0或异常 | 检查数据源，更换数据接口 |
| 北向资金不可用 | 直接忽略，不虚构 |
| 节假日无数据 | 使用最近交易日数据，并标注 |

---

## 依赖

- **必需**：akshare >= 1.18.0, pandas >= 1.3.0
- **可选**：requests（用于搜索模式）

---

## 注意事项

1. **数据精度**：指数涨跌幅精确到小数点后两位，成交额单位统一为"亿元"或"万亿元"
2. **历史查询**：腾讯数据源仅支持当日快照，历史查询用东方财富EM源
3. **频率限制**：东方财富API可能有访问频率限制，批量查询添加适当延迟
4. **容错优先**：任何数据获取失败都不应阻断文章撰写，使用"数据获取失败"标注
