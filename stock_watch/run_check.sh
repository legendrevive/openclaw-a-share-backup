#!/bin/bash
# 股票监控检查脚本 - 通过 OpenClaw 发送飞书通知

cd /Users/liuyazhou/.openclaw/workspace/stock_watch

# 运行监控脚本并捕获输出
OUTPUT=$(python3 stock_monitor.py 2>&1)

# 检查是否有警报
if echo "$OUTPUT" | grep -q "\[ALERT\]"; then
    # 有警报，发送飞书消息
    echo "$OUTPUT" | grep -v "\[ALERT\]" | openclaw message send --target "user:ou_8b07ed9ccd79a1ed981ab6888dd977d1" --channel feishu --message "$(cat)"
fi

# 记录日志
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查完成" >> stock_log.txt
