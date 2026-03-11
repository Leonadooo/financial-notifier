#!/bin/bash
# 一键测试脚本 - 验证金融资讯推送系统是否正常

echo ""
echo "=========================================="
echo "🚀 金融资讯推送系统 - 一键测试"
echo "=========================================="
echo ""

# 检查Python是否安装
if ! command -v python &> /dev/null; then
    echo "❌ 错误：未找到Python"
    echo "请先安装Python 3.7或更高版本"
    exit 1
fi

echo "✅ Python已安装"
echo ""

# 检查必要的文件是否存在
echo "📋 检查必要文件..."

FILES=(
    "scripts/daily_notification.py"
    "config/notification_config.json"
    "src/agents/agent.py"
    "src/tools/financial_news_tool.py"
    "src/tools/notification_tool.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
        exit 1
    fi
done

echo ""
echo "🔍 检查依赖包..."

# 尝试导入必要的模块
python -c "import langchain" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ langchain"
else
    echo "  ❌ langchain (未安装)"
    echo "  运行: pip install langchain langchain-openai langgraph"
    exit 1
fi

python -c "import coze_coding_dev_sdk" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ coze_coding-dev-sdk"
else
    echo "  ⚠️  coze-coding-dev-sdk (可能未安装)"
    echo "  如遇问题，请安装: pip install coze-coding-dev-sdk"
fi

echo ""
echo "=========================================="
echo "📝 配置信息"
echo "=========================================="

# 读取配置文件
if [ -f "config/notification_config.json" ]; then
    echo "推送渠道:"
    grep -o '"enabled_channels":\s*\[.*\]' config/notification_config.json | head -1
    echo ""
    echo "内容类型:"
    grep -o '"content_types":\s*\[.*\]' config/notification_config.json | head -1
else
    echo "❌ 配置文件不存在"
    exit 1
fi

echo ""
echo "=========================================="
echo "🧪 开始测试"
echo "=========================================="
echo ""

# 运行推送脚本
python scripts/daily_notification.py

# 检查退出码
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 测试成功！系统运行正常"
    echo "=========================================="
    echo ""
    echo "下一步："
    echo "1. 配置推送渠道（企业微信/飞书/邮件）"
    echo "2. 设置定时任务（每天早上9点自动推送）"
    echo ""
    echo "详细文档请查看: docs/DEPLOYMENT_GUIDE.md"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ 测试失败，请检查错误信息"
    echo "=========================================="
    echo ""
    echo "查看完整文档: docs/DEPLOYMENT_GUIDE.md"
    echo "查看日志: tail -f logs/daily_notification.log"
    echo ""
    exit 1
fi
