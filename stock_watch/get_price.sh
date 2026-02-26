#!/bin/bash
# 获取 A 股股票行情数据
# 数据来源：腾讯财经

get_stock_price() {
    local code=$1
    local prefix=""
    
    # 判断市场
    if [[ $code == 6* ]]; then
        prefix="sh"
    elif [[ $code == 0* || $code == 3* ]]; then
        prefix="sz"
    fi
    
    # 获取数据
    curl -s "https://qt.gtimg.cn/q=${prefix}${code}" | grep -o '"[^"]*"' | tr -d '"'
}

# 测试
echo "=== 洛阳钼业 (603993) ==="
get_stock_price "603993"

echo ""
echo "=== 北方稀土 (600111) ==="
get_stock_price "600111"

echo ""
echo "=== 雷科防务 (002413) ==="
get_stock_price "002413"
