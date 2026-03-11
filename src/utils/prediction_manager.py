"""
ETF预测管理模块
用于保存和读取每日的ETF预测，支持验证昨日预测的准确性
"""
import json
import os
from datetime import datetime, timedelta


def get_prediction_file_path(date):
    """
    获取指定日期的预测文件路径

    Args:
        date: 日期对象或日期字符串（YYYY-MM-DD）

    Returns:
        文件路径
    """
    if isinstance(date, datetime):
        date_str = date.strftime('%Y-%m-%d')
    else:
        date_str = date

    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    predictions_dir = os.path.join(workspace_path, "assets", "predictions")

    # 确保目录存在
    os.makedirs(predictions_dir, exist_ok=True)

    return os.path.join(predictions_dir, f"etf_prediction_{date_str}.json")


def save_prediction(content: str, prediction_summary: dict = None):
    """
    保存当日的ETF预测

    Args:
        content: 完整的分析报告内容
        prediction_summary: 预测摘要（包含关键预测点）

    Returns:
        保存的文件路径
    """
    today = datetime.now()
    file_path = get_prediction_file_path(today)

    prediction_data = {
        "date": today.strftime('%Y-%m-%d'),
        "datetime": today.strftime('%Y-%m-%d %H:%M:%S'),
        "content": content,
        "summary": prediction_summary or {}
    }

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(prediction_data, f, ensure_ascii=False, indent=2)
        return file_path
    except Exception as e:
        print(f"❌ 保存预测失败: {e}")
        return None


def load_yesterday_prediction():
    """
    读取昨日的ETF预测

    Returns:
        预测数据字典，如果不存在则返回None
    """
    yesterday = datetime.now() - timedelta(days=1)
    file_path = get_prediction_file_path(yesterday)

    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ 读取昨日预测失败: {e}")
        return None


def extract_prediction_summary(content: str) -> dict:
    """
    从分析报告中提取预测摘要

    Args:
        content: 分析报告内容

    Returns:
        预测摘要字典
    """
    summary = {}

    # 提取关键信息（简化版）
    lines = content.split('\n')

    for i, line in enumerate(lines):
        # 提取大宗商品预测
        if '原油' in line and '涨' in line:
            summary['oil_trend'] = '看涨'
        elif '原油' in line and '跌' in line:
            summary['oil_trend'] = '看跌'

        # 提取黄金预测
        if '黄金' in line and '涨' in line:
            summary['gold_trend'] = '看涨'
        elif '黄金' in line and '跌' in line:
            summary['gold_trend'] = '看跌'

        # 提取关键ETF预测
        if '沪深300' in line and '偏多' in line:
            summary['hs300_trend'] = '偏多'
        elif '沪深300' in line and '偏空' in line:
            summary['hs300_trend'] = '偏空'

        if '油气(512200)' in line and '偏多' in line:
            summary['oil_etf_trend'] = '偏多'

    return summary


def list_recent_predictions(days: int = 7):
    """
    列出最近几天的预测文件

    Args:
        days: 列出最近多少天的预测

    Returns:
        预测文件列表
    """
    predictions_dir = os.path.join(
        os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"),
        "assets",
        "predictions"
    )

    if not os.path.exists(predictions_dir):
        return []

    files = []
    for filename in os.listdir(predictions_dir):
        if filename.startswith('etf_prediction_') and filename.endswith('.json'):
            file_path = os.path.join(predictions_dir, filename)
            files.append({
                "filename": filename,
                "path": file_path,
                "date": filename.replace('etf_prediction_', '').replace('.json', '')
            })

    # 按日期排序，最新的在前
    files.sort(key=lambda x: x['date'], reverse=True)

    return files[:days]
