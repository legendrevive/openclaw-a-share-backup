#!/usr/bin/env python3
import subprocess

crontab_content = """# 股票监控系统 - 定时任务配置

# ============ 股票价格监控 ============
*/5 9-11 * * 1-5 cd /Users/liuyazhou/.openclaw/workspace/stock_watch && python3 stock_monitor.py >> stock_log.txt 2>&1
*/5 13-15 * * 1-5 cd /Users/liuyazhou/.openclaw/workspace/stock_watch && python3 stock_monitor.py >> stock_log.txt 2>&1

# ============ 期货监控 ============
*/10 8-11 * * 1-5 cd /Users/liuyazhou/.openclaw/workspace/stock_watch && python3 futures_monitor.py >> futures_log.txt 2>&1
*/10 13-15 * * 1-5 cd /Users/liuyazhou/.openclaw/workspace/stock_watch && python3 futures_monitor.py >> futures_log.txt 2>&1

# ============ 新闻监控 ============
0 7-22 * * * cd /Users/liuyazhou/.openclaw/workspace/stock_watch && python3 news_monitor.py >> news_log.txt 2>&1

# ============ 每日动量报告 ============
0 8 * * 1-5 cd /Users/liuyazhou/.openclaw/workspace/stock_watch && python3 momentum_report.py >> momentum_log.txt 2>&1

# ============ 盘前推荐 ============
30 8 * * 1-5 cd /Users/liuyazhou/.openclaw/workspace/stock_watch && python3 morning_recommend.py >> morning_log.txt 2>&1

# ============ 收盘总结 ============
30 15 * * 1-5 cd /Users/liuyazhou/.openclaw/workspace/stock_watch && python3 stock_monitor.py >> stock_log.txt 2>&1
"""

# 写入 crontab
proc = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
proc.communicate(crontab_content)
print("✅ crontab 已更新")
