#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题分析工具
对抓取的热点进行智能分析，推荐优质选题
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import pytz


class TopicAnalyzer:
    """选题分析器"""
    
    # 财经相关关键词
    FINANCE_KEYWORDS = [
        "股票", "基金", "投资", "理财", "金融", "银行", "证券",
        "A股", "港股", "美股", "基金", "理财", "保险",
        "IPO", "上市", "并购", "融资", "估值",
        "利率", "汇率", "通胀", "GDP", "央行",
        "新能源", "芯片", "AI", "科技", "创新",
    ]
    
    # 评分权重
    SCORING_WEIGHTS = {
        "热度": 0.4,
        "相关性": 0.3,
        "创作价值": 0.3,
    }
    
    def __init__(self, data: Dict):
        self.data = data
        self.topics = self._extract_topics()
    
    def _extract_topics(self) -> List[Dict]:
        """提取所有话题"""
        topics = []
        
        for platform_id, platform_data in self.data.get("data", {}).items():
            platform_name = platform_data.get("name", platform_id)
            
            for rank, item in enumerate(platform_data.get("items", []), 1):
                topic = {
                    "title": item.get("title", ""),
                    "rank": rank,
                    "platform": platform_name,
                    "platform_id": platform_id,
                    "url": item.get("url", ""),
                    "mobile_url": item.get("mobileUrl", ""),
                }
                topics.append(topic)
        
        return topics
    
    def calculate_hotness_score(self, topic: Dict) -> float:
        """
        计算热度分（0-100）
        
        考虑因素：
        - 排名（越靠前分数越高）
        - 平台权重（财经平台权重更高）
        """
        rank = topic.get("rank", 10)
        
        # 排名得分（排名1-50，对应分数100-50）
        rank_score = max(100 - (rank - 1) * 1.5, 50)
        
        # 平台权重加成
        platform_id = topic.get("platform_id", "")
        if platform_id in ["cls-hot", "_36kr", "gelonghui"]:
            platform_bonus = 10
        else:
            platform_bonus = 0
        
        return min(rank_score + platform_bonus, 100)
    
    def calculate_relevance_score(self, topic: Dict) -> float:
        """
        计算相关性分（0-100）
        
        考虑因素：
        - 是否包含财经关键词
        - 关键词数量
        """
        title = topic.get("title", "").lower()
        
        # 计算匹配的关键词数量
        matched_keywords = [kw for kw in self.FINANCE_KEYWORDS if kw.lower() in title]
        match_count = len(matched_keywords)
        
        # 基础分
        if match_count == 0:
            base_score = 30
        elif match_count == 1:
            base_score = 60
        elif match_count == 2:
            base_score = 80
        else:
            base_score = 100
        
        return base_score
    
    def calculate_creation_value_score(self, topic: Dict) -> float:
        """
        计算创作价值分（0-100）
        
        考虑因素：
        - 标题长度（适中更好）
        - 内容深度潜力
        - 时效性
        """
        title = topic.get("title", "")
        title_length = len(title)
        
        # 标题长度得分（15-30字最佳）
        if 15 <= title_length <= 30:
            length_score = 100
        elif 10 <= title_length < 15 or 30 < title_length <= 40:
            length_score = 80
        else:
            length_score = 60
        
        # 内容深度潜力（包含关键词越多越有深度）
        depth_keywords = ["分析", "解读", "影响", "原因", "趋势", "机会"]
        depth_score = 80 if any(kw in title for kw in depth_keywords) else 70
        
        # 综合得分
        return (length_score + depth_score) / 2
    
    def calculate_overall_score(self, topic: Dict) -> float:
        """
        计算综合评分（0-100）
        """
        hotness = self.calculate_hotness_score(topic)
        relevance = self.calculate_relevance_score(topic)
        creation_value = self.calculate_creation_value_score(topic)
        
        overall = (
            hotness * self.SCORING_WEIGHTS["热度"] +
            relevance * self.SCORING_WEIGHTS["相关性"] +
            creation_value * self.SCORING_WEIGHTS["创作价值"]
        )
        
        return round(overall, 1)
    
    def analyze_all_topics(self) -> List[Dict]:
        """分析所有话题"""
        analyzed_topics = []
        
        for topic in self.topics:
            # 计算各项得分
            hotness_score = self.calculate_hotness_score(topic)
            relevance_score = self.calculate_relevance_score(topic)
            creation_value_score = self.calculate_creation_value_score(topic)
            overall_score = self.calculate_overall_score(topic)
            
            # 添加评分信息
            analyzed_topic = {
                **topic,
                "scores": {
                    "热度": hotness_score,
                    "相关性": relevance_score,
                    "创作价值": creation_value_score,
                    "综合": overall_score,
                },
                "recommendation": self._generate_recommendation(topic, overall_score),
            }
            
            analyzed_topics.append(analyzed_topic)
        
        # 按综合评分排序
        analyzed_topics.sort(key=lambda x: x["scores"]["综合"], reverse=True)
        
        return analyzed_topics
    
    def _generate_recommendation(self, topic: Dict, score: float) -> str:
        """生成推荐理由"""
        if score >= 80:
            return "🔥 强烈推荐：高热度、强相关性、优质创作角度"
        elif score >= 70:
            return "✅ 推荐选择：综合表现优秀"
        elif score >= 60:
            return "💡 可以考虑：有一定创作价值"
        else:
            return "⚠️ 谨慎选择：相关性或热度不足"
    
    def get_top_topics(self, n: int = 10) -> List[Dict]:
        """获取 Top N 选题"""
        analyzed_topics = self.analyze_all_topics()
        return analyzed_topics[:n]
    
    def generate_report(self, top_n: int = 10, format: str = "markdown") -> str:
        """
        生成选题报告
        
        Args:
            top_n: 显示前 N 个选题
            format: 输出格式（markdown/json）
        
        Returns:
            报告内容
        """
        top_topics = self.get_top_topics(top_n)
        
        if format == "json":
            return json.dumps(top_topics, ensure_ascii=False, indent=2)
        
        # Markdown 格式
        report_lines = []
        
        # 标题
        fetch_time = self.data.get("fetch_time", datetime.now().isoformat())
        report_lines.append(f"# 财经热点选题推荐（{fetch_time}）\n")
        report_lines.append(f"## 🔥 Top {top_n} 选题\n")
        
        # 统计信息
        total_items = self.data.get("total_items", 0)
        report_lines.append(f"**数据来源：** {len(self.data.get('data', {}))} 个平台，共 {total_items} 条热点\n")
        
        # 选题列表
        for i, topic in enumerate(top_topics, 1):
            title = topic.get("title", "")
            scores = topic.get("scores", {})
            platform = topic.get("platform", "")
            rank = topic.get("rank", 0)
            recommendation = topic.get("recommendation", "")
            
            report_lines.append(f"### {i}. {title}\n")
            report_lines.append(f"**综合评分：** {scores['综合']}/100\n")
            report_lines.append(f"**热度指数：** {'⭐' * int(scores['热度'] / 20)}\n")
            report_lines.append(f"**来源：** {platform} | 排名: #{rank}\n")
            report_lines.append(f"**评分详情：** 热度 {scores['热度']:.0f} | 相关性 {scores['相关性']:.0f} | 创作价值 {scores['创作价值']:.0f}\n")
            report_lines.append(f"**推荐理由：** {recommendation}\n")
            
            # 创作角度建议
            angles = self._suggest_creation_angles(topic)
            if angles:
                report_lines.append("**创作角度：**\n")
                for angle in angles:
                    report_lines.append(f"- {angle}\n")
            
            # 目标受众
            audience = self._suggest_target_audience(topic)
            if audience:
                report_lines.append(f"**目标受众：** {audience}\n")
            
            report_lines.append("\n---\n")
        
        return "".join(report_lines)
    
    def _suggest_creation_angles(self, topic: Dict) -> List[str]:
        """建议创作角度"""
        angles = []
        title = topic.get("title", "")
        
        # 根据标题内容推荐角度
        if any(kw in title for kw in ["AI", "芯片", "科技"]):
            angles.append("普通投资者如何布局科技赛道？")
            angles.append("产业链深度解析")
        
        if any(kw in title for kw in ["新能源", "电动车"]):
            angles.append("新能源投资机会梳理")
            angles.append("产业链投资逻辑")
        
        if any(kw in title for kw in ["利率", "央行", "政策"]):
            angles.append("对普通人的影响")
            angles.append("投资策略调整建议")
        
        return angles[:3]  # 最多3个角度
    
    def _suggest_target_audience(self, topic: Dict) -> str:
        """建议目标受众"""
        title = topic.get("title", "")
        
        if any(kw in title for kw in ["基金", "理财", "投资"]):
            return "理财新手、普通投资者"
        elif any(kw in title for kw in ["股票", "A股", "港股"]):
            return "股票投资者、价值投资者"
        elif any(kw in title for kw in ["科技", "AI", "芯片"]):
            return "科技投资者、行业从业者"
        else:
            return "大众投资者、财经爱好者"
    
    def save_report(self, output_path: str, top_n: int = 10, format: str = "markdown") -> str:
        """保存报告到文件"""
        report = self.generate_report(top_n, format)
        
        # 生成文件名
        timestamp = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H%M%S")
        ext = "md" if format == "markdown" else "json"
        filename = f"topics_report_{timestamp}.{ext}"
        filepath = Path(output_path) / filename
        
        Path(filepath.parent).mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"💾 报告已保存: {filepath}")
        return str(filepath)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='选题分析工具')
    parser.add_argument('--input', type=str, required=True, help='输入文件路径（JSON）')
    parser.add_argument('--top', type=int, default=10, help='显示前 N 个选题')
    parser.add_argument('--format', type=str, default='markdown', choices=['markdown', 'json'], help='输出格式')
    parser.add_argument('--output', type=str, default='/tmp', help='输出路径')
    
    args = parser.parse_args()
    
    # 读取数据
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 分析选题
    analyzer = TopicAnalyzer(data)
    
    # 生成报告
    report = analyzer.generate_report(args.top, args.format)
    print(report)
    
    # 保存报告
    analyzer.save_report(args.output, args.top, args.format)


if __name__ == "__main__":
    main()
