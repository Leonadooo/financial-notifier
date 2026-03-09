#!/usr/bin/env python3
"""
金融资讯定时推送脚本
每天自动获取金融资讯并通过配置的渠道推送
"""
import sys
import os
import json
from datetime import datetime
import asyncio

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import HumanMessage, SystemMessage
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_utils.log.write_log import setup_logging
from coze_coding_utils.log.config import LOG_DIR, LOG_LEVEL

# 导入工具 - 使用内部实现函数
from src.tools.financial_news_tool import (
    _search_financial_news_impl
)
from src.tools.notification_tool import (
    send_wechat_notification,
    send_feishu_notification,
    send_email_notification
)

# 设置日志
LOG_FILE = os.path.join(LOG_DIR, "daily_notification.log")
setup_logging(
    log_file=LOG_FILE,
    max_bytes=100 * 1024 * 1024,
    backup_count=5,
    log_level=LOG_LEVEL,
    use_json_format=True,
    console_output=True
)


def get_notification_config():
    """获取推送配置"""
    config_path = os.path.join(
        os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"),
        "config",
        "notification_config.json"
    )

    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 默认配置
    return {
        "enabled_channels": ["console"],  # 默认只输出到控制台
        "wechat": {"enabled": False},
        "feishu": {"enabled": False},
        "email": {
            "enabled": False,
            "recipients": []
        },
        "content_types": ["gold", "oil", "financial"]  # 默认获取所有内容
    }


def gather_financial_news(content_types):
    """收集金融资讯"""
    print("\n" + "=" * 60)
    print(f"开始收集金融资讯 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")

    all_content = []

    if "gold" in content_types:
        print("📊 正在获取黄金价格分析...")
        try:
            gold_content = _search_financial_news_impl("黄金价格走势 影响因素 2024")
            all_content.append({
                "title": "🥇 黄金价格走势分析",
                "content": gold_content
            })
            print("✅ 黄金价格分析获取成功")
        except Exception as e:
            print(f"❌ 黄金价格分析获取失败: {e}")

    if "oil" in content_types:
        print("\n📊 正在获取原油价格分析...")
        try:
            oil_content = _search_financial_news_impl("原油价格走势 国际石油市场 影响因素 2024")
            all_content.append({
                "title": "🛢️ 原油价格走势分析",
                "content": oil_content
            })
            print("✅ 原油价格分析获取成功")
        except Exception as e:
            print(f"❌ 原油价格分析获取失败: {e}")

    if "financial" in content_types:
        print("\n📊 正在获取国际金融形势...")
        try:
            financial_content = _search_financial_news_impl("国际金融形势 全球经济 最新动态")
            all_content.append({
                "title": "🌍 国际金融形势",
                "content": financial_content
            })
            print("✅ 国际金融形势获取成功")
        except Exception as e:
            print(f"❌ 国际金融形势获取失败: {e}")

    return all_content


def format_notification(all_content):
    """格式化推送消息"""
    date_str = datetime.now().strftime("%Y年%m月%d日")
    header = f"# 📈 金融资讯早报\n\n**日期：{date_str}**\n\n"

    body = []
    for item in all_content:
        body.append(f"## {item['title']}\n\n")
        body.append(item['content'])
        body.append("\n\n" + "-" * 60 + "\n\n")

    footer = f"\n\n---\n🤖 由金融资讯助手自动生成 | {datetime.now().strftime('%H:%M')}"

    return header + "\n".join(body) + footer


def send_notification(content, config):
    """发送通知"""
    enabled_channels = config.get("enabled_channels", ["console"])
    success_count = 0
    total_count = 0

    # 控制台输出
    if "console" in enabled_channels:
        print("\n" + "=" * 80)
        print("【控制台输出】")
        print("=" * 80)
        print(content)
        print("=" * 80 + "\n")
        success_count += 1
        total_count += 1

    # 企业微信推送
    if "wechat" in enabled_channels and config.get("wechat", {}).get("enabled", False):
        total_count += 1
        try:
            result = send_wechat_notification(content, message_type="markdown")
            if "成功" in result:
                print("✅ 企业微信推送成功")
                success_count += 1
            else:
                print(f"❌ 企业微信推送失败: {result}")
        except Exception as e:
            print(f"❌ 企业微信推送异常: {e}")

    # 飞书推送
    if "feishu" in enabled_channels and config.get("feishu", {}).get("enabled", False):
        total_count += 1
        try:
            result = send_feishu_notification(
                content,
                message_type="rich",
                title=f"📈 金融资讯早报 - {datetime.now().strftime('%m/%d')}"
            )
            if "成功" in result:
                print("✅ 飞书推送成功")
                success_count += 1
            else:
                print(f"❌ 飞书推送失败: {result}")
        except Exception as e:
            print(f"❌ 飞书推送异常: {e}")

    # 邮件推送
    if "email" in enabled_channels and config.get("email", {}).get("enabled", False):
        recipients = config.get("email", {}).get("recipients", [])
        if recipients:
            total_count += 1
            try:
                result = send_email_notification(
                    subject=f"📈 金融资讯早报 - {datetime.now().strftime('%Y-%m-%d')}",
                    content=content,
                    to_addrs=recipients
                )
                if "成功" in result:
                    print("✅ 邮件推送成功")
                    success_count += 1
                else:
                    print(f"❌ 邮件推送失败: {result}")
            except Exception as e:
                print(f"❌ 邮件推送异常: {e}")

    return success_count, total_count


def main():
    """主函数"""
    print("\n" + "🚀" * 40)
    print("金融资讯定时推送服务启动")
    print("🚀" * 40)

    # 获取配置
    config = get_notification_config()
    content_types = config.get("content_types", ["gold", "oil", "financial"])

    print(f"\n📋 配置信息:")
    print(f"   - 启用渠道: {', '.join(config.get('enabled_channels', []))}")
    print(f"   - 内容类型: {', '.join(content_types)}")

    # 收集资讯
    all_content = gather_financial_news(content_types)

    if not all_content:
        print("\n⚠️  未能获取到任何资讯，请检查网络连接")
        return

    # 格式化内容
    formatted_content = format_notification(all_content)

    # 发送通知
    print("\n📤 开始推送消息...")
    success_count, total_count = send_notification(formatted_content, config)

    # 总结
    print("\n" + "📊" * 40)
    print("推送任务完成")
    print("📊" * 40)
    print(f"成功: {success_count}/{total_count}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if success_count < total_count:
        print("\n⚠️  部分推送渠道失败，请检查配置和凭证")
        sys.exit(1)
    else:
        print("\n✅ 所有推送渠道成功！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断执行")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
