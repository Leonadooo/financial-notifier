#!/bin/bash

# ============================================
# 金融资讯定时推送系统 - 项目打包脚本
# ============================================
# 用途：打包项目文件，准备上传到GitHub
# 使用：./scripts/package_for_github.sh
# ============================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACKAGE_NAME="financial-notifier-github"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${PACKAGE_NAME}_${TIMESTAMP}.tar.gz"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}金融资讯定时推送系统 - 项目打包${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 进入项目根目录
cd "$PROJECT_ROOT"

# 检查必要文件
echo -e "${YELLOW}检查必要文件...${NC}"
REQUIRED_FILES=(
    ".github/workflows/daily-notification.yml"
    "config/agent_llm_config.json"
    "config/notification_config.json"
    "scripts/daily_notification.py"
    "scripts/etf_analysis.py"
    "requirements.txt"
    "README.md"
    ".gitignore"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ 缺少文件: $file${NC}"
        exit 1
    else
        echo -e "${GREEN}✓${NC} $file"
    fi
done

echo ""
echo -e "${YELLOW}开始打包...${NC}"
echo ""

# 打包项目（排除不必要的文件）
tar -czf "$OUTPUT_FILE" \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.pyo' \
    --exclude='*.pyd' \
    --exclude='*.log' \
    --exclude='*.tmp' \
    --exclude='*.temp' \
    --exclude='.git' \
    --exclude='.git/*' \
    --exclude='assets/predictions' \
    --exclude='assets/predictions/*' \
    --exclude='logs' \
    --exclude='logs/*' \
    --exclude='*.zip' \
    --exclude='*.tar.gz' \
    --exclude='*.gz' \
    --exclude='*.rar' \
    --exclude='*.iso' \
    --exclude='*.dmg' \
    --exclude='node_modules' \
    --exclude='.DS_Store' \
    --exclude='Thumbs.db' \
    --exclude='.env' \
    --exclude='.env.local' \
    --exclude='.venv' \
    --exclude='venv' \
    --exclude='ENV' \
    --exclude='env' \
    --exclude='dist' \
    --exclude='build' \
    --exclude='*.egg-info' \
    --exclude='.pytest_cache' \
    --exclude='htmlcov' \
    --exclude='.coverage' \
    --exclude='*.db' \
    --exclude='*.sqlite' \
    --exclude='*.sqlite3' \
    --exclude='.idea' \
    --exclude='.vscode' \
    --exclude='*.swp' \
    --exclude='*.swo' \
    --exclude='*~' \
    --exclude='*.pdf' \
    --exclude='*.docx' \
    --exclude='*.doc' \
    --exclude='*.xlsx' \
    --exclude='*.xls' \
    --exclude='*.ppt' \
    --exclude='*.pptx' \
    --exclude='*.mp4' \
    --exclude='*.avi' \
    --exclude='*.mov' \
    --exclude='*.wmv' \
    --exclude='*.flv' \
    --exclude='*.mkv' \
    --exclude='*.webm' \
    --exclude='*.m4v' \
    --exclude='*.mpeg' \
    --exclude='*.mpg' \
    --exclude='*.3gp' \
    --exclude='*.f4v' \
    --exclude='*.rmvb' \
    --exclude='*.vob' \
    --exclude='*.o' \
    --exclude='*.a' \
    --exclude='vendor' \
    .

# 检查打包是否成功
if [ -f "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}打包成功！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "文件名: ${GREEN}$OUTPUT_FILE${NC}"
    echo -e "大小:   ${GREEN}$FILE_SIZE${NC}"
    echo -e "位置:   ${GREEN}$(pwd)/$OUTPUT_FILE${NC}"
    echo ""
    echo -e "${YELLOW}下一步操作：${NC}"
    echo -e "1. 解压文件到新目录："
    echo -e "   ${GREEN}tar -xzf $OUTPUT_FILE${NC}"
    echo ""
    echo -e "2. 初始化Git仓库："
    echo -e "   ${GREEN}cd <解压后的目录>${NC}"
    echo -e "   ${GREEN}git init${NC}"
    echo ""
    echo -e "3. 添加文件并提交："
    echo -e "   ${GREEN}git add .${NC}"
    echo -e "   ${GREEN}git commit -m '初始提交'${NC}"
    echo ""
    echo -e "4. 关联GitHub仓库并推送："
    echo -e "   ${GREEN}git remote add origin <你的GitHub仓库地址>${NC}"
    echo -e "   ${GREEN}git branch -M main${NC}"
    echo -e "   ${GREEN}git push -u origin main${NC}"
    echo ""
    echo -e "详细部署指南请查看: ${GREEN}docs/GITHUB_DEPLOYMENT.md${NC}"
    echo ""
else
    echo -e "${RED}打包失败！${NC}"
    exit 1
fi
