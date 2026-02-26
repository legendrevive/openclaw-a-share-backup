#!/usr/bin/env python3
"""
股票监控报告生成
支持：盘中汇报、盘后总结、异动预警
"""

import subprocess
import re
import json
from datetime import datetime

def get_stock_data(code):
    """获取单只股票数据"""
    if code.startswith('6'):
        prefix = 'sh'
    elif code.startswith('0') or code.startswith('3'):
        prefix = 'sz'
    else:
        return None
    
    cmd = f'curl -s "https://qt.gtimg.cn/q={prefix}{code}"'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    
    if not result.stdout:
        return None
    
    try:
        data_str = result.stdout.decode('gbk').strip()
    except:
        data_str = result.stdout.decode('utf-8', errors='ignore').strip()
    
    match = re.search(r'"([^"]*)"', data_str)
    if not match:
        return None
    
    fields = match.group(1).split('~')
    
    if len(fields) < 35:
        return None
    
    try:
        return {
            'code': code,
            'name': fields[1],
            'price': float(fields[3]),
            'open': float(fields[4]),
            'high': float(fields[5]),
            'low': float(fields[34]),
            'volume': int(fields[6]),
            'change': float(fields[31]),
            'change_pct': float(fields[32]),
            'timestamp': fields[30]
        }
    except (ValueError, IndexError):
        return None

def generate_report(stocks, report_type="intraday"):
    """生成报告"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M")
    
    lines = []
    lines.append("📈 A 股监控报告")
    lines.append(f"时间：{date_str}")
    lines.append("=" * 40)
    
    for code, name in stocks:
        data = get_stock_data(code)
        if data:
            change_symbol = "📈" if data['change_pct'] > 0 else "📉" if data['change_pct'] < 0 else "➖"
            lines.append(f"\n{code} {name}")
            lines.append(f"  {data['price']:.2f} {change_symbol} ({data['change_pct']:+.2f}%)")
            if report_type == "detailed":
                lines.append(f"  开：{data['open']:.2f}  高：{data['high']:.2f}  低：{data['low']:.2f}")
                lines.append(f"  量：{data['volume']:,}手")
        else:
            lines.append(f"\n{code} {name} | 获取失败")
    
    lines.append("\n" + "=" * 40)
    
    return "\n".join(lines)

def main():
    stocks = [
        ('603993', '洛阳钼业'),
        ('600111', '北方稀土'),
        ('002413', '雷科防务')
    ]
    
    report = generate_report(stocks, "detailed")
    print(report)

if __name__ == '__main__':
    main()
