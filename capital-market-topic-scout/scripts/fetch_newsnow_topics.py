# coding=utf-8
"""
资本市场热点抓取脚本 - 基于 NewsNow API

数据源：https://newsnow.busiyi.world/api/s
支持的财经平台：
- 财联社 (cls-hot)
- 华尔街见闻 (wallstreetcn-hot)
- 新浪财经 (sina-finance)

特性：
- 真实调用 NewsNow API
- 自动重试机制
- 财经关键词过滤
- JSON 格式输出
- Windows 中文编码兼容
"""

import json
import random
import time
import sys
import io
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests

# Windows 控制台编码修复
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


# ================================================================
# 配置区域
# ================================================================

# NewsNow API 配置
API_BASE_URL = "https://newsnow.busiyi.world/api/s"

# 请求头（模拟浏览器）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
}

# 支持的财经平台列表
FINANCE_PLATFORMS = [
    ("cls-hot", "财联社热门"),
    ("wallstreetcn-hot", "华尔街见闻"),
    ("sina-finance", "新浪财经"),
]

# 财经相关关键词（用于过滤和标记）
FINANCE_KEYWORDS = [
    # 股市相关
    "A股", "港股", "美股", "股市", "上证", "深证", "创业板", "科创板",
    "股票", "涨停", "跌停", "大盘", "指数", "个股", "板块",

    # 宏观经济
    "GDP", "CPI", "PPI", "PMI", "通胀", "通缩", "央行", "降息", "加息",
    "货币政策", "财政政策", "宏观经济", "经济数据",

    # 金融产品
    "基金", "债券", "理财", "信托", "保险", "银行", "证券", "期货",
    "期权", "外汇", "汇率", "黄金", "原油", "大宗商品",

    # 投资相关
    "投资", "融资", "IPO", "上市", "退市", "并购", "重组", "定增",
    "减持", "增持", "回购", "分红", "派息",

    # 行业概念
    "新能源", "半导体", "芯片", "人工智能", "AI", "医药", "消费",
    "地产", "房地产", "基建", "能源", "电力", "汽车",

    # 市场情绪
    "利好", "利空", "暴涨", "暴跌", "震荡", "反弹", "回调", "突破",
    "跳水", "飙升", "走强", "走弱",

    # 政策相关
    "政策", "监管", "法规", "税务", "税率", "补贴", "优惠",

    # 企业相关
    "财报", "业绩", "营收", "利润", "亏损", "盈利", "财报季",
    "年报", "季报", "中报",

    # 国际相关
    "美联储", "欧洲央行", "英国央行", "日本央行", "贸易战", "制裁",
    "关税", "贸易摩擦",
]


# ================================================================
# 核心类
# ================================================================

class NewsNowFetcher:
    """NewsNow API 数据获取器"""

    def __init__(self, api_url: str = API_BASE_URL):
        """
        初始化获取器

        Args:
            api_url: API 基础 URL
        """
        self.api_url = api_url

    def fetch_single_platform(
        self,
        platform_id: str,
        max_retries: int = 2,
        min_wait: int = 3,
        max_wait: int = 5,
    ) -> Optional[Dict]:
        """
        获取单个平台的热点数据

        Args:
            platform_id: 平台 ID（如 "cls-hot"）
            max_retries: 最大重试次数
            min_wait: 最小等待时间（秒）
            max_wait: 最大等待时间（秒）

        Returns:
            成功返回解析后的 JSON 数据，失败返回 None
        """
        url = f"{self.api_url}?id={platform_id}&latest"

        for attempt in range(max_retries + 1):
            try:
                response = requests.get(
                    url,
                    headers=HEADERS,
                    timeout=10,
                )
                response.raise_for_status()

                data = response.json()

                # 检查响应状态
                status = data.get("status", "")
                if status not in ["success", "cache"]:
                    raise ValueError(f"API 返回异常状态: {status}")

                status_text = "最新数据" if status == "success" else "缓存数据"
                print(f"[OK] 获取 {platform_id} 成功 ({status_text})")

                return data

            except requests.exceptions.RequestException as e:
                print(f"[X] 请求 {platform_id} 失败 (尝试 {attempt + 1}/{max_retries + 1}): {e}")

                if attempt < max_retries:
                    wait_time = random.uniform(min_wait, max_wait) + attempt * random.uniform(1, 2)
                    print(f"  {wait_time:.1f} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"  达到最大重试次数，放弃获取 {platform_id}")
                    return None

            except json.JSONDecodeError as e:
                print(f"[X] 解析 {platform_id} 响应失败: {e}")
                return None

            except Exception as e:
                print(f"[X] 处理 {platform_id} 时发生未知错误: {e}")
                return None

        return None

    def fetch_multiple_platforms(
        self,
        platforms: List[Tuple[str, str]],
        request_interval: float = 1.0,
    ) -> Dict[str, Dict]:
        """
        批量获取多个平台的热点数据

        Args:
            platforms: 平台列表，格式 [(platform_id, platform_name), ...]
            request_interval: 请求间隔（秒）

        Returns:
            格式：{platform_id: {"name": str, "data": dict, "items": list}}
        """
        results = {}

        for i, (platform_id, platform_name) in enumerate(platforms):
            print(f"\n正在获取: {platform_name} ({platform_id})")
            print("-" * 60)

            api_data = self.fetch_single_platform(platform_id)

            if api_data:
                # 提取热点条目
                items = self._extract_items(api_data)

                results[platform_id] = {
                    "name": platform_name,
                    "data": api_data,
                    "items": items,
                }

                print(f"  提取到 {len(items)} 条热点")
            else:
                print(f"  跳过 {platform_name}（获取失败）")

            # 请求间隔（除了最后一个）
            if i < len(platforms) - 1:
                actual_interval = request_interval + random.uniform(-0.1, 0.2)
                actual_interval = max(0.5, actual_interval)
                print(f"  等待 {actual_interval:.1f} 秒...")
                time.sleep(actual_interval)

        return results

    def _extract_items(self, api_data: Dict) -> List[Dict]:
        """
        从 API 响应中提取并清理热点条目

        Args:
            api_data: API 返回的原始数据

        Returns:
            清理后的条目列表
        """
        items = []

        for index, item in enumerate(api_data.get("items", []), start=1):
            title = item.get("title")

            # 跳过无效标题
            if not title or isinstance(title, float) or not str(title).strip():
                continue

            title = str(title).strip()

            items.append({
                "rank": index,
                "title": title,
                "url": item.get("url", ""),
                "mobile_url": item.get("mobileUrl", ""),
            })

        return items


# ================================================================
# 数据处理类
# ================================================================

class FinanceTopicAnalyzer:
    """财经热点分析器"""

    def __init__(self, keywords: List[str] = None):
        """
        初始化分析器

        Args:
            keywords: 财经关键词列表，默认使用 FINANCE_KEYWORDS
        """
        self.keywords = keywords or FINANCE_KEYWORDS

    def filter_finance_topics(self, items: List[Dict]) -> List[Dict]:
        """
        过滤出财经相关的热点

        Args:
            items: 原始热点列表

        Returns:
            包含财经关键词的热点列表
        """
        finance_items = []

        for item in items:
            title = item.get("title", "")

            # 检查是否包含财经关键词
            matched_keywords = self._match_keywords(title)

            if matched_keywords:
                finance_item = item.copy()
                finance_item["matched_keywords"] = matched_keywords
                finance_items.append(finance_item)

        return finance_items

    def _match_keywords(self, text: str) -> List[str]:
        """
        匹配文本中的财经关键词

        Args:
            text: 待匹配的文本

        Returns:
            匹配到的关键词列表
        """
        matched = []

        for keyword in self.keywords:
            if keyword in text:
                matched.append(keyword)

        return matched

    def analyze_all_platforms(self, fetch_results: Dict) -> Dict:
        """
        分析所有平台的数据

        Args:
            fetch_results: fetch_multiple_platforms 的返回结果

        Returns:
            分析结果，包含过滤后的财经热点
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "platforms": {},
            "summary": {
                "total_platforms": len(fetch_results),
                "total_items": 0,
                "finance_items": 0,
            }
        }

        for platform_id, platform_data in fetch_results.items():
            items = platform_data["items"]
            finance_items = self.filter_finance_topics(items)

            analysis["platforms"][platform_id] = {
                "name": platform_data["name"],
                "total_items": len(items),
                "finance_items": len(finance_items),
                "items": finance_items,
            }

            analysis["summary"]["total_items"] += len(items)
            analysis["summary"]["finance_items"] += len(finance_items)

        return analysis


# ================================================================
# 输出类
# ================================================================

class ResultsExporter:
    """结果导出器"""

    @staticmethod
    def save_json(data: Dict, output_path: str, ensure_ascii: bool = False):
        """
        保存为 JSON 文件（支持中文）

        Args:
            data: 要保存的数据
            output_path: 输出文件路径
            ensure_ascii: False 表示保留中文字符（不转义）
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=ensure_ascii,
                    indent=2,
                )
            print(f"\n[OK] JSON 已保存: {output_path}")
        except Exception as e:
            print(f"\n[X] 保存 JSON 失败: {e}")

    @staticmethod
    def print_summary(analysis: Dict):
        """
        打印分析摘要

        Args:
            analysis: analyze_all_platforms 的返回结果
        """
        print("\n" + "=" * 60)
        print("抓取结果摘要")
        print("=" * 60)

        summary = analysis["summary"]
        print(f"平台数量: {summary['total_platforms']}")
        print(f"总热点数: {summary['total_items']}")
        print(f"财经相关: {summary['finance_items']}")

        if summary["total_items"] > 0:
            ratio = (summary["finance_items"] / summary["total_items"]) * 100
            print(f"财经占比: {ratio:.1f}%")

        print("\n各平台详情:")
        print("-" * 60)

        for platform_id, platform in analysis["platforms"].items():
            name = platform["name"]
            total = platform["total_items"]
            finance = platform["finance_items"]

            if total > 0:
                ratio = (finance / total) * 100
                print(f"  {name:12s}: {total:3d} 条热点, {finance:3d} 条财经相关 ({ratio:5.1f}%)")
            else:
                print(f"  {name:12s}: 无数据")

        print("=" * 60)


# ================================================================
# 主函数
# ================================================================

def main():
    """主函数"""
    print("=" * 60)
    print("资本市场热点抓取工具")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"平台数量: {len(FINANCE_PLATFORMS)}")
    print(f"关键词数量: {len(FINANCE_KEYWORDS)}")
    print("=" * 60)

    # 1. 获取数据
    fetcher = NewsNowFetcher()
    fetch_results = fetcher.fetch_multiple_platforms(
        platforms=FINANCE_PLATFORMS,
        request_interval=1.0,  # 每次请求间隔 1 秒
    )

    if not fetch_results:
        print("\n[X] 未能获取任何平台数据，程序退出")
        return

    # 2. 分析数据
    print("\n正在分析数据...")
    analyzer = FinanceTopicAnalyzer()
    analysis = analyzer.analyze_all_platforms(fetch_results)

    # 3. 打印摘要
    ResultsExporter.print_summary(analysis)

    # 4. 保存结果
    output_dir = "D:/project/skills/capital-market-topic-scout/output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/finance_topics_{timestamp}.json"

    ResultsExporter.save_json(analysis, output_file, ensure_ascii=False)

    # 5. 显示部分财经热点预览
    print("\n财经热点预览（前 5 条）:")
    print("-" * 60)

    count = 0
    for platform_id, platform in analysis["platforms"].items():
        for item in platform["items"]:
            if count >= 5:
                break

            print(f"\n[{platform['name']}] #{item['rank']}")
            print(f"  标题: {item['title']}")
            print(f"  关键词: {', '.join(item['matched_keywords'])}")
            if item.get('url'):
                print(f"  链接: {item['url'][:80]}...")

            count += 1

    print("\n" + "=" * 60)
    print("抓取完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
