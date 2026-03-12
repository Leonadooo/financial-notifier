#!/usr/bin/env python3
"""
API 连接测试脚本
用于测试 Coze API 是否能正常访问并返回数据
"""
import os
import sys
import json
from datetime import datetime
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import HumanMessage, SystemMessage


def test_api_connection():
    """
    测试 Coze API 连接
    """
    print("=" * 70)
    print("🔍 Coze API 连接测试")
    print("=" * 70)
    print(f"📅 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 获取环境变量
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY") or os.getenv("COZE_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL") or os.getenv("COZE_BASE_URL")

    # 打印配置信息（隐藏敏感信息）
    print("📋 配置信息：")
    print(f"   API Key: {api_key[:20]}...{api_key[-10:] if len(api_key) > 30 else api_key}" if api_key else "   API Key: ❌ 未配置")
    print(f"   Base URL: {base_url}" if base_url else "   Base URL: ❌ 未配置")
    print()

    # 检查配置
    if not api_key:
        print("❌ 错误：未找到 API Key")
        print("   请在 GitHub Secrets 中配置 COZE_API_KEY")
        return False

    if not base_url:
        print("❌ 错误：未找到 Base URL")
        print("   请在 GitHub Secrets 中配置 COZE_BASE_URL")
        return False

    print("✅ 配置检查通过")
    print()

    # 初始化 LLM Client
    try:
        ctx = new_context(method="test_api")

        from coze_coding_dev_sdk import Config
        config = Config(
            api_key=api_key,
            base_url=base_url
        )

        client = LLMClient(ctx=ctx, config=config)
        print("✅ LLM Client 初始化成功")
        print()

    except Exception as e:
        print(f"❌ LLM Client 初始化失败：{str(e)}")
        return False

    # 发送测试请求
    print("📤 发送测试请求...")
    print()

    try:
        test_prompt = "请用一句话介绍你自己。"

        messages = [
            SystemMessage(content="你是一个AI助手。"),
            HumanMessage(content=test_prompt)
        ]

        response = client.invoke(messages=messages, temperature=0.7)

        # 处理响应
        content = response.content

        # 如果是列表格式，转换为字符串
        if isinstance(content, list):
            if content and isinstance(content[0], str):
                content = " ".join(content)
            else:
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                content = " ".join(text_parts)

        print("✅ API 调用成功！")
        print()
        print("📊 返回结果：")
        print("-" * 70)
        print(content.strip())
        print("-" * 70)
        print()

        # 验证返回内容
        if content and len(content.strip()) > 0:
            print("✅ 数据验证通过：返回内容不为空")
            print(f"   内容长度：{len(content.strip())} 字符")
            return True
        else:
            print("⚠️  警告：返回内容为空")
            return False

    except Exception as e:
        print(f"❌ API 调用失败：{str(e)}")
        print()
        print("可能的原因：")
        print("   1. API Key 错误或已失效")
        print("   2. Base URL 错误")
        print("   3. 网络连接问题")
        print("   4. Coze 服务暂时不可用")
        return False


def test_simple_generation():
    """
    测试简单的文本生成
    """
    print()
    print("=" * 70)
    print("🧪 文本生成测试")
    print("=" * 70)
    print()

    try:
        ctx = new_context(method="test_generation")

        api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY") or os.getenv("COZE_API_KEY")
        base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL") or os.getenv("COZE_BASE_URL")

        from coze_coding_dev_sdk import Config
        config = Config(api_key=api_key, base_url=base_url)
        client = LLMClient(ctx=ctx, config=config)

        # 测试生成一段简短的金融资讯
        prompt = "请用一句话描述今天的股市情况。"

        messages = [
            SystemMessage(content="你是一个专业的金融分析师。"),
            HumanMessage(content=prompt)
        ]

        response = client.invoke(messages=messages, temperature=0.7)
        content = response.content

        # 处理响应
        if isinstance(content, list):
            if content and isinstance(content[0], str):
                content = " ".join(content)
            else:
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                content = " ".join(text_parts)

        print("✅ 文本生成成功！")
        print()
        print("📝 生成内容：")
        print("-" * 70)
        print(content.strip())
        print("-" * 70)
        print()

        return True

    except Exception as e:
        print(f"❌ 文本生成失败：{str(e)}")
        return False


def main():
    """
    主函数
    """
    print()
    print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
    print("                    API 连接测试工具")
    print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
    print()

    # 测试 1：基本连接
    result1 = test_api_connection()

    # 测试 2：文本生成
    result2 = test_simple_generation()

    # 总结
    print()
    print("=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    print()

    if result1 and result2:
        print("✅ 所有测试通过！")
        print()
        print("🎉 API 连接正常，可以正常使用金融资讯推送服务！")
        print()
        return 0
    else:
        print("❌ 部分测试失败")
        print()
        if not result1:
            print("❌ 基本连接测试失败")
        if not result2:
            print("❌ 文本生成测试失败")
        print()
        print("💡 建议：")
        print("   1. 检查 GitHub Secrets 配置是否正确")
        print("   2. 确认 API Key 是否有效")
        print("   3. 确认 Base URL 是否正确")
        print("   4. 查看详细的错误日志")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
