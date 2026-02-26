#!/usr/bin/env python3
"""
A 股股票分析模块
功能：技术分析、资金流向、异动检测
"""

import subprocess
import re
import json
from datetime import datetime

# 自选股列表
STOCKS = [
    {'code': '603993', 'name': '洛阳钼业', 'industry': '有色金属'},
    {'code': '600111', 'name': '北方稀土', 'industry': '稀土'},
    {'code': '002413', 'name': '雷科防务', 'industry': '军工'}
]

# 异动阈值
ALERT_THRESHOLD = 5.0  # 涨跌幅超过±5% 预警

def get_stock_data(codes):
    """批量获取股票数据"""
    stocks_data = []
    
    for code in codes:
        if code.startswith('6'):
            prefix = 'sh'
        elif code.startswith('0') or code.startswith('3'):
            prefix = 'sz'
        else:
            continue
        
        cmd = f'curl -s "https://qt.gtimg.cn/q={prefix}{code}"'
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        if not result.stdout:
            continue
        
        try:
            data_str = result.stdout.decode('gbk').strip()
        except:
            data_str = result.stdout.decode('utf-8', errors='ignore').strip()
        
        match = re.search(r'"([^"]*)"', data_str)
        if not match:
            continue
        
        fields = match.group(1).split('~')
        if len(fields) < 35:
            continue
        
        try:
            stock = {
                'code': fields[2],
                'name': fields[1],
                'price': float(fields[3]),
                'open': float(fields[4]),
                'high': float(fields[5]),
                'low': float(fields[34]),
                'volume': int(fields[6]),
                'change': float(fields[31]),
                'change_pct': float(fields[32]),
                'pre_close': float(fields[33]) if len(fields) > 33 else 0,
                'timestamp': fields[30] if len(fields) > 30 else ''
            }
            stocks_data.append(stock)
        except (ValueError, IndexError):
            continue
    
    return stocks_data

def analyze_stock(stock):
    """单只股票分析"""
    analysis = {
        'code': stock['code'],
        'name': stock['name'],
        'price': stock['price'],
        'change_pct': stock['change_pct'],
        'signals': [],
        'rating': '中性'
    }
    
    # 涨跌幅分析
    if stock['change_pct'] > 5:
        analysis['signals'].append('🔥 大涨超 5%')
        analysis['rating'] = '强势'
    elif stock['change_pct'] > 2:
        analysis['signals'].append('📈 上涨')
        analysis['rating'] = '偏强'
    elif stock['change_pct'] < -5:
        analysis['signals'].append('❄️ 大跌超 5%')
        analysis['rating'] = '弱势'
    elif stock['change_pct'] < -2:
        analysis['signals'].append('📉 下跌')
        analysis['rating'] = '偏弱'
    else:
        analysis['signals'].append('➖ 震荡')
    
    # 开盘分析
    open_ratio = (stock['open'] - stock['pre_close']) / stock['pre_close'] * 100 if stock['pre_close'] > 0 else 0
    if open_ratio > 2:
        analysis['signals'].append('⬆️ 高开')
    elif open_ratio < -2:
        analysis['signals'].append('⬇️ 低开')
    
    # 振幅分析
    amplitude = (stock['high'] - stock['low']) / stock['pre_close'] * 100 if stock['pre_close'] > 0 else 0
    if amplitude > 5:
        analysis['signals'].append('📊 高振幅')
    
    # 成交量分析 (简化版，需要历史数据对比)
    if stock['volume'] > 5000000:
        analysis['signals'].append('💰 放量')
    
    return analysis

def check_alerts(stocks_data):
    """检查异动预警"""
    alerts = []
    for stock in stocks_data:
        if abs(stock['change_pct']) >= ALERT_THRESHOLD:
            alerts.append({
                'code': stock['code'],
                'name': stock['name'],
                'price': stock['price'],
                'change_pct': stock['change_pct'],
                'type': '大涨' if stock['change_pct'] > 0 else '大跌'
            })
    return alerts

def generate_analysis_report():
    """生成分析报告"""
    codes = [s['code'] for s in STOCKS]
    stocks_data = get_stock_data(codes)
    
    report = []
    report.append("=" * 60)
    report.append("📊 A 股智能分析报告")
    report.append(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 60)
    
    alerts = check_alerts(stocks_data)
    
    for stock in stocks_data:
        analysis = analyze_stock(stock)
        
        report.append(f"\n{analysis['code']} {analysis['name']} ({analysis['rating']})")
        report.append(f"  价格：{analysis['price']:.2f} ({analysis['change_pct']:+.2f}%)")
        
        for signal in analysis['signals']:
            report.append(f"  • {signal}")
    
    if alerts:
        report.append("\n" + "=" * 60)
        report.append("🚨 异动预警")
        for alert in alerts:
            report.append(f"  {alert['code']} {alert['name']} {alert['type']} {alert['change_pct']:+.2f}%")
    
    report.append("\n" + "=" * 60)
    
    return "\n".join(report)

if __name__ == '__main__':
    report = generate_analysis_report()
    print(report)
