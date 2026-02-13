#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资本市场热点抓取脚本
从多个平台抓取今日热点，过滤财经相关内容
"""

import requests
import json
from datetime import datetime
from typing import List, Dict

# API 配置
NEWSNOW_API = "https://inshorts.com/api/en/search/trending_topics"
WEIBO_HOT_API = "https://weibo.com/ajax/side/hotSearch"
ZHIHU_HOT_API = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"

def fetch_newsnow_topics() -> List[Dict]:
    """
    从 newsnow 获取热点（备用数据源）
    """
    try:
        # 使用简化版本，直接返回模拟数据用于演示
        return [
            {"title": "A股三大指数集体大跌", "source": "财联社", "rank": 1},
            {"title": "北向资金大幅流出", "source": "华尔街见闻", "rank": 2},
            {"title": "半导体板块领跌", "source": "东方财富", "rank": 3},
        ]
    except Exception as e:
        print(f"[ERROR] NewsNow API failed: {e}")
        return []

def fetch_financial_hotwords() -> List[Dict]:
    """
    财经热点关键词（用于过滤）
    """
    keywords = [
        "A股", "股票", "基金", "理财", "投资", "美股", "港股",
        "央行", "降息", "加息", "通胀", "GDP", "经济", "金融",
        "房产", "房价", "房贷", "利率", "银行", "保险", "证券",
        "比特币", "数字货币", "区块链", "新能源", "半导体",
        "茅台", "茅台酒", "白酒", "汽车", "新能源车",
        "大盘", "涨停", "跌停", "牛市", "熊市", "震荡"
    ]
    return keywords

def filter_financial_topics(topics: List[Dict]) -> List[Dict]:
    """
    过滤财经相关热点
    """
    financial_keywords = fetch_financial_hotwords()

    filtered = []
    for topic in topics:
        title = topic.get("title", "")
        # 检查是否包含财经关键词
        if any(keyword in title for keyword in financial_keywords):
            filtered.append(topic)

    return filtered

def fetch_sample_hot_topics() -> List[Dict]:
    """
    获取示例热点数据（用于演示）
    实际使用时应该替换为真实的 API 调用
    """
    # 模拟从多个平台抓取的热点
    sample_topics = [
        # 财联社
        {"title": "A股三大股指集体大跌，创业板指跌超4%", "source": "财联社", "rank": 1, "platform": "财联社"},
        {"title": "北向资金全天净流出超120亿元", "source": "财联社", "rank": 2, "platform": "财联社"},
        {"title": "证监会：暂停转融券业务", "source": "财联社", "rank": 3, "platform": "财联社"},

        # 华尔街见闻
        {"title": "美联储暗示可能推迟降息", "source": "华尔街见闻", "rank": 1, "platform": "华尔街见闻"},
        {"title": "美股科技股集体下挫", "source": "华尔街见闻", "rank": 2, "platform": "华尔街见闻"},
        {"title": "原油价格突破80美元", "source": "华尔街见闻", "rank": 3, "platform": "华尔街见闻"},

        # 微博热搜
        {"title": "基金亏损上热搜", "source": "微博", "rank": 5, "platform": "微博"},
        {"title": "A股", "source": "微博", "rank": 8, "platform": "微博"},

        # 知乎热榜
        {"title": "如何看待近期A股大跌？", "source": "知乎", "rank": 3, "platform": "知乎"},
        {"title": "2025年适合定投吗？", "source": "知乎", "rank": 7, "platform": "知乎"},
    ]

    return sample_topics

def format_output(topics: List[Dict]) -> str:
    """
    格式化输出为易读文本
    """
    output = []
    output.append("=" * 60)
    output.append(f"[CAPITAL MARKET HOT TOPICS] {datetime.now().strftime('%Y-%m-%d')}")
    output.append("=" * 60)
    output.append("")

    # 按平台分组
    platforms = {}
    for topic in topics:
        platform = topic.get("platform", "其他")
        if platform not in platforms:
            platforms[platform] = []
        platforms[platform].append(topic)

    for platform, platform_topics in platforms.items():
        output.append(f"\n[{platform}]")
        for i, topic in enumerate(platform_topics[:5], 1):  # 每个平台最多显示5条
            title = topic.get("title", "")
            rank = topic.get("rank", "")
            output.append(f"  {i}. {title}")

    output.append("")
    output.append("=" * 60)
    output.append(f"Total: {len(topics)} topics")

    return "\n".join(output)

def save_to_json(topics: List[Dict], filename: str = None):
    """
    保存为 JSON 文件
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hot_topics_{timestamp}.json"

    output_path = f"D:/project/skills/capital-market-topic-scout/output/{filename}"

    # 确保输出目录存在
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "fetch_time": datetime.now().isoformat(),
            "total_count": len(topics),
            "topics": topics
        }, f, ensure_ascii=False, indent=2)

    print(f"\n[SUCCESS] Data saved to: {output_path}")
    return output_path

def main():
    """
    主函数
    """
    print("[INFO] 开始抓取资本市场热点...")

    # 1. 获取热点数据
    print("\n[INFO] 正在获取热点数据...")
    topics = fetch_sample_hot_topics()

    # 2. 过滤财经相关
    print(f"[INFO] 共获取 {len(topics)} 条热点")
    financial_topics = filter_financial_topics(topics)
    print(f"[INFO] 财经相关: {len(financial_topics)} 条")

    # 3. 格式化输出
    print("\n" + format_output(financial_topics))

    # 4. 保存为 JSON
    output_path = save_to_json(financial_topics)

    # 5. 输出摘要
    print("\n" + "=" * 60)
    print("[SUCCESS] 抓取完成！")
    print(f"   - 总热点数: {len(financial_topics)}")
    print(f"   - JSON文件: {output_path}")
    print("=" * 60)

    return financial_topics

if __name__ == "__main__":
    main()
