# 📘 模擬案件①：複数店舗の売上データを1つに統合し、店舗別集計表を出力

## 🧾 クライアント要件書
全国の複数店舗から日次売上CSVが送られてきます。  
これらを1つにまとめ、店舗別の月次集計表をExcelに出力してほしいです。

---

## 🔧 詳細要件
- データ形式：各店舗ごとに `sales_tokyo.csv`, `sales_osaka.csv` など
- 各ファイルには「日付」「売上」「利益」列がある
- 出力：
  - 1つのExcelファイル（`merged_sales.xlsx`）に店舗別売上・利益を集計
  - シート名：店舗別集計

### 処理内容
1. 各CSVを pandas で読み込み  
2. すべて結合（店舗名列を追加）  
3. 店舗ごと・月ごとに売上・利益を合計  
4. Excelに出力  

---

## 💻 使用技術
- pandas（read_csv, concat, groupby）
- openpyxl（Excel出力）
- glob / os（複数ファイル処理）

## 🧾 出力結果プレビュー
<img width="730" height="470" alt="スクリーンショット 2025-11-12 5 54 49" src="https://github.com/user-attachments/assets/c33e7400-d2ef-4adf-861b-9a94ecf90383" />




