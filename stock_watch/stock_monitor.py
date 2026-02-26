#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控脚本 - 监控指定股票价格并发送飞书通知
"""

import json
import urllib.request
import urllib.error
import sys
from datetime import datetime

# 股票配置文件路径
CONFIG_PATH = "/Users/liuyazhou/.openclaw/workspace/stock_watch/stocks.json"
STATE_PATH = "/Users/liuyazhou/.openclaw/workspace/stock_watch/last_prices.json"

def get_stock_price(code, market):
    """
    从腾讯财经获取股票实时价格
    market: SH (上海) 或 SZ (深圳)
    code: 股票代码
    """
    if market == "SH":
        symbol = f"sh{code}"
    else:
        symbol = f"sz{code}"
    
    url = f"http://qt.gtimg.cn/q={symbol}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'http://stock.tencent.com/'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('gbk')
            # 解析数据：v_sh603993="51~洛阳钼业~603993~7.85~7.80~7.82~..."
            # 格式：类型~名字~代码~当前~开盘~昨收~最高~最低~...
            parts = data.strip().split('"')[1].split('~')
            if len(parts) >= 7:
                name = parts[1]
                current = float(parts[3])
                open_price = float(parts[4])
                prev_close = float(parts[5])
                high = float(parts[33]) if len(parts) > 33 else float(parts[6])
                low = float(parts[34]) if len(parts) > 34 else float(parts[7])
                
                # 计算涨跌幅
                change = current - prev_close
                change_pct = (change / prev_close) * 100 if prev_close else 0
                
                return {
                    "name": name,
                    "code": code,
                    "market": market,
                    "current": current,
                    "open": open_price,
                    "prev_close": prev_close,
                    "high": high,
                    "low": low,
                    "change": change,
                    "change_pct": change_pct
                }
    except Exception as e:
        print(f"获取 {symbol} 价格失败：{e}", file=sys.stderr)
    
    return None

def load_state():
    """加载上次价格状态"""
    try:
        with open(STATE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(state):
    """保存价格状态"""
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_config():
    """加载配置文件"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def send_feishu_notification(message):
    """
    发送飞书通知
    使用 OpenClaw 的 message 工具发送
    """
    import subprocess
    try:
        cmd = [
            "openclaw", "message", "send",
            "--target", "user:ou_8b07ed9ccd79a1ed981ab6888dd977d1",
            "--channel", "feishu",
            "--message", message
        ]
        subprocess.run(cmd, capture_output=True, timeout=30)
        return True
    except Exception as e:
        print(f"发送飞书消息失败：{e}", file=sys.stderr)
        return False

def send_feishu_alerts(alert_data_list):
    """发送价格警报到飞书"""
    import subprocess
    import json
    
    for alert in alert_data_list:
        icon = "🚨" if alert.get('alert_type') == 'sharp' else "⚠️"
        change_icon = "📈" if alert['change_pct'] >= 0 else "📉"
        sign = "+" if alert['change_pct'] >= 0 else ""
        
        message = f"""{icon} **价格警报**

{alert['name']} ({alert['code']})
当前价格：¥{alert['current']:.2f} {change_icon}
涨跌幅：{sign}{alert['change_pct']:.2f}%

时间：{datetime.now().strftime('%H:%M:%S')}"""
        
        try:
            cmd = [
                "openclaw", "message", "send",
                "--target", "user:ou_8b07ed9ccd79a1ed981ab6888dd977d1",
                "--channel", "feishu",
                "--message", message
            ]
            subprocess.run(cmd, capture_output=True, timeout=30)
            print(f"[通知] 已发送 {alert['name']} 警报")
        except Exception as e:
            print(f"发送警报失败：{e}", file=sys.stderr)

def format_stock_info(stock_data):
    """格式化股票信息"""
    change_symbol = "📈" if stock_data["change"] >= 0 else "📉"
    change_sign = "+" if stock_data["change"] >= 0 else ""
    
    return f"""{stock_data['name']} ({stock_data['code']})
当前：¥{stock_data['current']:.2f} {change_symbol}
涨跌：{change_sign}{stock_data['change']:.2f} ({change_sign}{stock_data['change_pct']:.2f}%)
开盘：¥{stock_data['open']:.2f}
最高：¥{stock_data['high']:.2f}
最低：¥{stock_data['low']:.2f}
昨收：¥{stock_data['prev_close']:.2f}"""

def check_price_alerts(stock_data, config_stock, last_prices):
    """检查价格提醒"""
    alerts = []
    alert_data = []
    code = stock_data["code"]
    current = stock_data["current"]
    change_pct = stock_data["change_pct"]
    
    # 检查目标价格
    if config_stock.get("target_price_up") and current >= config_stock["target_price_up"]:
        alerts.append(f"⚠️ {stock_data['name']} 达到目标价：¥{current:.2f} ≥ ¥{config_stock['target_price_up']:.2f}")
        alert_data.append({
            "name": stock_data['name'],
            "code": code,
            "current": current,
            "change_pct": change_pct,
            "alert_type": "target_up"
        })
    
    if config_stock.get("target_price_down") and current <= config_stock["target_price_down"]:
        alerts.append(f"⚠️ {stock_data['name']} 跌破目标价：¥{current:.2f} ≤ ¥{config_stock['target_price_down']:.2f}")
        alert_data.append({
            "name": stock_data['name'],
            "code": code,
            "current": current,
            "change_pct": change_pct,
            "alert_type": "target_down"
        })
    
    # 检查大幅波动（超过 5%）
    if code in last_prices:
        last_price = last_prices[code]
        price_change_pct = abs((current - last_price) / last_price) * 100
        if price_change_pct >= 5:
            direction = "上涨" if current > last_price else "下跌"
            alerts.append(f"🚨 {stock_data['name']} 大幅{direction}：{price_change_pct:.2f}%")
            alert_data.append({
                "name": stock_data['name'],
                "code": code,
                "current": current,
                "change_pct": change_pct,
                "alert_type": "sharp"
            })
    
    # 发送飞书通知
    if alert_data:
        send_feishu_alerts(alert_data)
    
    return alerts

def main():
    """主函数"""
    config = load_config()
    last_prices = load_state()
    
    notifications = []
    new_prices = {}
    
    for stock_config in config["stocks"]:
        stock_data = get_stock_price(stock_config["code"], stock_config["market"])
        
        if stock_data:
            new_prices[stock_data["code"]] = stock_data["current"]
            
            # 格式化股票信息
            stock_info = format_stock_info(stock_data)
            notifications.append(f"📊 {stock_info}")
            
            # 检查价格提醒
            alerts = check_price_alerts(stock_data, stock_config, last_prices)
            notifications.extend(alerts)
        else:
            notifications.append(f"❌ 获取 {stock_config['name']} 价格失败")
    
    # 保存当前价格状态
    save_state(new_prices)
    
    # 输出结果
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"⏰ 股票监控报告 - {timestamp}"
    
    full_message = header + "\n\n" + "\n\n---\n\n".join(notifications)
    
    print(full_message)
    
    # 如果有警报，输出特殊标记
    has_alerts = any("⚠️" in n or "🚨" in n for n in notifications)
    if has_alerts:
        print("\n[ALERT]")
    
    return 0 if not has_alerts else 1

if __name__ == "__main__":
    sys.exit(main())
