#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试飞书通知功能
"""

import subprocess
import sys

def send_test_message():
    """发送测试消息"""
    message = """✅ **小 k 通知测试**

飞书推送功能已启用！

📊 你将收到以下通知:
• 股票价格警报（涨跌幅≥5% 或达到目标价）
• 每日盘前推荐（交易日 8:30）
• 收盘总结（交易日 15:30）

时间：2026-02-26 21:38
"""
    
    cmd = [
        "openclaw", "message", "send",
        "--target", "user:ou_8b07ed9ccd79a1ed981ab6888dd977d1",
        "--channel", "feishu",
        "--message", message
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ 测试消息发送成功！")
            return True
        else:
            print(f"❌ 发送失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 异常：{e}")
        return False

if __name__ == "__main__":
    success = send_test_message()
    sys.exit(0 if success else 1)
