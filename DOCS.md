# 📚 文档导航指南

## 📖 文档结构说明

本文档帮助您快速找到需要的文档。

---

## 🎯 快速开始（推荐阅读顺序）

### 1️⃣ 第一次使用？从这里开始
- **[README.md](README.md)** - 项目主文档，了解系统全貌
- **[QQ邮箱SMTP开启指南.md](QQ邮箱SMTP开启指南.md)** - 如何开启QQ邮箱的SMTP服务

### 2️⃣ 选择部署方式
根据您的需求选择：

#### 电脑一直开机 → 本地部署
- **[⚡ 快速开始（5分钟）](docs/QUICK_START.md)** - 最快上手
- **[📖 完整部署指南](docs/DEPLOYMENT_GUIDE.md)** - 详细教程

#### 电脑不一直开机 → 远程部署（推荐）⭐
- **[🚀 GitHub Actions教程（10分钟）](docs/GITHUB_ACTIONS_TUTORIAL.md)** - 最简单、完全免费
- **[🌐 远程部署方案](docs/REMOTE_DEPLOYMENT.md)** - GitHub Actions + 云服务器

### 3️⃣ 部署完成后的检查
- **[部署完成总结](docs/INSTALLATION_SUMMARY.md)** - 功能说明和检查清单

---

## 📂 文档分类

### 📄 核心文档（项目根目录）

| 文档 | 说明 | 推荐度 |
|------|------|--------|
| [README.md](README.md) | 项目主文档，包含所有功能介绍 | ⭐⭐⭐⭐⭐ |
| [QQ邮箱SMTP开启指南.md](QQ邮箱SMTP开启指南.md) | 如何开启QQ邮箱SMTP服务 | ⭐⭐⭐⭐ |

### 📚 部署教程（docs/目录）

| 文档 | 说明 | 适用场景 | 推荐度 |
|------|------|----------|--------|
| [QUICK_START.md](docs/QUICK_START.md) | 5分钟快速开始 | 本地部署，快速测试 | ⭐⭐⭐⭐⭐ |
| [GITHUB_ACTIONS_TUTORIAL.md](docs/GITHUB_ACTIONS_TUTORIAL.md) | GitHub Actions教程 | 远程部署，推荐 | ⭐⭐⭐⭐⭐ |
| [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) | 完整部署指南 | 本地部署，详细了解 | ⭐⭐⭐⭐ |
| [REMOTE_DEPLOYMENT.md](docs/REMOTE_DEPLOYMENT.md) | 远程部署方案 | 云服务器部署 | ⭐⭐⭐ |
| [INSTALLATION_SUMMARY.md](docs/INSTALLATION_SUMMARY.md) | 部署完成总结 | 检查功能是否正常 | ⭐⭐⭐⭐ |

---

## 🎯 按使用场景查找

### 场景1：个人投资者，电脑不常开机
**推荐阅读顺序：**
1. [README.md](README.md) - 了解系统功能
2. [QQ邮箱SMTP开启指南.md](QQ邮箱SMTP开启指南.md) - 配置邮箱
3. [GitHub Actions教程](docs/GITHUB_ACTIONS_TUTORIAL.md) - 部署系统
4. [部署完成总结](docs/INSTALLATION_SUMMARY.md) - 检查功能

### 场景2：投资团队，电脑常开机
**推荐阅读顺序：**
1. [README.md](README.md) - 了解系统功能
2. [快速开始](docs/QUICK_START.md) - 本地部署
3. [完整部署指南](docs/DEPLOYMENT_GUIDE.md) - 详细配置

### 场景3：需要高稳定性
**推荐阅读顺序：**
1. [README.md](README.md) - 了解系统功能
2. [远程部署方案](docs/REMOTE_DEPLOYMENT.md) - 云服务器部署

### 场景4：快速测试
**推荐阅读顺序：**
1. [快速开始](docs/QUICK_START.md) - 一键测试
2. [README.md](README.md) - 了解更多功能

---

## 🔍 常见问题快速索引

### Q: 如何配置邮箱？
**A:** 查看 [QQ邮箱SMTP开启指南.md](QQ邮箱SMTP开启指南.md)

### Q: 如何部署到GitHub Actions？
**A:** 查看 [GitHub Actions教程](docs/GITHUB_ACTIONS_TUTORIAL.md)

### Q: 如何本地运行测试？
**A:** 查看 [快速开始](docs/QUICK_START.md)

### Q: 如何查看系统功能？
**A:** 查看 [README.md](README.md)

### Q: 部署完成后如何检查？
**A:** 查看 [部署完成总结](docs/INSTALLATION_SUMMARY.md)

---

## 📊 文档关系图

```
┌─────────────────────────────────────┐
│         README.md（主文档）          │
│      了解系统所有功能和介绍          │
└──────────┬──────────────────────────┘
           │
           ├──→ QQ邮箱SMTP开启指南.md（邮箱配置）
           │
           ├──→ 本地部署
           │     ├──→ QUICK_START.md（快速开始）
           │     └──→ DEPLOYMENT_GUIDE.md（详细教程）
           │
           └──→ 远程部署
                 ├──→ GITHUB_ACTIONS_TUTORIAL.md（推荐）
                 ├──→ REMOTE_DEPLOYMENT.md（云服务器）
                 └──→ INSTALLATION_SUMMARY.md（检查清单）
```

---

## 💡 使用建议

1. **新用户**：按推荐顺序阅读，从 [README.md](README.md) 开始
2. **快速测试**：直接看 [QUICK_START.md](docs/QUICK_START.md)
3. **远程部署**：重点看 [GITHUB_ACTIONS_TUTORIAL.md](docs/GITHUB_ACTIONS_TUTORIAL.md)
4. **遇到问题**：查看对应文档的常见问题部分

---

## 📝 文档维护

- **最后更新**：2026-03-10
- **版本**：v2.1.0
- **状态**：✅ 文档结构已优化

如有文档相关问题，请提交 Issue。
