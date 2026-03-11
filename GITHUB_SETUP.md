# 🚀 GitHub 部署快速指南

> 将金融资讯定时推送系统部署到GitHub，实现完全免费、无需电脑开机的定时推送

---

## 📦 快速开始（3步完成）

### 第1步：上传项目到GitHub

#### 方法A：使用Git命令行（推荐）

```bash
# 进入项目目录
cd /path/to/your/project

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "初始提交：金融资讯定时推送系统"

# 关联GitHub仓库
git remote add origin https://github.com/你的用户名/financial-notifier.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

#### 方法B：使用GitHub网页上传

1. 访问您的GitHub仓库
2. 点击 `uploading an existing file`
3. 拖拽所有项目文件到上传区域
4. 点击 `Commit changes`

---

### 第2步：配置GitHub Secrets

1. 打开仓库的 `Settings` → `Secrets and variables` → `Actions`
2. 添加以下Secrets：

   **COZE_API_KEY**
   - Name: `COZE_API_KEY`
   - Value: `你的API密钥`

   **COZE_BASE_URL**
   - Name: `COZE_BASE_URL`
   - Value: `https://integration.coze.cn/api/v3/chat/completions`

---

### 第3步：测试推送

1. 进入仓库的 `Actions` 页面
2. 点击 `Run workflow` 手动触发测试
3. 等待1-3分钟，查看运行结果
4. 检查邮箱是否收到测试邮件

---

## 📚 详细文档

- **完整部署指南**：[docs/GITHUB_DEPLOYMENT.md](docs/GITHUB_DEPLOYMENT.md)
- **功能介绍**：[README.md](README.md)
- **文档导航**：[DOCS.md](DOCS.md)

---

## ✅ 部署检查清单

- [ ] 已上传所有项目文件到GitHub
- [ ] 已配置 `COZE_API_KEY` Secret
- [ ] 已配置 `COZE_BASE_URL` Secret
- [ ] 已手动触发测试推送
- [ ] 已收到测试邮件

---

## ⚠️ 重要提醒

1. **API密钥安全**：
   - 使用GitHub Secrets存储API密钥
   - 不要将密钥提交到代码中

2. **邮箱配置**：
   - 如果配置了邮件推送，邮箱信息会显示在仓库中
   - 建议使用私有仓库

3. **定时推送**：
   - 默认每天北京时间9点推送
   - 可在 `.github/workflows/daily-notification.yml` 中修改

---

## 🔧 常见问题

### Q: 如何修改推送时间？

编辑 `.github/workflows/daily-notification.yml`：
```yaml
schedule:
  - cron: '0 9 * * *'  # 每天早上9点
```

### Q: 如何配置多个推送渠道？

编辑 `config/notification_config.json`：
```json
{
  "enabled_channels": ["email", "wechat"]
}
```

### Q: 工作流运行失败怎么办？

1. 查看 `Actions` 页面的运行日志
2. 检查GitHub Secrets是否正确配置
3. 查看详细部署指南：[docs/GITHUB_DEPLOYMENT.md](docs/GITHUB_DEPLOYMENT.md)

---

## 🎉 部署成功！

如果您已成功部署并收到测试邮件，恭喜您！

现在系统会在每天指定时间自动推送ETF投资分析报告到您的邮箱。

---

**预计时间**：10分钟
**费用**：完全免费
**难度**：⭐⭐（简单）

需要帮助？查看详细文档：[docs/GITHUB_DEPLOYMENT.md](docs/GITHUB_DEPLOYMENT.md)
