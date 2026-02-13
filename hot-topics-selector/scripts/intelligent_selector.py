#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能财经选题工具 - 基于大模型的选题推荐
新流程：标题抓取 → 大模型筛选 → 内容抓取 → 选题生成
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pytz


class IntelligentTopicSelector:
    """智能选题选择器（基于大模型）"""
    
    def __init__(self, data: Dict):
        self.data = data
        self.all_titles = self._extract_all_titles()
    
    def _extract_all_titles(self) -> List[Dict]:
        """提取所有标题"""
        titles = []
        
        for platform_id, platform_data in self.data.get("data", {}).items():
            platform_name = platform_data.get("name", platform_id)
            
            for rank, item in enumerate(platform_data.get("items", []), 1):
                title_info = {
                    "title": item.get("title", ""),
                    "rank": rank,
                    "platform": platform_name,
                    "platform_id": platform_id,
                    "url": item.get("url", ""),
                }
                titles.append(title_info)
        
        return titles
    
    def filter_titles_with_llm(self) -> List[Dict]:
        """
        使用大模型筛选标题
        
        返回：值得展开的标题列表
        """
        print("\n🤖 使用大模型筛选标题...")
        print(f"总标题数: {len(self.all_titles)}")
        
        # 准备提示词
        prompt = self._build_filter_prompt()
        
        # 保存提示词到文件（供 agent 使用）
        prompt_file = "/tmp/topic_filter_prompt.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"\n✓ 提示词已保存: {prompt_file}")
        print("请使用大模型处理提示词，返回 JSON 格式的筛选结果")
        
        # 返回所有标题（等待大模型筛选）
        return self.all_titles
    
    def _build_filter_prompt(self) -> str:
        """构建筛选提示词"""
        
        # 准备标题列表
        titles_text = []
        for i, title_info in enumerate(self.all_titles[:50], 1):  # 限制50个避免太长
            titles_text.append(
                f"{i}. [{title_info['platform']}] {title_info['title']}"
            )
        
        prompt = f"""# 任务：筛选适合大众的财经选题

## 背景

目标受众：**不炒股的普通大众**（通过抖音/小红书看到内容）
**核心目标：软性引导他们进行证券开户、基金投资等理财操作**

## 筛选标准（投资关联性为核心）

**✅ 必须满足：可以自然转向证券开户、基金投资、理财规划**

### 优先级排序：

#### 🔥🔥🔥🔥🔥 最高优先级（必须包含）
**能直接关联投资理财：**
- 赚钱故事 → 投资理财产品
- 理财话题 → 证券开户/基金定投
- 资产增值 → 投资工具推荐

**示例：**
- AI月入200万 → 普通人如何通过投资分享AI红利（✅ 可关联基金/股票投资）
- 黄金赚196万 → 普通人如何投资黄金（✅ 可关联黄金ETF/券商产品）
- 年终奖话题 → 年终奖如何理财（✅ 可关联基金定投/证券开户）

#### 🔥🔥🔥🔥 高优先级
**痛点驱动 + 可关联投资：**
- 薪资话题 → 工资收入vs投资收入
- 储蓄话题 → 存钱vs投资
- 消费话题 → 消费降级vs理财规划

#### 🔥🔥🔥 中优先级
**情绪共鸣 + 勉强可关联：**
- 教育话题 → 教育基金规划
- 养老话题 → 养老金投资

**❌ 不选这类标题（无法关联投资）：**
1. 纯娱乐八卦（明星、综艺）
2. 纯社会新闻（与财经无关）
3. 太专业的证券新闻（大众不关心）
4. 无法转向投资的生活话题

## 标题列表

{chr(10).join(titles_text)}

## 输出格式

请返回 JSON 格式：

```json
{{
  "selected_indices": [1, 3, 5, 7, 9],
  "reasons": {{
    "1": "✅ 可直接关联：AI赚钱 → AI基金投资。符合最高优先级，传播性强。",
    "3": "✅ 可直接关联：黄金案例 → 黄金ETF/券商产品。符合最高优先级，数据冲击强。",
    "5": "✅ 可关联：薪资话题 → 工资收入vs投资收入。符合高优先级，共鸣强。"
  }},
  "investment_angles": {{
    "1": "可以推荐：AI主题基金、科技股票、券商AI产品",
    "3": "可以推荐：黄金ETF、券商黄金产品、资产配置",
    "5": "可以推荐：基金定投、证券开户、理财规划"
  }},
  "methodology_tags": {{
    "1": "痛点驱动+情绪共鸣+投资直接关联",
    "3": "数据冲击+故事表达+投资直接关联",
    "5": "痛点驱动+情绪共鸣+投资可关联"
  }},
  "title_variations": {{
    "1": [
      "不会技术也能AI搞钱？普通人如何通过投资分享红利",
      "月入200万的AI生意，普通人能参与吗？",
      "AI时代，普通人如何投资才能月入过万？"
    ]
  }},
  "investment_relevance_score": {{
    "1": 95,
    "3": 92,
    "5": 85
  }}
}}
```

**严格要求：**
- **固定选择 5 个标题**（不多不少）
- 每个标题必须说明：
  1. 是否可以关联证券开户/基金投资/理财规划
  2. 具体的投资产品推荐方向
  3. 投资关联度评分（0-100分）
- 投资关联度 ≥80分：最高优先级
- 投资关联度 60-79分：高优先级
- 投资关联度 <60分：不选择

**评分规则：**
- 可直接关联投资产品（基金/股票/券商产品）：90-100分
- 可关联理财规划（定投/配置）：80-89分
- 勉强可关联教育/养老：60-79分
- 无法关联：0分（不选择）
"""
        
        return prompt
    
    def save_titles_for_review(self, output_path: str = "/tmp"):
        """保存标题供人工审核"""
        timestamp = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d_%H%M%S")
        filename = f"titles_for_review_{timestamp}.txt"
        filepath = Path(output_path) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# 待筛选的标题列表\n\n")
            f.write(f"总数: {len(self.all_titles)}\n")
            f.write(f"时间: {datetime.now(pytz.timezone('Asia/Shanghai')).isoformat()}\n\n")
            
            for i, title_info in enumerate(self.all_titles, 1):
                f.write(f"{i}. [{title_info['platform']}] {title_info['title']}\n")
                f.write(f"   排名: #{title_info['rank']}\n\n")
        
        print(f"✓ 标题列表已保存: {filepath}")
        return str(filepath)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='智能财经选题工具')
    parser.add_argument('--input', type=str, required=True, help='输入文件路径（JSON）')
    parser.add_argument('--output', type=str, default='/tmp', help='输出路径')
    
    args = parser.parse_args()
    
    # 读取数据
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 初始化选择器
    selector = IntelligentTopicSelector(data)
    
    # 保存标题供审核
    selector.save_titles_for_review(args.output)
    
    # 生成筛选提示词
    selector.filter_titles_with_llm()
    
    print("\n" + "="*60)
    print("下一步操作：")
    print("1. 查看保存的标题列表")
    print("2. 使用大模型处理提示词")
    print("3. 根据返回的索引，抓取详细内容")
    print("="*60)


if __name__ == "__main__":
    main()
