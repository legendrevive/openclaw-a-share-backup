# GitHub 自动备份配置文档

> 创建时间：2026-03-01 22:25  
> 目的：防止版本更新时文件损坏或丢失

---

## 📦 仓库信息

| 项目 | 信息 |
|------|------|
| **仓库地址** | https://github.com/legendrevive/openclaw-a-share-backup |
| **所有者** | legendrevive |
| **描述** | A 股监控系统配置文件和记忆备份 |
| **可见性** | 公开 |

---

## 🔧 配置内容

### 1. 自动备份脚本

**位置：** `/Users/liuyazhou/.openclaw/workspace/scripts/auto-backup.sh`

**功能：**
- 自动提交配置文件和记忆文件
- 推送到 GitHub 仓库
- 记录备份日志

### 2. 定时任务

**执行时间：** 每天 20:30

**Cron 配置：**
```bash
30 20 * * * cd /Users/liuyazhou/.openclaw/workspace && /bin/bash /Users/liuyazhou/.openclaw/workspace/scripts/auto-backup.sh >> /Users/liuyazhou/.openclaw/workspace/backup.log 2>&1
```

### 3. .gitignore 配置

**排除的敏感文件：**
- `openclaw.json`（包含 API Key）
- `skills/imap-smtp-email/.env`（邮箱密码）
- `node_modules/`（依赖包）
- `*.log`（日志文件）
- `*.txt`（临时文件）

**备份的核心文件：**
- ✅ `MEMORY.md` - 长期记忆
- ✅ `memory/YYYY-MM-DD.md` - 每日记忆
- ✅ `HEARTBEAT.md` - 心跳任务配置
- ✅ `stock_watch/*.py` - 监控脚本
- ✅ `scripts/*.sh` - 自动化脚本
- ✅ `skills/*/` - 技能文件（排除 node_modules）
- ✅ 所有 `.md` 文档

---

## 📊 备份统计

| 项目 | 数量 |
|------|------|
| 文件数 | ~900 个 |
| 代码行数 | ~14 万行 |
| 首次备份 | 2026-03-01 22:25 |
| 备份频率 | 每日一次 |

---

## 🎯 备份内容分类

### 核心配置
- ✅ AGENTS.md
- ✅ SOUL.md
- ✅ USER.md
- ✅ TOOLS.md
- ✅ IDENTITY.md
- ✅ HEARTBEAT.md

### 记忆文件
- ✅ MEMORY.md
- ✅ memory/2026-02-28.md
- ✅ memory/2026-03-01.md
- ✅ memory/stock_log.md

### 监控脚本（57 个）
- ✅ stock_monitor.py
- ✅ momentum_report.py
- ✅ morning_recommend.py
- ✅ realtime_t_monitor.py
- ✅ institution_monitor.py
- ✅ ... (更多)

### 自动化脚本
- ✅ auto-backup.sh
- ✅ evomap_daemon.sh
- ✅ evomap_heartbeat.sh
- ✅ evomap_check_invite.sh
- ✅ monitor_daemon.sh

### 技能文件
- ✅ tavily-search/
- ✅ imap-smtp-email/
- ✅ find-skills/
- ✅ proactive-agent/
- ✅ self-improving-agent/
- ✅ evomap/

---

## 📝 手动备份

如需立即备份，执行：

```bash
cd /Users/liuyazhou/.openclaw/workspace
./scripts/auto-backup.sh
```

---

## 📋 查看备份历史

**GitHub 仓库：**
https://github.com/legendrevive/openclaw-a-share-backup/commits/main

**本地日志：**
```bash
tail -20 /Users/liuyazhou/.openclaw/workspace/backup.log
```

---

## ⚠️ 注意事项

1. **敏感信息**：openclaw.json 已排除，不包含 API Key
2. **大文件**：node_modules 已排除，减小仓库体积
3. **日志文件**：*.log 已排除，保持仓库整洁
4. **嵌套 Git**：skills/evolver 已排除，避免冲突

---

## 🔄 恢复数据

如需从 GitHub 恢复：

```bash
cd /Users/liuyazhou/.openclaw/workspace
git clone https://github.com/legendrevive/openclaw-a-share-backup.git backup_restore
cp backup_restore/* ./
```

---

*最后更新：2026-03-01 22:25*
*备份状态：✅ 正常运行*
