# 🚀 GitHub Actions 零基础教程 - 10分钟完成部署

> 最简单的远程部署方案，完全免费，不需要任何技术背景

---

## 📝 前置准备

你需要：
- ✅ 一个邮箱账号（用于接收推送）
- ✅ 能上网的电脑
- ✅ 5-10分钟时间

---

## 🎯 整体流程（3步搞定）

```
注册GitHub → 上传代码 → 配置邮箱 → 完成！
   (2分钟)     (3分钟)     (2分钟)
```

就这么简单！

---

## 第1步：注册GitHub账号（2分钟）

### 1.1 打开网站

在浏览器中访问：https://github.com

### 1.2 注册账号

1. 点击右上角绿色的 **"Sign up"** 按钮
2. 填写信息：
   - **Email address**: 你的邮箱
   - **Password**: 设置密码（至少8位，包含数字和字母）
   - **Username**: 用户名（英文，如：financial-user-2025）
3. 点击 **"Continue"**
4. 完成人机验证（如果是图片，点击所有包含某个物体的图片）
5. 选择 **"Free"**（免费账号）
6. 验证邮箱（去你的邮箱查收验证邮件并点击链接）

### 1.3 登录

验证后自动登录，或者手动登录。

---

## 第2步：创建仓库（1分钟）

### 2.1 新建仓库

1. 点击右上角的 **"+"** 号
2. 选择 **"New repository"**

### 2.2 填写信息

填写以下信息：

- **Repository name**: 输入 `financial-notifier`（必须这个名字，方便后续）
- **Description**: 输入 `金融资讯定时推送系统`（可选）
- **Public/Private**: 选择 **Public**（⚠️ **必须选择Public，免费使用GitHub Actions**）
- 勾选 **"Add a README file"**（可选）

### 2.3 创建

点击绿色的 **"Create repository"** 按钮

---

## 第3步：上传项目文件（3分钟）

### 方法A：网页上传（最简单，推荐）

#### 3.1 准备文件

在你的电脑上，找到项目文件夹：
```
C:\workspace\projects
```

需要上传的文件和文件夹：
```
src/
config/
scripts/
requirements.txt
.github/
```

⚠️ **重要：不要上传整个C盘，只上传这些文件！**

#### 3.2 上传文件

1. 在GitHub仓库页面，点击 **"uploading an existing file"** 文字链接
2. 弹出文件选择窗口
3. 将上面的文件和文件夹**拖拽**到浏览器窗口中
4. 等待上传完成
5. 在最下方的 **"Commit changes"** 上面，填写：
   - Commit message: `Initial commit`（或者留空也可以）
6. 点击绿色的 **"Commit changes"** 按钮

#### 3.3 验证上传

刷新页面，你应该能看到上传的文件和文件夹。

---

### 方法B：使用Git命令（如果你熟悉Git）

在项目文件夹打开命令行（Win+R，输入cmd）：

```bash
cd C:\workspace\projects
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/financial-notifier.git
git push -u origin main
```

---

## 第4步：配置推送渠道（2分钟）

### 4.1 打开配置文件

1. 在GitHub仓库页面，找到 `config` 文件夹
2. 点击 `notification_config.json` 文件

### 4.2 编辑配置

1. 点击右上角的 **✏️ 铅笔图标**
2. 将内容修改为：

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
    "recipients": ["你的邮箱@163.com"]
  },
  "content_types": ["gold", "oil", "financial"]
}
```

**重要修改点：**
- 将 `"你的邮箱@163.com"` 改成你的真实邮箱地址
- 可以添加多个邮箱：`["邮箱1@example.com", "邮箱2@example.com"]`

3. 点击绿色的 **"Commit changes"** 按钮

---

## 第5步：测试运行（2分钟）

### 5.1 打开Actions页面

1. 点击仓库顶部的 **"Actions"** 标签
2. 可能会看到提示 "I understand my workflows, go ahead and enable them"，点击它

### 5.2 手动触发运行

1. 左侧菜单找到 **"金融资讯定时推送"**（或 "financial-notifier"）
2. 点击它
3. 右侧点击 **"Run workflow"** 按钮
4. 点击绿色的 **"Run workflow"** 按钮

### 5.3 查看运行结果

1. 等待1-2分钟
2. 点击刚才运行的任务（应该是最上面的一条）
3. 查看运行状态：
   - ✅ **绿色 ✓** = 成功！
   - ❌ **红色 ✗** = 失败，点击查看日志

### 5.4 检查邮箱

如果成功，检查你的邮箱，应该收到一封金融资讯邮件！

---

## 第6步：完成！

🎉 **恭喜你！**

从明天开始，每天北京时间早上9点，GitHub会自动运行脚本，发送金融资讯到你的邮箱。

**你不需要：**
- ❌ 电脑开机
- ❌ 安装任何软件
- ❌ 购买服务器
- ❌ 学习编程

**你需要做的：**
- ✅ 每天早上查看邮箱

---

## 📊 如何查看历史推送

### 查看运行记录

1. 点击仓库的 **"Actions"** 标签
2. 可以看到每天的历史运行记录
3. 点击任意一条查看详细日志

### 查看邮件

- 直接去邮箱查看
- 邮件标题：`📈 金融资讯早报 - 日期`

---

## ⚙️ 高级配置（可选）

### 修改推送时间

默认是每天早上9点（北京时间）

如果要修改：

1. 打开 `.github/workflows/daily-notification.yml` 文件
2. 找到这行：
   ```yaml
   - cron: '0 9 * * *'
   ```
3. 修改时间：
   - 改成早上8点：`0 8 * * *`
   - 改成中午12点：`0 12 * * *`
   - 改成晚上8点：`0 20 * * *`
4. Commit changes

### 修改推送内容

修改 `config/notification_config.json` 中的 `content_types`：

```json
{
  "content_types": ["gold"]  // 只推送黄金
}

{
  "content_types": ["oil", "financial"]  // 推送石油和金融
}
```

---

## ❓ 常见问题

### Q1: Actions运行失败怎么办？

**解决方案：**

1. 点击红色的任务
2. 查看日志，找到错误信息
3. 常见错误：
   - **文件未上传**：检查是否上传了所有文件
   - **配置错误**：检查 `notification_config.json` 格式是否正确
   - **邮箱配置问题**：检查邮箱是否开启SMTP服务

### Q2: 没有收到邮件？

**检查清单：**

1. GitHub Actions是否成功运行（绿色✓）
2. 配置文件中的邮箱地址是否正确
3. 邮箱是否被标记为垃圾邮件
4. 邮箱是否开启了SMTP服务

### Q3: 如何停止推送？

**方法1：禁用Actions**
1. 仓库 → Settings → Actions
2. 选择 "Disable all workflows"

**方法2：删除仓库**
1. Settings → General
2. 滚动到最下面，点击 "Delete this repository"

### Q4: 可以同时推送到多个邮箱吗？

**可以！** 修改配置：

```json
{
  "email": {
    "enabled": true,
    "recipients": [
      "邮箱1@163.com",
      "邮箱2@qq.com",
      "邮箱3@gmail.com"
    ]
  }
}
```

---

## 🎯 下一步

现在你已经完成了部署，可以：

1. **测试一下**：等待明天早上9点的邮件
2. **自定义内容**：修改配置，只关注你感兴趣的内容
3. **分享给朋友**：让他们也创建一个GitHub账号，按照这个教程部署

---

## 📞 需要帮助？

### GitHub官方文档：
- https://docs.github.com

### 常用链接：
- 仓库设置：点击仓库的 Settings
- Actions日志：点击仓库的 Actions
- 编辑文件：点击文件右上角的 ✏️

---

## 🎊 总结

**你刚才做了什么：**

1. ✅ 注册了GitHub账号
2. ✅ 创建了代码仓库
3. ✅ 上传了项目文件
4. ✅ 配置了推送邮箱
5. ✅ 测试了运行

**现在你会得到什么：**

- 📧 每天早上9点自动收到金融资讯邮件
- 💰 完全免费
- 🚀 不需要任何技术维护

**就这么简单！** 🎉

---

**祝使用愉快！** 📈📧
