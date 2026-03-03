# -*- coding: utf-8 -*-
"""
A股数据获取模块 - 多数据源版本
支持东方财富、新浪财经、腾讯财经等多个数据源备用

当主数据源失败时，自动切换到备用数据源
"""

import akshare as ak
import time
import pandas as pd
import json
import os
from typing import Optional, Dict, List, Any, Callable
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class MultiSourceDataFetcher:
    """多数据源数据获取器"""

    # 数据源配置
    DATA_SOURCES = {
        'realtime_quotes': {
            'name': '实时行情',
            'sources': [
                ('东方财富', 'stock_zh_a_spot_em', {}),
                ('新浪财经', 'stock_zh_a_spot', {}),
            ]
        },
        'industry_board': {
            'name': '行业板块',
            'sources': [
                ('东方财富', 'stock_board_industry_name_em', {}),
                ('东方财富实时', 'stock_board_industry_spot_em', {}),
            ]
        },
        'concept_board': {
            'name': '概念板块',
            'sources': [
                ('东方财富', 'stock_board_concept_name_em', {}),
                ('东方财富实时', 'stock_board_concept_spot_em', {}),
            ]
        },
        'north_money': {
            'name': '北向资金',
            'sources': [
                ('资金流向汇总', 'stock_hsgt_fund_flow_summary_em', {}),
                ('沪深港通历史', 'stock_hsgt_hist_em', {}),
            ]
        },
        'stock_hist': {
            'name': '个股历史',
            'sources': [
                ('东方财富', 'stock_zh_a_hist', {'period': 'daily', 'adjust': ''}),
                ('腾讯财经', 'stock_zh_a_hist_tx', {}),
            ]
        }
    }

    def __init__(self, max_retries: int = 2, cache_dir: str = None, cache_expire: int = 3600):
        """
        初始化

        Args:
            max_retries: 最大重试次数
            cache_dir: 缓存目录
            cache_expire: 缓存过期时间(秒)
        """
        self.max_retries = max_retries
        self.cache_expire = cache_expire
        self.success_source = {}  # 记录成功的数据源

        # 设置缓存目录
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(__file__).parent / '.cache'

        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _log(self, msg: str, level: str = 'INFO'):
        """安全日志输出"""
        prefix = {
            'INFO': '[I]',
            'WARN': '[W]',
            'ERROR': '[E]',
            'OK': '[OK]',
            'FAIL': '[X]'
        }.get(level, '[?]')

        try:
            print(f"  {prefix} {msg}")
        except UnicodeEncodeError:
            print(f"  {prefix} {msg.encode('gbk', errors='replace').decode('gbk')}")

    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{key}.json"

    def _load_cache(self, key: str) -> Optional[Dict]:
        """加载缓存"""
        cache_file = self._get_cache_path(key)
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 检查是否过期
                cache_time = datetime.fromisoformat(data.get('cache_time', '2000-01-01'))
                if datetime.now() - cache_time < timedelta(seconds=self.cache_expire):
                    return data.get('data')
            except:
                pass
        return None

    def _save_cache(self, key: str, data: Any):
        """保存缓存"""
        cache_file = self._get_cache_path(key)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'cache_time': datetime.now().isoformat(),
                    'data': data
                }, f, ensure_ascii=False, indent=2, default=str)
        except:
            pass

    def _call_with_retry(self, func: Callable, *args, **kwargs) -> tuple:
        """带重试的函数调用"""
        last_error = None

        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                return result, None
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(1 + attempt)

        return None, last_error

    def _try_sources(self, data_type: str, **extra_kwargs) -> pd.DataFrame:
        """
        尝试多个数据源

        Args:
            data_type: 数据类型 (对应 DATA_SOURCES 中的键)
            **extra_kwargs: 额外参数

        Returns:
            DataFrame 或空 DataFrame
        """
        if data_type not in self.DATA_SOURCES:
            self._log(f"未知数据类型: {data_type}", 'ERROR')
            return pd.DataFrame()

        config = self.DATA_SOURCES[data_type]
        self._log(f"获取{config['name']}...")

        # 尝试每个数据源
        for source_name, func_name, default_kwargs in config['sources']:
            try:
                # 合并参数
                kwargs = {**default_kwargs, **extra_kwargs}

                # 获取函数
                if not hasattr(ak, func_name):
                    continue

                func = getattr(ak, func_name)
                self._log(f"尝试 {source_name}...")

                # 调用函数
                result, error = self._call_with_retry(func, **kwargs)

                if error:
                    raise error

                if result is not None and not (isinstance(result, pd.DataFrame) and result.empty):
                    self._log(f"{source_name} 成功", 'OK')
                    self.success_source[data_type] = source_name

                    # 如果是DataFrame，转换为可序列化格式
                    if isinstance(result, pd.DataFrame):
                        return result
                    return result

            except Exception as e:
                self._log(f"{source_name} 失败: {str(e)[:60]}", 'FAIL')
                continue

        self._log(f"所有{config['name']}数据源均失败", 'ERROR')
        return pd.DataFrame()

    # ============ 公共接口 ============

    def get_realtime_quotes(self, symbols: List[str] = None) -> pd.DataFrame:
        """获取实时行情"""
        df = self._try_sources('realtime_quotes')

        if not df.empty and symbols and '代码' in df.columns:
            return df[df['代码'].isin(symbols)]

        return df

    def get_index_quotes(self) -> Dict[str, Any]:
        """获取主要指数行情"""
        df = self.get_realtime_quotes()

        if df.empty:
            return self._get_default_index_data()

        # 指数代码映射
        index_map = {
            '000001': '上证指数',
            '399001': '深证成指',
            '399006': '创业板指',
            '000016': '上证50',
            '000300': '沪深300',
            '000688': '科创50'
        }

        result = {}

        # 提取指数数据
        if '代码' in df.columns:
            for code, name in index_map.items():
                row = df[df['代码'] == code]
                if not row.empty:
                    r = row.iloc[0]
                    result[code] = {
                        'name': name,
                        'price': float(r.get('最新价', 0) or 0),
                        'change_pct': float(r.get('涨跌幅', 0) or 0),
                        'amount': float(r.get('成交额', 0) or 0)
                    }

        # 市场统计
        if '涨跌幅' in df.columns:
            result['_market'] = {
                'up_count': int((df['涨跌幅'] > 0).sum()),
                'down_count': int((df['涨跌幅'] < 0).sum()),
                'flat_count': int((df['涨跌幅'] == 0).sum()),
                'total_amount': float(df.get('成交额', pd.Series([0])).sum())
            }

        result['_source'] = self.success_source.get('realtime_quotes', '未知')
        return result

    def _get_default_index_data(self) -> Dict[str, Any]:
        """获取默认指数数据（离线）"""
        return {
            '000001': {'name': '上证指数', 'price': 0, 'change_pct': 0, 'amount': 0},
            '399001': {'name': '深证成指', 'price': 0, 'change_pct': 0, 'amount': 0},
            '399006': {'name': '创业板指', 'price': 0, 'change_pct': 0, 'amount': 0},
            '_market': {'up_count': 0, 'down_count': 0, 'flat_count': 0, 'total_amount': 0},
            '_source': '离线数据',
            '_offline': True
        }

    def get_industry_board(self, top_n: int = 10) -> pd.DataFrame:
        """获取行业板块"""
        df = self._try_sources('industry_board')

        if not df.empty and '涨跌幅' in df.columns:
            return df.nlargest(top_n, '涨跌幅')

        return df.head(top_n) if not df.empty else df

    def get_concept_board(self, top_n: int = 10) -> pd.DataFrame:
        """获取概念板块"""
        df = self._try_sources('concept_board')

        if not df.empty and '涨跌幅' in df.columns:
            return df.nlargest(top_n, '涨跌幅')

        return df.head(top_n) if not df.empty else df

    def get_north_money(self) -> pd.DataFrame:
        """获取北向资金"""
        return self._try_sources('north_money')

    def get_stock_hist(self, symbol: str, start_date: str = '', end_date: str = '') -> pd.DataFrame:
        """获取个股历史行情"""
        return self._try_sources('stock_hist', symbol=symbol, start_date=start_date, end_date=end_date)

    def get_hot_news(self, max_count: int = 20) -> List[Dict[str, Any]]:
        """
        获取热门财经资讯

        Args:
            max_count: 最大获取条数，默认20条

        Returns:
            资讯列表，每条包含标题、摘要、来源、时间等
        """
        self._log("获取热门财经资讯...")
        news_list = []

        # 数据源优先级：财联社 > 东方财富 > CCTV
        news_sources = [
            ('财联社主线新闻', self._fetch_news_cailian),
            ('东方财富股票新闻', self._fetch_news_eastmoney),
            ('CCTV财经新闻', self._fetch_news_cctv),
        ]

        for source_name, fetch_func in news_sources:
            try:
                self._log(f"尝试 {source_name}...")
                news = fetch_func(max_count - len(news_list))
                if news:
                    news_list.extend(news)
                    self._log(f"{source_name} 获取 {len(news)} 条", 'OK')

                if len(news_list) >= max_count:
                    break
            except Exception as e:
                self._log(f"{source_name} 失败: {str(e)[:50]}", 'FAIL')
                continue

        # 去重并限制数量
        seen_titles = set()
        unique_news = []
        for item in news_list:
            title = item.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(item)

        self._log(f"共获取 {len(unique_news[:max_count])} 条热门资讯", 'OK')
        return unique_news[:max_count]

    def _fetch_news_cailian(self, max_count: int = 20) -> List[Dict[str, Any]]:
        """从财联社获取主线新闻"""
        news_list = []
        try:
            df = ak.stock_news_main_cx()
            if df is not None and not df.empty:
                for _, row in df.head(max_count).iterrows():
                    news_list.append({
                        'title': row.get('tag', ''),
                        'summary': row.get('summary', ''),
                        'source': '财联社',
                        'url': row.get('url', ''),
                        'time': ''
                    })
        except Exception as e:
            self._log(f"财联社获取失败: {str(e)[:50]}", 'FAIL')
        return news_list

    def _fetch_news_eastmoney(self, max_count: int = 20) -> List[Dict[str, Any]]:
        """从东方财富获取股票新闻"""
        news_list = []
        try:
            # 获取大盘相关新闻
            df = ak.stock_news_em(symbol='000001')
            if df is not None and not df.empty:
                for _, row in df.head(max_count).iterrows():
                    news_list.append({
                        'title': row.get('新闻标题', ''),
                        'summary': row.get('新闻内容', '')[:200] if row.get('新闻内容') else '',
                        'source': row.get('文章来源', '东方财富'),
                        'url': row.get('新闻链接', ''),
                        'time': row.get('发布时间', '')
                    })
        except Exception as e:
            self._log(f"东方财富获取失败: {str(e)[:50]}", 'FAIL')
        return news_list

    def _fetch_news_cctv(self, max_count: int = 20) -> List[Dict[str, Any]]:
        """从CCTV获取财经新闻"""
        news_list = []
        try:
            # 获取今天的日期
            today = datetime.now().strftime('%Y%m%d')
            df = ak.news_cctv(date=today)
            if df is not None and not df.empty:
                for _, row in df.head(max_count).iterrows():
                    news_list.append({
                        'title': row.get('title', ''),
                        'summary': row.get('content', '')[:200] if row.get('content') else '',
                        'source': 'CCTV',
                        'url': '',
                        'time': row.get('date', '')
                    })
        except Exception as e:
            self._log(f"CCTV获取失败: {str(e)[:50]}", 'FAIL')
        return news_list

    def get_market_summary(self) -> Dict[str, Any]:
        """获取市场概览"""
        self._log("=" * 50)
        self._log("获取市场概览")
        self._log("=" * 50)

        result = {
            'timestamp': datetime.now().isoformat(),
            'index': self.get_index_quotes(),
            'industry': {},
            'concept': {},
            'north_money': {},
            'hot_news': []  # 新增热门资讯
        }

        # 行业板块 TOP5
        industry_df = self.get_industry_board(top_n=5)
        if not industry_df.empty and '板块名称' in industry_df.columns:
            result['industry'] = {
                row['板块名称']: float(row.get('涨跌幅', 0) or 0)
                for _, row in industry_df.iterrows()
            }

        # 概念板块 TOP5
        concept_df = self.get_concept_board(top_n=5)
        if not concept_df.empty and '板块名称' in concept_df.columns:
            result['concept'] = {
                row['板块名称']: float(row.get('涨跌幅', 0) or 0)
                for _, row in concept_df.iterrows()
            }

        # 热门财经资讯
        result['hot_news'] = self.get_hot_news(max_count=20)

        return result


def test_multi_source():
    """测试多数据源获取器"""
    print("\n" + "=" * 60)
    print("测试多数据源数据获取器")
    print("=" * 60 + "\n")

    fetcher = MultiSourceDataFetcher(max_retries=2, cache_expire=300)

    # 1. 测试指数
    print("\n[1] 获取指数行情")
    index_data = fetcher.get_index_quotes()

    if not index_data.get('_offline'):
        print("\n  主要指数:")
        for code in ['000001', '399001', '399006']:
            if code in index_data:
                d = index_data[code]
                print(f"    {d['name']}: {d['price']:.2f} ({d['change_pct']:+.2f}%)")

        if '_market' in index_data:
            m = index_data['_market']
            print(f"\n  市场: 涨 {m['up_count']} / 跌 {m['down_count']} / 平 {m['flat_count']}")

        print(f"\n  数据源: {index_data.get('_source', '未知')}")
    else:
        print("  [离线模式] 无法获取实时数据")

    # 2. 测试行业板块
    print("\n[2] 获取行业板块 TOP5")
    industry_df = fetcher.get_industry_board(top_n=5)
    if not industry_df.empty and '板块名称' in industry_df.columns:
        for _, row in industry_df.iterrows():
            print(f"    {row['板块名称']}: {row.get('涨跌幅', 0):+.2f}%")
    else:
        print("  无法获取行业板块数据")

    # 3. 测试北向资金
    print("\n[3] 获取北向资金")
    north_df = fetcher.get_north_money()
    if not north_df.empty:
        print(f"  成功获取 {len(north_df)} 条记录")
        print(f"  最新: {north_df.iloc[-1].to_dict() if len(north_df) > 0 else '无数据'}")
    else:
        print("  无法获取北向资金数据")

    # 4. 测试热门资讯
    print("\n[4] 获取热门财经资讯")
    news_list = fetcher.get_hot_news(max_count=10)
    if news_list:
        for i, news in enumerate(news_list, 1):
            print(f"    [{i}] {news.get('title', '')[:40]}... ({news.get('source', '')})")
    else:
        print("  无法获取热门资讯")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == '__main__':
    test_multi_source()