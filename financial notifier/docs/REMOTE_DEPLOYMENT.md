# 远程部署指南 - 电脑关机也能收到推送

> 🎯 适用于：Windows电脑不一直开机，但仍想每天自动收到邮件推送

---

## 📋 方案对比

### 方案1：GitHub Actions（⭐⭐⭐⭐⭐ 最推荐）

**优点：**
- ✅ 完全免费
- ✅ 不需要购买服务器
- ✅ 操作最简单
- ✅ 稳定可靠
- ✅ 不需要Linux知识

**缺点：**
- 需要注册GitHub账号

**适合：** 所有人，特别是零技术背景用户

---

### 方案2：云服务器（⭐⭐⭐⭐）

**优点：**
- ✅ 稳定性最高
- ✅ 完全控制
- ✅ 可以做更多扩展

**缺点：**
- ❌ 需要购买（约30-100元/月）
- ❌ 需要一点Linux知识

**适合：** 对稳定性要求极高的用户

---

## 🚀 方案1：GitHub Actions（推荐）

### 步骤1：注册GitHub账号

1. 访问 https://github.com
2. 点击右上角 "Sign up"
3. 填写信息注册账号
4. 验证邮箱

### 步骤2：创建GitHub仓库

1. 登录GitHub后，点击右上角 "+" 号
2. 选择 "New repository"
3. **Repository name**: 输入 `financial-notifier`
4. **Description**: 输入 `金融资讯定时推送系统`
5. 选择 **Public**（公开仓库，免费使用GitHub Actions）
6. 点击 **"Create repository"**

### 步骤3：上传项目文件

**方法A：使用GitHub网页上传（最简单）**

1. 在新建的仓库页面，点击 **"uploading an existing file"**
2. 电脑上打开项目文件夹：`C:\workspace\projects`
3. 将以下文件拖拽到浏览器窗口：
   ```
   src/
   config/
   scripts/
   requirements.txt
   .github/
   ```
   **注意：** 需要保持文件夹结构

4. 填写提交信息：`Initial commit`
5. 点击 **"Commit changes"**

**方法B：使用Git命令（推荐，需要安装Git）**

在项目文件夹（`C:\workspace\projects`）打开命令行，执行：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/financial-notifier.git
git push -u origin main
```

### 步骤4：配置推送渠道

在GitHub网页上：

1. 进入你的仓库 `financial-notifier`
2. 点击 `config/notification_config.json` 文件
3. 点击右上角 **✏️ 铅笔图标**编辑
4. 修改为邮件推送：

```json
{
  "enabled_channels": ["email"],
  "wechat": {
    "enabled": false
  },
  "feishu": {
    "enabled": false
  },
  "email": {
    "enabled": true,
    "recipients": ["你的邮箱@example.com"]
  },
  "content_types": ["gold", "oil", "financial"]
}
```

5. 点击 **"Commit changes"**

### 步骤5：配置环境变量（重要！）

1. 在仓库页面，点击 **"Settings"** 标签
2. 左侧菜单找到 **"Secrets and variables"** → **"Actions"**
3. 点击 **"New repository secret"**

需要添加以下环境变量：

**如果不需要API密钥（使用默认配置）：**
可以跳过此步骤

**如果需要自定义API配置：**

添加以下变量：

1. **Name:** `COZE_API_KEY`
   **Value:** 你的API密钥（如果有的话）
   点击 **"Add secret"**

2. **Name:** `COZE_BASE_URL`
   **Value:** 你的API基础URL（如果有的话）
   点击 **"Add secret"**

### 步骤6：启用GitHub Actions

1. 点击 **"Actions"** 标签
2. 可能会提示启用Actions，点击 **"I understand my workflows, go ahead and enable them"**

### 步骤7：手动测试（验证配置）

1. 点击 **"Actions"** 标签
2. 左侧选择 **"金融资讯定时推送"** workflow
3. 点击 **"Run workflow"** 按钮
4. 点击绿色的 **"Run workflow"**

等待几分钟，查看运行结果：
- ✅ 绿色 ✓ 表示成功
- ❌ 红色 ✗ 表示失败

如果失败，点击任务查看日志。

### 步骤8：等待定时推送

GitHub Actions已经配置好，**每天北京时间早上9点**会自动运行。

你不需要电脑开机，GitHub的服务器会自动执行并发送邮件！

### 步骤9：查看日志

1. 点击 **"Actions"** 标签
2. 可以看到每天的历史运行记录
3. 点击任意一次运行查看详细日志

---

## 💰 方案2：云服务器部署

### 步骤1：购买云服务器

**推荐平台：**

1. **阿里云** - https://www.aliyun.com
2. **腾讯云** - https://cloud.tencent.com
3. **华为云** - https://www.huaweicloud.com

**推荐配置：**
- CPU: 1核
- 内存: 1GB
- 带宽: 1Mbps
- 系统: Ubuntu 20.04 或 22.04
- 价格: 约 30-60元/月

### 步骤2：购买并启动服务器

1. 注册账号并实名认证
2. 购买服务器（按上述配置）
3. 等待服务器启动（约5分钟）
4. 获取：
   - 公网IP地址（如：123.45.67.89）
   - 用户名（通常是：root）
   - 密码

### 步骤3：连接服务器

**使用SSH工具：**

推荐工具：
- **Windows:** PuTTY 或 Xshell
- **Mac/Linux:** 终端自带

**连接命令（Mac/Linux）：**
```bash
ssh root@你的公网IP
# 输入密码
```

**使用PuTTY（Windows）：**
1. 下载并安装 PuTTY
2. Host Name: 你的公网IP
3. Port: 22
4. 点击 Open
5. 输入用户名和密码

### 步骤4：安装Docker

连接服务器后执行：

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动Docker
sudo systemctl start docker
sudo systemctl enable docker

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 步骤5：上传项目文件

**方法A：使用SCP命令**

在你的Windows电脑上（在项目文件夹打开命令行）：

```bash
# 打包项目
tar -czf financial-notifier.tar.gz .

# 上传到服务器
scp financial-notifier.tar.gz root@你的公网IP:/root/

# 连接服务器
ssh root@你的公网IP

# 解压
cd /root
tar -xzf financial-notifier.tar.gz
mkdir -p financial-notifier
mv src config scripts requirements.txt Dockerfile docker-compose.yml .github financial-notifier/
cd financial-notifier
```

**方法B：使用SFTP工具（推荐）**

工具：FileZilla 或 WinSCP

1. 安装FileZilla
2. 连接信息：
   - 主机: 你的公网IP
   - 用户名: root
   - 密码: 你的密码
   - 端口: 22
3. 将项目文件夹整个拖拽上传到 `/root/financial-notifier/`

### 步骤6：配置推送渠道

```bash
cd /root/financial-notifier

# 编辑配置文件
nano config/notification_config.json
```

修改为：

```json
{
  "enabled_channels": ["email"],
  "email": {
    "enabled": true,
    "recipients": ["你的邮箱@example.com"]
  }
}
```

保存退出（Ctrl+O, 回车, Ctrl+X）

### 步骤7：创建环境变量文件

```bash
nano .env
```

如果不需要自定义API，可以留空或创建空文件：

```bash
touch .env
```

### 步骤8：启动服务

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 如果看到成功消息，按 Ctrl+C 退出
```

### 步骤9：手动测试

```bash
# 运行一次测试
docker-compose exec financial-notifier python scripts/daily_notification.py
```

检查你的邮箱，应该收到邮件了！

### 步骤10：查看定时任务

Docker服务已经自动配置了定时任务，每天9点运行。

查看日志：
```bash
docker-compose logs -f
```

查看定时任务：
```bash
docker-compose exec financial-notifier crontab -l
```

---

## 📊 两种方案对比

| 特性 | GitHub Actions | 云服务器 |
|------|---------------|---------|
| **费用** | 完全免费 | 30-60元/月 |
| **技术要求** | 非常简单 | 需要Linux基础 |
| **设置时间** | 10分钟 | 30-60分钟 |
| **稳定性** | 高 | 极高 |
| **可扩展性** | 一般 | 高 |
| **访问日志** | GitHub网页 | SSH登录查看 |

---

## 🎯 推荐选择

### 如果你：
- ✅ 想要免费
- ✅ 不想学习Linux
- ✅ 快速上手

**选择：GitHub Actions**

---

### 如果你：
- ✅ 对稳定性要求极高
- ✅ 想要完全控制
- ✅ 愿意学习一点Linux
- ✅ 不介意每月几十元费用

**选择：云服务器**

---

## ❓ 常见问题

### Q1: GitHub Actions的邮件总是发送失败怎么办？

**解决方案：**
1. 检查邮箱是否开启SMTP服务
2. 使用"授权码"而不是"登录密码"
3. 查看GitHub Actions日志，确认具体错误

### Q2: 云服务器太贵了怎么办？

**解决方案：**
1. 使用GitHub Actions（免费）
2. 购买更便宜的配置（1核1G即可）
3. 使用阿里云/腾讯云的免费试用活动

### Q3: 我可以同时使用两个方案吗？

**可以！** 但不建议，因为你会收到两份相同的邮件。

### Q4: 如何停止推送？

**GitHub Actions：**
1. 进入仓库 → Settings → Actions
2. 选择 "Disable all workflows"

**云服务器：**
```bash
docker-compose stop
docker-compose rm
```

---

## 📞 需要帮助？

### GitHub Actions问题：
- 查看Actions日志
- 检查配置文件格式
- 确认仓库是Public

### 云服务器问题：
- 检查Docker是否正常运行：`docker ps`
- 查看日志：`docker-compose logs`
- 重启服务：`docker-compose restart`

---

## 🎉 完成！

选择一个方案后，你将：
- ✅ 不需要电脑一直开机
- ✅ 每天早上9点自动收到金融资讯邮件
- ✅ 完全免费（GitHub Actions）或低成本（云服务器）

**祝使用愉快！** 🚀📧
