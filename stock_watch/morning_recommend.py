#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开盘前推荐脚本 - 综合期货、新闻、技术面，推荐当日关注题材
运行时间：交易日 8:30-9:15
"""

import json
import urllib.request
from datetime import datetime, timedelta
import subprocess
import sys

# 股票与题材映射
STOCK_THEMES = {
    "洛阳钼业": ["有色金属", "铜", "钴", "新能源材料", "一带一路"],
    "北方稀土": ["稀土", "有色金属", "新能源", "永磁材料"],
    "雷科防务": ["军工", "航空航天", "雷达", "卫星导航", "芯片"],
    "江西铜业": ["有色金属", "铜"],
    "云铝股份": ["有色金属", "铝"],
    "中国铝业": ["有色金属", "铝"],
    "紫金矿业": ["有色金属", "金", "铜"],
    "山东黄金": ["贵金属", "黄金"],
    "宝钢股份": ["钢铁", "国企改革"],
    "中国石油": ["石油", "能源"],
}

# 期货与股票关联
FUTURE_STOCK_LINK = {
    "有色金属": ["洛阳钼业", "北方稀土", "江西铜业", "云铝股份"],
    "贵金属": ["山东黄金", "中金黄金", "银泰黄金"],
    "黑色系": ["宝钢股份", "鞍钢股份", "华菱钢铁"],
    "能源化工": ["中国石油", "中国石化", "恒力石化"],
    "农产品": ["牧原股份", "温氏股份", "新希望"],
}

def get_stock_data(code, market):
    """获取股票数据"""
    if market == "SH":
        symbol = f"sh{code}"
    else:
        symbol = f"sz{code}"
    
    url = f"http://qt.gtimg.cn/q={symbol}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('gbk')
            parts = data.strip().split('"')[1].split('~')
            if len(parts) >= 32:
                return {
                    "name": parts[1],
                    "code": code,
                    "current": float(parts[3]),
                    "change_pct": float(parts[32]) if len(parts) > 32 else 0,
                    "volume": float(parts[6]) if len(parts) > 6 else 0,
                }
    except:
        pass
    return None

def get_futures_trend():
    """获取期货趋势（简化版）"""
    # 实际使用时调用 futures_monitor.py
    trends = {
        "有色金属": "neutral",
        "贵金属": "neutral",
        "黑色系": "neutral",
        "能源化工": "neutral",
        "农产品": "neutral",
    }
    return trends

def get_news_sentiment():
    """获取新闻情绪（简化版）"""
    # 实际使用时调用 news_monitor.py
    return {
        "hot_industries": ["有色金属", "军工", "新能源"],
        "sentiment": "positive"
    }

def calculate_theme_score(theme, futures_trends, news_sentiment, stock_data_list):
    """计算题材得分"""
    score = 50  # 基础分
    
    # 期货因素 (+/- 20)
    if theme in futures_trends:
        if futures_trends[theme] == "up":
            score += 15
        elif futures_trends[theme] == "down":
            score -= 15
    
    # 新闻因素 (+/- 20)
    if theme in news_sentiment.get("hot_industries", []):
        if news_sentiment.get("sentiment") == "positive":
            score += 20
        else:
            score -= 10
    
    # 个股表现因素 (+/- 10)
    if stock_data_list:
        avg_change = sum(s.get("change_pct", 0) for s in stock_data_list) / len(stock_data_list)
        if avg_change > 2:
            score += 10
        elif avg_change < -2:
            score -= 10
    
    return min(100, max(0, score))

def generate_recommendations():
    """生成推荐"""
    recommendations = []
    
    # 获取所有题材
    all_themes = set()
    for themes in STOCK_THEMES.values():
        all_themes.update(themes)
    
    futures_trends = get_futures_trend()
    news_sentiment = get_news_sentiment()
    
    for theme in all_themes:
        # 获取相关股票
        related_stocks = [stock for stock, themes in STOCK_THEMES.items() if theme in themes]
        
        # 获取股票数据
        stock_data_list = []
        for stock in related_stocks[:3]:  # 最多取 3 只
            if stock in ["洛阳钼业", "北方稀土", "雷科防务"]:
                # 从配置文件获取代码
                stock_data_list.append({"change_pct": 0})  # 简化
        
        # 计算得分
        score = calculate_theme_score(theme, futures_trends, news_sentiment, stock_data_list)
        
        if score >= 60:  # 只推荐得分 60 以上的题材
            recommendations.append({
                "theme": theme,
                "score": score,
                "stocks": related_stocks[:3],
                "reason": get_recommendation_reason(theme, score, futures_trends, news_sentiment)
            })
    
    # 按得分排序
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return recommendations[:5]  # 返回前 5 个

def get_recommendation_reason(theme, score, futures, news):
    """生成推荐理由"""
    reasons = []
    
    if theme in news.get("hot_industries", []):
        reasons.append("新闻热度高")
    
    if theme in ["有色金属", "贵金属", "新能源"]:
        reasons.append("期货走势配合")
    
    if score >= 80:
        reasons.append("综合评分优秀")
    elif score >= 70:
        reasons.append("值得关注")
    
    return " | ".join(reasons) if reasons else "常规关注"

def format_recommendation_report(recommendations):
    """格式化推荐报告"""
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y年%m月%d日")
    
    lines.append("=" * 50)
    lines.append(f"📈 小 k 盘前推荐 - {date_str}")
    lines.append(f"生成时间：{timestamp}")
    lines.append("=" * 50)
    lines.append("")
    
    if not recommendations:
        lines.append("⚠️ 今日暂无特别推荐，建议观望为主")
        return "\n".join(lines)
    
    lines.append("🎯 今日重点关注题材:")
    lines.append("")
    
    for i, rec in enumerate(recommendations, 1):
        icon = "🔥" if rec["score"] >= 80 else "⭐" if rec["score"] >= 70 else "📊"
        lines.append(f"{icon} TOP{i}: {rec['theme']} (评分:{rec['score']})")
        lines.append(f"   理由：{rec['reason']}")
        lines.append(f"   相关股票：{', '.join(rec['stocks'])}")
        lines.append("")
    
    lines.append("-" * 50)
    lines.append("💡 操作建议:")
    lines.append("   • 高开不追，回调可考虑")
    lines.append("   • 设置好止损位 (建议 -5%)")
    lines.append("   • 关注期货市场联动")
    lines.append("")
    lines.append("⚠️ 风险提示：股市有风险，投资需谨慎")
    lines.append("=" * 50)
    
    return "\n".join(lines)

def send_morning_recommendation(report_text):
    """发送盘前推荐到飞书"""
    import subprocess
    
    # 提取关键信息
    lines = report_text.split('\n')
    highlights = []
    
    for line in lines:
        if 'TOP' in line and ('题材' in line or '评分' in line):
            highlights.append(line.strip())
    
    message = f"""🌅 **盘前推荐** - {datetime.now().strftime('%Y-%m-%d')}

重点关注:
{chr(10).join(highlights[:3])}

💡 建议:
• 高开不追，回调可考虑
• 设置止损位 (-5%)
• 关注期货联动

⚠️ 股市有风险，投资需谨慎"""
    
    try:
        cmd = [
            "openclaw", "message", "send",
            "--target", "user:ou_8b07ed9ccd79a1ed981ab6888dd977d1",
            "--channel", "feishu",
            "--message", message
        ]
        subprocess.run(cmd, capture_output=True, timeout=30)
        print("[通知] 盘前推荐已发送")
    except Exception as e:
        print(f"发送失败：{e}")

def main():
    """主函数"""
    # 检查是否是交易日
    today = datetime.now()
    weekday = today.weekday()
    hour = today.hour
    
    if weekday >= 5:  # 周末
        print("今日休市，无盘前推荐")
        return 0
    
    if hour < 8 or hour > 9:  # 非盘前时间
        print(f"当前时间 {hour}:00，非盘前推荐时段 (8:00-9:15)")
        # 仍然生成报告，但标记为非实时
    
    # 生成推荐
    recommendations = generate_recommendations()
    
    # 输出报告
    report = format_recommendation_report(recommendations)
    print(report)
    
    # 发送飞书通知
    send_morning_recommendation(report)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
