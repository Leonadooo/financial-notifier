#!/usr/bin/env python3
"""
网络诊断工具
用于诊断 GitHub Actions 环境的网络连接问题
"""
import os
import sys
import time
import socket
import requests
from datetime import datetime


def test_dns_resolution():
    """
    测试 DNS 解析
    """
    print("=" * 70)
    print("🔍 DNS 解析测试")
    print("=" * 70)
    print()

    domains = [
        "www.coze.cn",
        "api.coze.cn",
        "integration.coze.cn",
        "www.coze.com",
    ]

    results = {}

    for domain in domains:
        try:
            start_time = time.time()
            ip_address = socket.gethostbyname(domain)
            elapsed_time = (time.time() - start_time) * 1000
            
            results[domain] = {
                "success": True,
                "ip": ip_address,
                "time": elapsed_time
            }
            
            print(f"✅ {domain}")
            print(f"   IP: {ip_address}")
            print(f"   耗时: {elapsed_time:.2f}ms")
            print()
            
        except Exception as e:
            results[domain] = {
                "success": False,
                "error": str(e)
            }
            
            print(f"❌ {domain}")
            print(f"   错误: {str(e)}")
            print()

    return results


def test_http_connection():
    """
    测试 HTTP 连接
    """
    print("=" * 70)
    print("🔍 HTTP 连接测试")
    print("=" * 70)
    print()

    urls = [
        "https://www.coze.cn",
        "https://api.coze.cn",
        "https://integration.coze.cn",
    ]

    results = {}

    for url in urls:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            elapsed_time = (time.time() - start_time) * 1000
            
            results[url] = {
                "success": True,
                "status_code": response.status_code,
                "time": elapsed_time
            }
            
            print(f"✅ {url}")
            print(f"   状态码: {response.status_code}")
            print(f"   耗时: {elapsed_time:.2f}ms")
            print()
            
        except Exception as e:
            results[url] = {
                "success": False,
                "error": str(e)
            }
            
            print(f"❌ {url}")
            print(f"   错误: {str(e)}")
            print()

    return results


def test_llm_api():
    """
    测试 LLM API 连接
    """
    print("=" * 70)
    print("🔍 LLM API 测试")
    print("=" * 70)
    print()

    # 获取环境变量
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY") or os.getenv("COZE_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL") or os.getenv("COZE_BASE_URL")

    if not api_key:
        print("❌ API Key 未配置")
        return {"success": False, "error": "API Key 未配置"}

    if not base_url:
        print("❌ Base URL 未配置")
        return {"success": False, "error": "Base URL 未配置"}

    print(f"📋 配置：")
    print(f"   API Key: {api_key[:20]}...{api_key[-10:] if len(api_key) > 30 else api_key}")
    print(f"   Base URL: {base_url}")
    print()

    # 测试 API 连接
    try:
        from coze_coding_dev_sdk import LLMClient
        from coze_coding_utils.runtime_ctx.context import new_context
        from langchain_core.messages import HumanMessage, SystemMessage

        ctx = new_context(method="diagnostic")
        
        from coze_coding_dev_sdk import Config
        config = Config(
            api_key=api_key,
            base_url=base_url
        )
        
        client = LLMClient(ctx=ctx, config=config)
        
        print("📤 发送测试请求...")
        start_time = time.time()
        
        messages = [
            SystemMessage(content="你是一个AI助手。"),
            HumanMessage(content="请用一句话介绍你自己。")
        ]
        
        response = client.invoke(messages=messages, temperature=0.7)
        
        elapsed_time = (time.time() - start_time) * 1000
        
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
        
        print(f"✅ API 调用成功！")
        print(f"   耗时: {elapsed_time:.2f}ms")
        print()
        print(f"📝 返回内容：")
        print("-" * 70)
        print(content.strip())
        print("-" * 70)
        print()
        
        return {
            "success": True,
            "time": elapsed_time,
            "content_length": len(content.strip())
        }
        
    except Exception as e:
        print(f"❌ API 调用失败：{str(e)}")
        print()
        return {"success": False, "error": str(e)}


def test_network_speed():
    """
    测试网络速度
    """
    print("=" * 70)
    print("🔍 网络速度测试")
    print("=" * 70)
    print()

    # 下载一个小文件测试速度
    test_url = "https://www.google.com"
    
    try:
        start_time = time.time()
        response = requests.get(test_url, timeout=10)
        elapsed_time = (time.time() - start_time) * 1000
        
        content_size = len(response.content)
        speed_kb = (content_size / 1024) / (elapsed_time / 1000)
        
        print(f"✅ 速度测试完成")
        print(f"   URL: {test_url}")
        print(f"   下载大小: {content_size} bytes ({content_size/1024:.2f} KB)")
        print(f"   耗时: {elapsed_time:.2f}ms")
        print(f"   速度: {speed_kb:.2f} KB/s")
        print()
        
        return {
            "success": True,
            "speed_kb": speed_kb
        }
        
    except Exception as e:
        print(f"❌ 速度测试失败：{str(e)}")
        print()
        return {"success": False, "error": str(e)}


def check_environment():
    """
    检查环境信息
    """
    print("=" * 70)
    print("🔍 环境信息")
    print("=" * 70)
    print()

    # 运行环境
    print("📊 运行环境：")
    print(f"   平台: {sys.platform}")
    print(f"   Python 版本: {sys.version}")
    print(f"   当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 网络环境
    print("🌐 网络环境：")
    hostname = socket.gethostname()
    print(f"   主机名: {hostname}")
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"   本地IP: {local_ip}")
    except:
        print(f"   本地IP: 无法获取")
    print()

    # 环境变量
    print("🔑 环境变量：")
    env_vars = [
        "COZE_WORKSPACE_PATH",
        "COZE_API_KEY",
        "COZE_BASE_URL",
        "COZE_INTEGRATION_MODEL_BASE_URL",
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if "KEY" in var or "TOKEN" in var:
                display_value = value[:20] + "..." + value[-10:] if len(value) > 30 else "***"
            else:
                display_value = value
            print(f"   {var}: {display_value}")
        else:
            print(f"   {var}: ❌ 未设置")
    
    print()


def main():
    """
    主函数
    """
    print()
    print("🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧")
    print("                    网络诊断工具")
    print("🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧🔧")
    print()

    # 检查环境
    check_environment()

    # 测试 DNS 解析
    dns_results = test_dns_resolution()

    # 测试 HTTP 连接
    http_results = test_http_connection()

    # 测试 LLM API
    llm_results = test_llm_api()

    # 测试网络速度
    speed_results = test_network_speed()

    # 总结
    print("=" * 70)
    print("📊 诊断总结")
    print("=" * 70)
    print()

    print("✅ 成功的测试：")
    
    dns_success = sum(1 for r in dns_results.values() if r.get("success"))
    print(f"   DNS 解析: {dns_success}/{len(dns_results)}")
    
    http_success = sum(1 for r in http_results.values() if r.get("success"))
    print(f"   HTTP 连接: {http_success}/{len(http_results)}")
    
    if llm_results.get("success"):
        print(f"   LLM API: ✅ 成功")
    else:
        print(f"   LLM API: ❌ 失败 - {llm_results.get('error', '未知错误')}")
    
    if speed_results.get("success"):
        print(f"   网络速度: ✅ {speed_results.get('speed_kb', 0):.2f} KB/s")
    else:
        print(f"   网络速度: ❌ 失败")
    
    print()
    
    # 建议
    print("💡 诊断建议：")
    print()
    
    if dns_success < len(dns_results):
        print("⚠️  DNS 解析有问题，可能的原因：")
        print("   1. 网络连接不稳定")
        print("   2. DNS 服务器配置问题")
        print("   3. 防火墙阻止 DNS 查询")
        print()
    
    if http_success < len(http_results):
        print("⚠️  HTTP 连接有问题，可能的原因：")
        print("   1. 网络连接不稳定")
        print("   2. 防火墙阻止 HTTP 请求")
        print("   3. 代理配置问题")
        print()
    
    if not llm_results.get("success"):
        print("⚠️  LLM API 连接失败，建议：")
        print("   1. 检查 API Key 是否正确")
        print("   2. 检查 Base URL 是否正确")
        print("   3. 检查网络连接是否正常")
        print("   4. 尝试使用不同的 Base URL")
        print()
    
    print()


if __name__ == "__main__":
    main()
