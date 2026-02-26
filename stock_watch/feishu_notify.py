#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书通知推送脚本
通过 OpenClaw message 工具发送消息到飞书
"""

import sys
import subprocess
import json
from datetime import datetime

# 用户飞书 ID
FEISHU_USER_ID = "ou_8b07ed9ccd79a1ed981ab6888dd977d1"

def send_feishu_message(message, title=None):
    """
    通过 OpenClaw 发送飞书消息
    """
    # 构建完整消息
    if title:
        full_message = f"**{title}**\n\n{message}"
    else:
        full_message = message
    
    # 使用 OpenClaw message 工具发送
    cmd = [
        "openclaw", "message", "send",
        "--target", f"user:{FEISHU_USER_ID}",
        "--channel", "feishu",
        "--message", full_message
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"[OK] 消息已发送")
            return True
        else:
            print(f"[ERROR] 发送失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] 异常：{e}")
        return False

def send_stock_alert(stock_name, code, current_price, change_pct, alert_type):
    """发送股票价格警报"""
    icon = "🚨" if alert_type == "sharp" else "⚠️"
    change_icon = "📈" if change_pct >= 0 else "📉"
    change_sign = "+" if change_pct >= 0 else ""
    
    message = f"""{icon} **价格警报**

{stock_name} ({code})
当前价格：¥{current_price:.2f} {change_icon}
涨跌幅：{change_sign}{change_pct:.2f}%

时间：{datetime.now().strftime('%H:%M:%S')}"""
    
    return send_feishu_message(message, f"{icon} {stock_name} 价格警报")

def send_morning_recommendation(report_text):
    """发送盘前推荐"""
    # 提取关键信息
    lines = report_text.split('\n')
    highlights = []
    
    for line in lines:
        if 'TOP' in line and '题材' in line:
            highlights.append(line.strip())
    
    message = f"""🌅 **盘前推荐** - {datetime.now().strftime('%Y-%m-%d')}

重点关注:
{chr(10).join(highlights[:3])}

💡 建议:
• 高开不追，回调可考虑
• 设置止损位 (-5%)
• 关注期货联动

⚠️ 股市有风险，投资需谨慎"""
    
    return send_feishu_message(message, "📈 小 k 盘前推荐")

def send_market_summary(stock_data_list, futures_summary=None):
    """发送市场概览"""
    stocks_up = sum(1 for s in stock_data_list if s.get('change_pct', 0) > 0)
    stocks_down = len(stock_data_list) - stocks_up
    
    market_icon = "🟢" if stocks_up > stocks_down else ("🔴" if stocks_down > stocks_up else "🟡")
    
    message = f"""{market_icon} **市场概览** - {datetime.now().strftime('%H:%M:%S')}

关注股票:
"""
    
    for stock in stock_data_list:
        icon = "📈" if stock.get('change_pct', 0) >= 0 else "📉"
        sign = "+" if stock.get('change_pct', 0) >= 0 else ""
        message += f"{icon} {stock['name']}: ¥{stock['current']:.2f} ({sign}{stock['change_pct']:.2f}%)\n"
    
    if futures_summary:
        message += f"\n🏭 期货：{futures_summary}"
    
    return send_feishu_message(message, "📊 市场快报")

def send_news_digest(news_list):
    """发送新闻摘要"""
    message = f"""📰 **行业动态** - {datetime.now().strftime('%Y-%m-%d %H:%M')}

重点关注:
"""
    
    for i, news in enumerate(news_list[:5], 1):
        message += f"{i}. {news.get('title', '无标题')}\n"
    
    message += f"\n共 {len(news_list)} 条相关新闻"
    
    return send_feishu_message(message, "📰 行业快讯")

def send_custom_message(title, content):
    """发送自定义消息"""
    return send_feishu_message(content, title)

def main():
    """主函数 - 根据参数发送不同类型的消息"""
    if len(sys.argv) < 2:
        print("用法：python3 feishu_notify.py <类型> [参数...]")
        print("类型：stock_alert, morning, market, news, custom")
        return 1
    
    notify_type = sys.argv[1]
    
    if notify_type == "stock_alert":
        # 从标准输入读取股票数据
        data = json.loads(sys.stdin.read())
        return 0 if send_stock_alert(
            data['name'], data['code'], 
            data['current'], data['change_pct'],
            data.get('alert_type', 'normal')
        ) else 1
    
    elif notify_type == "morning":
        # 从文件读取盘前推荐
        try:
            with open('morning_log.txt', 'r') as f:
                content = f.read()
            return 0 if send_morning_recommendation(content) else 1
        except FileNotFoundError:
            print("[ERROR] morning_log.txt 不存在")
            return 1
    
    elif notify_type == "market":
        # 从标准输入读取市场数据
        data = json.loads(sys.stdin.read())
        return 0 if send_market_summary(
            data.get('stocks', []),
            data.get('futures')
        ) else 1
    
    elif notify_type == "news":
        # 从标准输入读取新闻
        data = json.loads(sys.stdin.read())
        return 0 if send_news_digest(data.get('news', [])) else 1
    
    elif notify_type == "custom":
        # 自定义消息
        title = sys.argv[2] if len(sys.argv) > 2 else "消息"
        content = sys.stdin.read()
        return 0 if send_custom_message(title, content) else 1
    
    else:
        print(f"[ERROR] 未知类型：{notify_type}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
