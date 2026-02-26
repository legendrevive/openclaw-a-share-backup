# 📈 小 k 股票监控系统 - 完整版

## 🎯 功能概览

| 功能 | 说明 | 运行时间 |
|------|------|----------|
| 📊 股票盯盘 | 监控洛阳钼业、北方稀土、雷科防务实时价格 | 交易日 9:00-15:00 |
| 🏭 期货监控 | 跟踪有色金属、贵金属、黑色系等期货 | 交易日 8:30-15:30 |
| 📰 行业动态 | 抓取财经新闻，分析行业热点 | 每日 7:00-22:00 |
| 🌅 盘前推荐 | 综合期货、新闻、技术面推荐题材 | 交易日 8:30 |
| 📉 收盘总结 | 自动生成收盘报告 | 交易日 15:30 |

---

## 📋 已关注股票

| 股票 | 代码 | 题材 |
|------|------|------|
| 洛阳钼业 | 603993 | 有色金属、铜、钴、新能源 |
| 北方稀土 | 600111 | 稀土、有色金属、永磁 |
| 雷科防务 | 002413 | 军工、航空航天、芯片 |

---

## 🏆 期货监控品种

### 有色金属
沪铜、沪铝、沪锌、沪铅、沪镍、沪锡

### 贵金属
沪金、沪银

### 黑色系
螺纹钢、热轧卷板、铁矿石、焦煤、焦炭

### 能源化工
原油、燃油、PTA、甲醇、塑料、PVC

### 农产品
豆粕、豆油、棕榈油、玉米、生猪

---

## ⚙️ 配置文件

### stocks.json - 股票配置
```json
{
  "stocks": [
    {
      "name": "洛阳钼业",
      "code": "603993",
      "market": "SH",
      "target_price_up": 25.00,
      "target_price_down": 22.00
    }
  ]
}
```

### crontab.txt - 定时任务
编辑后运行：`crontab /Users/liuyazhou/.openclaw/workspace/stock_watch/crontab.txt`

---

## 📂 文件结构

```
stock_watch/
├── stocks.json           # 股票配置
├── stock_monitor.py      # 股票监控脚本
├── futures_monitor.py    # 期货监控脚本
├── news_monitor.py       # 新闻监控脚本
├── morning_recommend.py  # 盘前推荐脚本
├── run_check.sh          # 运行脚本
├── crontab.txt           # 定时任务配置
├── last_prices.json      # 上次价格（自动生成）
├── stock_log.txt         # 股票日志（自动生成）
├── futures_log.txt       # 期货日志（自动生成）
├── news_log.txt          # 新闻日志（自动生成）
├── morning_log.txt       # 推荐日志（自动生成）
├── README_FULL.md        # 完整说明（本文件）
└── SETUP_COMPLETE.md     # 快速入门
```

---

## 🔧 常用命令

```bash
# 手动检查股票
cd /Users/liuyazhou/.openclaw/workspace/stock_watch
python3 stock_monitor.py

# 查看期货
python3 futures_monitor.py

# 查看新闻
python3 news_monitor.py

# 生成盘前推荐
python3 morning_recommend.py

# 查看日志
tail -f stock_log.txt
tail -f futures_log.txt
tail -f news_log.txt

# 查看定时任务
crontab -l

# 暂停所有监控
crontab -r

# 恢复监控
crontab /Users/liuyazhou/.openclaw/workspace/stock_watch/crontab.txt
```

---

## 📱 飞书通知 ✅

**已启用！** 你将自动收到以下通知：

| 通知类型 | 触发条件 | 发送时间 |
|---------|---------|---------|
| 🚨 价格警报 | 涨跌幅≥5% 或达到目标价 | 实时 |
| 🌅 盘前推荐 | 每日自动生成 | 交易日 8:30 |
| 📊 收盘总结 | 每日收盘后 | 交易日 15:30 |

详细说明见 `NOTIFY_CONFIG.md`

---

## 💡 使用建议

1. **盘前（8:30-9:15）**: 查看 `morning_recommend.py` 生成的推荐
2. **盘中（9:30-15:00）**: 关注股票和期货实时监控
3. **收盘后（15:30+）**: 查看收盘总结，复盘当日表现
4. **晚间（20:00+）**: 浏览新闻，了解行业动态

---

## ⚠️ 风险提示

- 本系统仅供参考，不构成投资建议
- 股市有风险，投资需谨慎
- 期货数据可能有延迟，以交易所为准
- 新闻分析为自动抓取，请自行判断

---

**小 k 📈** - 你的股票推荐助手
最后更新：2026-02-26
