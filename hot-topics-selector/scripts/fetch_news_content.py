#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取新闻详细内容
根据选题索引，从原始数据中提取URL并抓取详细内容
"""

import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
import pytz
import time
from typing import List, Dict
import re


class NewsContentFetcher:
    """新闻内容抓取器"""
    
    def __init__(self, input_file: str, indices: List[int]):
        self.input_file = input_file
        self.indices = indices
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载原始数据"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _extract_urls_by_indices(self) -> List[Dict]:
        """根据索引提取URL"""
        all_items = []
        
        for platform_id, platform_data in self.data.get("data", {}).items():
            for rank, item in enumerate(platform_data.get("items", []), 1):
                all_items.append({
                    "platform": platform_data.get("name", platform_id),
                    "rank": rank,
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                })
        
        # 根据索引提取
        selected_items = []
        for idx in self.indices:
            if 1 <= idx <= len(all_items):
                selected_items.append(all_items[idx - 1])
        
        return selected_items
    
    def _fetch_content(self, url: str) -> str:
        """抓取新闻内容"""
        if not url:
            return "无链接"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            # 简单的内容提取（实际项目中可能需要更复杂的解析）
            # 这里只是示例，实际需要根据具体网站进行解析
            text = response.text
            
            # 移除HTML标签
            text = re.sub(r'<[^>]+>', '', text)
            # 移除多余空白
            text = re.sub(r'\s+', ' ', text)
            # 截取前2000字
            content = text[:2000]
            
            return content
            
        except Exception as e:
            return f"抓取失败: {str(e)}"
    
    def fetch_all_content(self) -> Dict:
        """抓取所有选中新闻的内容"""
        selected_items = self._extract_urls_by_indices()
        
        articles = []
        for idx, item in enumerate(selected_items, 1):
            print(f"正在抓取第 {idx}/{len(selected_items)} 篇: {item['title']}")
            
            # 抓取内容
            content = self._fetch_content(item['url'])
            
            # 提取关键词（简单示例）
            keywords = self._extract_keywords(item['title'])
            
            article = {
                "index": self.indices[idx - 1],
                "title": item['title'],
                "url": item['url'],
                "platform": item['platform'],
                "content": content,
                "publish_time": datetime.now(pytz.timezone("Asia/Shanghai")).isoformat(),
                "keywords": keywords
            }
            
            articles.append(article)
            
            # 避免请求过快
            time.sleep(1)
        
        result = {
            "fetch_time": datetime.now(pytz.timezone("Asia/Shanghai")).isoformat(),
            "total_articles": len(articles),
            "articles": articles
        }
        
        return result
    
    def _extract_keywords(self, title: str) -> List[str]:
        """提取关键词（简单示例）"""
        keywords = []
        keyword_list = ["AI", "黄金", "基金", "股票", "投资", "理财", "赚钱", "创业"]
        
        for keyword in keyword_list:
            if keyword in title:
                keywords.append(keyword)
        
        return keywords
    
    def save(self, output_path: str):
        """保存结果"""
        result = self.fetch_all_content()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 内容已保存: {output_path}")
        print(f"总计: {result['total_articles']} 篇文章")
        
        return result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='抓取新闻详细内容')
    parser.add_argument('--input', type=str, required=True, help='输入文件路径（JSON）')
    parser.add_argument('--indices', type=str, required=True, help='选题索引，逗号分隔（如：1,3,5,7,9）')
    parser.add_argument('--output', type=str, default='/tmp/news_content.json', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 解析索引
    indices = [int(x.strip()) for x in args.indices.split(',')]
    
    # 初始化抓取器
    fetcher = NewsContentFetcher(args.input, indices)
    
    # 抓取并保存
    fetcher.save(args.output)


if __name__ == "__main__":
    main()
