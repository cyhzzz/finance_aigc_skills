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
目标：**软性引导他们了解投资理财**

## 筛选标准

**✅ 选择这类标题：**
1. 与普通人生活相关（房价、物价、就业、工资、消费）
2. 大众关注度高（AI、新能源、教育、医疗、养老）
3. 可以自然转向投资（赚钱故事、理财启发）
4. 引发情感共鸣（焦虑、希望、好奇）

**❌ 不选这类标题：**
1. 太专业的证券新闻（证券、券商、监管、处罚）
2. 技术分析类（K线、技术面、量能）
3. 与生活无关的行业新闻
4. 负面情绪过强（恐吓、诈骗）

## 标题列表

{chr(10).join(titles_text)}

## 输出格式

请返回 JSON 格式：

```json
{{
  "selected_indices": [1, 3, 5, 7, 9],
  "reasons": {{
    "1": "与生活相关，房价是大众关注话题",
    "3": "AI赚钱故事，可以转向投资",
    "5": "就业话题，引发共鸣"
  }}
}}
```

**要求：**
- 选择 5-10 个最值得展开的标题
- 每个标题简要说明选择理由
- 理由要说明为什么适合大众、如何转向投资
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
