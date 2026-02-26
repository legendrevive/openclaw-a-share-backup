#!/usr/bin/env python3
"""
A 股股票行情数据解析
数据来源：腾讯财经
"""

import subprocess
import re

def get_stock_data(code):
    """获取单只股票数据"""
    # 判断市场
    if code.startswith('6'):
        prefix = 'sh'
    elif code.startswith('0') or code.startswith('3'):
        prefix = 'sz'
    else:
        return None
    
    # 获取数据
    cmd = f'curl -s "https://qt.gtimg.cn/q={prefix}{code}"'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    
    if not result.stdout:
        return None
    
    # 解码 (GBK 编码)
    try:
        data_str = result.stdout.decode('gbk').strip()
    except:
        data_str = result.stdout.decode('utf-8', errors='ignore').strip()
    
    # 提取引号内的数据
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
            'price': float(fields[3]),      # 当前价
            'open': float(fields[4]),       # 开盘
            'high': float(fields[5]),       # 最高
            'volume': int(fields[6]),       # 成交量 (手)
            'low': float(fields[34]),       # 最低
            'change': float(fields[31]),    # 涨跌额
            'change_pct': float(fields[32]), # 涨跌幅%
            'timestamp': fields[30]         # 时间戳
        }
    except (ValueError, IndexError) as e:
        return None

def main():
    stocks = [
        ('603993', '洛阳钼业'),
        ('600111', '北方稀土'),
        ('002413', '雷科防务')
    ]
    
    print("=" * 60)
    print("A 股实时监控")
    print("=" * 60)
    
    for code, name in stocks:
        data = get_stock_data(code)
        if data:
            change_symbol = "📈" if data['change_pct'] > 0 else "📉" if data['change_pct'] < 0 else "➖"
            print(f"\n{code} {name}")
            print(f"  价格：{data['price']:.2f} {change_symbol} ({data['change_pct']:+.2f}%)")
            print(f"  开：{data['open']:.2f}  高：{data['high']:.2f}  低：{data['low']:.2f}")
            print(f"  成交量：{data['volume']:,}手")
        else:
            print(f"\n{code} {name} | 获取失败")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
