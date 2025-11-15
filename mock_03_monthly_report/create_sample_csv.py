import pandas as pd
import random
import os

# ==================================================
# 📘 模擬案件③：ダミー月次売上データ生成スクリプト
# ==================================================

# 出力フォルダを指定
output_folder = "sample_data"
os.makedirs(output_folder, exist_ok=True)

# 出力ファイルパス
output_file = os.path.join(output_folder, "monthly_sales.csv")

# 月ごとの売上・利益データをランダム生成
months = list(range(1, 13))
sales = [random.randint(80000, 200000) for _ in months]
profits = [int(s * random.uniform(0.15, 0.25)) for s in sales]  # 売上の15〜25%

# DataFrame化
df = pd.DataFrame({"月": months, "売上": sales, "利益": profits})

# CSVとして出力
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("✅ ダミー月次売上データを作成しました！")
print(f"📂 出力ファイル：{output_file}")
