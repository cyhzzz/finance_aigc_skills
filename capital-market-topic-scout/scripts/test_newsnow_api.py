# coding=utf-8
"""
NewsNow API 测试脚本

用于快速测试单个平台的连接性和数据格式
"""

import json
import sys
import io
import requests

# Windows 控制台编码修复
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def test_platform(platform_id: str, platform_name: str = ""):
    """
    测试单个平台

    Args:
        platform_id: 平台 ID
        platform_name: 平台名称（可选）
    """
    url = "https://newsnow.busiyi.world/api/s"

    print(f"\n{'='*60}")
    print(f"测试平台: {platform_name or platform_id} ({platform_id})")
    print(f"{'='*60}\n")

    print(f"请求 URL: {url}?id={platform_id}&latest")

    try:
        response = requests.get(
            f"{url}?id={platform_id}&latest",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
            },
            timeout=10,
        )

        print(f"\n状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            print(f"响应状态: {data.get('status', 'N/A')}")
            print(f"数据条数: {len(data.get('items', []))}")

            print("\n前 3 条数据:")
            print("-" * 60)

            for i, item in enumerate(data.get('items', [])[:3], start=1):
                title = item.get('title', 'N/A')
                url = item.get('url', 'N/A')
                print(f"\n{i}. {title}")
                print(f"   链接: {url[:80]}...")

            # 保存完整响应
            output_file = f"test_response_{platform_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n完整响应已保存: {output_file}")

        else:
            print(f"错误响应: {response.text[:200]}")

    except requests.exceptions.Timeout:
        print("\n[错误] 请求超时")
    except requests.exceptions.ConnectionError:
        print("\n[错误] 连接失败，请检查网络")
    except json.JSONDecodeError:
        print(f"\n[错误] JSON 解析失败，响应内容:\n{response.text[:200]}")
    except Exception as e:
        print(f"\n[错误] {type(e).__name__}: {e}")


def main():
    """主函数"""
    # 常用财经平台列表
    platforms = [
        ("cls-hot", "财联社热门"),
        ("wallstreetcn-hot", "华尔街见闻"),
        ("sina-finance", "新浪财经"),
        ("ifeng", "凤凰网"),
        ("thepaper", "澎湃新闻"),
    ]

    print("=" * 60)
    print("NewsNow API 测试工具")
    print("=" * 60)

    # 如果命令行提供了参数，测试指定平台
    if len(sys.argv) > 1:
        platform_id = sys.argv[1]
        platform_name = sys.argv[2] if len(sys.argv) > 2 else ""
        test_platform(platform_id, platform_name)
    else:
        # 否则测试所有平台
        for platform_id, platform_name in platforms:
            test_platform(platform_id, platform_name)

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
