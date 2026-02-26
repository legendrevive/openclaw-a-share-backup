# HEARTBEAT.md

# 股票监控任务

## 盘中监控 (交易时段 9:30-15:00)
- 每 2 小时检查一次自选股价格
- 涨跌幅超过±5% 时立即通知
- 记录到 memory/stock_log.md

## 盘后总结 (15:30)
- 生成当日持仓报告
- 记录重要新闻/公告

## 待安装技能
- find-skills (速率限制中，稍后重试)
- joko-proactive-agent (速率限制中，稍后重试)
- feishu-proactive-messenger (可选)
