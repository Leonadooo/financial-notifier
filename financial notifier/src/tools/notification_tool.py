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

from langchain.tools import tool, ToolRuntime
from coze_workload_identity import Client
from cozeloop.decorator import observe
import requests
from coze_coding_utils.runtime_ctx.context import new_context


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
