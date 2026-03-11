"""
消息推送工具
支持通过微信、飞书、邮件等多个渠道推送金融资讯
"""
import json
import smtplib
import ssl
from typing import Optional
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, formatdate, make_msgid
from datetime import datetime

from langchain.tools import tool, ToolRuntime
from coze_workload_identity import Client
from cozeloop.decorator import observe
import requests
from coze_coding_utils.runtime_ctx.context import new_context


def _format_content_to_html(content: str, title: str = None) -> str:
    """
    将Markdown内容转换为美观的HTML格式

    Args:
        content: Markdown格式的内容
        title: 可选的标题

    Returns:
        HTML格式的邮件内容
    """
    try:
        # 提取标题（如果没有提供）
        if not title:
            lines = content.strip().split('\n')
            for line in lines:
                if line.strip().startswith('#'):
                    title = line.strip('#').strip()
                    break

        # 生成HTML内容
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title or '金融资讯'}</title>
    <style>
        /* 全局样式 */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            color: #333333;
            background-color: #f5f7fa;
            margin: 0;
            padding: 20px;
        }}

        /* 容器样式 */
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
            overflow: hidden;
        }}

        /* 头部样式 */
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}

        .header h1 {{
            margin: 0;
            font-size: 32px;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .header .date {{
            margin-top: 10px;
            font-size: 14px;
            opacity: 0.9;
        }}

        /* 内容区域 */
        .content {{
            padding: 30px;
        }}

        /* 标题样式 */
        h1 {{
            color: #2c3e50;
            font-size: 28px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
        }}

        h2 {{
            color: #34495e;
            font-size: 22px;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-left: 10px;
            border-left: 4px solid #667eea;
            background-color: #f8f9fa;
            padding: 10px 15px;
            border-radius: 0 6px 6px 0;
        }}

        h3 {{
            color: #5a6c7d;
            font-size: 18px;
            margin-top: 25px;
            margin-bottom: 12px;
            padding-left: 15px;
            border-left: 3px solid #95a5a6;
        }}

        /* 段落样式 */
        p {{
            margin: 15px 0;
            text-align: justify;
        }}

        /* 列表样式 */
        ul, ol {{
            margin: 15px 0;
            padding-left: 25px;
        }}

        li {{
            margin: 8px 0;
            line-height: 1.8;
        }}

        /* 表格样式 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border-radius: 6px;
            overflow: hidden;
        }}

        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            padding: 14px;
            text-align: left;
        }}

        td {{
            padding: 12px 14px;
            border-bottom: 1px solid #e1e8ed;
        }}

        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        tr:hover {{
            background-color: #f0f3f7;
        }}

        /* 代码样式 */
        code {{
            background-color: #f4f4f4;
            color: #e74c3c;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: "Courier New", monospace;
            font-size: 0.9em;
        }}

        /* 引用样式 */
        blockquote {{
            border-left: 4px solid #667eea;
            margin: 20px 0;
            padding: 15px 20px;
            background-color: #f8f9fa;
            border-radius: 0 6px 6px 0;
            color: #555;
        }}

        /* 分割线 */
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 30px 0;
        }}

        /* 重点标记 */
        strong {{
            color: #e74c3c;
            font-weight: 600;
        }}

        /* 链接样式 */
        a {{
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: all 0.3s;
        }}

        a:hover {{
            border-bottom-color: #667eea;
        }}

        /* 标签样式 */
        .tag {{
            display: inline-block;
            padding: 4px 12px;
            margin: 5px 5px 5px 0;
            background-color: #e8f0fe;
            color: #1967d2;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 500;
        }}

        .tag.success {{
            background-color: #e6f4ea;
            color: #137333;
        }}

        .tag.warning {{
            background-color: #fef7e0;
            color: #b06000;
        }}

        .tag.danger {{
            background-color: #fce8e6;
            color: #c5221f;
        }}

        /* 页脚样式 */
        .footer {{
            background-color: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #e1e8ed;
        }}

        /* 响应式设计 */
        @media screen and (max-width: 600px) {{
            .container {{
                border-radius: 0;
                margin: 0;
            }}

            .header {{
                padding: 30px 20px;
            }}

            .header h1 {{
                font-size: 24px;
            }}

            .content {{
                padding: 20px;
            }}

            h1 {{
                font-size: 22px;
            }}

            h2 {{
                font-size: 18px;
            }}

            table {{
                font-size: 12px;
            }}

            th, td {{
                padding: 8px 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title or '金融资讯推送'}</h1>
            <div class="date">{datetime.now().strftime('%Y年%m月%d日 %H:%M')}</div>
        </div>

        <div class="content">
            {_markdown_to_html(content)}
        </div>

        <div class="footer">
            <p>🤖 由金融资讯助手自动生成 | 如有疑问请联系管理员</p>
            <p>💡 本邮件内容仅供参考，不构成投资建议</p>
        </div>
    </div>
</body>
</html>"""

        return html_content

    except Exception as e:
        # 如果转换失败，返回简单的HTML
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.8; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
    </style>
</head>
<body>
    <div class="container">
        <pre>{content}</pre>
    </div>
</body>
</html>"""


def _markdown_to_html(content: str) -> str:
    """
    简单的Markdown转HTML转换器

    Args:
        content: Markdown格式的内容

    Returns:
        HTML格式的内容
    """
    lines = content.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    in_table = False
    is_first_row = False

    for line in lines:
        # 代码块
        if line.strip().startswith('```'):
            # 如果在表格中，先关闭表格
            if in_table:
                html_lines.append('</tbody></table>\n')
                in_table = False
                is_first_row = False
            
            in_code_block = not in_code_block
            if in_code_block:
                html_lines.append('<pre><code>')
            else:
                html_lines.append('</code></pre>')
            continue

        if in_code_block:
            html_lines.append(line + '\n')
            continue

        # 表格处理
        if line.strip().startswith('|') and '|' in line.strip():
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            
            # 检查是否是分隔行（全为-）
            if all(c.replace('-', '').replace(' ', '') == '' for c in cells):
                continue
            
            # 开始表格
            if not in_table:
                html_lines.append('<table>\n')
                html_lines.append('<thead>\n')
                in_table = True
                is_first_row = True
            
            # 第一行作为表头
            if is_first_row:
                html_lines.append('<tr>' + ''.join(f'<th>{cell}</th>' for cell in cells) + '</tr>\n')
                html_lines.append('</thead>\n')
                html_lines.append('<tbody>\n')
                is_first_row = False
            else:
                html_lines.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>\n')
        else:
            # 如果不在表格行，关闭表格
            if in_table:
                html_lines.append('</tbody></table>\n')
                in_table = False
                is_first_row = False
            
            # 标题
            if line.strip().startswith('# '):
                html_lines.append(f'<h1>{line.strip()[2:]}</h1>\n')
            elif line.strip().startswith('## '):
                html_lines.append(f'<h2>{line.strip()[3:]}</h2>\n')
            elif line.strip().startswith('### '):
                html_lines.append(f'<h3>{line.strip()[4:]}</h3>\n')
            # 分割线
            elif line.strip().startswith('---'):
                html_lines.append('<hr>\n')
            # 引用
            elif line.strip().startswith('>'):
                html_lines.append(f'<blockquote>{line.strip()[2:]}</blockquote>\n')
            # 列表
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                if not in_list:
                    html_lines.append('<ul>\n')
                    in_list = True
                html_lines.append(f'<li>{line.strip()[2:]}</li>\n')
            # 空行或普通段落
            elif line.strip() == '':
                if in_list:
                    html_lines.append('</ul>\n')
                    in_list = False
                html_lines.append('<p></p>\n')
            else:
                if in_list:
                    html_lines.append('</ul>\n')
                    in_list = False
                # 处理行内格式
                formatted_line = line
                formatted_line = formatted_line.replace('**', '<strong>').replace('**', '</strong>')
                formatted_line = formatted_line.replace('*', '<em>').replace('*', '</em>')
                formatted_line = formatted_line.replace('`', '<code>').replace('`', '</code>')
                if formatted_line.strip():
                    html_lines.append(f'<p>{formatted_line}</p>\n')

    # 关闭未关闭的标签
    if in_list:
        html_lines.append('</ul>\n')
    if in_table:
        html_lines.append('</tbody></table>\n')

    return ''.join(html_lines)


def get_wechat_webhook_key() -> str:
    """获取企业微信机器人webhook key"""
    client = Client()
    wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
    webhook_key = json.loads(wechat_bot_credential)["webhook_key"]
    if "https" in webhook_key:
        import re
        webhook_key = re.search(r"key=([a-zA-Z0-9-]+)", webhook_key).group(1)
    return webhook_key


def get_feishu_webhook_url() -> str:
    """获取飞书机器人webhook URL"""
    client = Client()
    feishu_credential = client.get_integration_credential("integration-feishu-message")
    webhook_url = json.loads(feishu_credential)["webhook_url"]
    return webhook_url


def get_email_config() -> dict:
    """获取邮件配置信息"""
    client = Client()
    email_credential = client.get_integration_credential("integration-email-imap-smtp")
    return json.loads(email_credential)


@tool
def send_wechat_notification(content: str, message_type: str = "text", runtime: ToolRuntime = None) -> str:
    """
    通过企业微信机器人发送消息

    Args:
        content: 消息内容
        message_type: 消息类型，支持 "text" (文本) 或 "markdown" (Markdown格式)

    Returns:
        发送结果
    """
    try:
        webhook_key = get_wechat_webhook_key()
        send_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

        if message_type == "markdown":
            payload = {
                "msgtype": "markdown",
                "markdown": {"content": content}
            }
        else:
            payload = {
                "msgtype": "text",
                "text": {"content": content}
            }

        response = requests.post(send_url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("errcode", 0) != 0:
            return f"企业微信消息发送失败：{data}"

        return "企业微信消息发送成功"

    except Exception as e:
        return f"企业微信消息发送异常：{str(e)}"


@tool
def send_feishu_notification(content: str, message_type: str = "text", title: Optional[str] = None, runtime: ToolRuntime = None) -> str:
    """
    通过飞书机器人发送消息

    Args:
        content: 消息内容
        message_type: 消息类型，支持 "text" (文本) 或 "rich" (富文本)
        title: 富文本消息的标题（仅当message_type为"rich"时需要）

    Returns:
        发送结果
    """
    try:
        webhook_url = get_feishu_webhook_url()

        if message_type == "rich":
            if not title:
                title = "金融资讯推送"
            payload = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": title,
                            "content": [[{"tag": "text", "text": content}]]
                        }
                    }
                }
            }
        else:
            payload = {
                "msg_type": "text",
                "content": {"text": content}
            }

        response = requests.post(webhook_url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("code", 0) != 0:
            return f"飞书消息发送失败：{data}"

        return "飞书消息发送成功"

    except Exception as e:
        return f"飞书消息发送异常：{str(e)}"


def _send_email_notification_impl(subject: str, content: str, to_addrs: list, config_override: dict = None) -> str:
    """
    通过邮件发送金融资讯（内部实现函数）

    Args:
        subject: 邮件主题
        content: 邮件内容（支持Markdown格式，会自动转换为美观的HTML）
        to_addrs: 收件人邮箱列表，如 ["user@example.com"]
        config_override: 覆盖的配置信息（可选）

    Returns:
        发送结果
    """
    try:
        # 使用覆盖配置或从环境获取
        if config_override:
            smtp_server = config_override.get("smtp_server")
            smtp_port = config_override.get("smtp_port", 465)
            account = config_override.get("account")
            auth_code = config_override.get("auth_code")
        else:
            from coze_workload_identity import Client
            client = Client()
            email_config = json.loads(client.get_integration_credential("integration-email-imap-smtp"))
            smtp_server = email_config.get("smtp_server")
            smtp_port = email_config.get("smtp_port")
            account = email_config.get("account")
            auth_code = email_config.get("auth_code")

        if not smtp_server or not account or not auth_code:
            return "邮件配置信息不完整"

        # 将Markdown内容转换为美观的HTML格式
        html_content = _format_content_to_html(content, title=subject)

        # 创建HTML格式邮件
        msg = MIMEText(html_content, "html", "utf-8")
        msg["From"] = formataddr(("金融资讯助手", account))
        msg["To"] = ", ".join(to_addrs) if to_addrs else ""
        msg["Subject"] = Header(subject, "utf-8")
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()

        if not to_addrs:
            return "收件人列表为空"

        # 发送邮件
        ctx = ssl.create_default_context()
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2

        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ctx, timeout=30) as server:
            server.ehlo()
            server.login(account, auth_code)
            server.sendmail(account, to_addrs, msg.as_string())
            server.quit()

        return f"邮件成功发送给 {len(to_addrs)} 位收件人"

    except Exception as e:
        return f"邮件发送异常：{str(e)}"


@tool
def send_email_notification(subject: str, content: str, to_addrs: list, runtime: ToolRuntime = None) -> str:
    """
    通过邮件发送金融资讯

    Args:
        subject: 邮件主题
        content: 邮件内容（支持HTML格式）
        to_addrs: 收件人邮箱列表，如 ["user@example.com"]

    Returns:
        发送结果
    """
    try:
        config = get_email_config()

        # 创建HTML格式邮件
        msg = MIMEText(content, "html", "utf-8")
        msg["From"] = formataddr(("金融资讯助手", config["account"]))
        msg["To"] = ", ".join(to_addrs) if to_addrs else ""
        msg["Subject"] = Header(subject, "utf-8")
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()

        if not to_addrs:
            return "收件人列表为空"

        # 发送邮件
        ctx = ssl.create_default_context()
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2

        with smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"], context=ctx, timeout=30) as server:
            server.ehlo()
            server.login(config["account"], config["auth_code"])
            server.sendmail(config["account"], to_addrs, msg.as_string())
            server.quit()

        return f"邮件成功发送给 {len(to_addrs)} 位收件人"

    except Exception as e:
        return f"邮件发送异常：{str(e)}"
