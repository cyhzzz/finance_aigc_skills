#!/usr/bin/env python3
"""
投顾写作Skill工厂 - 市场数据获取固化模块

功能：
1. 获取A股市场主要指数数据（上证、深证、创业板）
2. 获取板块行情数据
3. 获取资金流向数据
4. 格式化输出供写作使用

用法：
python market_data.py [日期]
python market_data.py 2026-03-25

依赖：
pip install akshare pandas requests
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

# 尝试导入akshare，如果失败则使用模拟数据
try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    print("⚠️ 警告: akshare未安装，将使用模拟数据")
    print("   安装命令: pip install akshare")


# ============ 数据获取函数 ============

def get_previous_trading_day(date_str: Optional[str] = None) -> str:
    """获取指定日期的前一个交易日"""
    if date_str:
        target = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        target = datetime.now()

    # 简单实现：如果是周末，往前找
    while target.weekday() >= 5:  # 5=Saturday, 6=Sunday
        target -= timedelta(days=1)

    return target.strftime("%Y-%m-%d")


def fetch_index_data(symbol: str, name: str, date: str) -> Dict[str, Any]:
    """获取单个指数数据"""
    result = {
        "name": name,
        "symbol": symbol,
        "date": date,
        "status": "unknown",
    }

    if not HAS_AKSHARE:
        result["status"] = "mock"
        result["close"] = 3000.0 + hash(date) % 1000
        result["change"] = 0.5
        result["change_pct"] = 0.5
        result["volume"] = 250000000000
        result["amount"] = 2500000000000
        return result

    try:
        if symbol == "000001":  # 上证指数
            df = ak.index_zh_a_hist(symbol="000001", period="daily", start_date=date, end_date=date)
        elif symbol == "399001":  # 深证成指
            df = ak.index_zh_a_hist(symbol="399001", period="daily", start_date=date, end_date=date)
        elif symbol == "399006":  # 创业板指
            df = ak.index_zh_a_hist(symbol="399006", period="daily", start_date=date, end_date=date)
        else:
            df = ak.index_zh_a_hist(symbol=symbol, period="daily", start_date=date, end_date=date)

        if df is not None and len(df) > 0:
            row = df.iloc[-1]
            result["close"] = float(row.get("收盘", row.get("close", 0)))
            result["open"] = float(row.get("开盘", row.get("open", 0)))
            result["high"] = float(row.get("最高", row.get("high", 0)))
            result["low"] = float(row.get("最低", row.get("low", 0)))
            result["volume"] = float(row.get("成交量", row.get("volume", 0)))
            result["amount"] = float(row.get("成交额", row.get("amount", 0)))

            # 计算涨跌幅
            prev_close = float(row.get("前收盘", row.get("pre_close", result["close"])))
            if prev_close > 0:
                result["change"] = result["close"] - prev_close
                result["change_pct"] = (result["change"] / prev_close) * 100

            result["status"] = "success"
        else:
            result["status"] = "no_data"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def fetch_market_data(date: Optional[str] = None) -> Dict[str, Any]:
    """获取市场数据主函数"""
    if not date:
        date = get_previous_trading_day()
    else:
        date = get_previous_trading_day(date)

    result = {
        "date": date,
        "indices": {},
        "market_summary": {},
        "status": "unknown",
    }

    # 获取三大指数
    indices = [
        ("000001", "上证指数"),
        ("399001", "深证成指"),
        ("399006", "创业板指"),
    ]

    for symbol, name in indices:
        result["indices"][symbol] = fetch_index_data(symbol, name, date)

    # 计算市场整体情况
    all_success = all(idx.get("status") == "success" for idx in result["indices"].values())

    if all_success:
        # 上涨/下跌/平盘计数
        rises = sum(1 for idx in result["indices"].values() if idx.get("change_pct", 0) > 0)
        falls = sum(1 for idx in result["indices"].values() if idx.get("change_pct", 0) < 0)

        total_amount = sum(idx.get("amount", 0) for idx in result["indices"].values())
        avg_change = sum(idx.get("change_pct", 0) for idx in result["indices"].values()) / len(indices)

        result["market_summary"] = {
            "rise_count": rises,
            "fall_count": falls,
            "total_amount": total_amount,
            "avg_change_pct": avg_change,
            "market_type": "普涨" if rises > falls else ("普跌" if falls > rises else "分化"),
        }
        result["status"] = "success"
    else:
        result["status"] = "partial"
        result["market_summary"] = {
            "rise_count": 0,
            "fall_count": 0,
            "market_type": "数据获取失败",
        }

    return result


def format_market_report(data: Dict[str, Any]) -> str:
    """格式化市场数据为可读报告"""
    if data.get("status") == "error":
        return f"❌ 数据获取失败: {data.get('error', '未知错误')}"

    date = data.get("date", "未知日期")
    lines = [
        f"=== A股市场数据 ({date}) ===",
        "",
        "【主要指数】",
    ]

    for symbol, idx in data.get("indices", {}).items():
        name = idx.get("name", symbol)
        status = idx.get("status", "unknown")

        if status == "success":
            close = idx.get("close", 0)
            change = idx.get("change", 0)
            change_pct = idx.get("change_pct", 0)
            amount = idx.get("amount", 0)

            direction = "▲" if change > 0 else ("▼" if change < 0 else "―")
            change_str = f"{direction}{abs(change):.2f}点({change_pct:+.2f}%)"

            # 格式化成交额
            if amount >= 100000000000:
                amount_str = f"{amount/100000000000:.2f}万亿元"
            else:
                amount_str = f"{amount/100000000:.2f}亿元"

            lines.append(f"  {name}: {close:.2f} {change_str} 成交额{amount_str}")
        else:
            lines.append(f"  {name}: 数据获取失败({status})")

    summary = data.get("market_summary", {})
    if summary:
        lines.extend([
            "",
            "【市场概况】",
            f"  整体态势: {summary.get('market_type', '未知')}",
        ])

    return "\n".join(lines)


# ============ CLI入口 ============

def main():
    parser = argparse.ArgumentParser(description="获取A股市场数据")
    parser.add_argument("date", nargs="?", default=None, help="交易日期(YYYY-MM-DD)，默认为上一交易日")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--format", choices=["report", "json", "raw"], default="report", help="输出格式")

    args = parser.parse_args()

    # 获取数据
    data = fetch_market_data(args.date)

    # 根据格式输出
    if args.format == "json" or args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.format == "raw":
        for symbol, idx in data.get("indices", {}).items():
            print(f"{symbol}: {idx}")
    else:
        print(format_market_report(data))

    # 返回状态码
    return 0 if data.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
