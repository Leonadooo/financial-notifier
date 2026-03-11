# 金融资讯定时推送系统 - 零基础部署指南

> 🎯 本指南专为零技术背景用户编写，按照步骤操作即可完成部署

---

## 📋 目录

1. [快速开始（5分钟版）](#快速开始5分钟版)
2. [完整部署流程](#完整部署流程)
3. [配置推送渠道](#配置推送渠道)
4. [设置定时任务](#设置定时任务)
5. [常见问题解答](#常见问题解答)

---

## 🚀 快速开始（5分钟版）

### 第一步：测试运行（验证系统是否正常）

在命令行中执行以下命令：

```bash
python scripts/daily_notification.py
```

**预期结果：**
- 你会看到系统正在获取金融资讯
- 资讯内容会显示在屏幕上
- 最后显示"✅ 所有推送渠道成功！"

**如果看到这个结果，恭喜你！系统已经可以正常工作了！** 🎉

---

## 📖 完整部署流程

### 阶段一：理解系统架构

```
┌─────────────────┐
│  每天9点        │
│  自动触发       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  收集金融资讯   │  ← 获取黄金、石油、国际金融资讯
│  (联网搜索)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  整理分析报告   │  ← 生成结构化的资讯报告
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  推送到你的设备 │  ← 企业微信/飞书/邮件
└─────────────────┘
```

### 阶段二：手动测试

**目的：** 确保系统能正常获取资讯

#### 步骤1：打开命令行

- **Windows：** 按 `Win + R`，输入 `cmd`，按回车
- **Mac：** 打开"终端"应用
- **Linux：** 打开"终端"

#### 步骤2：进入项目目录

```bash
cd /workspace/projects
```

#### 步骤3：运行测试脚本

```bash
python scripts/daily_notification.py
```

#### 步骤4：查看结果

如果一切正常，你会看到类似这样的输出：

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
金融资讯定时推送服务启动
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

📋 配置信息:
   - 启用渠道: console
   - 内容类型: gold, oil, financial

开始收集金融资讯 - 2025-01-15 09:00:00
============================================================

📊 正在获取黄金价格分析...
✅ 黄金价格分析获取成功

📊 正在获取原油价格分析...
✅ 原油价格分析获取成功

📊 正在获取国际金融形势...
✅ 国际金融形势获取成功

📤 开始推送消息...

✅ 所有推送渠道成功！
```

**如果看到错误，请查看[常见问题解答](#常见问题解答)**

---

## ⚙️ 配置推送渠道

### 说明

系统支持3种推送方式，你可以选择其中一种或多种：

1. **企业微信机器人**（推荐⭐⭐⭐⭐⭐）
   - 需要配置企业微信webhook
   - 适合企业内部使用

2. **飞书机器人**（推荐⭐⭐⭐⭐⭐）
   - 需要配置飞书webhook
   - 适合团队协作

3. **邮件**（推荐⭐⭐⭐⭐）
   - 需要配置SMTP邮箱
   - 适合个人使用

### 配置方法

#### 方法1：修改配置文件（推荐）

**步骤1：** 打开配置文件
```bash
# Windows
notepad config/notification_config.json

# Mac/Linux
nano config/notification_config.json
```

**步骤2：** 修改配置

文件内容如下：

```json
{
  "enabled_channels": ["console"],
  "wechat": {
    "enabled": false
  },
  "feishu": {
    "enabled": false
  },
  "email": {
    "enabled": false,
    "recipients": ["your_email@example.com"]
  },
  "content_types": ["gold", "oil", "financial"]
}
```

**如何修改：**

**场景1：只想在屏幕上看（默认）**
```json
{
  "enabled_channels": ["console"]
}
```

**场景2：通过企业微信推送**
```json
{
  "enabled_channels": ["wechat"],
  "wechat": {
    "enabled": true
  }
}
```

**场景3：通过飞书推送**
```json
{
  "enabled_channels": ["feishu"],
  "feishu": {
    "enabled": true
  }
}
```

**场景4：通过邮件推送**
```json
{
  "enabled_channels": ["email"],
  "email": {
    "enabled": true,
    "recipients": ["your_email@163.com", "other_email@qq.com"]
  }
}
```

**场景5：多渠道同时推送**
```json
{
  "enabled_channels": ["console", "wechat", "email"],
  "wechat": {
    "enabled": true
  },
  "email": {
    "enabled": true,
    "recipients": ["your_email@example.com"]
  }
}
```

**步骤3：** 保存文件并测试
```bash
python scripts/daily_notification.py
```

---

## ⏰ 设置定时任务

### 说明

要让系统每天早上9点自动推送，需要设置"定时任务"。

**重要：** 这一步是系统自动运行的最后一步！

---

### 方案1：Linux/Mac 系统（最简单）

**步骤1：** 编辑定时任务
```bash
crontab -e
```

**步骤2：** 在文件末尾添加以下内容

```bash
# 每天早上9点执行
0 9 * * * cd /workspace/projects && python scripts/daily_notification.py >> logs/daily_notification.log 2>&1

# 可选：同时备份日志
0 9 * * * cd /workspace/projects && python scripts/daily_notification.py >> logs/daily_notification_$(date +\%Y\%m\%d).log 2>&1
```

**步骤3：** 保存并退出
- 按 `Ctrl + O`，然后按回车（保存）
- 按 `Ctrl + X`（退出）

**步骤4：** 验证定时任务
```bash
crontab -l
```

你应该能看到刚才添加的定时任务。

---

### 方案2：Windows 系统

**步骤1：** 创建批处理文件

在项目目录下创建文件 `run_daily_notification.bat`，内容如下：

```batch
@echo off
cd /d C:\workspace\projects
python scripts/daily_notification.py >> logs\daily_notification.log 2>&1
```

**步骤2：** 打开任务计划程序

- 按 `Win + R`
- 输入 `taskschd.msc`
- 按回车

**步骤3：** 创建基本任务

1. 点击右侧的"创建基本任务"
2. **名称**：输入"金融资讯推送"
3. **触发器**：选择"每天"
4. **开始时间**：设置为 09:00:00
5. **操作**：选择"启动程序"
6. **程序/脚本**：浏览选择刚才创建的 `run_daily_notification.bat` 文件
7. 点击"完成"

**步骤4：** 测试定时任务

在任务计划程序中，右键点击刚才创建的任务，选择"运行"。

---

### 方案3：Docker 系统（如果你在使用Docker）

**步骤1：** 创建Docker定时任务配置

在项目目录下创建文件 `docker-crontab`，内容如下：

```cron
# 每天早上9点执行
0 9 * * * root cd /workspace/projects && python scripts/daily_notification.py >> /workspace/projects/logs/daily_notification.log 2>&1
```

**步骤2：** 修改Docker配置（需要Docker技术，建议咨询技术人员）

**注意：** 如果不熟悉Docker，建议使用方案1或方案2

---

### 方案4：Python定时任务（最灵活）

如果不想配置系统定时任务，可以使用Python的定时任务库。

**步骤1：** 安装依赖
```bash
pip install schedule
```

**步骤2：** 创建定时任务脚本

在 `scripts/` 目录下创建文件 `scheduler.py`，内容如下：

```python
#!/usr/bin/env python3
import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

def run_daily_notification():
    """运行每日推送"""
    print(f"\n{'='*60}")
    print(f"定时任务触发 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        subprocess.run([sys.executable, "scripts/daily_notification.py"], check=True)
        print("\n✅ 定时任务执行成功")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 定时任务执行失败: {e}")

# 每天早上9点执行
schedule.every().day.at("09:00").do(run_daily_notification)

print("🕐 定时任务服务已启动，等待每天09:00执行...")
print("按 Ctrl+C 停止服务\n")

while True:
    schedule.run_pending()
    time.sleep(60)  # 每分钟检查一次
```

**步骤3：** 运行定时任务服务

```bash
python scripts/scheduler.py
```

**注意：** 这个方法需要保持命令行窗口一直打开，关闭窗口后定时任务会停止。

**推荐：** 将这个服务设置为后台运行（需要技术人员协助）

---

## ❓ 常见问题解答

### Q1: 运行时报错 "No module named xxx"

**解决方案：**

```bash
pip install -r requirements.txt
```

如果还有问题，尝试：

```bash
pip install coze-coding-dev-sdk langchain langchain-openai langgraph requests
```

---

### Q2: 企业微信推送失败

**可能原因：**
1. 未配置企业微信webhook
2. webhook URL不正确
3. 企业微信机器人被禁用

**解决方案：**

1. 确认已配置企业微信机器人
2. 检查webhook URL是否正确
3. 在企业微信群中测试机器人是否正常

**如何获取企业微信webhook：**

1. 打开企业微信群
2. 群设置 → 群机器人 → 添加机器人
3. 复制webhook URL

---

### Q3: 邮件推送失败

**可能原因：**
1. 邮箱未开启SMTP服务
2. 密码配置错误
3. 邮箱限制发送频率

**解决方案：**

**以网易邮箱（163.com）为例：**

1. 登录163邮箱
2. 设置 → POP3/SMTP/IMAP
3. 开启SMTP服务
4. 获取授权码（不是登录密码！）
5. 在系统中使用授权码配置

**注意：** 不同邮箱的SMTP配置不同，请参考对应邮箱的帮助文档。

---

### Q4: 资讯获取失败

**可能原因：**
1. 网络连接问题
2. 搜索服务临时不可用

**解决方案：**

1. 检查网络连接
2. 等待几分钟后重试
3. 如果持续失败，可能是服务问题，请联系技术支持

---

### Q5: 定时任务没有执行

**检查清单：**

**Linux/Mac：**
```bash
# 查看定时任务是否配置
crontab -l

# 查看日志
tail -f logs/daily_notification.log

# 查看系统日志
grep CRON /var/log/syslog
```

**Windows：**
1. 打开"任务计划程序"
2. 查看"金融资讯推送"任务
3. 右键 → 属性 → 检查触发器和操作
4. 查看历史记录

---

### Q6: 如何停止定时推送？

**Linux/Mac：**
```bash
# 编辑定时任务
crontab -e

# 删除或注释掉相关行（在行首加 #）
# 0 9 * * * cd /workspace/projects && python scripts/daily_notification.py
```

**Windows：**
1. 打开"任务计划程序"
2. 找到"金融资讯推送"任务
3. 右键 → 禁用

---

## 📞 获取帮助

如果遇到问题：

1. **查看日志：**
   ```bash
   tail -f logs/daily_notification.log
   ```

2. **手动测试：**
   ```bash
   python scripts/daily_notification.py
   ```

3. **联系技术支持：** 提供日志文件和错误信息

---

## 📝 配置检查清单

在完成部署前，请确认：

- [ ] 手动运行脚本成功（`python scripts/daily_notification.py`）
- [ ] 配置文件正确（`config/notification_config.json`）
- [ ] 推送渠道已配置（企业微信/飞书/邮件）
- [ ] 定时任务已设置（crontab/任务计划程序）
- [ ] 日志文件可以正常写入

---

## 🎉 部署完成！

恭喜你！如果完成了以上所有步骤，你的金融资讯推送系统已经可以正常工作了！

从明天早上9点开始，你将每天收到最新的金融资讯推送。

---

## 💡 进阶配置

### 自定义推送时间

**Linux/Mac - 修改定时任务：**

```bash
# 早上8点
0 8 * * * cd /workspace/projects && python scripts/daily_notification.py

# 中午12点
0 12 * * * cd /workspace/projects && python scripts/daily_notification.py

# 每周一早上9点
0 9 * * 1 cd /workspace/projects && python scripts/daily_notification.py
```

**Windows - 修改任务计划程序：**

1. 打开任务计划程序
2. 右键任务 → 属性
3. 修改触发器 → 编辑
4. 修改开始时间

### 自定义推送内容

修改 `config/notification_config.json` 中的 `content_types`：

```json
{
  "content_types": ["gold"]  // 只推送黄金价格
}

{
  "content_types": ["oil", "financial"]  // 推送石油和国际金融
}
```

---

## 📚 附录

### 文件说明

```
config/
├── agent_llm_config.json       # Agent配置（模型、提示词等）
└── notification_config.json    # 推送配置（渠道、收件人等）

scripts/
└── daily_notification.py       # 定时推送主脚本

src/
├── agents/
│   └── agent.py               # Agent核心逻辑
└── tools/
    ├── financial_news_tool.py # 资讯获取工具
    └── notification_tool.py   # 消息推送工具
```

---

**文档版本：** v1.0
**最后更新：** 2025-01-15
