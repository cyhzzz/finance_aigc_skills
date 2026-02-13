# Step 1: 大盘行情数据获取

## 明确目标
获取指定交易日的主要指数数据（上证指数、深证成指、创业板指）和资金流向数据（北向资金），为后续分析提供基础数据。

## 具体操作

### 1. 使用哪些工具
- **Shell工具**：`scripts/fetch_market_data.py`
- **数据库/API**：akshare API
- **搜索工具**：不需要

### 2. 查询哪些数据表/字段

#### akshare API映射
| 数据类型 | akshare API | 核心字段 |
|---------|-------------|---------|
| 上证指数 | `ak.index_zh_a_hist(symbol="000001")` | close, open, high, low, volume, amount |
| 深证成指 | `ak.index_zh_a_hist(symbol="399001")` | close, open, high, low, volume, amount |
| 创业板指 | `ak.index_zh_a_hist(symbol="399006")` | close, open, high, low, volume, amount |
| 北向资金 | `ak.stock_hsgt_north_net_flow_in_em()` | 净流入 |

### 3. 筛选和排序规则
- **筛选**：按日期筛选，获取指定交易日的数据
- **排序**：按涨跌幅排序，找出表现最好和最差的指数（Top 3）

### 4. 计算逻辑

#### 涨跌幅计算
```python
change = close - open
change_pct = (close - open) / open * 100
```

#### 方向判断
```python
direction = "上涨" if change > 0 else ("下跌" if change < 0 else "持平")
```

### 5. 操作流程
```
1. 输入日期参数（YYYY-MM-DD）
2. 调用 fetch_market_data.py
3. 获取三大指数数据
4. 获取北向资金数据
5. 计算涨跌幅和方向
6. 保存为JSON格式
```

## 输出格式

### 数据文件格式
JSON格式，包含：
- date: 交易日期
- indices: 指数数据字典
- funds: 资金数据字典

### 用户回复格式
```
=== 大盘行情数据获取完成 ===

日期：2026-02-10

主要指数表现：
1. 创业板指：2168.42点，+28.67点，+1.34%（领涨）
2. 深证成指：10852.36点，+89.45点，+0.83%
3. 上证指数：3268.15点，+25.68点，+0.79%

资金流向：
- 北向资金：净流入58.62亿元，持续流入

市场特征：
- 三大指数集体收涨
- 创业板指表现最为强势
- 北向资金大幅流入
```

## 下一步预告

接下来将进入 **Step 2: 板块数据获取**，获取行业板块表现数据，包括：
- 领涨板块 Top 5
- 领跌板块 Top 5
- 涨跌停统计
- 市场情绪指标

请确认是否继续？
