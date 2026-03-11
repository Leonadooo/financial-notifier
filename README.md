# 金融资讯定时推送系统

> 🎯 每天早上9点自动推送国际金融形势、黄金、石油等大宗商品最新资讯和ETF投资分析报告

---

## 🚀 快速开始

### 场景1：电脑一直开机（本地部署）

**一键测试（30秒）：**

```bash
python scripts/daily_notifier.py
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

### 配置指南

- **[QQ邮箱SMTP开启指南](QQ邮箱SMTP开启指南.md)** - 如何开启QQ邮箱的SMTP服务

### 其他文档

- [部署完成总结](docs/INSTALLATION_SUMMARY.md) - 功能说明和检查清单
- [项目结构](#项目结构) - 了解系统架构
- [常见问题](#常见问题) - 问题排查

---

## 🎯 系统功能

### 1. 市场数据收集
- ✅ 国际事件（美联储、欧央行、地缘政治、中美关系等）
- ✅ 大宗商品价格（原油、黄金、铜、天然气、农产品）
- ✅ 全球金融动态（美元指数、美债收益率、资金流向、风险偏好）

### 2. ETF投资分析 ⭐ 核心功能
- ✅ A股宽基ETF（沪深300、中证500、科创50、创业板）
- ✅ A股行业ETF（半导体、新能源、医药、消费、金融、煤炭、有色、黄金、油气）
- ✅ 港股宽基ETF（恒生指数、恒生科技、国企指数）
- ✅ 港股行业ETF（互联网、医药、金融、能源）

### 3. 昨日预测验证 ⭐ 新功能
- ✅ 自动保存每日预测到JSON文件
- ✅ 自动读取昨日预测进行验证分析
- ✅ 生成验证结果表格（准确/偏差/部分准确）
- ✅ 分析偏差原因

### 4. 多渠道推送
- ✅ 控制台输出
- ✅ 邮件推送（QQ邮箱、163邮箱等）
- ⏳ 企业微信机器人推送（配置中）
- ⏳ 飞书机器人推送（配置中）

### 5. 美观格式支持
- ✅ HTML格式邮件（渐变头部、卡片布局）
- ✅ Markdown格式内容
- ✅ 表格自动美化（渐变表头、斑马纹、悬停高亮）
- ✅ 响应式设计，支持手机阅读

---

## 📊 ETF投资分析报告结构

### 完整报告包含以下8个板块：

1. **今日关键国际事件总结**
   - 美联储/欧央行政策动态
   - 地缘政治事件
   - 中美关系
   - 全球经济数据

2. **大宗商品价格走势分析**（表格格式）
   | 品种 | 涨跌表现 | 核心逻辑 |

3. **全球金融动态分析**
   - 美元指数走势
   - 美债收益率变化
   - 北向/南向资金流向
   - 全球风险偏好变化

4. **对A股ETF的直接影响**（双表格）
   - 宽基ETF表格
   - 行业ETF表格

5. **对港股ETF的直接影响**（双表格）
   - 宽基ETF表格
   - 行业ETF表格

6. **A股与港股ETF的联动差异**
   - 港股更敏感于外资/美元因素
   - A股更敏感于内资/政策因素

7. **当日ETF交易关注点**
   - 高弹性方向
   - 防御方向
   - 资金流向信号

8. **昨日预测验证** ⭐ 新功能（表格格式）
   | 预测内容 | 验证结果 | 实际情况 | 偏差原因 |

---

## 🔧 昨日预测验证功能详解

### 工作流程
1. **首次运行**：
   - 生成分析报告
   - 保存为当日预测
   - 验证板块显示"无昨日预测数据"

2. **后续运行**：
   - 读取昨日预测
   - 收集今日市场数据
   - 对比验证昨日预测
   - 生成验证报告
   - 保存为当日预测

### 验证结果标注
- ✅准确：预测与实际情况一致
- ⚠️部分准确：预测部分正确
- ❌偏差：预测与实际情况相反
- ❓无法判断：数据不足无法验证

### 示例输出
```
## 8. 昨日预测验证

昨日日期：2026-03-09

| 预测内容 | 验证结果 | 实际情况 | 偏差原因 |
|---------|---------|---------|---------|
| 预测原油上涨 | ❌偏差 | 原油今日下跌6.70% | 中东地缘风险溢价快速消退 |
| 预测黄金上涨 | ✅准确 | 黄金收窄跌幅 | 避险需求与利空因素对冲 |
```

---

## 📁 项目结构

```
workspace/projects/
├── .github/
│   └── workflows/
│       ├── daily-notification.yml      # 每日推送配置
│       └── etf-analysis.yml           # ETF分析配置
│
├── config/                             # 配置文件
│   ├── agent_llm_config.json          # Agent配置（模型、提示词）
│   └── notification_config.json       # 推送配置（渠道、收件人）
│
├── scripts/                            # 脚本文件
│   ├── daily_notifier.py              # 每日推送脚本
│   ├── etf_analysis.py                # ETF分析脚本 ⭐
│   ├── test_system.sh                 # 一键测试脚本（Linux/Mac）
│   ├── test_system.bat                # 一键测试脚本（Windows）
│   └── scheduler.py                   # Python定时任务服务
│
├── src/                                # 源代码
│   ├── agents/
│   │   └── agent.py                   # Agent核心逻辑
│   ├── tools/
│   │   ├── financial_news_tool.py     # 资讯获取工具
│   │   └── notification_tool.py       # 消息推送工具
│   ├── storage/
│   │   └── memory/
│   │       └── memory_saver.py        # 记忆存储
│   └── utils/
│       └── prediction_manager.py      # 预测管理 ⭐
│
├── assets/                             # 资源文件
│   ├── predictions/                   # 预测存储 ⭐
│   │   └── etf_prediction_YYYY-MM-DD.json
│   └── data/                          # 数据文件
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
├── requirements.txt                    # Python依赖
├── QQ邮箱SMTP开启指南.md              # 邮箱配置指南
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
```json
{
  "enabled_channels": ["email"],
  "email": {
    "enabled": true,
    "recipients": ["investor@example.com"]
  }
}
```

### 场景2：投资团队，企业微信群推送
```json
{
  "enabled_channels": ["wechat"],
  "wechat": {
    "enabled": true
  }
}
```

### 场景3：同时推送到邮件和企业微信
```json
{
  "enabled_channels": ["email", "wechat"],
  "email": {
    "enabled": true,
    "recipients": ["team@example.com"]
  },
  "wechat": {
    "enabled": true
  }
}
```

---

## 🤖 技术架构

### 技术栈
- Python 3.12
- LangChain / LangGraph
- coze-coding-dev-sdk
- requests

### 核心模块
- **Agent**: 基于LangChain的智能Agent，负责协调各个工具
- **Tools**: 金融资讯获取、消息推送工具
- **Memory**: 记忆存储，支持多轮对话
- **Prediction Manager**: 预测管理模块，实现验证功能

---

## 🚦 运行脚本

### 运行每日推送
```bash
python scripts/daily_notifier.py
```

### 运行ETF分析
```bash
python scripts/etf_analysis.py
```

### 一键测试（Linux/Mac）
```bash
bash scripts/test_system.sh
```

### 一键测试（Windows）
```bash
scripts\test_system.bat
```

---

## 📈 智能特性

- 🤖 **AI智能摘要** - 快速了解重点
- 📊 **多源信息整合** - 综合多家权威来源
- 📝 **结构化报告** - 清晰易读
- 🕐 **实时更新** - 每天最新资讯
- 🔍 **预测验证** - 验证昨日预测准确性

---

## ❓ 常见问题

### Q1: 如何修改推送时间？
A: 修改 GitHub Actions 工作流文件中的 `cron` 表达式。

### Q2: 如何添加新的推送渠道？
A: 在 `config/notification_config.json` 中添加相应配置，并在 `src/tools/notification_tool.py` 中实现推送逻辑。

### Q3: 如何查看历史预测？
A: 历史预测存储在 `assets/predictions/` 目录，文件名为 `etf_prediction_YYYY-MM-DD.json`。

### Q4: 验证功能需要额外配置吗？
A: 不需要，验证功能会自动运行。首次运行时会显示"无昨日预测数据"，后续运行时会自动验证。

### Q5: 支持哪些邮箱？
A: 支持QQ邮箱、163邮箱、Outlook、Gmail等，需要在配置文件中设置对应的SMTP服务器和端口。

---

## 📝 更新日志

### v2.1.0 (2026-03-10)
- ✨ 新增昨日预测验证功能
- ✨ 优化HTML邮件格式（渐变头部、表格美化）
- 🐛 修复表格显示问题

### v2.0.0 (2026-03-09)
- ✨ 新增ETF投资分析功能
- ✨ 支持A股和港股ETF分析
- ✨ 支持HTML格式邮件

### v1.0.0 (2026-03-08)
- ✨ 初始版本发布
- ✨ 支持黄金、原油等大宗商品资讯推送
- ✨ 支持邮件、企业微信、飞书推送

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📧 联系方式

如有问题或建议，请提交 Issue。

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
