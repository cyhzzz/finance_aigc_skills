#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场环境分析工具
分析当前时点的特殊因素：节假日、重大事件、特殊时期等
"""

import json
from datetime import datetime, timedelta
from chinese_calendar import is_workday, is_holiday
import sys


def analyze_market_context(date_str):
    """
    分析市场环境背景
    
    Args:
        date_str: 日期字符串，格式 'YYYY-MM-DD'
    
    Returns:
        dict: 市场环境分析结果
    """
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return {
            "error": "日期格式错误",
            "date": date_str
        }
    
    context = {
        "date": date_str,
        "weekday": target_date.strftime('%A'),
        "is_weekend": target_date.weekday() >= 5,
        "special_periods": [],
        "holiday_info": {},
        "market_sentiment_factors": [],
        "recommendations": []
    }
    
    # 1. 判断节假日相关
    holiday_analysis = analyze_holiday_context(target_date)
    context["holiday_info"] = holiday_analysis
    
    if holiday_analysis["is_pre_holiday"]:
        context["special_periods"].append({
            "type": "pre_holiday",
            "name": holiday_analysis["holiday_name"],
            "impact": "节前避险情绪，成交萎缩，资金兑现需求"
        })
        context["market_sentiment_factors"].append("节前效应")
        context["recommendations"].append("关注节前避险情绪对市场的影响")
    
    if holiday_analysis["is_post_holiday"]:
        context["special_periods"].append({
            "type": "post_holiday",
            "name": holiday_analysis["holiday_name"],
            "impact": "节后资金回流，情绪修复"
        })
        context["market_sentiment_factors"].append("节后效应")
    
    # 2. 判断月末/季末/年末效应
    period_analysis = analyze_period_effect(target_date)
    if period_analysis:
        context["special_periods"].append(period_analysis)
    
    # 3. 判断特殊时间窗口
    window_analysis = analyze_special_window(target_date)
    if window_analysis:
        context["special_periods"].extend(window_analysis)
    
    return context


def analyze_holiday_context(target_date):
    """
    分析节假日相关背景
    
    Args:
        target_date: datetime.date 对象
    
    Returns:
        dict: 节假日分析结果
    """
    holiday_info = {
        "is_pre_holiday": False,
        "is_post_holiday": False,
        "holiday_name": None,
        "days_to_holiday": None
    }
    
    # 定义主要节假日的典型时间段（近似，实际应使用农历）
    # 格式：(月份, 开始日, 结束日, 假期长度)
    major_holidays = {
        "春节": (2, 1, 15, 7),    # 2月1-15日左右，假期7天
        "国庆节": (10, 1, 7, 7),   # 10月1-7日
        "劳动节": (5, 1, 5, 5),    # 5月1-5日
        "元旦": (1, 1, 3, 3),      # 1月1-3日
        "清明节": (4, 4, 6, 3),    # 4月4-6日
    }
    
    # 检查是否临近节假日
    for holiday_name, (month, start_day, end_day, duration) in major_holidays.items():
        if target_date.month == month:
            # 计算距离假期的天数
            holiday_start = target_date.replace(day=start_day)
            holiday_end = target_date.replace(day=end_day)
            
            days_to_start = (holiday_start - target_date).days
            days_to_end = (holiday_end - target_date).days
            
            # 判断节前（假期开始前1-5个交易日）
            if -5 <= days_to_start <= -1:
                holiday_info["is_pre_holiday"] = True
                holiday_info["holiday_name"] = holiday_name
                holiday_info["days_to_holiday"] = abs(days_to_start)
                break
            
            # 判断假期中
            elif 0 <= days_to_start and days_to_end <= 0:
                holiday_info["holiday_name"] = holiday_name + "假期中"
                break
            
            # 判断节后（假期结束后1-3个交易日）
            elif 1 <= days_to_end <= 3:
                holiday_info["is_post_holiday"] = True
                holiday_info["holiday_name"] = holiday_name
                break
    
    return holiday_info


def analyze_period_effect(target_date):
    """
    分析月末/季末/年末效应
    
    Args:
        target_date: datetime.date 对象
    
    Returns:
        dict or None: 时期效应分析
    """
    # 月末效应（最后3个交易日）
    if target_date.day >= 28:
        return {
            "type": "month_end",
            "name": "月末",
            "impact": "月末结算压力，资金面波动"
        }
    
    # 季末效应（3月、6月、9月、12月的最后5个交易日）
    if target_date.month in [3, 6, 9, 12] and target_date.day >= 26:
        return {
            "type": "quarter_end",
            "name": "季末",
            "impact": "季末考核压力，机构调仓换股"
        }
    
    # 年末效应（12月最后10个交易日）
    if target_date.month == 12 and target_date.day >= 22:
        return {
            "type": "year_end",
            "name": "年末",
            "impact": "年末结算，资金面紧张，机构排名压力"
        }
    
    return None


def analyze_special_window(target_date):
    """
    分析特殊时间窗口
    
    Args:
        target_date: datetime.date 对象
    
    Returns:
        list: 特殊窗口列表
    """
    windows = []
    
    # 两会期间（3月初-3月中旬）
    if target_date.month == 3 and 3 <= target_date.day <= 15:
        windows.append({
            "type": "policy_window",
            "name": "两会期间",
            "impact": "政策预期升温，市场关注政策导向"
        })
    
    # 财报季（1月、4月、7月、10月）
    if target_date.month in [1, 4, 7, 10]:
        if 15 <= target_date.day <= 31:
            windows.append({
                "type": "earnings_season",
                "name": "财报季",
                "impact": "业绩披露密集，市场关注业绩预期"
            })
    
    # FOMC会议周（通常每月第三周）
    if 14 <= target_date.day <= 21:
        windows.append({
            "type": "fomc_week",
            "name": "FOMC会议周",
            "impact": "美联储政策预期，全球市场波动"
        })
    
    return windows


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='市场环境分析工具')
    parser.add_argument('date', nargs='?', help='分析日期 (YYYY-MM-DD)', 
                        default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--pre-holiday', help='手动指定为节前', metavar='HOLIDAY_NAME')
    parser.add_argument('--post-holiday', help='手动指定为节后', metavar='HOLIDAY_NAME')
    
    args = parser.parse_args()
    date_str = args.date
    
    print("=" * 60)
    print(f"市场环境分析 - {date_str}")
    print("=" * 60)
    
    context = analyze_market_context(date_str)
    
    # 手动覆盖节假日判断
    if args.pre_holiday:
        context['holiday_info'] = {
            'is_pre_holiday': True,
            'is_post_holiday': False,
            'holiday_name': args.pre_holiday,
            'days_to_holiday': '?',
            'manual_override': True
        }
        context['special_periods'] = [{
            'type': 'pre_holiday',
            'name': args.pre_holiday,
            'impact': '节前避险情绪，成交萎缩，资金兑现需求'
        }]
        context['market_sentiment_factors'] = ['节前效应']
        context['recommendations'] = ['关注节前避险情绪对市场的影响']
    
    if args.post_holiday:
        context['holiday_info'] = {
            'is_pre_holiday': False,
            'is_post_holiday': True,
            'holiday_name': args.post_holiday,
            'manual_override': True
        }
        context['special_periods'] = [{
            'type': 'post_holiday',
            'name': args.post_holiday,
            'impact': '节后资金回流，情绪修复'
        }]
        context['market_sentiment_factors'] = ['节后效应']
    
    # 输出分析结果
    print(f"\n📅 日期信息:")
    print(f"  日期: {context['date']}")
    print(f"  星期: {context['weekday']}")
    print(f"  是否周末: {'是' if context['is_weekend'] else '否'}")
    
    if context['holiday_info']:
        print(f"\n🎭 节假日信息:")
        holiday = context['holiday_info']
        if holiday.get('is_pre_holiday'):
            print(f"  ⚠️ 节前效应: {holiday['holiday_name']}")
            print(f"  距离假期: {holiday.get('days_to_holiday', '?')} 天")
        if holiday.get('is_post_holiday'):
            print(f"  ✅ 节后效应: {holiday['holiday_name']}")
    
    if context['special_periods']:
        print(f"\n📊 特殊时期:")
        for period in context['special_periods']:
            print(f"  • {period['name']}: {period['impact']}")
    
    if context['market_sentiment_factors']:
        print(f"\n💭 市场情绪因素:")
        for factor in context['market_sentiment_factors']:
            print(f"  • {factor}")
    
    if context['recommendations']:
        print(f"\n💡 分析建议:")
        for rec in context['recommendations']:
            print(f"  • {rec}")
    
    # 保存为 JSON
    output_file = f"/tmp/market_context_{date_str}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 分析结果已保存: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
