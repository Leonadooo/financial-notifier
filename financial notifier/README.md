# 金融资讯定时推送系统

> 🎯 每天早上9点自动推送国际金融形势、黄金、石油等大宗商品最新资讯

---

## 🚀 快速开始

### 场景1：电脑一直开机（本地部署）

**一键测试（30秒）：**

```bash
python scripts/daily_notification.py
```

如果看到"✅ 测试成功！"，系统已经可以运行了！

**详细步骤：** [docs/QUICK_START.md](docs/QUICK_START.md)

---

### 场景2：电脑不一直开机，要邮件推送（推荐）⭐

**使用 GitHub Actions（完全免费）：**

- ✅ 不需要购买服务器
- ✅ 不需要电脑开机
- ✅ 完全免费
- ✅ 操作最简单（10分钟搞定）

**详细教程：** [docs/GITHUB_ACTIONS_TUTORIAL.md](docs/GITHUB_ACTIONS_TUTORIAL.md)

**简要步骤：**
1. 注册GitHub账号
2. 上传代码到GitHub
3. 配置邮箱
4. 完成！每天自动推送

---

### 场景3：需要最高稳定性（云服务器）

**使用云服务器（30-60元/月）：**

- ✅ 稳定性最高
- ✅ 完全控制
- ✅ 可以做更多扩展

**详细教程：** [docs/REMOTE_DEPLOYMENT.md](docs/REMOTE_DEPLOYMENT.md)

---

## 📚 文档导航

### 零基础教程（推荐按顺序阅读）

1. **[🚀 GitHub Actions 10分钟教程](docs/GITHUB_ACTIONS_TUTORIAL.md)** - 最简单的远程部署
2. **[⚡ 5分钟快速开始](docs/QUICK_START.md)** - 本地快速测试
3. **[📖 完整部署指南](docs/DEPLOYMENT_GUIDE.md)** - 本地部署详细教程
4. **[🌐 远程部署方案](docs/REMOTE_DEPLOYMENT.md)** - GitHub Actions + 云服务器

### 其他文档

- [部署完成总结](docs/INSTALLATION_SUMMARY.md) - 功能说明和检查清单
- [项目结构](#项目结构) - 了解系统架构
- [常见问题](#常见问题) - 问题排查

---

## 🎯 系统功能

### 推送内容
- 🥇 **黄金价格走势分析** - 最新价格、影响因素、未来展望
- 🛢️ **原油价格走势分析** - 国际油价、市场动态、供需分析
- 🌍 **国际金融形势** - 全球经济、政策变化、市场趋势

### 推送方式
- ✅ **企业微信机器人** - 适合团队使用
- ✅ **飞书机器人** - 适合团队协作
- ✅ **邮件** - 适合个人使用（推荐）
- ✅ **控制台输出** - 开发测试用

### 智能特性
- 🤖 AI智能摘要 - 快速了解重点
- 📊 多源信息整合 - 综合多家权威来源
- 📝 结构化报告 - 清晰易读
- 🕐 实时更新 - 每天最新资讯

---

## 📁 项目结构

```
workspace/projects/
├── .github/
│   └── workflows/
│       └── daily-notification.yml      # GitHub Actions配置
│
├── config/                             # 配置文件
│   ├── agent_llm_config.json          # Agent配置（模型、提示词）
│   └── notification_config.json       # 推送配置（渠道、收件人）
│
├── scripts/                            # 脚本文件
│   ├── daily_notification.py          # 定时推送主脚本 ⭐
│   ├── test_system.sh                 # 一键测试脚本（Linux/Mac）
│   ├── test_system.bat                # 一键测试脚本（Windows）
│   └── scheduler.py                   # Python定时任务服务
│
├── src/                                # 源代码
│   ├── agents/
│   │   └── agent.py                   # Agent核心逻辑
│   │
│   └── tools/
│       ├── financial_news_tool.py     # 资讯获取工具
│       └── notification_tool.py       # 消息推送工具
│
├── docs/                               # 文档
│   ├── GITHUB_ACTIONS_TUTORIAL.md     # GitHub Actions教程 ⭐
│   ├── REMOTE_DEPLOYMENT.md           # 远程部署方案
│   ├── QUICK_START.md                 # 快速开始
│   ├── DEPLOYMENT_GUIDE.md            # 完整部署指南
│   └── INSTALLATION_SUMMARY.md        # 部署完成总结
│
├── Dockerfile                          # Docker配置（云服务器）
├── docker-compose.yml                  # Docker Compose配置
└── README.md                           # 本文件
```

---

## 🚀 三种部署方案对比

| 特性 | 本地部署 | GitHub Actions | 云服务器 |
|------|---------|---------------|---------|
| **费用** | 免费 | 免费 | 30-60元/月 |
| **需要电脑开机** | ✅ 是 | ❌ 否 | ❌ 否 |
| **技术难度** | 中等 | 简单 | 较高 |
| **设置时间** | 5分钟 | 10分钟 | 30-60分钟 |
| **稳定性** | 依赖电脑 | 高 | 极高 |
| **推荐度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## ⚙️ 配置说明

### 推送渠道配置

文件：`config/notification_config.json`

**通过邮件推送：**
```json
{
  "enabled_channels": ["email"],
  "email": {
    "enabled": true,
    "recipients": ["你的邮箱@example.com"]
  }
}
```

**通过企业微信推送：**
```json
{
  "enabled_channels": ["wechat"],
  "wechat": {
    "enabled": true
  }
}
```

**通过飞书推送：**
```json
{
  "enabled_channels": ["feishu"],
  "feishu": {
    "enabled": true
  }
}
```

**多渠道同时推送：**
```json
{
  "enabled_channels": ["email", "wechat"],
  "email": {
    "enabled": true,
    "recipients": ["user@example.com"]
  },
  "wechat": {
    "enabled": true
  }
}
```

---

## 💡 使用场景示例

### 场景1：个人投资者，每天早上查看邮件

**推荐方案：** GitHub Actions + 邮件推送

**优势：**
- 完全免费
- 不需要电脑开机
- 手机就能查看邮件

**教程：** [docs/GITHUB_ACTIONS_TUTORIAL.md](docs/GITHUB_ACTIONS_TUTORIAL.md)

---

### 场景2：团队协作，需要群内通知

**推荐方案：** 云服务器 + 企业微信/飞书推送

**优势：**
- 稳定性高
- 全员可见
- 方便讨论

**教程：** [docs/REMOTE_DEPLOYMENT.md](docs/REMOTE_DEPLOYMENT.md)

---

### 场景3：开发者，本地开发和测试

**推荐方案：** 本地部署 + 控制台输出

**优势：**
- 快速测试
- 便于调试
- 灵活配置

**教程：** [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

---

## ❓ 常见问题

### Q: 我应该选择哪种部署方式？

**根据你的情况选择：**

| 你的情况 | 推荐方案 |
|---------|---------|
| 电脑不一直开机，想要邮件推送 | GitHub Actions |
| 团队协作，需要群通知 | 云服务器 |
| 开发测试，快速验证 | 本地部署 |

---

### Q: GitHub Actions真的完全免费吗？

**是的！**

- ✅ 公开仓库（Public）完全免费
- ✅ 每月2000分钟免费额度
- ✅ 我们的脚本运行约2分钟，每天一次，远远不够用

---

### Q: 如何修改推送时间？

**GitHub Actions：**
- 编辑 `.github/workflows/daily-notification.yml`
- 修改 `cron: '0 9 * * *'` 中的时间
- 9 = 早上9点，8 = 早上8点

**本地/云服务器：**
- 修改定时任务配置
- Linux/Mac: 修改crontab
- Windows: 修改任务计划程序

---

### Q: 邮件推送失败怎么办？

**检查清单：**

1. ✅ 邮箱是否开启SMTP服务
2. ✅ 是否使用"授权码"而不是"登录密码"
3. ✅ 配置文件格式是否正确
4. ✅ GitHub Actions是否成功运行

**详细说明：** [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md#邮件推送配置)

---

### Q: 如何停止推送？

**GitHub Actions：**
1. 仓库 → Settings → Actions
2. 选择 "Disable all workflows"

**本地/云服务器：**
- 删除或禁用定时任务

---

## 🎯 快速决策树

```
你的电脑是否一直开机？
├─ 是 → 本地部署（5分钟）
│      └─ 参考：docs/QUICK_START.md
│
└─ 否 → 你想要免费吗？
       ├─ 是 → GitHub Actions（10分钟，推荐）
       │      └─ 参考：docs/GITHUB_ACTIONS_TUTORIAL.md
       │
       └─ 否 → 云服务器（30-60分钟）
              └─ 参考：docs/REMOTE_DEPLOYMENT.md
```

---

## 📞 获取帮助

### 查看文档

根据你的情况选择：

- **不想要电脑开机，想邮件推送**：[GitHub Actions教程](docs/GITHUB_ACTIONS_TUTORIAL.md)
- **想要快速测试**：[快速开始](docs/QUICK_START.md)
- **想要详细了解**：[完整部署指南](docs/DEPLOYMENT_GUIDE.md)

### 问题排查

**GitHub Actions问题：**
- 查看Actions日志
- 检查配置文件格式
- 确认仓库是Public

**本地部署问题：**
```bash
# 查看日志
tail -f logs/daily_notification.log

# 运行测试
python scripts/daily_notification.py
```

**云服务器问题：**
```bash
# 查看Docker日志
docker-compose logs -f

# 重启服务
docker-compose restart
```

---

## 🎊 开始使用

### 最推荐的方式（10分钟）

1. 注册GitHub账号
2. 上传代码到GitHub
3. 配置邮箱
4. 完成！

**详细教程：** [docs/GITHUB_ACTIONS_TUTORIAL.md](docs/GITHUB_ACTIONS_TUTORIAL.md)

### 最快速的方式（5分钟）

1. 运行测试脚本
2. 配置推送渠道
3. 设置定时任务

**详细教程：** [docs/QUICK_START.md](docs/QUICK_START.md)

---

## 📖 参考链接

- **GitHub官网**: https://github.com
- **GitHub Actions文档**: https://docs.github.com/actions
- **阿里云**: https://www.aliyun.com
- **腾讯云**: https://cloud.tencent.com

---

## 🎉 总结

这个系统已经为你准备好了所有代码和配置，你只需要：

1. **选择部署方式**（GitHub Actions最推荐）
2. **配置推送邮箱**
3. **等待每天9点的推送**

就这么简单！

---

**祝使用愉快！每天都能及时获取有价值的金融资讯！** 🚀📈📧
