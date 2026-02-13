#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
准备收评生成所需的数据
整合市场数据和分析结果，为大模型生成收评提供结构化数据
"""

import json
import sys
import os


def calculate_support_resistance(close, change_pct):
    """
    计算支撑位和压力位

    Args:
        close: 收盘价
        change_pct: 涨跌幅

    Returns:
        dict: 支撑位和压力位
    """
    support1 = round(close * 0.98, 2)
    support2 = round(close * 0.95, 2)
    pressure1 = round(close * 1.02, 2)
    pressure2 = round(close * 1.05, 2)

    return {
        'support1': support1,
        'support2': support2,
        'pressure1': pressure1,
        'pressure2': pressure2
    }


def determine_trend(change_pct):
    """
    判断趋势

    Args:
        change_pct: 涨跌幅

    Returns:
        tuple: (趋势描述, 形态描述)
    """
    if change_pct > 1:
        return "强势上涨", "强势多头"
    elif change_pct > 0.5:
        return "上涨", "多头"
    elif change_pct > 0:
        return "温和上涨", "震荡偏多"
    elif change_pct < -1:
        return "强势下跌", "强势空头"
    elif change_pct < -0.5:
        return "下跌", "空头"
    elif change_pct < 0:
        return "温和下跌", "震荡偏空"
    else:
        return "震荡", "震荡"


def determine_sentiment(change_pct, north_inflow):
    """
    判断市场情绪

    Args:
        change_pct: 平均涨跌幅
        north_inflow: 北向资金净流入

    Returns:
        str: 市场情绪
    """
    if change_pct > 0.5 and north_inflow > 0:
        return "偏多"
    elif change_pct > 0 and north_inflow >= 0:
        return "中性偏多"
    elif change_pct < -0.5 and north_inflow < 0:
        return "偏空"
    elif change_pct < 0 and north_inflow <= 0:
        return "中性偏空"
    else:
        return "中性"


def prepare_data(date_str):
    """
    准备收评生成所需的数据

    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'

    Returns:
        dict: 准备好的结构化数据
    """
    # 读取市场数据
    data_file = f'/tmp/market_data_{date_str}.json'
    analysis_file = f'/tmp/market_data_{date_str}_analysis.json'

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    indices = data.get('indices', {})
    funds = data.get('funds', {})
    statistics = data.get('statistics', {})
    sectors = data.get('sectors', {})

    north_inflow = funds.get('north', {}).get('net_inflow', 0)

    # 准备指数数据
    indices_prepared = {}
    for key, idx in indices.items():
        if isinstance(idx, dict) and 'close' in idx:
            close = idx.get('close', 0)
            change_pct = idx.get('change_pct', 0)

            # 计算支撑位和压力位
            sr = calculate_support_resistance(close, change_pct)
            trend_desc, pattern_desc = determine_trend(change_pct)

            indices_prepared[key] = {
                'name': idx.get('name', ''),
                'code': idx.get('code', ''),
                'close': close,
                'open': idx.get('open', 0),
                'high': idx.get('high', 0),
                'low': idx.get('low', 0),
                'change': idx.get('change', 0),
                'change_pct': change_pct,
                'amount': idx.get('amount', 0),
                'trend': trend_desc,
                'pattern': pattern_desc,
                'support1': sr['support1'],
                'support2': sr['support2'],
                'pressure1': sr['pressure1'],
                'pressure2': sr['pressure2'],
                'short_term_trend': "上涨" if change_pct > 0 else "下跌" if change_pct < 0 else "震荡"
            }

    # 计算平均涨跌幅
    if indices_prepared:
        avg_change = sum(idx['change_pct'] for idx in indices_prepared.values()) / len(indices_prepared)
    else:
        avg_change = 0

    # 准备资金流向数据
    funds_prepared = {
        'north_inflow': north_inflow,
        'north_desc': "净流入" if north_inflow >= 0 else "净流出",
        'north_sign': '+' if north_inflow >= 0 else '',
        'sh_inflow': funds.get('north', {}).get('sh_inflow', 0),
        'sz_inflow': funds.get('north', {}).get('sz_inflow', 0),
        'total_amount': sum(idx.get('amount', 0) for idx in indices_prepared.values()),
        'volume_desc': "放量" if sum(idx.get('amount', 0) for idx in indices_prepared.values()) > 10000 else "缩量" if sum(idx.get('amount', 0) for idx in indices_prepared.values()) < 5000 else "平量"
    }

    # 判断市场情绪
    sentiment = determine_sentiment(avg_change, north_inflow)

    # 准备涨跌统计
    limit_up = statistics.get('limit_up', 0)
    limit_down = statistics.get('limit_down', 0)
    up_count = analysis.get('indices_analysis', {}).get('rising_count', 0)
    down_count = analysis.get('indices_analysis', {}).get('falling_count', 0)

    if limit_up > 0 and limit_down > 0:
        up_ratio = up_count / (up_count + down_count) * 100 if (up_count + down_count) > 0 else 50
        market_feature = "赚钱效应明显" if up_ratio > 60 else "赚钱效应较差" if up_ratio < 40 else "赚钱效应一般"

        statistics_prepared = {
            'limit_up': limit_up,
            'limit_down': limit_down,
            'up_count': up_count,
            'down_count': down_count,
            'up_ratio': round(up_ratio, 1),
            'market_feature': market_feature,
            'data_available': True
        }
    else:
        statistics_prepared = {
            'limit_up': 0,
            'limit_down': 0,
            'up_count': up_count,
            'down_count': down_count,
            'up_ratio': 0,
            'market_feature': "暂无法判断",
            'data_available': False,
            'note': "涨跌停统计接口暂时不可用"
        }

    # 准备板块数据
    top_gain = sectors.get('top_gain', [])
    top_loss = sectors.get('top_loss', [])

    if top_gain:
        sectors_prepared = {
            'top_gain': top_gain[:5],
            'top_loss': top_loss[:5],
            'data_available': True
        }
    else:
        sectors_prepared = {
            'top_gain': [],
            'top_loss': [],
            'data_available': False,
            'note': "板块数据接口暂时不可用"
        }

    # 整合所有数据
    prepared = {
        'date': date_str,
        'indices': indices_prepared,
        'funds': funds_prepared,
        'statistics': statistics_prepared,
        'sectors': sectors_prepared,
        'market_direction': analysis.get('indices_analysis', {}).get('market_direction', '震荡'),
        'best_index': analysis.get('indices_analysis', {}).get('best_index', ''),
        'worst_index': analysis.get('indices_analysis', {}).get('worst_index', ''),
        'overall_sentiment': sentiment,
        'core_opinion': analysis.get('summary', ''),
        'data_source': data.get('source', 'akshare')
    }

    return prepared


def main():
    """主函数"""
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        # 默认使用今天
        from datetime import datetime
        date_str = datetime.now().strftime('%Y-%m-%d')

    # 准备数据
    prepared = prepare_data(date_str)

    # 保存数据
    output_file = f'/tmp/market_data_{date_str}_prepared.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(prepared, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✓ 数据已准备: {output_file}")
    print(f"{'='*60}")

    # 打印数据概况
    print(f"\n数据概况 ({date_str}):")
    print(f"  指数数量: {len(prepared.get('indices', {}))}")
    print(f"  市场方向: {prepared.get('market_direction', '未知')}")
    print(f"  整体情绪: {prepared.get('overall_sentiment', '未知')}")
    print(f"  北向资金: {prepared.get('funds', {}).get('north_desc', '未知')} {prepared.get('funds', {}).get('north_sign', '')}{abs(prepared.get('funds', {}).get('north_inflow', 0)):.2f}亿元")
    print(f"  涨跌停统计: {'可用' if prepared.get('statistics', {}).get('data_available') else '不可用'}")
    print(f"  板块数据: {'可用' if prepared.get('sectors', {}).get('data_available') else '不可用'}")

    return prepared


if __name__ == '__main__':
    main()
