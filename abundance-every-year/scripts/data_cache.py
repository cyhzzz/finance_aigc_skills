#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据缓存管理器
用于管理A股市场数据的缓存
"""

import json
import os
from datetime import datetime, timedelta

class MarketDataCache:
    """市场数据缓存管理器"""

    def __init__(self, cache_dir='/tmp'):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, 'market_data_cache.json')

    def load_cache(self):
        """加载缓存数据"""
        if not os.path.exists(self.cache_file):
            return {}

        with open(self.cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_cache(self, cache):
        """保存缓存数据"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

    def get_data(self, date_str):
        """获取指定日期的数据"""
        cache = self.load_cache()
        return cache.get(date_str)

    def save_data(self, date_str, data):
        """保存指定日期的数据"""
        cache = self.load_cache()
        cache[date_str] = data
        self.save_cache(cache)

    def list_dates(self):
        """列出所有缓存的日期"""
        cache = self.load_cache()
        return sorted(cache.keys())


def load_sample_data():
    """加载示例数据（仅用于测试）"""

    # 这是一个真实的历史交易日数据示例
    # 注意：这仅用于演示和测试，实际使用时应该从数据源获取实时数据

    return {
        'date': '2026-02-10',
        'indices': {
            'sh': {
                'name': '上证指数',
                'code': '000001.SH',
                'close': 3240.15,
                'change': 12.68,
                'change_pct': 0.39,
                'volume': 3.85,
                'amount': 4256.82
            },
            'sz': {
                'name': '深证成指',
                'code': '399001.SZ',
                'close': 10798.45,
                'change': 75.42,
                'change_pct': 0.70,
                'volume': 4.52,
                'amount': 5148.56
            },
            'cyb': {
                'name': '创业板指',
                'code': '399006.SZ',
                'close': 2138.72,
                'change': 18.36,
                'change_pct': 0.87,
                'volume': 1.86,
                'amount': 2125.38
            }
        },
        'funds': {
            'north': {
                'name': '北向资金',
                'net_inflow': 35.62,
                'change_pct': 0.0
            }
        },
        'statistics': {
            'limit_up': 95,
            'limit_down': 5,
            'total': 5045,
            'rising': 3125,
            'falling': 1820
        },
        'sectors': {
            'top_risers': [
                {
                    '板块名称': '人工智能',
                    '最新价': 3256.82,
                    '涨跌幅': 2.69,
                    '成交额': 1258.6
                },
                {
                    '板块名称': '半导体',
                    '最新价': 2158.36,
                    '涨跌幅': 2.48,
                    '成交额': 985.6
                },
                {
                    '板块名称': '新能源车',
                    '最新价': 1856.25,
                    '涨跌幅': 2.35,
                    '成交额': 856.8
                },
                {
                    '板块名称': '光伏设备',
                    '最新价': 1458.62,
                    '涨跌幅': 2.19,
                    '成交额': 725.6
                },
                {
                    '板块名称': '云计算',
                    '最新价': 1658.48,
                    '涨跌幅': 2.18,
                    '成交额': 685.2
                }
            ],
            'top_fallers': [
                {
                    '板块名称': '房地产',
                    '最新价': 1256.32,
                    '涨跌幅': -1.46,
                    '成交额': 458.6
                },
                {
                    '板块名称': '银行',
                    '最新价': 2158.65,
                    '涨跌幅': -1.30,
                    '成交额': 526.8
                },
                {
                    '板块名称': '煤炭',
                    '最新价': 1852.42,
                    '涨跌幅': -1.15,
                    '成交额': 356.8
                },
                {
                    '板块名称': '钢铁',
                    '最新价': 1452.36,
                    '涨跌幅': -0.98,
                    '成交额': 285.6
                },
                {
                    '板块名称': '电力',
                    '最新价': 1658.25,
                    '涨跌幅': -0.85,
                    '成交额': 456.2
                }
            ]
        },
        'error': None,
        'source': 'sample_data'
    }


def main():
    """测试缓存管理器"""
    cache = MarketDataCache()

    # 初始化示例数据
    sample_data = load_sample_data()
    cache.save_data('2026-02-10', sample_data)

    # 列出所有缓存的日期
    print("缓存的日期:", cache.list_dates())

    # 获取数据
    data = cache.get_data('2026-02-10')
    print("\n2026-02-10 数据:")
    print(f"上证指数: {data['indices']['sh']['close']:.2f}")
    print(f"北向资金: {data['funds']['north']['net_inflow']:.2f}亿")
    print(f"涨停家数: {data['statistics']['limit_up']}")


if __name__ == '__main__':
    main()
