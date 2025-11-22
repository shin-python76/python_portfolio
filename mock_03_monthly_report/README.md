# 📘 模擬案件③：グラフ付き月報レポート自動生成

## 🧾 クライアント要件書
月次売上データをもとに、グラフ付きのExcel月報を自動で作成してほしいです。

---

## 🔧 詳細要件
- 入力：`monthly_sales.csv`
- 処理内容：
    1. 月別売上集計（pandas）
    2. 棒グラフ作成（matplotlib）
    3. openpyxlでグラフをExcelに貼り付け
- 出力：`monthly_report.xlsx`（グラフ＋表形式）

---

## 💻 使用技術
- pandas（集計）
- matplotlib（グラフ作成）
- openpyxl.drawing（画像貼り付け）

---

## 🧾 出力結果プレビュー
<img width="1016" height="623" alt="スクリーンショット 2025-11-22 10 30 49" src="https://github.com/user-attachments/assets/17e1e1f0-ced4-467d-b0c9-841a616390c2" />
