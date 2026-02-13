#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取A股市场数据 - 多数据源支持
为每个数据类型提供2-3个数据源，按顺序尝试，提高健壮性
数据源：
- 上证指数：3个数据源（中证、腾讯、新浪）
- 深证成指：1个数据源（腾讯）
- 创业板指：1个数据源（腾讯）
- 北向资金：1个数据源（东方财富API，仅支持当日数据）
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

        # 1. 获取上证指数（3个数据源）
        print(f"\n[1/4] 获取上证指数（3个数据源）...")
        sh_sources = [fetch_sh_index_csindex, fetch_sh_index_tx, fetch_sh_index_sina]
        sh_source_names = ['中证数据', '腾讯数据', '新浪数据（实时）']

        for i, (source_func, source_name) in enumerate(zip(sh_sources, sh_source_names), 1):
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
                    print(f" ✅ 成功")
                    print(f"    收盘: {sh_data['close']:.2f} ({sign}{sh_data['change']:.2f}, {sign}{sh_data['change_pct']:.2f}%)")
                    print(f"    成交额: {sh_data['amount']:.2f}亿元")
                    break
                else:
                    print(f" ❌ 无数据")
            except Exception as e:
                print(f" ❌ 失败: {str(e)[:60]}")
                continue

        if 'sh' not in data['indices']:
            print(f"  ❌ 所有数据源均失败")
            data['error'] = '上证指数所有数据源均失败'

        # 2. 获取深证成指（1个数据源）
        print(f"\n[2/4] 获取深证成指（1个数据源）...")
        print(f"  尝试数据源1 (腾讯数据)...", end='', flush=True)
        try:
            sz_data = fetch_sz_index_tx(date_str)
            if sz_data:
                data['indices']['sz'] = {
                    'name': '深证成指',
                    'code': '399001.SZ',
                    **sz_data
                }
                sign = '+' if sz_data['change'] >= 0 else ''
                print(f" ✅ 成功")
                print(f"    收盘: {sz_data['close']:.2f} ({sign}{sz_data['change']:.2f}, {sign}{sz_data['change_pct']:.2f}%)")
                print(f"    成交额: {sz_data['amount']:.2f}亿元")
            else:
                print(f" ❌ 无数据")
        except Exception as e:
            print(f" ❌ 失败: {str(e)[:60]}")

        # 3. 获取创业板指（1个数据源）
        print(f"\n[3/4] 获取创业板指（1个数据源）...")
        print(f"  尝试数据源1 (腾讯数据)...", end='', flush=True)
        try:
            cyb_data = fetch_cyb_index_tx(date_str)
            if cyb_data:
                data['indices']['cyb'] = {
                    'name': '创业板指',
                    'code': '399006.SZ',
                    **cyb_data
                }
                sign = '+' if cyb_data['change'] >= 0 else ''
                print(f" ✅ 成功")
                print(f"    收盘: {cyb_data['close']:.2f} ({sign}{cyb_data['change']:.2f}, {sign}{cyb_data['change_pct']:.2f}%)")
                print(f"    成交额: {cyb_data['amount']:.2f}亿元")
            else:
                print(f" ❌ 无数据")
        except Exception as e:
            print(f" ❌ 失败: {str(e)[:60]}")

        # 4. 获取北向资金（1个数据源）
        print(f"\n[4/4] 获取北向资金（东方财富API）...")
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
                print(f" ✅ 成功")
                print(f"    净流入: {sign}{abs(funds_data['net_inflow']):.2f}亿 (沪:{funds_data['sh_inflow']:+.2f}亿, 深:{funds_data['sz_inflow']:+.2f}亿)")

                # 检查是否为当日数据
                today = datetime.now().strftime('%Y-%m-%d')
                if date_str != today and abs(funds_data['net_inflow']) < 0.01:
                    print(f"    ⚠️  警告: {date_str}不是当日，返回的数据可能是当日数据或无效数据")
                    data['funds']['north']['note'] = f'API仅支持获取当日数据，{date_str}的历史数据不可用'
            else:
                print(f" ❌ 无数据")
                data['funds']['north'] = {
                    'name': '北向资金',
                    'net_inflow': None,
                    'sh_inflow': None,
                    'sz_inflow': None,
                    'source': 'eastmoney',
                    'note': 'API仅支持获取当日数据'
                }
        except Exception as e:
            print(f" ❌ 失败: {str(e)[:60]}")
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
        print(f"\n❌ 数据获取失败: {error_msg[:100]}")
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
    print(f"✓ 数据已保存: {output_file}")

    # 检查数据质量
    if data.get('error') or not data.get('indices'):
        print(f"\n❌ 数据获取失败: {data.get('error', '未知错误')}")
        print(f"\n无法生成收评报告")
        sys.exit(1)

    # 打印关键数据
    print(f"\n{'='*60}")
    print(f"市场概况 ({date_str})")
    print(f"{'='*60}")

    for key, idx in data['indices'].items():
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
    print(f"✓ 数据获取成功")

    # 保存到缓存
    cache = MarketDataCache()
    cache.save_data(date_str, data)
    print(f"✓ 数据已保存到缓存")

    return data


if __name__ == '__main__':
    main()
