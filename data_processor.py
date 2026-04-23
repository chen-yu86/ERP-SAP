import pandas as pd
import json

def run_mrp_pipeline(initial_stock=400):
    """
    模擬從 ERP 匯出的大量數據，並使用 Pandas 進行高效運算
    """
    # 1. 模擬 ERP 原始數據 (這部分在實務中會是 pd.read_excel 或 pd.read_sql)
    raw_data = [
        {"date": "2026-05-01", "type": "demand", "qty": 150},
        {"date": "2026-05-02", "type": "demand", "qty": 180},
        {"date": "2026-05-03", "type": "supply", "qty": 700},
        {"date": "2026-05-04", "type": "demand", "qty": 220},
        {"date": "2026-05-05", "type": "demand", "qty": 280},
        {"date": "2026-05-06", "type": "supply", "qty": 450},
        {"date": "2026-05-07", "type": "demand", "qty": 120},
    ]
    
    # 2. 轉化為 Pandas DataFrame (展現處理表格數據的能力)
    df = pd.DataFrame(raw_data)
    
    # 3. 核心 MRP 計算邏輯：將需求設為負值，供應設為正值
    df['adjustment'] = df.apply(lambda x: -x['qty'] if x['type'] == 'demand' else x['qty'], axis=1)
    
    # 4. 關鍵步驟：使用向量化運算 (Cumulative Sum) 取代迴圈，這是 Pandas 的精髓
    # 這就是為什麼 Python 可以秒級處理萬筆資料的原因
    df['projected_balance'] = initial_stock + df['adjustment'].cumsum()
    
    # 5. 自動判斷狀態
    df['status'] = df['projected_balance'].apply(lambda x: "⚠️ SHORTAGE" if x < 0 else "✅ SAFE")
    
    return df

if __name__ == "__main__":
    print("--- [Python Pandas MRP 運算引擎] ---")
    
    # 執行運算
    result_df = run_mrp_pipeline(400)
    
    # 展示運算結果的表格
    print("\n[Step 1] 數據清洗與合併結果：")
    print(result_df[['date', 'type', 'qty', 'projected_balance', 'status']])
    
    # 導出為前端使用的格式
    final_json = result_df.to_json(orient='records', force_ascii=False)
    print("\n[Step 2] 已產出 JSON 數據供 Chart.js 視覺化呈現。")
