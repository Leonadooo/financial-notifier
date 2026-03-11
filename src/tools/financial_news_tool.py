"""
金融资讯生成工具
使用LLM生成国际金融形势、黄金、石油等大宗商品的最新资讯和分析
"""
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime


def _generate_financial_news_impl(query: str, max_items: int = 5) -> str:
    """
    生成金融相关资讯（使用 LLM）

    Args:
        query: 搜索关键词
        max_items: 最多返回的新闻条数（默认5条）

    Returns:
        生成的资讯摘要，包括标题、内容等关键信息
    """
    ctx = new_context(method="generate.news")

    try:
        client = LLMClient(ctx=ctx)
        
        current_date = datetime.now().strftime("%Y年%m月%d日")
        
        prompt = f"""请生成关于"{query}"的最新资讯和分析。

当前日期：{current_date}

要求：
1. 提供{max_items}条相关资讯
2. 每条资讯包含：标题、时间、事件描述、影响分析
3. 信息要准确、专业、具有参考价值
4. 关注最新的市场动态和政策变化
5. 格式清晰易读，使用列表形式

请以以下格式输出：
【AI生成资讯】
📊 生成时间：{current_date}

1. [资讯标题]
   📅 时间：[具体时间或近期]
   📝 内容：[事件描述]
   💡 影响：[影响分析]

2. [资讯标题]
   ...

【综合分析】
[对整体形势的总结分析]"""

        messages = [
            SystemMessage(content="你是一个专业的金融分析师，擅长分析国际金融市场动态、大宗商品价格走势和宏观经济政策。你的回答应该专业、准确、有深度。"),
            HumanMessage(content=prompt)
        ]
        
        response = client.invoke(messages=messages, temperature=0.7)
        
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
        
        return content.strip()
        
    except Exception as e:
        return f"生成金融资讯时出错：{str(e)}"


@tool
def search_financial_news(query: str, runtime: ToolRuntime = None) -> str:
    """
    生成金融相关资讯

    Args:
        query: 搜索关键词，如"国际金融形势"、"黄金价格走势"、"原油市场"等

    Returns:
        生成的资讯摘要，包括标题、内容等关键信息
    """
    return _generate_financial_news_impl(query)


@tool
def get_gold_price_analysis(runtime: ToolRuntime = None) -> str:
    """
    获取黄金价格走势及影响因素分析

    Returns:
        黄金价格最新资讯、走势分析和影响因素
    """
    return _generate_financial_news_impl("黄金价格走势 影响因素 市场动态")


@tool
def get_oil_price_analysis(runtime: ToolRuntime = None) -> str:
    """
    获取原油价格走势及影响因素分析

    Returns:
        原油价格最新资讯、走势分析和影响因素
    """
    return _generate_financial_news_impl("原油价格走势 国际石油市场 影响因素")


@tool
def get_international_financial_situation(runtime: ToolRuntime = None) -> str:
    """
    获取国际金融形势最新动态

    Returns:
        国际金融形势的综合资讯和分析
    """
    return _generate_financial_news_impl("国际金融形势 全球经济 最新动态")


# ===== 新增：ETF分析专用生成函数 =====

def _generate_market_data_impl(query: str, category: str) -> str:
    """
    生成市场数据（内部实现函数）

    Args:
        query: 生成关键词
        category: 数据类别（如"国际事件"、"大宗商品"等）

    Returns:
        生成的市场数据摘要
    """
    ctx = new_context(method="generate.market_data")

    try:
        client = LLMClient(ctx=ctx)
        
        current_date = datetime.now().strftime("%Y年%m月%d日")
        
        prompt = f"""请生成关于"{category}"的最新市场数据和分析。

查询内容：{query}
当前日期：{current_date}

要求：
1. 提供最新的市场数据
2. 分析当前市场趋势
3. 提供投资建议或参考
4. 信息要准确、专业
5. 格式清晰易读

请以结构化的方式输出。"""

        messages = [
            SystemMessage(content="你是一个专业的市场分析师，擅长分析各类金融市场的动态和趋势。"),
            HumanMessage(content=prompt)
        ]
        
        response = client.invoke(messages=messages, temperature=0.7)
        
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
        
        return content.strip()
        
    except Exception as e:
        return f"生成市场数据时出错：{str(e)}"


@tool
def get_international_events(runtime: ToolRuntime = None) -> str:
    """
    获取国际重大事件对市场的影响分析

    Returns:
        国际重大事件的最新动态及市场影响分析
    """
    return _generate_market_data_impl("国际重大事件", "国际事件")


@tool
def get_commodity_analysis(runtime: ToolRuntime = None) -> str:
    """
    获取大宗商品市场分析

    Returns:
        大宗商品（黄金、石油、白银等）的市场分析
    """
    return _generate_market_data_impl("大宗商品市场分析", "大宗商品")


@tool
def get_currency_market(runtime: ToolRuntime = None) -> str:
    """
    获取外汇市场动态

    Returns:
        外汇市场的最新动态和分析
    """
    return _generate_market_data_impl("外汇市场动态", "外汇市场")


@tool
def get_stock_market_overview(runtime: ToolRuntime = None) -> str:
    """
    获取股市概况

    Returns:
        全球股市的最新概况和分析
    """
    return _generate_market_data_impl("全球股市概况", "股市")


# ===== ETF分析专用函数 =====

def _get_international_events_impl() -> str:
    """
    获取国际事件（ETF分析专用）

    Returns:
        国际重大事件的最新动态及市场影响分析
    """
    return _generate_market_data_impl("国际重大事件", "国际事件")


def _get_commodity_prices_impl() -> str:
    """
    获取大宗商品价格（ETF分析专用）

    Returns:
        大宗商品（黄金、石油、白银等）的价格和市场分析
    """
    return _generate_market_data_impl("大宗商品价格走势", "大宗商品")


def _get_financial_dynamics_impl() -> str:
    """
    获取金融动态（ETF分析专用）

    Returns:
        全球金融市场的最新动态和分析
    """
    return _generate_market_data_impl("全球金融动态", "金融动态")
