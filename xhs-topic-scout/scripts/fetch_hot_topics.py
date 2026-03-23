#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财经热点抓取工具
通过 CDP Proxy API 获取热点新闻页面内容

依赖:
  - web-access skill (CDP Proxy)
  - Python 3.x

降级策略:
  - 如果CDP不可用，可以手动复制页面内容进行分析
  - 如果Python脚本不可用，可以直接使用CDP命令获取热点
"""

import json
import os
import subprocess
import time
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class HotTopicsFetcher:
    """热点抓取器 - 基于CDP"""

    CDP_BASE_URL = os.environ.get("CDP_PROXY_URL", "http://localhost:3456")

    # 数据来源配置（均为财经新闻源，无需关键词筛选）
    SOURCES = {
        "cls": {
            "name": "财联社",
            "url": "https://www.cls.cn/depth?id=1000"
        },
        "sina": {
            "name": "新浪财经",
            "url": "https://finance.sina.com.cn/7x24/"
        },
        "eastmoney": {
            "name": "东方财富",
            "url": "https://finance.eastmoney.com/a/cdfsd_2.html"
        }
    }

    def __init__(self):
        self.targets = {}

    def check_health(self) -> bool:
        """检查CDP Proxy健康状态"""
        try:
            with urllib.request.urlopen(f"{self.CDP_BASE_URL}/health", timeout=5) as resp:
                data = json.loads(resp.read().decode())
                return data.get("connected", False)
        except Exception:
            return False

    def create_tab(self, url: str) -> Optional[str]:
        """创建新tab并返回targetId"""
        try:
            with urllib.request.urlopen(f"{self.CDP_BASE_URL}/new?url={url}", timeout=15) as resp:
                data = json.loads(resp.read().decode())
                return data.get("targetId")
        except Exception as e:
            print(f"[FAIL] create tab: {e}")
            return None

    def get_page_text(self, target_id: str, max_length: int = 5000) -> str:
        """获取页面文本内容"""
        try:
            # 等待页面加载
            time.sleep(3)

            # 执行JS获取页面文本
            req = urllib.request.Request(
                f"{self.CDP_BASE_URL}/eval?target={target_id}",
                data=b'document.body?.innerText?.slice(0, 5000) || ""',
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                return data.get("value", "")
        except Exception as e:
            print(f"[FAIL] get page text: {e}")
            return ""

    def close_tab(self, target_id: str):
        """关闭tab"""
        try:
            with urllib.request.urlopen(f"{self.CDP_BASE_URL}/close?target={target_id}", timeout=5):
                pass
        except Exception:
            pass

    def extract_news(self, text: str, source_name: str) -> List[Dict]:
        """从页面文本中提取新闻"""
        news_items = []

        # 按行分割，过滤有效行
        lines = text.split('\n')
        current_item = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 时间模式匹配 (10:44, 10:43:27等)
            time_match = re.match(r'^(\d{1,2}:\d{2}(?::\d{2})?)$', line)
            if time_match and current_item.get('text'):
                # 保存上一个条目
                if current_item.get('text'):
                    current_item['time'] = time_match.group(1)
                    news_items.append(current_item)
                current_item = {'text': '', 'time': time_match.group(1)}
                continue

            # 阅读量模式匹配
            read_match = re.search(r'([\d.]+[万万亿]?\s*阅读)', line)
            if read_match:
                current_item['read_count'] = read_match.group(1)

            # 收集文本内容
            if line and not line.startswith('财联社') and not line.startswith('新浪财经'):
                current_item['text'] = (current_item.get('text', '') + ' ' + line).strip()

        # 保存最后一个条目
        if current_item.get('text'):
            news_items.append(current_item)

        return news_items

    def filter_by_keywords(self, news: List[Dict], keywords: List[str]) -> List[Dict]:
        """根据关键词过滤新闻"""
        filtered = []
        for item in news:
            text = item.get('text', '')
            if any(kw in text for kw in keywords):
                filtered.append(item)
        return filtered

    def fetch_all_sources(self) -> Dict:
        """抓取所有来源的新闻"""
        results = {}

        print("[START] Fetching hot topics...")

        for source_id, config in self.SOURCES.items():
            print(f"\n[FETCH] {config['name']}...")

            # 创建tab
            target_id = self.create_tab(config['url'])
            if not target_id:
                print(f"[FAIL] {config['name']}")
                continue

            self.targets[source_id] = target_id

            # 获取页面文本
            text = self.get_page_text(target_id)

            if not text:
                print(f"[FAIL] {config['name']} - empty content")
                continue

            # 提取新闻（财经新闻源，无需关键词筛选）
            news = self.extract_news(text, config['name'])

            results[source_id] = {
                "name": config['name'],
                "url": config['url'],
                "all_count": len(news),
                "news": news[:20]  # 最多保留20条
            }

            print(f"[OK] {config['name']}: {len(news)} news items")

            # 请求间隔
            time.sleep(1)

        return results

    def save_to_file(self, data: Dict, output_path: str = "/tmp") -> str:
        """保存数据到JSON文件"""
        Path(output_path).mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hot_topics_{timestamp}.json"
        filepath = Path(output_path) / filename

        output_data = {
            "fetch_time": datetime.now().isoformat(),
            "sources_count": len(data),
            "total_news": sum(s.get("all_count", 0) for s in data.values()),
            "data": data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"\n[SAVE] {filepath}")
        return str(filepath)

    def print_summary(self, data: Dict):
        """打印摘要"""
        print("\n" + "="*60)
        print("[SUMMARY] Hot Topics")
        print("="*60)

        for source_id, source_data in data.items():
            print(f"\n[{source_data['name']}]")
            for i, news in enumerate(source_data.get('news', [])[:5], 1):
                text = news.get('text', '')[:60]
                print(f"  {i}. {text}...")

        print("\n" + "="*60)

    def cleanup(self):
        """清理所有tab"""
        for target_id in self.targets.values():
            self.close_tab(target_id)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='财经热点抓取工具 - 通过CDP获取财联社/新浪/东财热点',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
数据来源:
  - 财联社深度: https://www.cls.cn/depth?id=1000
  - 新浪财经7×24: https://finance.sina.com.cn/7x24/
  - 东方财富操盘必读: https://finance.eastmoney.com/a/cdfsd_2.html

示例:
  python fetch_hot_topics.py                          # 默认保存到 /tmp
  python fetch_hot_topics.py --output ./data          # 保存到 ./data
  python fetch_hot_topics.py --cdp-url http://localhost:3456  # 指定CDP地址
        """
    )
    parser.add_argument('--output', default='/tmp', help='输出目录 (default: /tmp)')
    parser.add_argument('--cdp-url', default=None, help='CDP Proxy地址')
    args = parser.parse_args()

    fetcher = HotTopicsFetcher()
    if args.cdp_url:
        fetcher.CDP_BASE_URL = args.cdp_url

    # 检查CDP连接
    if not fetcher.check_health():
        print("[FAIL] CDP Proxy not connected. Start with: node ~/.claude/skills/web-access/scripts/cdp-proxy.mjs")
        return

    print("[OK] CDP Proxy connected")

    # 抓取数据
    data = fetcher.fetch_all_sources()

    if not data:
        print("[FAIL] No data fetched")
        return

    # 保存
    filepath = fetcher.save_to_file(data, args.output)

    # 打印摘要
    fetcher.print_summary(data)

    # 清理
    fetcher.cleanup()


if __name__ == "__main__":
    main()
