# GitHub 部署指南

> 🚀 将金融资讯定时推送系统部署到GitHub，实现完全免费、无需电脑开机的定时推送

---

## 📋 前置要求

1. **GitHub账号**：如果没有，请先注册 [GitHub](https://github.com)
2. **Git客户端**：电脑上需要安装Git（[下载地址](https://git-scm.com/downloads)）
3. **Python环境**：本地测试时需要Python 3.12（可选）

---

## 🎯 部署步骤（10分钟完成）

### 第1步：准备项目文件

#### 方案A：直接使用本项目文件（推荐）

1. **下载项目文件**：
   - 确保您有完整的项目文件
   - 项目应包含以下关键文件：
     ```
     金融资讯定时推送系统/
     ├── .github/
     │   └── workflows/
     │       └── daily-notification.yml
     ├── config/
     │   ├── agent_llm_config.json
     │   └── notification_config.json
     ├── scripts/
     │   ├── daily_notification.py
     │   └── etf_analysis.py
     ├── src/
     │   ├── agents/
     │   ├── tools/
     │   ├── storage/
     │   └── utils/
     ├── docs/
     ├── requirements.txt
     ├── README.md
     └── .gitignore
     ```

2. **检查关键文件是否存在**：
   ```bash
   # 检查是否有GitHub Actions配置
   ls -la .github/workflows/daily-notification.yml

   # 检查是否有配置文件
   ls -la config/

   # 检查是否有脚本文件
   ls -la scripts/
   ```

#### 方案B：打包项目（适用于需要分享的情况）

在项目根目录运行：
```bash
# 创建部署包（排除临时文件）
tar -czf financial-notifier-deploy.tar.gz \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.log' \
  --exclude='.git' \
  --exclude='assets/predictions' \
  --exclude='logs' \
  --exclude='*.zip' \
  --exclude='*.tar.gz' \
  --exclude='node_modules' \
  --exclude='.DS_Store' \
  .
```

---

### 第2步：在GitHub上创建仓库

1. **登录GitHub**：访问 [GitHub](https://github.com) 并登录

2. **创建新仓库**：
   - 点击右上角的 `+` 按钮
   - 选择 `New repository`
   - 填写仓库信息：
     - **Repository name**：`financial-notifier`（或您喜欢的名称）
     - **Description**：`金融资讯定时推送系统 - 每天早上9点自动推送ETF投资分析报告`
     - **Public/Private**：建议选择 **Private**（私有）
   - 勾选 `Add a README file`（可选）
   - 点击 `Create repository`

3. **记录仓库地址**：
   - 创建后会显示仓库地址，格式如：
     ```
     https://github.com/你的用户名/financial-notifier.git
     ```

---

### 第3步：上传项目到GitHub

#### 方法A：使用Git命令行（推荐）

1. **打开终端/命令提示符**：
   - Windows：按 `Win + R`，输入 `cmd`，回车
   - Mac/Linux：打开 `Terminal`

2. **进入项目目录**：
   ```bash
   cd /path/to/your/project
   ```

3. **初始化Git仓库**：
   ```bash
   git init
   ```

4. **添加所有文件到暂存区**：
   ```bash
   git add .
   ```

5. **查看将要上传的文件**（可选）：
   ```bash
   git status
   ```
   - 确认没有上传敏感文件（如 `.env`）

6. **提交更改**：
   ```bash
   git commit -m "初始提交：金融资讯定时推送系统"
   ```

7. **关联远程仓库**：
   ```bash
   git remote add origin https://github.com/你的用户名/financial-notifier.git
   ```

8. **推送到GitHub**：
   ```bash
   git branch -M main
   git push -u origin main
   ```

9. **输入GitHub凭据**（如果需要）：
   - 用户名：GitHub用户名
   - 密码：使用 **Personal Access Token**（不是登录密码）
     - 获取Token：[GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
     - 选择权限：`repo`（完整仓库访问权限）

#### 方法B：使用GitHub网页上传（适合小型项目）

1. **在仓库页面点击**：
   - 点击 `uploading an existing file` 链接

2. **拖拽文件**：
   - 将项目文件拖拽到上传区域
   - 或点击 `choose your files` 选择文件

3. **填写提交信息**：
   - Commit message：`初始提交：金融资讯定时推送系统`

4. **点击**：
   - `Commit changes`

---

### 第4步：配置GitHub Secrets

#### 4.1 获取API密钥

**方法A：如果使用Coze集成**
- API Key：联系Coze平台获取
- Base URL：`https://integration.coze.cn/api/v3/chat/completions`

**方法B：如果使用OpenAI**
- API Key：[OpenAI API Keys](https://platform.openai.com/api-keys)
- Base URL：`https://api.openai.com/v1`

#### 4.2 在GitHub中配置Secrets

1. **打开仓库设置**：
   - 进入您的GitHub仓库
   - 点击 `Settings` 标签页

2. **进入Secrets设置**：
   - 左侧菜单中，找到 `Secrets and variables`
   - 点击 `Actions`

3. **点击**：
   - `New repository secret`

4. **添加以下Secrets**：

   **Secret 1：COZE_API_KEY**
   - Name: `COZE_API_KEY`
   - Value: `你的API密钥`
   - 点击 `Add secret`

   **Secret 2：COZE_BASE_URL**
   - Name: `COZE_BASE_URL`
   - Value: `https://integration.coze.cn/api/v3/chat/completions`
   - 点击 `Add secret`

#### 4.3 验证Secrets配置

确保配置了以下Secrets：
- ✅ `COZE_API_KEY`：API密钥
- ✅ `COZE_BASE_URL`：API基础URL

---

### 第5步：配置推送邮箱（可选）

如果您需要邮件推送，需要修改 `config/notification_config.json`：

1. **在GitHub仓库中打开**：
   - `config/notification_config.json`

2. **点击编辑按钮**：
   - 铅笔图标 ✏️

3. **修改邮箱配置**：
   ```json
   {
     "enabled_channels": ["email"],
     "email": {
       "enabled": true,
       "recipients": ["your_email@qq.com"],
       "smtp_server": "smtp.qq.com",
       "smtp_port": 465,
       "account": "your_email@qq.com",
       "auth_code": "your_auth_code"
     }
   }
   ```

4. **填写您的邮箱信息**：
   - `recipients`：接收邮件的邮箱地址
   - `account`：发送邮件的邮箱地址
   - `auth_code`：邮箱授权码（不是登录密码）
     - QQ邮箱获取：[QQ邮箱SMTP开启指南.md](QQ邮箱SMTP开启指南.md)

5. **提交更改**：
   - Commit message: `配置邮件推送`
   - 点击 `Commit changes`

⚠️ **注意**：邮箱信息会明文显示在仓库中，如果是私有仓库则相对安全。如果是公开仓库，建议使用GitHub Secrets存储邮箱信息。

---

### 第6步：测试GitHub Actions

#### 6.1 手动触发推送

1. **进入Actions页面**：
   - 在仓库页面点击 `Actions` 标签页

2. **选择工作流**：
   - 找到 `金融资讯定时推送` 工作流
   - 点击右侧的 `Run workflow` 按钮

3. **确认运行**：
   - 点击 `Run workflow` 绿色按钮

#### 6.2 查看运行日志

1. **等待执行**：
   - 工作流会自动开始运行
   - 预计需要1-3分钟完成

2. **查看详情**：
   - 点击运行中的工作流查看日志

3. **检查结果**：
   - ✅ 绿色对勾：成功
   - ❌ 红色叉：失败（查看日志排查错误）

#### 6.3 查看邮件推送

如果配置了邮件推送，检查邮箱是否收到测试邮件。

---

### 第7步：配置定时推送

#### 7.1 查看当前定时配置

1. **打开工作流文件**：
   - 在仓库中打开 `.github/workflows/daily-notification.yml`

2. **查看定时配置**：
   ```yaml
   on:
     schedule:
       - cron: '0 9 * * *'
   ```

#### 7.2 修改推送时间

Cron表达式格式：`分 时 日 月 周`

**常见推送时间配置**：
- `0 9 * * *`：每天早上9点（推荐）
- `0 8 * * *`：每天早上8点
- `0 20 * * *`：每天晚上8点
- `0 */6 * * *`：每6小时推送一次

**示例**：改为每天早上8点半
```yaml
schedule:
  - cron: '30 8 * * *'
```

#### 7.3 提交更改

1. 修改后点击 `Commit changes`
2. 工作流会自动更新

---

## 🔍 常见问题排查

### Q1: 工作流运行失败，提示 "No such file or directory"

**原因**：文件路径错误或文件未上传

**解决方法**：
1. 检查仓库中是否有所有必要文件
2. 查看Actions日志，确认哪个文件缺失
3. 补充缺失的文件后重新提交

### Q2: 提示 "COZE_API_KEY not found"

**原因**：未配置GitHub Secrets

**解决方法**：
1. 按照"第4步"配置GitHub Secrets
2. 确保Secret名称正确：`COZE_API_KEY`、`COZE_BASE_URL`

### Q3: 邮件发送失败

**原因**：邮箱配置错误

**解决方法**：
1. 检查 `config/notification_config.json` 配置
2. 确认授权码正确（不是登录密码）
3. 检查SMTP服务器和端口是否正确
4. 查看Actions日志中的错误信息

### Q4: 推送时间不正确

**原因**：时区问题

**解决方法**：
- GitHub Actions使用UTC时间
- 中国时区（UTC+8）需要减8小时
  - 北京时间9点 → UTC时间1点 → `0 1 * * *`

### Q5: 如何查看历史推送记录？

**方法1：查看Actions日志**
1. 进入 `Actions` 页面
2. 查看历史运行记录
3. 点击具体运行查看日志

**方法2：查看上传的日志文件**
1. Actions会自动上传日志文件
2. 在运行记录中下载日志文件

---

## 📊 项目文件清单

### 必须上传的文件

```
金融资讯定时推送系统/
├── .github/
│   └── workflows/
│       └── daily-notification.yml          # GitHub Actions配置 ✅
├── config/
│   ├── agent_llm_config.json              # LLM配置 ✅
│   └── notification_config.json           # 推送配置 ✅
├── scripts/
│   ├── daily_notification.py              # 每日推送脚本 ✅
│   └── etf_analysis.py                    # ETF分析脚本 ✅
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agent.py                       # Agent核心 ✅
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── financial_news_tool.py         # 金融资讯工具 ✅
│   │   └── notification_tool.py           # 推送工具 ✅
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   └── memory_saver.py            # 记忆存储 ✅
│   │   ├── s3/
│   │   │   ├── __init__.py
│   │   │   └── s3_storage.py              # S3存储 ✅
│   │   └── database/
│   │       ├── __init__.py
│   │       └── db.py                      # 数据库 ✅
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── prediction_manager.py          # 预测管理 ✅
│   │   └── file/
│   │       ├── __init__.py
│   │       └── file.py                    # 文件工具 ✅
│   ├── main.py                            # 主入口 ✅
│   └── __init__.py
├── docs/
│   ├── GITHUB_ACTIONS_TUTORIAL.md         # GitHub教程 ✅
│   ├── QUICK_START.md                     # 快速开始 ✅
│   ├── DEPLOYMENT_GUIDE.md                # 部署指南 ✅
│   ├── REMOTE_DEPLOYMENT.md               # 远程部署 ✅
│   └── INSTALLATION_SUMMARY.md            # 部署总结 ✅
├── requirements.txt                       # Python依赖 ✅
├── README.md                              # 项目说明 ✅
├── QQ邮箱SMTP开启指南.md                  # 邮箱配置指南 ✅
├── DOCS.md                                # 文档导航 ✅
└── .gitignore                             # Git忽略文件 ✅
```

### 不需要上传的文件（已被.gitignore排除）

```
❌ __pycache__/          # Python缓存
❌ *.pyc                 # 编译文件
❌ .env                  # 环境变量
❌ logs/                 # 日志文件
❌ assets/predictions/   # 预测数据
❌ *.log                 # 日志文件
❌ .DS_Store             # Mac系统文件
❌ *.zip                 # 压缩包
❌ *.tar.gz              # 压缩包
```

---

## 🎉 部署完成检查清单

- [ ] 已在GitHub上创建仓库
- [ ] 已上传所有必要文件
- [ ] 已配置 `COZE_API_KEY` Secret
- [ ] 已配置 `COZE_BASE_URL` Secret
- [ ] 已配置推送邮箱（如需要）
- [ ] 已手动触发测试推送
- [ ] 已收到测试邮件
- [ ] 已确认定时推送时间正确

---

## 📞 需要帮助？

- **查看详细教程**：[docs/GITHUB_ACTIONS_TUTORIAL.md](docs/GITHUB_ACTIONS_TUTORIAL.md)
- **查看日志**：在GitHub仓库的 `Actions` 页面查看
- **提交问题**：在GitHub仓库提交Issue

---

**祝您部署成功！🎊**

**预计时间**：10分钟
**难度**：⭐⭐（简单）
**费用**：完全免费
