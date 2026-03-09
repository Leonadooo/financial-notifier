"""
金融资讯搜索工具
用于获取国际金融形势、黄金、石油等大宗商品的最新资讯和分析
"""
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context


def _search_financial_news_impl(query: str) -> str:
    """
    搜索金融相关资讯（内部实现函数）

    Args:
        query: 搜索关键词

    Returns:
        搜索结果的摘要，包括标题、来源、链接等关键信息
    """
    ctx = new_context(method="search.financial_news")

    try:
        client = SearchClient(ctx=ctx)

        # 使用带AI摘要的搜索
        response = client.web_search_with_summary(
            query=query,
            count=10
        )

        if not response.web_items:
            return f"未找到关于 '{query}' 的相关资讯"

        result_parts = []

        # 添加AI摘要（如果有）
        if response.summary:
            result_parts.append(f"【AI摘要】\n{response.summary}\n")

        # 添加搜索结果
        result_parts.append(f"【关于 '{query}' 的最新资讯】\n")
        result_parts.append("=" * 60 + "\n")

        for idx, item in enumerate(response.web_items, 1):
            result_parts.append(f"{idx}. {item.title}\n")
            result_parts.append(f"   来源：{item.site_name}\n")
            if item.publish_time:
                result_parts.append(f"   发布时间：{item.publish_time}\n")
            result_parts.append(f"   摘要：{item.snippet}\n")
            result_parts.append(f"   链接：{item.url}\n")
            if item.summary:
                result_parts.append(f"   AI解读：{item.summary}\n")
            result_parts.append("-" * 60 + "\n")

        return "\n".join(result_parts)

    except Exception as e:
        return f"搜索金融资讯时出错：{str(e)}"


@tool
def search_financial_news(query: str, runtime: ToolRuntime = None) -> str:
    """
    搜索金融相关资讯

    Args:
        query: 搜索关键词，如"国际金融形势"、"黄金价格走势"、"原油市场"等

    Returns:
        搜索结果的摘要，包括标题、来源、链接等关键信息
    """
    return _search_financial_news_impl(query)


@tool
def get_gold_price_analysis(runtime: ToolRuntime = None) -> str:
    """
    获取黄金价格走势及影响因素分析

    Returns:
        黄金价格最新资讯、走势分析和影响因素
    """
    return _search_financial_news_impl("黄金价格走势 影响因素 2024")


@tool
def get_oil_price_analysis(runtime: ToolRuntime = None) -> str:
    """
    获取原油价格走势及影响因素分析

    Returns:
        原油价格最新资讯、走势分析和影响因素
    """
    return _search_financial_news_impl("原油价格走势 国际石油市场 影响因素 2024")


@tool
def get_international_financial_situation(runtime: ToolRuntime = None) -> str:
    """
    获取国际金融形势最新动态

    Returns:
        国际金融形势的综合资讯和分析
    """
    return _search_financial_news_impl("国际金融形势 全球经济 最新动态")
