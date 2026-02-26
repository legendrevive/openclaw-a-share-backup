#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期货监控脚本 - 监控主要期货品种价格
"""

import urllib.request
import json
from datetime import datetime

# 关注的期货品种
FUTURES_WATCHLIST = [
    # 有色金属
    {"name": "沪铜", "code": "CU2602", "category": "有色金属"},
    {"name": "沪铝", "code": "AL2602", "category": "有色金属"},
    {"name": "沪锌", "code": "ZN2602", "category": "有色金属"},
    {"name": "沪铅", "code": "PB2602", "category": "有色金属"},
    {"name": "沪镍", "code": "NI2602", "category": "有色金属"},
    {"name": "沪锡", "code": "SN2602", "category": "有色金属"},
    
    # 贵金属
    {"name": "沪金", "code": "AU2602", "category": "贵金属"},
    {"name": "沪银", "code": "AG2602", "category": "贵金属"},
    
    # 黑色系
    {"name": "螺纹钢", "code": "RB2602", "category": "黑色系"},
    {"name": "热轧卷板", "code": "HC2602", "category": "黑色系"},
    {"name": "铁矿石", "code": "I2602", "category": "黑色系"},
    {"name": "焦煤", "code": "JM2602", "category": "黑色系"},
    {"name": "焦炭", "code": "J2602", "category": "黑色系"},
    
    # 能源化工
    {"name": "原油", "code": "SC2602", "category": "能源化工"},
    {"name": "燃油", "code": "FU2602", "category": "能源化工"},
    {"name": "PTA", "code": "TA2602", "category": "能源化工"},
    {"name": "甲醇", "code": "MA2602", "category": "能源化工"},
    {"name": "塑料", "code": "L2602", "category": "能源化工"},
    {"name": "PVC", "code": "V2602", "category": "能源化工"},
    
    # 农产品
    {"name": "豆粕", "code": "M2602", "category": "农产品"},
    {"name": "豆油", "code": "Y2602", "category": "农产品"},
    {"name": "棕榈油", "code": "P2602", "category": "农产品"},
    {"name": "玉米", "code": "C2602", "category": "农产品"},
    {"name": "生猪", "code": "LH2602", "category": "农产品"},
]

def get_future_price(code):
    """
    从东方财富获取期货实时价格
    """
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={code}&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f116,f60,f45,f52,f50,f48,f167,f117,f71,f113,f114,f115,f292,f119,f120,f121,f122,f296"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Referer': 'http://quote.eastmoney.com/'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('data'):
                d = data['data']
                return {
                    "name": d.get('f58', ''),
                    "code": code,
                    "current": d.get('f43', 0) / 100,  # 价格转换
                    "change": d.get('f169', 0) / 100,
                    "change_pct": d.get('f170', 0),
                    "open": d.get('f46', 0) / 100,
                    "high": d.get('f44', 0) / 100,
                    "low": d.get('f47', 0) / 100,
                    "prev_close": d.get('f60', 0) / 100,
                    "volume": d.get('f48', 0),
                    "amount": d.get('f50', 0)
                }
    except Exception as e:
        print(f"获取期货 {code} 失败：{e}")
    
    return None

def get_futures_summary():
    """获取期货市场概览"""
    results = {"categories": {}}
    
    for future in FUTURES_WATCHLIST:
        data = get_future_price(future["code"])
        category = future["category"]
        
        if category not in results["categories"]:
            results["categories"][category] = []
        
        if data:
            data["category"] = category
            results["categories"][category].append(data)
        else:
            results["categories"][category].append({
                "name": future["name"],
                "code": future["code"],
                "error": True
            })
    
    return results

def format_futures_report(futures_data):
    """格式化期货报告"""
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"⏰ 期货市场快报 - {timestamp}")
    lines.append("")
    
    for category, items in futures_data["categories"].items():
        # 计算类别整体表现
        up_count = sum(1 for i in items if not i.get("error") and i.get("change_pct", 0) > 0)
        down_count = sum(1 for i in items if not i.get("error") and i.get("change_pct", 0) < 0)
        
        if up_count > down_count:
            category_icon = "📈"
        elif down_count > up_count:
            category_icon = "📉"
        else:
            category_icon = "➖"
        
        lines.append(f"🔹 {category_icon} {category}")
        
        for item in items:
            if item.get("error"):
                lines.append(f"   {item['name']}: 数据暂缺")
            else:
                change_symbol = "📈" if item["change"] >= 0 else "📉"
                change_sign = "+" if item["change"] >= 0 else ""
                lines.append(f"   {item['name']}: {item['current']:.2f} {change_symbol} {change_sign}{item['change_pct']:.2f}%")
        
        lines.append("")
    
    return "\n".join(lines)

def get_related_stocks(futures_category):
    """根据期货类别推荐相关股票"""
    mappings = {
        "有色金属": ["洛阳钼业", "北方稀土", "江西铜业", "云铝股份", "锌业股份"],
        "贵金属": ["山东黄金", "中金黄金", "银泰黄金", "盛达资源"],
        "黑色系": ["宝钢股份", "鞍钢股份", "华菱钢铁", "铁矿石概念"],
        "能源化工": ["中国石油", "中国石化", "恒力石化", "荣盛石化"],
        "农产品": ["牧原股份", "温氏股份", "新希望", "北大荒"],
    }
    return mappings.get(futures_category, [])

def main():
    """主函数"""
    futures_data = get_futures_summary()
    report = format_futures_report(futures_data)
    print(report)
    
    # 分析强势板块
    strong_categories = []
    for category, items in futures_data["categories"].items():
        valid_items = [i for i in items if not i.get("error")]
        if valid_items:
            avg_change = sum(i.get("change_pct", 0) for i in valid_items) / len(valid_items)
            if avg_change > 1:
                strong_categories.append((category, avg_change))
    
    if strong_categories:
        print("\n🔥 强势板块:")
        for cat, avg in sorted(strong_categories, key=lambda x: x[1], reverse=True):
            print(f"   {cat}: 平均 +{avg:.2f}%")
            stocks = get_related_stocks(cat)
            if stocks:
                print(f"   相关股票：{', '.join(stocks[:3])}")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
