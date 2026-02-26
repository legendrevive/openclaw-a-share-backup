#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业动态监控脚本 - 抓取财经新闻和行业政策
"""

import urllib.request
import json
import re
from datetime import datetime, timedelta

# 关注的行业关键词
INDUSTRY_KEYWORDS = [
    "有色金属", "稀土", "锂电池", "新能源", "半导体", "芯片",
    "人工智能", "AI", "机器人", "军工", "防务", "航空航天",
    "钢铁", "煤炭", "石油", "化工", "农业", "养殖",
    "医药", "医疗", "消费", "白酒", "金融", "券商",
    "房地产", "基建", "一带一路", "国企改革"
]

# 新闻源配置
NEWS_SOURCES = [
    {
        "name": "东方财富",
        "url": "https://news-api.eastmoney.com/News/GetNewsListByWeb?callback=jQuery&pageSize=20&pageIndex=1&newType=0",
        "enabled": False  # 需要动态解析，暂时禁用
    },
    {
        "name": "同花顺",
        "url": "http://news.10jqka.com.cn/",
        "enabled": False
    }
]

def get_financial_news(limit=20):
    """
    获取财经新闻（使用简化方法）
    """
    news_list = []
    
    # 模拟新闻数据（实际使用时可以接入真实 API）
    # 这里提供一个框架，用户可以配置自己的新闻源
    try:
        # 尝试获取新浪财经新闻
        url = "https://feeds.finance.sina.cn/api/feed?channel=finance&num=20"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('result'):
                for item in data['result'][:limit]:
                    news_list.append({
                        "title": item.get('title', ''),
                        "time": item.get('ctime', ''),
                        "url": item.get('url', ''),
                        "source": "新浪财经"
                    })
    except Exception as e:
        print(f"获取新闻失败：{e}")
        # 返回示例数据
        news_list = get_sample_news()
    
    return news_list

def get_sample_news():
    """返回示例新闻（当 API 不可用时）"""
    return [
        {"title": "有色金属板块走强 机构看好铜铝价格", "time": "08:30", "source": "财经新闻", "url": ""},
        {"title": "稀土价格指数继续上涨 多家企业上调报价", "time": "08:15", "source": "财经新闻", "url": ""},
        {"title": "军工板块消息面活跃 多股涨停", "time": "07:50", "source": "财经新闻", "url": ""},
        {"title": "新能源汽车销量超预期 产业链受益", "time": "07:30", "source": "财经新闻", "url": ""},
    ]

def filter_by_keywords(news_list, keywords):
    """根据关键词筛选新闻"""
    filtered = []
    for news in news_list:
        title = news.get("title", "").lower()
        for keyword in keywords:
            if keyword.lower() in title:
                news["matched_keyword"] = keyword
                filtered.append(news)
                break
    return filtered

def analyze_news_sentiment(news_list):
    """简单分析新闻情绪"""
    positive_words = ["上涨", "走强", "利好", "突破", "创新高", "超预期", "受益", "涨停"]
    negative_words = ["下跌", "走弱", "利空", "跌破", "新低", "低于预期", "亏损", "跌停"]
    
    results = {"positive": [], "negative": [], "neutral": []}
    
    for news in news_list:
        title = news.get("title", "")
        score = 0
        for word in positive_words:
            if word in title:
                score += 1
        for word in negative_words:
            if word in title:
                score -= 1
        
        if score > 0:
            results["positive"].append(news)
        elif score < 0:
            results["negative"].append(news)
        else:
            results["neutral"].append(news)
    
    return results

def format_news_report(news_list, sentiment_results):
    """格式化新闻报告"""
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"📰 行业动态简报 - {timestamp}")
    lines.append("")
    
    # 情绪统计
    pos_count = len(sentiment_results["positive"])
    neg_count = len(sentiment_results["negative"])
    neu_count = len(sentiment_results["neutral"])
    
    if pos_count > neg_count:
        sentiment_icon = "🟢 偏多"
    elif neg_count > pos_count:
        sentiment_icon = "🔴 偏空"
    else:
        sentiment_icon = "🟡 中性"
    
    lines.append(f"整体情绪：{sentiment_icon} (利好:{pos_count} 利空:{neg_count} 中性:{neu_count})")
    lines.append("")
    
    # 重要新闻
    lines.append("📌 重点关注:")
    for i, news in enumerate(news_list[:10], 1):
        icon = "✅" if news in sentiment_results["positive"] else ("❌" if news in sentiment_results["negative"] else "•")
        time_str = news.get("time", "")[:5] if news.get("time") else ""
        lines.append(f"   {icon} [{time_str}] {news.get('title', '无标题')}")
    
    lines.append("")
    
    # 按行业分类
    lines.append("🏭 行业分布:")
    industry_count = {}
    for news in news_list:
        keyword = news.get("matched_keyword", "其他")
        industry_count[keyword] = industry_count.get(keyword, 0) + 1
    
    for industry, count in sorted(industry_count.items(), key=lambda x: x[1], reverse=True)[:5]:
        lines.append(f"   {industry}: {count}条")
    
    return "\n".join(lines)

def main():
    """主函数"""
    # 获取新闻
    news_list = get_financial_news()
    
    # 筛选相关行业新闻
    filtered_news = filter_by_keywords(news_list, INDUSTRY_KEYWORDS)
    
    # 如果没有筛选结果，使用全部新闻
    if not filtered_news:
        filtered_news = news_list[:10]
    
    # 分析情绪
    sentiment = analyze_news_sentiment(filtered_news)
    
    # 输出报告
    report = format_news_report(filtered_news, sentiment)
    print(report)
    
    # 输出热点行业
    if filtered_news:
        print("\n🔥 今日热点:")
        industry_count = {}
        for news in filtered_news:
            keyword = news.get("matched_keyword", "其他")
            industry_count[keyword] = industry_count.get(keyword, 0) + 1
        
        hot_industries = sorted(industry_count.items(), key=lambda x: x[1], reverse=True)[:5]
        for industry, count in hot_industries:
            print(f"   {industry}: {count}条新闻")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
