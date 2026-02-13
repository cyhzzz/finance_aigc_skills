#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财经热点抓取工具
基于 TrendRadar 项目能力，抓取真实热点资讯
"""

import json
import time
import random
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union

import requests
import pytz


class HotTopicsFetcher:
    """热点抓取器"""
    
    # API 基础地址
    API_BASE_URL = "https://newsnow.busiyi.world/api/s"
    
    # 支持的平台
    PLATFORMS = {
        "cls-hot": "财联社热门",
        "_36kr": "36氪",
        "gelonghui": "格隆汇",
        "toutiao": "今日头条",
        "baidu": "百度热搜",
        "weibo": "微博",
        "douyin": "抖音",
        "zhihu": "知乎",
    }
    
    # 财经相关平台（专业）
    FINANCE_PLATFORMS = ["cls-hot", "_36kr", "gelonghui"]
    
    # 综合资讯平台（大众关注度高）
    GENERAL_PLATFORMS = ["toutiao", "baidu", "weibo", "douyin", "zhihu"]
    
    # 默认推荐平台（平衡专业和大众）
    RECOMMENDED_PLATFORMS = ["weibo", "baidu", "toutiao", "cls-hot", "douyin"]
    
    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.session = requests.Session()
        
    def fetch_platform_data(
        self, 
        platform_id: str, 
        max_retries: int = 2,
        retry_wait: int = 3
    ) -> Tuple[Optional[Dict], str]:
        """
        抓取指定平台的热点数据
        
        Args:
            platform_id: 平台ID（如 cls-hot）
            max_retries: 最大重试次数
            retry_wait: 重试等待时间（秒）
        
        Returns:
            (数据字典, 平台名称)
        """
        platform_name = self.PLATFORMS.get(platform_id, platform_id)
        url = f"{self.API_BASE_URL}?id={platform_id}&latest"
        
        # 配置代理
        proxies = None
        if self.proxy_url:
            proxies = {"http": self.proxy_url, "https": self.proxy_url}
        
        # 请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
        }
        
        # 重试逻辑
        for attempt in range(max_retries + 1):
            try:
                response = self.session.get(url, proxies=proxies, headers=headers, timeout=10)
                response.raise_for_status()
                
                data = json.loads(response.text)
                return data, platform_name
                
            except Exception as e:
                if attempt < max_retries:
                    wait_time = retry_wait + random.uniform(1, 2) * attempt
                    print(f"⚠️ {platform_name} 抓取失败: {e}，{wait_time:.1f}秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ {platform_name} 抓取失败: {e}")
                    return None, platform_name
        
        return None, platform_name
    
    def fetch_all_platforms(
        self,
        platforms: Optional[List[str]] = None,
        request_interval: int = 1000
    ) -> Dict:
        """
        抓取多个平台的热点数据
        
        Args:
            platforms: 平台列表，None 表示使用财经平台
            request_interval: 请求间隔（毫秒）
        
        Returns:
            包含所有平台数据的字典
        """
        if platforms is None:
            platforms = self.FINANCE_PLATFORMS
        
        results = {}
        
        print(f"\n🔍 开始抓取 {len(platforms)} 个平台的热点...")
        print(f"平台列表: {', '.join([self.PLATFORMS.get(p, p) for p in platforms])}")
        
        for i, platform_id in enumerate(platforms):
            data, platform_name = self.fetch_platform_data(platform_id)
            
            if data and "items" in data:
                results[platform_id] = {
                    "name": platform_name,
                    "items": data["items"],
                    "count": len(data["items"])
                }
                print(f"✅ {platform_name}: {len(data['items'])} 条")
            else:
                results[platform_id] = {
                    "name": platform_name,
                    "items": [],
                    "count": 0
                }
                print(f"❌ {platform_name}: 0 条")
            
            # 请求间隔
            if i < len(platforms) - 1:
                interval = request_interval / 1000 + random.uniform(-0.1, 0.1)
                time.sleep(max(0.5, interval))
        
        return results
    
    def filter_by_keywords(
        self,
        data: Dict,
        include_keywords: Optional[List[str]] = None,
        exclude_keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        根据关键词过滤热点
        
        Args:
            data: 原始数据
            include_keywords: 包含关键词列表
            exclude_keywords: 排除关键词列表
        
        Returns:
            过滤后的数据
        """
        if not include_keywords and not exclude_keywords:
            return data
        
        filtered_data = {}
        
        for platform_id, platform_data in data.items():
            filtered_items = []
            
            for item in platform_data.get("items", []):
                title = item.get("title", "")
                
                # 检查排除关键词
                if exclude_keywords:
                    if any(kw.lower() in title.lower() for kw in exclude_keywords):
                        continue
                
                # 检查包含关键词
                if include_keywords:
                    if not any(kw.lower() in title.lower() for kw in include_keywords):
                        continue
                
                filtered_items.append(item)
            
            filtered_data[platform_id] = {
                **platform_data,
                "items": filtered_items,
                "count": len(filtered_items)
            }
        
        return filtered_data
    
    def save_to_file(
        self,
        data: Dict,
        output_path: Optional[str] = None,
        filename_prefix: str = "hot_topics"
    ) -> str:
        """
        保存数据到 JSON 文件
        
        Args:
            data: 热点数据
            output_path: 输出路径
            filename_prefix: 文件名前缀
        
        Returns:
            保存的文件路径
        """
        if output_path is None:
            output_path = "/tmp"
        
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = Path(output_path) / filename
        
        # 添加元数据
        output_data = {
            "fetch_time": datetime.now(pytz.timezone("Asia/Shanghai")).isoformat(),
            "platforms_count": len(data),
            "total_items": sum(p.get("count", 0) for p in data.values()),
            "data": data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 数据已保存: {filepath}")
        return str(filepath)
    
    def print_summary(self, data: Dict):
        """打印数据摘要"""
        print("\n" + "="*60)
        print("📊 热点数据摘要")
        print("="*60)
        
        total_items = sum(p.get("count", 0) for p in data.values())
        print(f"总平台数: {len(data)}")
        print(f"总热点数: {total_items}")
        
        print("\n各平台数据:")
        for platform_id, platform_data in data.items():
            name = platform_data.get("name", platform_id)
            count = platform_data.get("count", 0)
            print(f"  • {name}: {count} 条")
        
        # 显示 Top 5
        print("\n🔥 综合热度 Top 5:")
        all_items = []
        for platform_id, platform_data in data.items():
            for idx, item in enumerate(platform_data.get("items", [])[:10], 1):
                all_items.append({
                    "title": item.get("title", ""),
                    "rank": idx,
                    "platform": platform_data.get("name", ""),
                    "url": item.get("url", ""),
                })
        
        # 按排名排序
        all_items.sort(key=lambda x: x["rank"])
        for i, item in enumerate(all_items[:5], 1):
            print(f"{i}. {item['title']}")
            print(f"   来源: {item['platform']} | 排名: #{item['rank']}")
        
        print("="*60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='财经热点抓取工具')
    parser.add_argument('--platforms', type=str, help='平台列表（逗号分隔）')
    parser.add_argument('--keywords', type=str, help='包含关键词（逗号分隔）')
    parser.add_argument('--exclude', type=str, help='排除关键词（逗号分隔）')
    parser.add_argument('--output', type=str, default='/tmp', help='输出路径')
    parser.add_argument('--finance', action='store_true', help='只抓取财经平台')
    
    args = parser.parse_args()
    
    # 初始化抓取器
    fetcher = HotTopicsFetcher()
    
    # 确定平台列表
    if args.platforms:
        platforms = [p.strip() for p in args.platforms.split(',')]
    elif args.finance:
        platforms = HotTopicsFetcher.FINANCE_PLATFORMS
    else:
        # 默认使用推荐平台（平衡专业和大众）
        platforms = HotTopicsFetcher.RECOMMENDED_PLATFORMS
    
    # 抓取数据
    data = fetcher.fetch_all_platforms(platforms)
    
    # 关键词过滤
    include_keywords = [k.strip() for k in args.keywords.split(',')] if args.keywords else None
    exclude_keywords = [k.strip() for k in args.exclude.split(',')] if args.exclude else None
    
    if include_keywords or exclude_keywords:
        print("\n🔍 应用关键词过滤...")
        data = fetcher.filter_by_keywords(data, include_keywords, exclude_keywords)
    
    # 保存数据
    filepath = fetcher.save_to_file(data, args.output)
    
    # 打印摘要
    fetcher.print_summary(data)
    
    return filepath


if __name__ == "__main__":
    main()
