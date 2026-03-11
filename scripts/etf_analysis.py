#!/usr/bin/env python3
"""
ETF投资分析推送脚本
基于国际新闻、大宗商品价格、全球金融动态，分析对A股和港股ETF的影响
"""
import sys
import os
import json
from datetime import datetime

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_utils.log.write_log import setup_logging
from coze_coding_utils.log.config import LOG_DIR, LOG_LEVEL

# 导入工具 - 使用内部实现函数
from src.tools.financial_news_tool import (
    _get_international_events_impl,
    _get_commodity_prices_impl,
    _get_financial_dynamics_impl
)
from src.tools.notification_tool import (
    _send_email_notification_impl
)
from src.utils.prediction_manager import (
    save_prediction,
    load_yesterday_prediction,
    extract_prediction_summary
)

# 设置日志
LOG_FILE = os.path.join(LOG_DIR, "etf_analysis.log")
setup_logging(
    log_file=LOG_FILE,
    max_bytes=100 * 1024 * 1024,
    backup_count=5,
    log_level=LOG_LEVEL,
    use_json_format=True,
    console_output=True
)


def get_llm_config():
    """获取LLM配置"""
    config_path = os.path.join(
        os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"),
        "config",
        "agent_llm_config.json"
    )

    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


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

    return {
        "enabled_channels": ["console"],
        "email": {"enabled": False, "recipients": []}
    }


def gather_market_data():
    """收集市场数据"""
    print("\n" + "=" * 60)
    print(f"开始收集市场数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")

    all_data = {}

    # 1. 获取国际事件
    print("📊 正在获取今日关键国际事件...")
    try:
        all_data["international_events"] = _get_international_events_impl()
        print("✅ 国际事件获取成功")
    except Exception as e:
        print(f"❌ 国际事件获取失败: {e}")
        all_data["international_events"] = "暂无国际事件数据"

    # 2. 获取大宗商品价格
    print("\n📊 正在获取大宗商品价格...")
    try:
        all_data["commodity_prices"] = _get_commodity_prices_impl()
        print("✅ 大宗商品价格获取成功")
    except Exception as e:
        print(f"❌ 大宗商品价格获取失败: {e}")
        all_data["commodity_prices"] = "暂无大宗商品数据"

    # 3. 获取金融动态
    print("\n📊 正在获取全球金融动态...")
    try:
        all_data["financial_dynamics"] = _get_financial_dynamics_impl()
        print("✅ 金融动态获取成功")
    except Exception as e:
        print(f"❌ 金融动态获取失败: {e}")
        all_data["financial_dynamics"] = "暂无金融动态数据"

    return all_data


def analyze_etf_impact(market_data, yesterday_prediction=None):
    """使用LLM分析ETF影响"""
    print("\n" + "=" * 60)
    print("开始分析ETF影响...")
    print("=" * 60 + "\n")

    # 获取LLM配置
    llm_config = get_llm_config()
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    # 初始化LLM
    llm = ChatOpenAI(
        model=llm_config.get('config', {}).get('model', 'doubao-seed-1-8-251228'),
        api_key=api_key,
        base_url=base_url,
        temperature=0.7,
        timeout=600
    )

    # 构建昨日预测部分
    yesterday_section = ""
    if yesterday_prediction:
        yesterday_date = yesterday_prediction.get('date', '昨天')
        yesterday_content = yesterday_prediction.get('content', '暂无预测')
        yesterday_section = f"""

### 0. 昨日预测验证
**昨日日期：{yesterday_date}**

昨日预测内容摘要：
{yesterday_content[:2000]}

请根据今日市场数据，验证昨日预测的准确性，并分析原因：
- 哪些预测得到了验证？
- 哪些预测与实际情况不符？
- 偏差的原因是什么？

"""

    # 构建完整的提示词
    full_prompt = f"""你是一位专业的ETF投资分析师，擅长分析国际市场动态对A股和港股ETF的影响。

请基于以下今日市场数据，提供专业的ETF投资分析报告。

## 市场数据

### 1. 今日关键国际事件
{market_data.get('international_events', '暂无数据')}

### 2. 大宗商品价格走势
{market_data.get('commodity_prices', '暂无数据')}

### 3. 全球金融动态
{market_data.get('financial_dynamics', '暂无数据')}

## 分析要求

请按以下结构提供完整的ETF投资分析报告：

1. **今日关键国际事件总结**
   - 美联储/欧央行政策动态
   - 地缘政治事件
   - 中美关系
   - 全球经济数据

2. **大宗商品价格走势分析**（必须使用表格格式）
   - 表格格式：
   | 品种 | 涨跌表现 | 核心逻辑 |
   |------|----------|---------|
   | 原油 | 涨跌幅% | 上涨/下跌原因 |
   | 黄金 | 涨跌幅% | 上涨/下跌原因 |
   | 铜 | 涨跌幅% | 上涨/下跌原因 |
   | 天然气 | 涨跌幅% | 上涨/下跌原因 |
   - 覆盖：原油、黄金、铜、天然气、农产品
   - 要求：表格中每行一个品种，清晰展示涨跌和原因

3. **全球金融动态分析**
   - 美元指数走势
   - 美债收益率变化
   - 北向/南向资金流向
   - 全球风险偏好变化

4. **对A股ETF的直接影响**（必须使用表格格式，分两类）
   - **宽基ETF表格**：
   | ETF代码/名称 | 影响方向 | 核心原因 |
   |-------------|----------|---------|
   | 沪深300(510300) | 偏多/偏空/中性 | 具体原因说明 |
   | 中证500(510500) | 偏多/偏空/中性 | 具体原因说明 |
   | 科创50(588000) | 偏多/偏空/中性 | 具体原因说明 |
   | 创业板(159915) | 偏多/偏空/中性 | 具体原因说明 |
   - **行业ETF表格**：
   | ETF代码/名称 | 影响方向 | 核心原因 |
   |-------------|----------|---------|
   | 半导体(512480) | 偏多/偏空/中性 | 具体原因说明 |
   | 新能源(516160) | 偏多/偏空/中性 | 具体原因说明 |
   | 医药(512010) | 偏多/偏空/中性 | 具体原因说明 |
   | 消费(159928) | 偏多/偏空/中性 | 具体原因说明 |
   | 金融(512880) | 偏多/偏空/中性 | 具体原因说明 |
   | 煤炭(515220) | 偏多/偏空/中性 | 具体原因说明 |
   | 有色(512400) | 偏多/偏空/中性 | 具体原因说明 |
   | 黄金(518880) | 偏多/偏空/中性 | 具体原因说明 |
   | 油气(512200) | 偏多/偏空/中性 | 具体原因说明 |

5. **对港股ETF的直接影响**（必须使用表格格式，分两类）
   - **宽基ETF表格**：
   | ETF代码/名称 | 影响方向 | 核心原因 |
   |-------------|----------|---------|
   | 恒生指数(159920) | 偏多/偏空/中性 | 具体原因说明 |
   | 恒生科技(513180) | 偏多/偏空/中性 | 具体原因说明 |
   | 国企指数(159960) | 偏多/偏空/中性 | 具体原因说明 |
   - **行业ETF表格**：
   | ETF代码/名称 | 影响方向 | 核心原因 |
   |-------------|----------|---------|
   | 港股互联网(513050) | 偏多/偏空/中性 | 具体原因说明 |
   | 港股医药(513700) | 偏多/偏空/中性 | 具体原因说明 |
   | 港股金融(513550) | 偏多/偏空/中性 | 具体原因说明 |
   | 港股能源(513500) | 偏多/偏空/中性 | 具体原因说明 |

6. **A股与港股ETF的联动差异**
   - 港股更敏感于外资/美元因素
   - A股更敏感于内资/政策因素

7. **当日ETF交易关注点**
   - 高弹性方向
   - 防御方向
   - 资金流向信号

8. **昨日预测验证**（必须使用表格格式）
   - 表格格式：
   | 预测内容 | 验证结果 | 实际情况 | 偏差原因 |
   |---------|---------|---------|---------|
   | 预测原油上涨 | ✅准确 | 原油今日上涨X% | 预测与实际一致 |
   | 预测黄金下跌 | ❌偏差 | 黄金今日上涨Y% | 受突发事件影响 |
   - 如果没有昨日预测数据，请标注"无昨日预测数据"
   - 验证结果选项：✅准确、⚠️部分准确、❌偏差、❓无法判断

## 输出格式

⚠️ 重要：第2、4、5、8点必须使用Markdown表格格式，不要使用列表或段落！

- **第2点（大宗商品）**：使用一个表格，每行一个品种
- **第4点（A股ETF）**：使用两个表格，分别展示宽基ETF和行业ETF
- **第5点（港股ETF）**：使用两个表格，分别展示宽基ETF和行业ETF

表格格式示例：
| ETF代码/名称 | 影响方向 | 核心原因 |
|-------------|----------|---------|
| 沪深300(510300) | 偏多 | 原因说明... |

- 使用Markdown格式
- 逻辑清晰、数据驱动、不啰嗦
- 直接给出影响方向 + 原因 + 对应ETF代码/名称
- 适合当日ETF交易与配置参考

请开始分析：
"""

    try:
        # 调用LLM进行分析 - 使用stream
        response = llm.stream([{"role": "user", "content": full_prompt}])

        # 收集所有响应
        full_response = ""
        for chunk in response:
            if hasattr(chunk, 'content'):
                full_response += chunk.content
            else:
                full_response += str(chunk)

        print("✅ ETF影响分析完成")
        return full_response

    except Exception as e:
        print(f"❌ ETF影响分析失败: {e}")
        import traceback
        traceback.print_exc()
        # 返回简化版本
        return generate_fallback_analysis(market_data)


def generate_fallback_analysis(market_data, yesterday_prediction=None):
    """生成备用分析（当LLM调用失败时）"""
    date_str = datetime.now().strftime("%Y年%m月%d日")

    # 添加昨日预测部分
    yesterday_section = ""
    if yesterday_prediction:
        yesterday_date = yesterday_prediction.get('date', '昨天')
        yesterday_section = f"""

## 0. 昨日预测验证

**昨日日期：{yesterday_date}**

由于系统异常，暂时无法进行详细的预测验证分析。

"""

    return f"""# 📊 ETF投资分析报告

**日期：{date_str}**

## ⚠️ 分析说明

由于系统异常，今日无法生成完整的ETF影响分析。以下是基础市场数据：
{yesterday_section}
## 1. 今日关键国际事件
{market_data.get('international_events', '暂无数据')}

## 2. 大宗商品价格走势
{market_data.get('commodity_prices', '暂无数据')}

## 3. 全球金融动态
{market_data.get('financial_dynamics', '暂无数据')}

---
🤖 自动生成 | {datetime.now().strftime('%H:%M')}
"""


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

    # 邮件推送
    if "email" in enabled_channels and config.get("email", {}).get("enabled", False):
        recipients = config.get("email", {}).get("recipients", [])
        if recipients:
            total_count += 1
            try:
                email_config = config.get("email", {})
                result = _send_email_notification_impl(
                    subject=f"📊 ETF投资分析报告 - {datetime.now().strftime('%Y-%m-%d')}",
                    content=content,
                    to_addrs=recipients,
                    config_override=email_config
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
    print("\n" + "📊" * 40)
    print("ETF投资分析推送服务启动")
    print("📊" * 40)

    # 获取配置
    config = get_notification_config()

    print(f"\n📋 配置信息:")
    print(f"   - 启用渠道: {', '.join(config.get('enabled_channels', []))}")

    # 读取昨日预测
    print("\n📂 正在读取昨日预测...")
    yesterday_prediction = load_yesterday_prediction()
    if yesterday_prediction:
        yesterday_date = yesterday_prediction.get('date', '昨天')
        print(f"✅ 找到昨日预测 ({yesterday_date})，将进行验证分析")
    else:
        print("ℹ️  未找到昨日预测，本次分析将跳过验证环节")

    # 收集市场数据
    market_data = gather_market_data()

    # 分析ETF影响（传入昨日预测）
    analysis_report = analyze_etf_impact(market_data, yesterday_prediction)

    # 保存今日预测
    print("\n💾 正在保存今日预测...")
    try:
        prediction_summary = extract_prediction_summary(analysis_report)
        save_prediction(analysis_report, prediction_summary)
        print("✅ 今日预测已保存")
    except Exception as e:
        print(f"⚠️  保存预测失败: {e}")

    # 发送通知
    print("\n📤 开始推送分析报告...")
    success_count, total_count = send_notification(analysis_report, config)

    # 总结
    print("\n" + "📊" * 40)
    print("分析任务完成")
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
