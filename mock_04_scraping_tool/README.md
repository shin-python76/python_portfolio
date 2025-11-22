# 📘 模擬案件④：「Webスクレイピング＋Excel出力ツール」

## 🧾 クライアント要件書
指定サイト（例：家電量販店の特価商品一覧）から、商品名・価格・URLを自動取得し、  
Excelファイルに出力するスクリプトを作成してください。

---

## 🔧 詳細要件
- **ターゲットサイト**： [Books to Scrape](https://books.toscrape.com)
- **取得項目**：タイトル／価格／在庫状況／商品URL  
- **出力**：`output/scraped_data.xlsx`  
  - 列構成：タイトル, 価格, 在庫, URL  

---

## 💻 使用技術
| ライブラリ | 用途 |
|-------------|------|
| `requests` | HTMLの取得（HTTP通信） |
| `BeautifulSoup4` | HTML解析（タグ構造から情報抽出） |
| `pandas` | データ整形・Excel出力 |
| `openpyxl` | Excel操作エンジン |

---

## 🧠 主な処理の流れ
1. `requests` で各ページのHTMLを取得  
2. `BeautifulSoup` で書籍タイトル・価格・在庫・URLを抽出  
3. ページがなくなるまで自動巡回（1〜50ページ）  
4. 取得したデータを `pandas.DataFrame` に格納  
5. `to_excel()` でExcel出力（自動でフォルダ生成）

---

## 🧩 出力例（scraped_data.xlsx）

| タイトル | 価格 | 在庫 | URL |
|-----------|------|------|-----|
| A Light in the Attic | £51.77 | In stock | https://books.toscrape.com/... |
| Tipping the Velvet | £53.74 | In stock | https://books.toscrape.com/... |
| Soumission | £50.10 | In stock | https://books.toscrape.com/... |
| Sharp Objects | £47.82 | In stock | https://books.toscrape.com/... |
| Sapiens: A Brief History ... | £54.23 | In stock | https://books.toscrape.com/... |

