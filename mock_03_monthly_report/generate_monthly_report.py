import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import os

# ==================================================
# 📘 模擬案件③：グラフ付き月報レポート自動生成スクリプト
# ==================================================

# 入力CSVと出力先設定
input_file = "sample_data/monthly_sales.csv"
output_file = "monthly_report.xlsx"
graph_image = "monthly_sales_chart.png"

# graph_image: 一時的にグラフを画像化してExcelへ貼り付けるための中間ファイル。

# ✅ Macで日本語フォントを設定
plt.rcParams["font.family"] = "Hiragino Maru Gothic Pro"

# plt.rcParams: グラフ全体のフォント設定。Macでは日本語対応の "Hiragino Maru Gothic Pro" を使用。
# Windowsなら "MS Gothic" にすればOKです。
# rcParams（読み方：アールシー・パラメータズ）は、matplotlib全体の「設定（デフォルトスタイル）」を制御する辞書オブジェクトです。
# Wordでいう「標準フォント」や「段落設定」みたいな役割ですね。
# 一度設定すると、以降に描くすべてのグラフに自動で反映されます。

# --------------------------------------------------
# ① CSV読み込み
# --------------------------------------------------
df = pd.read_csv(input_file)
print("✅ CSVファイルを読み込みました")

# --------------------------------------------------
# ② 棒グラフ作成（matplotlib）
# --------------------------------------------------
plt.figure(figsize=(8, 5))
plt.bar(df["月"], df["売上"], color="skyblue")
plt.title("月別売上推移", fontsize=14)
plt.xlabel("月", fontsize=12)
plt.ylabel("売上（円）", fontsize=12)
plt.tight_layout()

# plt.figure(figsize=(8, 5))
# → グラフの描画領域を横8インチ×縦5インチに設定。

# plt.bar(df["月"], df["売上"])
# → 月をX軸、売上をY軸とした棒グラフを作成。

# plt.title / xlabel / ylabel
# → グラフにタイトル・軸ラベルを付与。

# plt.tight_layout()
# → ラベルやタイトルがはみ出ないようにレイアウトを自動調整。

# 📌 デザイン的ポイント
# カラーは "skyblue" にして柔らかく見せる（ビジネス資料向け）。
# フォントサイズを明示することで、Excel上でも視認性を確保。


# 画像ファイルとして保存
plt.savefig(graph_image)
plt.close()
print("📈 グラフ画像を作成しました")

# 📘 ここでは一時ファイルを作成
# matplotlibが描画したグラフをPNG形式で出力。
# この画像を後でopenpyxl経由でExcelに貼り付けます。

# 📌 補足
# plt.close() でメモリ解放。次のグラフ描画に影響しないようにします。


# --------------------------------------------------
# ③ openpyxlでExcel出力
# --------------------------------------------------
wb = Workbook()
ws = wb.active
ws.title = "月次レポート"

# 📗 openpyxlの基本操作
# Workbook()：新しいExcelファイル（ワークブック）を作成。
# .active：デフォルトのシートを選択。
# .title：シート名を変更。

# 見出しを追加
ws.append(["月", "売上", "利益"])

# データをExcelに書き込み
for _, row in df.iterrows():
    ws.append(row.tolist())

# 📘 処理の流れ
# .append() は1行分のリストを追加するメソッド。
# 最初の行でヘッダを追加。
# pandasの .iterrows() でDataFrameを1行ずつ取り出してExcelに追記。

# 📌 ポイント
# row.tolist() はSeries（行データ）をリスト化してExcelに渡せるように変換。
# 自動的にA1から順番に埋まります。

# グラフ画像を貼り付け
if os.path.exists(graph_image):
    img = Image(graph_image)
    img.width = 480
    img.height = 300
    ws.add_image(img, "E2")  # 貼り付け位置（セル）

# 📊 処理内容
# os.path.exists() で画像ファイルが存在するか確認。
# Image() でopenpyxl用の画像オブジェクトに変換。
# サイズ指定（ピクセル単位）。
# E2 セルを起点に貼り付け。

# 📌 実務的なポイント
# クライアントに渡すExcelでは、img.width と img.height を指定して整った見た目に。
# グラフの位置を「E2」に固定することで、表と重ならず綺麗に配置。

# 保存
wb.save(output_file)
print("💾 Excelファイルを出力しました！")
print(f"📂 出力先：{output_file}")

# --------------------------------------------------
# ④ 後処理（画像ファイルを削除してクリーンアップ）
# --------------------------------------------------
if os.path.exists(graph_image):
    os.remove(graph_image)
    print("🧹 一時画像ファイルを削除しました")

print("✅ グラフ付き月報レポートの作成が完了しました！")

# 📘 役割
# .save() でExcelファイルを保存。
# 一時ファイル（PNG）を削除して作業フォルダをクリーンに保つ。
# コンソール出力で処理完了を明示。

# 📌 実務視点のポイント
# こうした「削除処理」や「ログ出力」があることで、
# クライアントにとって安心できる“信頼性のあるスクリプト”になります。
