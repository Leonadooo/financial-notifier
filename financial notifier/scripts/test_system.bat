@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo 🚀 金融资讯推送系统 - 一键测试
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未找到Python
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

REM 检查必要的文件是否存在
echo 📋 检查必要文件...

set "FILES=scripts\daily_notification.py config\notification_config.json src\agents\agent.py src\tools\financial_news_tool.py src\tools\notification_tool.py"

for %%f in (%FILES%) do (
    if exist "%%f" (
        echo   ✅ %%f
    ) else (
        echo   ❌ %%f ^(缺失^)
        pause
        exit /b 1
    )
)

echo.
echo 🔍 检查依赖包...

python -c "import langchain" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ langchain
) else (
    echo   ❌ langchain ^(未安装^)
    echo   运行: pip install langchain langchain-openai langgraph
    pause
    exit /b 1
)

python -c "import coze_coding_dev_sdk" 2>nul
if %errorlevel% equ 0 (
    echo   ✅ coze-coding-dev-sdk
) else (
    echo   ⚠️  coze-coding-dev-sdk ^(可能未安装^)
    echo   如遇问题，请安装: pip install coze-coding-dev-sdk
)

echo.
echo ==========================================
echo 📝 配置信息
echo ==========================================

if exist "config\notification_config.json" (
    echo 推送渠道:
    findstr /C:"enabled_channels" config\notification_config.json
    echo.
    echo 内容类型:
    findstr /C:"content_types" config\notification_config.json
) else (
    echo ❌ 配置文件不存在
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 🧪 开始测试
echo ==========================================
echo.

REM 运行推送脚本
python scripts\daily_notification.py

REM 检查退出码
if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo ✅ 测试成功！系统运行正常
    echo ==========================================
    echo.
    echo 下一步：
    echo 1. 配置推送渠道（企业微信/飞书/邮件）
    echo 2. 设置定时任务（每天早上9点自动推送）
    echo.
    echo 详细文档请查看: docs\DEPLOYMENT_GUIDE.md
    echo.
) else (
    echo.
    echo ==========================================
    echo ❌ 测试失败，请检查错误信息
    echo ==========================================
    echo.
    echo 查看完整文档: docs\DEPLOYMENT_GUIDE.md
    echo 查看日志: type logs\daily_notification.log
    echo.
)

pause
