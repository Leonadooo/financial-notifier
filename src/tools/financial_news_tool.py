"""
金融资讯搜索工具
用于获取国际金融形势、黄金、石油等大宗商品的最新资讯和分析
"""
from langchain.tools import tool, ToolRuntime
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from datetime import datetime, timedelta


def _is_today(publish_time_str: str) -> bool:
    """
    判断新闻是否是今日发布的

    Args:
        publish_time_str: 发布时间字符串

    Returns:
        True如果是今日发布，否则False
    """
    if not publish_time_str:
        return False

    try:
        today = datetime.now().date()
        current_time = datetime.now()

        # 尝试解析各种常见的时间格式
        time_formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
        ]

        for fmt in time_formats:
            try:
                # 只取前25个字符，避免时区信息影响
                time_str = publish_time_str[:25]
                pub_time = datetime.strptime(time_str, fmt)

                # 检查是否是今天
                if pub_time.date() == today:
                    return True

                # 如果是24小时内的新闻，也算"今日"
                if (current_time - pub_time).total_seconds() <= 24 * 3600:
                    return True

                return False
            except ValueError:
                continue

        # 如果包含"今天"、"今日"、"小时前"、"分钟前"等关键词
        keywords_today = ["今天", "今日", "Today", "hour ago", "hours ago", "minute ago", "minutes ago", "刚刚"]
        if any(keyword in publish_time_str.lower() for keyword in keywords_today):
            return True

        return False
    except Exception:
        return False


def _search_financial_news_impl(query: str, max_items: int = 5) -> str:
    """
    搜索金融相关资讯（内部实现函数）

    Args:
        query: 搜索关键词
        max_items: 最多返回的新闻条数（默认5条）

    Returns:
        搜索结果的摘要，包括标题、来源、链接等关键信息
    """
    ctx = new_context(method="search.financial_news")

    try:
        client = SearchClient(ctx=ctx)

        # 使用search方法，添加时间过滤（1天内的新闻）
        response = client.search(
            query=query,
            search_type="web",
            count=15,  # 搜索更多条以便筛选
            time_range="1d",  # 尝试只搜索最近1天的新闻
            need_summary=True
        )

        if not response.web_items:
            return f"暂未找到关于 '{query}' 的相关资讯"

        # 筛选今日或24小时内的新闻
        today_items = []
        recent_items = []

        for item in response.web_items:
            if _is_today(item.publish_time):
                today_items.append(item)
            else:
                recent_items.append(item)

        # 优先使用今日新闻
        if today_items:
            final_items = today_items[:max_items]
            time_note = "（今日新闻）"
        elif recent_items:
            final_items = recent_items[:max_items]
            time_note = "（最新新闻，暂无今日更新）"
        else:
            final_items = response.web_items[:max_items]
            time_note = ""

        if not final_items:
            return f"今日暂无关于 '{query}' 的相关资讯"

        result_parts = []

        # 添加AI摘要（如果有，并精简）
        if response.summary and len(response.summary) > 50:
            summary_lines = response.summary.split('\n')[:2]  # 只取前2行
            result_parts.append(f"【AI摘要】\n{' '.join(summary_lines)}\n")

        # 添加提示信息
        if "今日新闻" in time_note:
            result_parts.append(f"✅ 已为您筛选今日发布的最新新闻\n")
        elif "暂无今日更新" in time_note:
            result_parts.append(f"⚠️  今日暂无更新，为您展示最新新闻\n")

        # 添加搜索结果
        for idx, item in enumerate(final_items, 1):
            result_parts.append(f"{idx}. {item.title}\n")
            result_parts.append(f"   📅 {item.publish_time[:10] if item.publish_time else '时间未知'} | {item.site_name}\n")
            result_parts.append("")

        return "\n".join(result_parts).strip()

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


# ===== 新增：ETF分析专用搜索函数 =====

def _search_market_data_impl(query: str, category: str) -> str:
    """
    搜索市场数据（内部实现函数）

    Args:
        query: 搜索关键词
        category: 数据类别（如"国际事件"、"大宗商品"等）

    Returns:
        搜索结果的摘要
    """
    ctx = new_context(method="search.market_data")

    try:
        client = SearchClient(ctx=ctx)

        response = client.search(
            query=query,
            search_type="web",
            count=5,
            time_range="1d",
            need_summary=True
        )

        if not response.web_items:
            return f"暂无{category}数据"

        result_parts = [f"## {category}\n\n"]

        for idx, item in enumerate(response.web_items, 1):
            result_parts.append(f"{idx}. {item.title}\n")
            if item.publish_time:
                result_parts.append(f"   时间：{item.publish_time[:10]}\n")
            if item.snippet:
                result_parts.append(f"   {item.snippet[:100]}\n")
            result_parts.append("")

        return "\n".join(result_parts).strip()

    except Exception as e:
        return f"搜索{category}数据时出错：{str(e)}"


def _get_international_events_impl() -> str:
    """获取今日关键国际事件"""
    return _search_market_data_impl(
        "美联储 欧央行 政策 中美关系 地缘政治 今日",
        "今日关键国际事件"
    )


def _get_commodity_prices_impl() -> str:
    """获取大宗商品价格"""
    return _search_market_data_impl(
        "原油价格 黄金价格 铜价格 天然气价格 农产品价格 今日",
        "大宗商品价格走势"
    )


def _get_financial_dynamics_impl() -> str:
    """获取金融动态"""
    return _search_market_data_impl(
        "美元指数 美债收益率 北向资金 南向资金 今日",
        "全球金融动态"
    )


@tool
def get_international_events(runtime: ToolRuntime = None) -> str:
    """
    获取今日关键国际事件

    Returns:
        美联储/欧央行政策、地缘政治、中美关系、全球经济数据等
    """
    return _get_international_events_impl()


@tool
def get_commodity_prices(runtime: ToolRuntime = None) -> str:
    """
    获取大宗商品价格走势

    Returns:
        原油、黄金、铜、天然气、农产品等大宗商品涨跌及核心逻辑
    """
    return _get_commodity_prices_impl()


@tool
def get_financial_dynamics(runtime: ToolRuntime = None) -> str:
    """
    获取全球金融动态

    Returns:
        美元指数、美债收益率、北向/南向资金、全球风险偏好变化
    """
    return _get_financial_dynamics_impl()
