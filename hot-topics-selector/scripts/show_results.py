#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展示大模型筛选结果
"""

import json
from pathlib import Path


def main():
    # 读取原始数据
    with open('/tmp/hot_topics_2026-02-13_194445.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 读取筛选结果
    with open('/tmp/selected_titles.json', 'r', encoding='utf-8') as f:
        selected = json.load(f)
    
    # 提取所有标题
    all_titles = []
    for platform_id, platform_data in data.get("data", {}).items():
        platform_name = platform_data.get("name", platform_id)
        for rank, item in enumerate(platform_data.get("items", []), 1):
            all_titles.append({
                "title": item.get("title", ""),
                "platform": platform_name,
                "rank": rank,
            })
    
    # 展示筛选结果
    print("="*60)
    print("🎯 大模型筛选结果")
    print("="*60)
    
    print(f"\n✅ 已选择 {len(selected['selected_indices'])} 个标题：\n")
    
    for idx in selected['selected_indices']:
        if idx <= len(all_titles):
            title_info = all_titles[idx-1]
            reason = selected['reasons'].get(str(idx), "")
            priority = selected['priority'].get(str(idx), "")
            angles = selected['creation_angles'].get(str(idx), [])
            
            print(f"📌 {idx}. {title_info['title']}")
            print(f"   平台: {title_info['platform']} | 排名: #{title_info['rank']}")
            print(f"   优先级: {priority}")
            print(f"   理由: {reason}")
            
            if angles:
                print(f"   创作角度:")
                for angle in angles:
                    print(f"     • {angle}")
            
            print()
    
    print("="*60)
    print("📋 下一步操作：")
    print("="*60)
    print("\n1. ✅ 标题筛选已完成")
    print("2. ⏭️  抓取选中新闻的详细内容")
    print("3. ⏭️  基于内容生成完整选题方案")
    print("\n推荐优先处理：")
    print("  • #1 AI月入200万（最高热度）")
    print("  • #49 黄金投资案例（最直接的投资话题）")
    print("  • #5/#46 年终奖话题（大众共鸣强）")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
