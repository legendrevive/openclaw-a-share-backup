# ✅ 股票盯盘系统配置完成！

## 📊 已关注股票

| 股票 | 代码 | 当前价格 | 涨跌幅 |
|------|------|---------|--------|
| 洛阳钼业 | 603993 | ¥23.03 | -2.95% 📉 |
| 北方稀土 | 600111 | ¥59.10 | -2.09% 📉 |
| 雷科防务 | 002413 | ¥14.94 | -0.07% 📉 |

*(以上为初始化时的价格，实时价格请以交易软件为准)*

## ⚙️ 已配置功能

### 1. 定时监控
- **频率**: 每 5 分钟检查一次
- **时段**: 交易日 9:00-11:00, 13:00-15:00
- **方式**: crontab 自动执行

### 2. 价格提醒
- **大幅波动**: 单次检查间隔涨跌超过 5% 时警报
- **目标价格**: 可设置上涨/下跌目标价（需手动配置）

### 3. 日志记录
- 日志文件：`/Users/liuyazhou/.openclaw/workspace/stock_watch/stock_log.txt`
- 查看日志：`tail -f stock_log.txt`

## 🎯 设置目标价格提醒

编辑 `/Users/liuyazhou/.openclaw/workspace/stock_watch/stocks.json`：

```json
{
  "name": "洛阳钼业",
  "code": "603993",
  "market": "SH",
  "target_price_up": 25.00,    // 涨到 25 元时提醒
  "target_price_down": 22.00    // 跌到 22 元时提醒
}
```

## 📱 接收通知

目前监控脚本会记录日志到文件。如需接收飞书通知，请告诉我，我可以配置自动推送。

## 🔧 常用命令

```bash
# 手动检查一次
cd /Users/liuyazhou/.openclaw/workspace/stock_watch
python3 stock_monitor.py

# 查看日志
tail -f stock_log.txt

# 查看定时任务
crontab -l

# 暂停监控
crontab -r

# 恢复监控
crontab /Users/liuyazhou/.openclaw/workspace/stock_watch/crontab.txt
```

## 📁 文件位置

```
/Users/liuyazhou/.openclaw/workspace/stock_watch/
├── stocks.json          # 股票配置
├── stock_monitor.py     # 监控脚本
├── run_check.sh         # 运行脚本
├── crontab.txt          # 定时任务配置
├── last_prices.json     # 上次价格记录（自动生成）
├── stock_log.txt        # 日志文件（自动生成）
└── README.md            # 使用说明
```

---

**配置完成时间**: 2026-02-26

有任何问题随时告诉我！🚀
