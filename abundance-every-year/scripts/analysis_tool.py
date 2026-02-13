#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析工具 - 分析市场数据，生成收评基础信息
"""

import json
import sys

def analyze_market_data(data_file):
    """
    分析市场数据，生成收评基础信息

    Args:
        data_file: 数据文件路径（JSON格式）

    Returns:
        dict: 分析结果
    """
    # 读取数据
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 检查数据错误
    if data.get('error'):
        error_msg = data['error']
        return {
            'error': error_msg,
            'message': f"数据获取失败: {error_msg}。无法生成收评报告。"
        }

    # 检查关键数据是否存在
    if not data.get('indices'):
        return {
            'error': 'indices_data_missing',
            'message': '关键指数数据缺失。无法生成收评报告。'
        }

    analysis = {
        'date': data['date'],
        'summary': '',
        'indices_analysis': {},
        'funds_analysis': {},
        'statistics_analysis': {},
        'sectors_analysis': {},
        'overall_sentiment': ''
    }

    # 分析指数表现
    indices = data.get('indices', {})
    if indices:
        # 找出涨幅最大和最小的指数
        index_list = [(k, v) for k, v in indices.items() if isinstance(v, dict)]
        sorted_indices = sorted(index_list, key=lambda x: x[1].get('change_pct', 0), reverse=True)

        best_index = sorted_indices[0] if sorted_indices else None
        worst_index = sorted_indices[-1] if sorted_indices else None

        # 判断市场整体涨跌
        rising_count = sum(1 for _, idx in indices.items() if isinstance(idx, dict) and idx.get('change_pct', 0) > 0)
        falling_count = sum(1 for _, idx in indices.items() if isinstance(idx, dict) and idx.get('change_pct', 0) < 0)

        if rising_count >= 2:
            market_direction = '上涨'
        elif falling_count >= 2:
            market_direction = '下跌'
        else:
            market_direction = '震荡'

        analysis['summary'] = f"{data['date']}，A股市场呈现{market_direction}态势。"

        if best_index:
            best_name = best_index[1]['name']
            best_pct = best_index[1]['change_pct']
            analysis['summary'] += f"{best_name}表现最强势，上涨{best_pct:.2f}%。"

        analysis['indices_analysis'] = {
            'best_index': best_index[0] if best_index else None,
            'worst_index': worst_index[0] if worst_index else None,
            'rising_count': rising_count,
            'falling_count': falling_count,
            'market_direction': market_direction
        }

    # 分析资金流向
    funds = data.get('funds', {})
    north_funds = funds.get('north', {})
    if isinstance(north_funds, dict) and 'net_inflow' in north_funds:
        net_inflow = north_funds['net_inflow']
        if net_inflow > 50:
            funds_direction = '大幅流入'
            sentiment = '偏多'
        elif net_inflow > 0:
            funds_direction = '小幅流入'
            sentiment = '谨慎偏多'
        elif net_inflow > -50:
            funds_direction = '小幅流出'
            sentiment = '偏空'
        else:
            funds_direction = '大幅流出'
            sentiment = '悲观'

        analysis['summary'] += f"北向资金{funds_direction}{abs(net_inflow):.2f}亿元，市场情绪{sentiment}。"

        analysis['funds_analysis'] = {
            'net_inflow': net_inflow,
            'funds_direction': funds_direction,
            'sentiment': sentiment
        }

        analysis['overall_sentiment'] = sentiment

    # 分析市场统计
    statistics = data.get('statistics', {})
    if 'limit_up' in statistics and 'rising' in statistics:
        limit_up = statistics['limit_up']
        limit_down = statistics['limit_down']
        rising = statistics['rising']
        falling = statistics['falling']
        total = statistics.get('total', rising + falling)

        if total > 0:
            rising_pct = rising / total * 100
        else:
            rising_pct = 0

        # 判断市场情绪
        if rising_pct > 75:
            market_sentiment = '强势'
        elif rising_pct > 66:
            market_sentiment = '偏多'
        elif rising_pct > 50:
            market_sentiment = '中性'
        elif rising_pct > 33:
            market_sentiment = '偏空'
        else:
            market_sentiment = '弱势'

        # 判断赚钱效应
        if limit_up > limit_down * 5:
            earning_effect = '明显'
        elif limit_up > limit_down * 2:
            earning_effect = '一般'
        else:
            earning_effect = '较差'

        analysis['statistics_analysis'] = {
            'limit_up': limit_up,
            'limit_down': limit_down,
            'rising': rising,
            'falling': falling,
            'rising_pct': rising_pct,
            'market_sentiment': market_sentiment,
            'earning_effect': earning_effect
        }

        if not analysis['overall_sentiment']:
            analysis['overall_sentiment'] = market_sentiment

    # 分析板块表现
    sectors = data.get('sectors', {})
    top_risers = sectors.get('top_risers', [])
    top_fallers = sectors.get('top_fallers', [])

    if top_risers:
        # 判断市场风格
        riser_names = [s.get('板块名称', '') for s in top_risers[:3]]
        tech_keywords = ['人工智能', '半导体', '云计算', '大数据', '5G', '芯片']
        consumer_keywords = ['白酒', '医药', '家电', '食品', '零售']
        cycle_keywords = ['钢铁', '煤炭', '有色', '化工', '建材']

        tech_count = sum(1 for name in riser_names if any(kw in name for kw in tech_keywords))
        consumer_count = sum(1 for name in riser_names if any(kw in name for kw in consumer_keywords))
        cycle_count = sum(1 for name in riser_names if any(kw in name for kw in cycle_keywords))

        if tech_count >= 2:
            market_style = '科技成长'
        elif consumer_count >= 2:
            market_style = '价值稳健'
        elif cycle_count >= 2:
            market_style = '周期轮动'
        else:
            market_style = '均衡'

        analysis['sectors_analysis'] = {
            'top_risers_count': len(top_risers),
            'top_fallers_count': len(top_fallers),
            'market_style': market_style,
            'top_3_sectors': riser_names
        }

    return analysis


def main():
    """主函数"""
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        data_file = '/tmp/market_data_2026-02-10.json'

    print(f"分析市场数据: {data_file}")
    print()

    # 分析数据
    analysis = analyze_market_data(data_file)

    if analysis.get('error'):
        error_msg = analysis.get('message', analysis['error'])
        print(f"✗ 分析失败: {error_msg}")
        print(f"\n❌ 无法生成收评报告")
        sys.exit(1)

    # 打印分析结果
    print("=== 市场数据分析 ===")
    print()
    print(f"日期: {analysis['date']}")
    print()
    print("核心观点:")
    print(analysis['summary'])
    print()

    # 指数分析
    if analysis['indices_analysis']:
        idx_ana = analysis['indices_analysis']
        print("指数分析:")
        print(f"- 市场方向: {idx_ana['market_direction']}")
        print(f"- 上涨指数: {idx_ana['rising_count']}个")
        print(f"- 下跌指数: {idx_ana['falling_count']}个")
        if idx_ana['best_index']:
            best_idx = idx_ana['best_index']
            print(f"- 表现最好: {best_idx}")
        print()

    # 资金分析
    if analysis['funds_analysis']:
        fund_ana = analysis['funds_analysis']
        print("资金分析:")
        print(f"- 北向资金: {fund_ana['funds_direction']} {abs(fund_ana['net_inflow']):.2f}亿元")
        print(f"- 市场情绪: {fund_ana['sentiment']}")
        print()

    # 统计分析
    if analysis['statistics_analysis']:
        stat_ana = analysis['statistics_analysis']
        print("统计分析:")
        print(f"- 涨停家数: {stat_ana['limit_up']}家")
        print(f"- 跌停家数: {stat_ana['limit_down']}家")
        print(f"- 上涨家数: {stat_ana['rising']}家")
        print(f"- 下跌家数: {stat_ana['falling']}家")
        print(f"- 上涨占比: {stat_ana['rising_pct']:.1f}%")
        print(f"- 市场情绪: {stat_ana['market_sentiment']}")
        print(f"- 赚钱效应: {stat_ana['earning_effect']}")
        print()

    # 板块分析
    if analysis['sectors_analysis']:
        sec_ana = analysis['sectors_analysis']
        print("板块分析:")
        print(f"- 领涨板块: {sec_ana['top_risers_count']}个")
        print(f"- 领跌板块: {sec_ana['top_fallers_count']}个")
        print(f"- 市场风格: {sec_ana['market_style']}")
        print(f"- Top 3板块: {', '.join(sec_ana['top_3_sectors'])}")
        print()

    # 综合判断
    print("综合判断:")
    print(f"- 整体情绪: {analysis['overall_sentiment']}")

    # 保存分析结果
    output_file = data_file.replace('.json', '_analysis.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 分析结果已保存: {output_file}")


if __name__ == '__main__':
    main()
