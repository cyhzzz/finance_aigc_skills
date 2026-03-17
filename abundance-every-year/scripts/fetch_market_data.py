#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取A股市场数据 - 多数据源支持
为每个数据类型提供2-3个数据源，按顺序尝试，提高健壮性
数据源：
- 上证指数：4个数据源（中证、腾讯、东方财富EM、新浪）
- 深证成指：2个数据源（腾讯、东方财富EM）
- 创业板指：2个数据源（腾讯、东方财富EM）
- 沪深300：1个数据源（东方财富EM）
- 北向资金：1个数据源（东方财富API，仅支持当日数据）

重要说明：
- 腾讯数据源（stock_zh_index_daily_tx）仅包含当日快照数据，历史日期查询可能返回空
- 东方财富EM数据源（stock_zh_index_daily_em）支持完整历史数据，是历史查询的主力源
- 建议：腾讯数据源作为第一选项（当日使用）；EM数据源作为历史日期的兜底
"""

import akshare as ak
import pandas as pd
from datetime import datetime, date
import json
import sys
import os
import time
import requests

# 导入data_cache
from data_cache import MarketDataCache


def fetch_sh_index_csindex(date_str):
    """
    数据源1: 使用 stock_zh_index_hist_csindex 获取上证指数历史数据（中证数据）

    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict or None: 指数数据，失败返回None
    """
    try:
        date_num = date_str.replace('-', '')
        df = ak.stock_zh_index_hist_csindex(symbol='000001', start_date=date_num, end_date=date_num)

        if df.empty:
            return None

        row = df.iloc[0]
        return {
            'close': float(row['收盘']),
            'open': float(row['开盘']),
            'high': float(row['最高']),
            'low': float(row['最低']),
            'change': float(row['涨跌']),
            'change_pct': float(row['涨跌幅']),
            'amount': float(row['成交金额']),
            'source': 'akshare.csindex'
        }
    except Exception as e:
        return None


def fetch_sh_index_tx(date_str):
    """
    数据源2: 使用 stock_zh_index_daily_tx 获取上证指数历史数据（腾讯数据）

    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict or None: 指数数据，失败返回None
    """
    try:
        df = ak.stock_zh_index_daily_tx(symbol='sh000001')

        if df.empty:
            return None

        year, month, day = map(int, date_str.split('-'))
        target_date = date(year, month, day)

        target_rows = df[df['date'] == target_date]

        if target_rows.empty:
            return None

        row = target_rows.iloc[0]

        # 计算涨跌和涨跌幅
        idx = df.index[df['date'] == target_date].tolist()[0]
        if idx > 0:
            prev_row = df.iloc[idx - 1]
            prev_close = float(prev_row['close'])
        else:
            prev_close = float(row['open'])

        change = float(row['close']) - prev_close
        change_pct = (change / prev_close) * 100 if prev_close > 0 else 0

        return {
            'close': float(row['close']),
            'open': float(row['open']),
            'high': float(row['high']),
            'low': float(row['low']),
            'change': change,
            'change_pct': change_pct,
            'amount': float(row['amount']) / 100000000,
            'source': 'akshare.tx'
        }
    except Exception as e:
        return None


def fetch_sh_index_sina(date_str):
    """
    数据源3: 使用 stock_zh_index_spot_sina 获取上证指数实时数据（新浪数据）
    注意：这是实时数据，不是历史数据

    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict or None: 指数数据，失败返回None
    """
    try:
        df = ak.stock_zh_index_spot_sina()

        if df.empty:
            return None

        # 查找上证指数
        sh_row = df[df['代码'] == 'sh000001']

        if sh_row.empty:
            return None

        row = sh_row.iloc[0]
        return {
            'close': float(row['最新价']),
            'open': float(row['今开']),
            'high': float(row['最高']),
            'low': float(row['最低']),
            'change': float(row['涨跌额']),
            'change_pct': float(row['涨跌幅']),
            'amount': float(row['成交额']) / 100000000 if '成交额' in row else 0,
            'source': 'akshare.sina'
        }
    except Exception as e:
        return None


def _fetch_index_em(symbol, date_str):
    """
    通用内部函数：使用 stock_zh_index_daily_em 获取指数历史数据（东方财富EM数据）
    支持历史数据查询，是腾讯数据源失效时的主力备用数据源。

    Args:
        symbol: 指数代码，如 'sh000001'（上证）、'sz399001'（深证）、'sz399006'（创业板）、'sh000300'（沪深300）
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict or None: 指数数据，失败返回None
    """
    try:
        date_num = date_str.replace('-', '')
        df = ak.stock_zh_index_daily_em(symbol=symbol, start_date=date_num, end_date=date_num)

        if df is None or df.empty:
            return None

        row = df.iloc[0]

        # 字段兼容处理：不同版本 akshare 列名可能有差异
        def get_col(row, *candidates):
            for c in candidates:
                if c in row.index:
                    return float(row[c])
            return 0.0

        close = get_col(row, 'close', '收盘')
        open_ = get_col(row, 'open', '开盘')
        high = get_col(row, 'high', '最高')
        low = get_col(row, 'low', '最低')
        # 涨跌幅：优先使用接口直接返回的字段
        change_pct = get_col(row, 'change_rate', '涨跌幅', 'pct_chg')
        # 涨跌额：部分接口直接给出；若无则由涨跌幅反算
        if 'change' in row.index:
            change = float(row['change'])
        elif '涨跌' in row.index:
            change = float(row['涨跌'])
        else:
            prev_close = close / (1 + change_pct / 100) if change_pct != 0 else close
            change = close - prev_close

        # 成交额：单位统一为亿元
        raw_amount = get_col(row, 'amount', '成交额', 'volume')
        # EM 接口成交额单位为元，需转换为亿元
        amount = raw_amount / 100000000 if raw_amount > 10000000 else raw_amount

        return {
            'close': close,
            'open': open_,
            'high': high,
            'low': low,
            'change': change,
            'change_pct': change_pct,
            'amount': amount,
            'source': 'akshare.em'
        }
    except Exception as e:
        return None


def fetch_sh_index_em(date_str):
    """
    数据源4: 使用东方财富EM接口获取上证指数历史数据
    """
    return _fetch_index_em('sh000001', date_str)


def fetch_sz_index_em(date_str):
    """
    数据源2: 使用东方财富EM接口获取深证成指历史数据
    """
    return _fetch_index_em('sz399001', date_str)


def fetch_cyb_index_em(date_str):
    """
    数据源2: 使用东方财富EM接口获取创业板指历史数据
    """
    return _fetch_index_em('sz399006', date_str)


def fetch_hs300_index_em(date_str):
    """
    数据源1: 使用东方财富EM接口获取沪深300历史数据
    """
    return _fetch_index_em('sh000300', date_str)


def fetch_sz_index_tx(date_str):
    """
    数据源1: 使用 stock_zh_index_daily_tx 获取深证成指历史数据（腾讯数据）

    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict or None: 指数数据，失败返回None
    """
    try:
        df = ak.stock_zh_index_daily_tx(symbol='sz399001')

        if df.empty:
            return None

        year, month, day = map(int, date_str.split('-'))
        target_date = date(year, month, day)

        target_rows = df[df['date'] == target_date]

        if target_rows.empty:
            return None

        row = target_rows.iloc[0]

        # 计算涨跌和涨跌幅
        idx = df.index[df['date'] == target_date].tolist()[0]
        if idx > 0:
            prev_row = df.iloc[idx - 1]
            prev_close = float(prev_row['close'])
        else:
            prev_close = float(row['open'])

        change = float(row['close']) - prev_close
        change_pct = (change / prev_close) * 100 if prev_close > 0 else 0

        return {
            'close': float(row['close']),
            'open': float(row['open']),
            'high': float(row['high']),
            'low': float(row['low']),
            'change': change,
            'change_pct': change_pct,
            'amount': float(row['amount']) / 100000000,
            'source': 'akshare.tx'
        }
    except Exception as e:
        return None


def fetch_cyb_index_tx(date_str):
    """
    数据源1: 使用 stock_zh_index_daily_tx 获取创业板指历史数据（腾讯数据）

    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict or None: 指数数据，失败返回None
    """
    try:
        df = ak.stock_zh_index_daily_tx(symbol='sz399006')

        if df.empty:
            return None

        year, month, day = map(int, date_str.split('-'))
        target_date = date(year, month, day)

        target_rows = df[df['date'] == target_date]

        if target_rows.empty:
            return None

        row = target_rows.iloc[0]

        # 计算涨跌和涨跌幅
        idx = df.index[df['date'] == target_date].tolist()[0]
        if idx > 0:
            prev_row = df.iloc[idx - 1]
            prev_close = float(prev_row['close'])
        else:
            prev_close = float(row['open'])

        change = float(row['close']) - prev_close
        change_pct = (change / prev_close) * 100 if prev_close > 0 else 0

        return {
            'close': float(row['close']),
            'open': float(row['open']),
            'high': float(row['high']),
            'low': float(row['low']),
            'change': change,
            'change_pct': change_pct,
            'amount': float(row['amount']) / 100000000,
            'source': 'akshare.tx'
        }
    except Exception as e:
        return None


def fetch_north_capital_em(date_str):
    """
    数据源1: 使用东方财富API获取北向资金数据（当日数据）
    重要说明：该API仅支持获取当日数据，无法查询历史日期的北向资金

    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict or None: 资金数据，失败返回None
    """
    try:
        # 使用东方财富API获取北向资金数据
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            "reportName": "RPT_MUTUAL_QUOTA",
            "columns": "TRADE_DATE,MUTUAL_TYPE,BOARD_TYPE,MUTUAL_TYPE_NAME,FUNDS_DIRECTION,"
            "INDEX_CODE,INDEX_NAME,BOARD_CODE",
            "quoteColumns": "status~07~BOARD_CODE,dayNetAmtIn~07~BOARD_CODE,dayAmtRemain~07~BOARD_CODE,"
            "dayAmtThreshold~07~BOARD_CODE,f104~07~BOARD_CODE,f105~07~BOARD_CODE,"
            "f106~07~BOARD_CODE,f3~03~INDEX_CODE~INDEX_f3,netBuyAmt~07~BOARD_CODE",
            "quoteType": "0",
            "pageNumber": "1",
            "pageSize": "5000",
            "sortTypes": "-1",
            "sortColumns": "TRADE_DATE",
            "source": "WEB",
            "client": "WEB",
            "filter": "(FUNDS_DIRECTION=\"北向\")",
        }

        import requests
        r = requests.get(url, params=params, timeout=10)
        data_json = r.json()

        if 'result' in data_json and data_json['result'] and 'data' in data_json['result']:
            df = pd.DataFrame(data_json['result']['data'])

            # 筛选沪股通和深股通
            sh_row = df[df['MUTUAL_TYPE_NAME'] == '沪股通']
            sz_row = df[df['MUTUAL_TYPE_NAME'] == '深股通']

            # 计算北向资金总净流入（单位：亿元）
            sh_inflow = float(sh_row.iloc[0]['netBuyAmt']) / 10000 if not sh_row.empty else 0
            sz_inflow = float(sz_row.iloc[0]['netBuyAmt']) / 10000 if not sz_row.empty else 0

            total_inflow = sh_inflow + sz_inflow

            return {
                'net_inflow': total_inflow,
                'sh_inflow': sh_inflow,
                'sz_inflow': sz_inflow,
                'date': date_str,
                'source': 'eastmoney',
                'note': '该API仅支持获取当日数据'
            }
        else:
            return None
    except Exception as e:
        return None


def try_multiple_sources(sources, date_str, source_names):
    """
    尝试多个数据源，按顺序尝试，直到成功或全部失败

    Args:
        sources: 数据源函数列表
        date_str: 日期字符串
        source_names: 数据源名称列表

    Returns:
        tuple: (数据dict, 使用的数据源索引)
    """
    last_error = None

    for i, (source_func, source_name) in enumerate(zip(sources, source_names)):
        try:
            data = source_func(date_str)
            if data:
                return data, i
            last_error = f"数据源 {source_name} 返回空数据"
        except Exception as e:
            last_error = str(e)
            continue

    return None, -1


def fetch_market_data(date_str):
    """
    获取指定日期的A股市场数据（多数据源支持）

    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict: 市场数据
    """
    data = {
        'date': date_str,
        'indices': {},
        'funds': {},
        'statistics': {},
        'sectors': {},
        'error': None
    }

    try:
        print(f"\n{'='*60}")
        print(f"获取 {date_str} A股市场数据（多数据源模式）")
        print(f"{'='*60}")

        # 1. 获取上证指数（4个数据源：中证 > 腾讯 > EM > 新浪）
        print(f"\n[1/5] 获取上证指数（4个数据源：中证 > 腾讯 > EM > 新浪）...")
        sh_sources = [
            (fetch_sh_index_csindex, '中证数据'),
            (fetch_sh_index_tx,      '腾讯数据'),
            (fetch_sh_index_em,      '东方财富EM'),
            (fetch_sh_index_sina,    '新浪实时'),
        ]

        for i, (source_func, source_name) in enumerate(sh_sources, 1):
            print(f"  尝试数据源{i} ({source_name})...", end='', flush=True)
            try:
                sh_data = source_func(date_str)
                if sh_data:
                    data['indices']['sh'] = {
                        'name': '上证指数',
                        'code': '000001.SH',
                        **sh_data
                    }
                    sign = '+' if sh_data['change'] >= 0 else ''
                    print(f" OK")
                    print(f"    收盘: {sh_data['close']:.2f} ({sign}{sh_data['change']:.2f}, {sign}{sh_data['change_pct']:.2f}%)")
                    print(f"    成交额: {sh_data['amount']:.2f}亿元")
                    break
                else:
                    print(f" 无数据")
            except Exception as e:
                print(f" 失败: {str(e)[:60]}")
                continue

        if 'sh' not in data['indices']:
            print(f"  所有数据源均失败")
            data['error'] = '上证指数所有数据源均失败'

        # 2. 获取深证成指（2个数据源：腾讯 > EM）
        print(f"\n[2/5] 获取深证成指（2个数据源：腾讯 > EM）...")
        sz_sources = [
            (fetch_sz_index_tx, '腾讯数据'),
            (fetch_sz_index_em, '东方财富EM'),
        ]

        for i, (source_func, source_name) in enumerate(sz_sources, 1):
            print(f"  尝试数据源{i} ({source_name})...", end='', flush=True)
            try:
                sz_data = source_func(date_str)
                if sz_data:
                    data['indices']['sz'] = {
                        'name': '深证成指',
                        'code': '399001.SZ',
                        **sz_data
                    }
                    sign = '+' if sz_data['change'] >= 0 else ''
                    print(f" OK")
                    print(f"    收盘: {sz_data['close']:.2f} ({sign}{sz_data['change']:.2f}, {sign}{sz_data['change_pct']:.2f}%)")
                    print(f"    成交额: {sz_data['amount']:.2f}亿元")
                    break
                else:
                    print(f" 无数据")
            except Exception as e:
                print(f" 失败: {str(e)[:60]}")
                continue

        if 'sz' not in data['indices']:
            print(f"  所有数据源均失败")

        # 3. 获取创业板指（2个数据源：腾讯 > EM）
        print(f"\n[3/5] 获取创业板指（2个数据源：腾讯 > EM）...")
        cyb_sources = [
            (fetch_cyb_index_tx, '腾讯数据'),
            (fetch_cyb_index_em, '东方财富EM'),
        ]

        for i, (source_func, source_name) in enumerate(cyb_sources, 1):
            print(f"  尝试数据源{i} ({source_name})...", end='', flush=True)
            try:
                cyb_data = source_func(date_str)
                if cyb_data:
                    data['indices']['cyb'] = {
                        'name': '创业板指',
                        'code': '399006.SZ',
                        **cyb_data
                    }
                    sign = '+' if cyb_data['change'] >= 0 else ''
                    print(f" OK")
                    print(f"    收盘: {cyb_data['close']:.2f} ({sign}{cyb_data['change']:.2f}, {sign}{cyb_data['change_pct']:.2f}%)")
                    print(f"    成交额: {cyb_data['amount']:.2f}亿元")
                    break
                else:
                    print(f" 无数据")
            except Exception as e:
                print(f" 失败: {str(e)[:60]}")
                continue

        if 'cyb' not in data['indices']:
            print(f"  所有数据源均失败")

        # 4. 获取沪深300（EM数据源）
        print(f"\n[4/5] 获取沪深300（东方财富EM）...")
        print(f"  尝试数据源1 (东方财富EM)...", end='', flush=True)
        try:
            hs300_data = fetch_hs300_index_em(date_str)
            if hs300_data:
                data['indices']['hs300'] = {
                    'name': '沪深300',
                    'code': '000300.SH',
                    **hs300_data
                }
                sign = '+' if hs300_data['change'] >= 0 else ''
                print(f" OK")
                print(f"    收盘: {hs300_data['close']:.2f} ({sign}{hs300_data['change']:.2f}, {sign}{hs300_data['change_pct']:.2f}%)")
                print(f"    成交额: {hs300_data['amount']:.2f}亿元")
            else:
                print(f" 无数据")
        except Exception as e:
            print(f" 失败: {str(e)[:60]}")

        # 5. 获取北向资金（东方财富API，仅当日）
        print(f"\n[5/5] 获取北向资金（东方财富API）...")
        print(f"  注意：该API仅支持获取当日数据，历史日期可能无有效数据", flush=True)
        print(f"  尝试数据源 (东方财富API)...", end='', flush=True)
        try:
            funds_data = fetch_north_capital_em(date_str)
            if funds_data:
                data['funds']['north'] = {
                    'name': '北向资金',
                    **funds_data
                }
                sign = '+' if funds_data['net_inflow'] >= 0 else ''
                print(f" OK")
                print(f"    净流入: {sign}{abs(funds_data['net_inflow']):.2f}亿 (沪:{funds_data['sh_inflow']:+.2f}亿, 深:{funds_data['sz_inflow']:+.2f}亿)")

                # 检查是否为当日数据
                today = datetime.now().strftime('%Y-%m-%d')
                if date_str != today and abs(funds_data['net_inflow']) < 0.01:
                    print(f"    警告: {date_str}不是当日，返回的数据可能是当日数据或无效数据")
                    data['funds']['north']['note'] = f'API仅支持获取当日数据，{date_str}的历史数据不可用'
            else:
                print(f" 无数据")
                data['funds']['north'] = {
                    'name': '北向资金',
                    'net_inflow': None,
                    'sh_inflow': None,
                    'sz_inflow': None,
                    'source': 'eastmoney',
                    'note': 'API仅支持获取当日数据'
                }
        except Exception as e:
            print(f" 失败: {str(e)[:60]}")
            data['funds']['north'] = {
                'name': '北向资金',
                'net_inflow': None,
                'sh_inflow': None,
                'sz_inflow': None,
                'source': 'eastmoney',
                'error': str(e)
            }

        # 检查是否有核心数据
        if not data['indices']:
            data['error'] = '所有指数数据均获取失败'
        else:
            data['source'] = 'akshare'

        return data

    except Exception as e:
        error_msg = str(e)
        data['error'] = error_msg
        print(f"\n数据获取失败: {error_msg[:100]}")
        return data


def main():
    """主函数 - 获取指定日期数据"""
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        # 默认使用今天
        date_str = datetime.now().strftime('%Y-%m-%d')

    data = fetch_market_data(date_str)

    # 保存为 JSON
    output_file = f'/tmp/market_data_{date_str}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"数据已保存: {output_file}")

    # 检查数据质量
    if data.get('error') or not data.get('indices'):
        print(f"\n数据获取失败: {data.get('error', '未知错误')}")
        print(f"\n无法生成收评报告")
        sys.exit(1)

    # 打印关键数据
    print(f"\n{'='*60}")
    print(f"市场概况 ({date_str})")
    print(f"{'='*60}")

    index_order = ['sh', 'sz', 'cyb', 'hs300']
    for key in index_order:
        idx = data['indices'].get(key)
        if isinstance(idx, dict) and 'name' in idx:
            sign = '+' if idx['change'] >= 0 else ''
            print(f"\n{idx['name']:8s}:")
            print(f"  收盘: {idx['close']:10.2f}")
            print(f"  涨跌: {sign}{idx['change']:8.2f} ({sign}{idx['change_pct']:6.2f}%)")
            print(f"  成交额: {idx['amount']:10.2f}亿元")
            if 'source' in idx:
                print(f"  数据源: {idx['source']}")

    if 'north' in data['funds'] and isinstance(data['funds']['north'], dict):
        funds = data['funds']['north']
        if 'net_inflow' in funds and funds['net_inflow'] is not None:
            sign = '+' if funds['net_inflow'] >= 0 else ''
            print(f"\n北向资金: {sign}{funds['net_inflow']:.2f}亿")
        else:
            print(f"\n北向资金: 数据不可用（API仅支持获取当日数据）")
            if 'note' in funds:
                print(f"  说明: {funds['note']}")

    print(f"\n数据来源: {data.get('source', 'akshare')}")
    print(f"{'='*60}")
    print(f"数据获取成功")

    # 保存到缓存
    cache = MarketDataCache()
    cache.save_data(date_str, data)
    print(f"数据已保存到缓存")

    return data


if __name__ == '__main__':
    main()
