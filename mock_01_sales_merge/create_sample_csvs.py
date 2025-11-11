import os
import pandas as pd
from datetime import datetime, timedelta

# 保存先フォルダ
folder_path = "sample_data"
os.makedirs(folder_path, exist_ok=True)

# 店舗リスト
stores = ["tokyo", "osaka", "nagoya"]

# 期間設定（2024年1月1日〜10日）
start_date = datetime(2024, 1, 1)
days = 10

# 各店舗のCSVを作成
for store in stores:
    data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        sales = 10000 + i * 1000 + (stores.index(store) * 500)
        profit = int(sales * 0.2)
        data.append([date.strftime("%Y-%m-%d"), sales, profit])

    df = pd.DataFrame(data, columns=["日付", "売上", "利益"])
    file_path = os.path.join(folder_path, f"sales_{store}.csv")
    df.to_csv(file_path, index=False, encoding="utf-8-sig")

print("✅ サンプルCSVを3店舗分作成しました！")
print(f"保存先フォルダ：{folder_path}")
