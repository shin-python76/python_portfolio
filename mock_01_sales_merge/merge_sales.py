import pandas as pd
import os
import glob

# pandas：CSVの読み込み・集計・出力を担当。
# os：ファイルパス操作に使用（WindowsでもMacでも安全に動作）。
# glob：特定パターンのファイルをまとめて取得（今回は sales_*.csv）。

# 📁 サンプルデータの格納フォルダ
folder_path = "sample_data"

# 🔍 sample_data 内の全CSVファイルを取得
csv_files = glob.glob(os.path.join(folder_path, "sales_*.csv"))

# os.path.join() で安全にパスを生成（OS差異を吸収）。
# glob.glob() で、sample_data 内の「sales_」で始まるCSVをすべて取得。

print(f"対象ファイル数: {len(csv_files)} 件")

# すべてのCSVを格納するリスト
dataframes = []

# 📖 各CSVを読み込み、店舗名列を追加してリストに保存
for file in csv_files:
    df = pd.read_csv(file)
    store_name = os.path.basename(file).replace("sales_", "").replace(".csv", "")
    df["店舗名"] = store_name
    dataframes.append(df)

# pd.read_csv()：CSV → DataFrame に読み込み。
# os.path.basename()：ファイル名だけを抽出（例：sales_tokyo.csv）。
# .replace()：不要な文字を除いて「tokyo」「osaka」などの店舗名を抽出。
# df["店舗名"] = store_name：新しい列を追加。

# 🧩 すべてのデータを結合
merged_df = pd.concat(dataframes, ignore_index=True)

# pd.concat() は「リストに格納したDataFrameを1つにまとめる」関数。
# ignore_index=True により、インデックスを再付番（0, 1, 2, ...）にリセット。
# 🧩 これで3店舗分のデータが1つの大きな表になります。

# 📅 日付列をdatetime型に変換し、「月」列を追加
merged_df["日付"] = pd.to_datetime(merged_df["日付"])
merged_df["月"] = merged_df["日付"].dt.month

# pd.to_datetime()：文字列の日付を「日付型」に変換。
# .dt.month：日付から「月だけ」を抽出（例：1月なら「1」）。
# 🧩 これにより、月ごと集計が可能になります。

# 📊 店舗別・月別に売上と利益を集計
summary = (
    merged_df.groupby(["店舗名", "月"], as_index=False)[["売上", "利益"]]
    .sum()
    .sort_values(["店舗名", "月"])
)

# groupby()：指定列（店舗名と月）でグループ化。
# [["売上", "利益"]]：対象列を限定。
# .sum()：グループごとに合計を計算。
# .sort_values()：店舗名・月順に並び替え。

# 💾 Excelに出力
output_file = "merged_sales.xlsx"
summary.to_excel(output_file, index=False, sheet_name="店舗別集計")

# to_excel()：DataFrame → Excelファイルに変換。
# index=False：行番号を出力しない。
# sheet_name="店舗別集計"：Excelシート名を指定。

print("✅ 結合・集計が完了しました！")
print(f"出力ファイル：{output_file}")
