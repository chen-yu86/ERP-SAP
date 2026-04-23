import json

# 模擬從 ERP (如 SAP) 匯出的原始大數據
raw_erp_data = [
    {"date": "2026-05-01", "type": "demand", "qty": 120},
    {"date": "2026-05-03", "type": "supply", "qty": 600},
    # ... 假設有成千上萬筆數據
]

def calculate_mrp_logic(initial_stock, data):
    """
    這是一個模擬物料需求計劃 (MRP) 的核心演算法
    展現 Python 處理邏輯與自動化的能力
    """
    stock_trend = []
    current_stock = initial_stock
    
    # 這裡可以加入更複雜的邏輯，例如安全庫存預警、前置時間(Lead Time)計算
    for entry in data:
        if entry['type'] == 'demand':
            current_stock -= entry['qty']
        else:
            current_stock += entry['qty']
        
        stock_trend.append({
            "date": entry['date'],
            "balance": current_stock,
            "status": "Shortage" if current_stock < 0 else "Safe"
        })
    
    return stock_trend

if __name__ == "__main__":
    # 執行計算並產出結果
    result = calculate_mrp_logic(350, raw_erp_data)
    
    # 將結果導出，這可以被前端 Chart.js 讀取
    print("計算完成，產出數據：")
    print(json.dumps(result, indent=2))
