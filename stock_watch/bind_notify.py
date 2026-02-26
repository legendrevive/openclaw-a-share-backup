#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知绑定确认 - 测试所有通知类型
"""

import subprocess
import sys
from datetime import datetime

FEISHU_USER_ID = "ou_8b07ed9ccd79a1ed981ab6888dd977d1"

def send_notification(title, content):
    """发送飞书通知"""
    message = f"**{title}**\n\n{content}"
    
    cmd = [
        "openclaw", "message", "send",
        "--target", f"user:{FEISHU_USER_ID}",
        "--channel", "feishu",
        "--message", message
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except:
        return False

def test_all_notifications():
    """测试所有通知类型"""
    tests = [
        {
            "title": "✅ 价格警报测试",
            "content": """🚨 价格警报测试

洛阳钼业 (603993)
当前价格：¥23.50 📈
涨跌幅：+2.15%

这是测试消息，确认通知绑定成功！"""
        },
        {
            "title": "📊 仓位提醒测试",
            "content": """💡 仓位提醒

当前建议仓位：50-70%
VIX 指数：18.5 (正常)

市场波动正常，可按计划操作。"""
        },
        {
            "title": "🔔 通知绑定确认",
            "content": f"""✅ **通知绑定成功！**

小 k 量化策略通知已绑定到你的飞书：
- 飞书 ID: {FEISHU_USER_ID}
- 绑定时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

你将收到以下通知：
📊 每日动量报告 (交易日 8:00)
🌅 盘前推荐 (交易日 8:30)
🚨 价格警报 (实时)
📉 收盘总结 (交易日 15:30)

回复"解绑通知"可取消绑定。"""
        }
    ]
    
    print("正在测试通知绑定...")
    print("")
    
    success_count = 0
    for i, test in enumerate(tests, 1):
        print(f"[{i}/3] 发送：{test['title']}")
        if send_notification(test['title'], test['content']):
            print(f"      ✅ 成功")
            success_count += 1
        else:
            print(f"      ❌ 失败")
    
    print("")
    print(f"测试结果：{success_count}/{len(tests)} 成功")
    
    return success_count == len(tests)

if __name__ == "__main__":
    success = test_all_notifications()
    if success:
        print("\n✅ 所有通知绑定成功！")
    else:
        print("\n⚠️ 部分通知发送失败，请检查配置")
    
    sys.exit(0 if success else 1)
