# 🚀 5分钟快速开始指南

> 已经为您准备好了所有代码和配置，只需要3步就能运行！

---

## ✅ 我已经为您完成的工作

### 1. 核心代码（已就绪）
- ✅ Agent智能助手代码
- ✅ 金融资讯搜索工具
- ✅ 多渠道消息推送工具
- ✅ 定时任务执行脚本

### 2. 配置文件（已就绪）
- ✅ Agent配置（模型、提示词）
- ✅ 推送配置模板

### 3. 部署文档（已就绪）
- ✅ 零基础部署指南（超详细）
- ✅ 快速开始卡片
- ✅ 常见问题解答

### 4. 测试工具（已就绪）
- ✅ 一键测试脚本（Linux/Mac）
- ✅ 一键测试脚本（Windows）
- ✅ 手动运行脚本

---

## 📋 您只需要做这3件事

### 第1步：测试系统（30秒）

**Linux/Mac：**
```bash
cd /workspace/projects
bash scripts/test_system.sh
```

**Windows：**
```bash
cd C:\workspace\projects
scripts\test_system.bat
```

**或者直接运行：**
```bash
python scripts/daily_notification.py
```

**预期结果：**
```
✅ 测试成功！系统运行正常
```

如果看到这个结果，说明系统已经可以正常工作了！🎉

---

### 第2步：配置推送渠道（2分钟）

编辑文件：`config/notification_config.json`

**选择你想要的推送方式：**

#### 方式1：只在电脑屏幕上看（最简单）
```json
{
  "enabled_channels": ["console"]
}
```

#### 方式2：通过邮件接收（推荐）
```json
{
  "enabled_channels": ["email"],
  "email": {
    "enabled": true,
    "recipients": ["你的邮箱@163.com", "你的邮箱@qq.com"]
  }
}
```

#### 方式3：通过企业微信接收
```json
{
  "enabled_channels": ["wechat"],
  "wechat": {
    "enabled": true
  }
}
```

#### 方式4：通过飞书接收
```json
{
  "enabled_channels": ["feishu"],
  "feishu": {
    "enabled": true
  }
}
```

#### 方式5：多渠道同时接收
```json
{
  "enabled_channels": ["console", "email"],
  "email": {
    "enabled": true,
    "recipients": ["你的邮箱@example.com"]
  }
}
```

**编辑完成后保存文件，然后再次测试：**
```bash
python scripts/daily_notification.py
```

---

### 第3步：设置定时任务（2分钟）

让系统每天早上9点自动推送！

#### 如果你在Linux/Mac上：

```bash
# 编辑定时任务
crontab -e

# 添加以下内容（按 i 进入编辑模式）
0 9 * * * cd /workspace/projects && python scripts/daily_notification.py

# 保存退出：按 Esc，然后输入 :wq，按回车
```

#### 如果你在Windows上：

1. 按 `Win + R`，输入 `taskschd.msc`，按回车
2. 点击右侧"创建基本任务"
3. 名称：输入"金融资讯推送"
4. 点击"下一步"
5. 触发器：选择"每天"
6. 点击"下一步"
7. 开始时间：设置为 09:00:00
8. 点击"下一步"
9. 操作：选择"启动程序"
10. 点击"下一步"
11. 程序/脚本：选择 `python`
12. 添加参数：`scripts/daily_notification.py`
13. 起始于：`C:\workspace\projects`
14. 点击"完成"

**详细步骤请参考：** [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

---

## 🎉 完成啦！

从明天早上9点开始，你将每天收到：
- 🥇 黄金价格走势分析
- 🛢️ 原油价格走势分析
- 🌍 国际金融形势动态

所有信息都由AI智能整理，直接送到你的手机或电脑！

---

## 📞 遇到问题？

### 问题1：运行报错

**解决方案：**
```bash
# 查看详细日志
tail -f logs/daily_notification.log

# 或查看完整文档
docs/DEPLOYMENT_GUIDE.md
```

### 问题2：邮件推送失败

**解决方案：**
1. 确认邮箱已开启SMTP服务
2. 使用"授权码"而不是"登录密码"
3. 查看部署指南的"邮件推送"章节

### 问题3：定时任务没有执行

**解决方案：**

**Linux/Mac：**
```bash
# 查看定时任务是否配置
crontab -l

# 查看日志
tail -f logs/daily_notification.log
```

**Windows：**
1. 打开"任务计划程序"
2. 查看"金融资讯推送"任务的历史记录

---

## 📚 更多信息

- [完整部署指南](docs/DEPLOYMENT_GUIDE.md) - 零基础详细教程
- [项目README](README.md) - 完整功能说明
- [配置说明](docs/DEPLOYMENT_GUIDE.md#配置推送渠道) - 高级配置

---

## 💡 小贴士

1. **第一次运行**：建议先手动测试，确认一切正常后再设置定时任务
2. **推送时间**：可以修改成任何你想要的时间
3. **内容类型**：可以选择只推送黄金、只推送石油，或全部推送
4. **多渠道推送**：支持同时推送到多个渠道

---

**祝你使用愉快！每天都能及时获取有价值的金融资讯！** 🚀📈
