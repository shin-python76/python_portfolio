# scraping_tool.py
# 模擬案件④：Webスクレイピング＋Excel出力ツール

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 🔍 解説：
# requests：Webページを取得するためのHTTP通信ライブラリ
# BeautifulSoup：HTMLを解析し、タグ構造から情報を抜き出すためのライブラリ
# pandas：データを表形式に整え、ExcelやCSVに出力するために使用
# os：出力フォルダを自動作成するための標準ライブラリ

# =========================================
# ① スクレイピング対象URL
# =========================================
BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = BASE_URL + "page-1.html"

# 🔍 解説：
# BASE_URL：サイトのベース部分。相対URLを絶対URLに直すために後で使う。
# START_URL：最初のページ（page-1.html）を定義。

# 🧠 なぜわざわざ START_URL を定義するのか？
# 大きく分けて3つの理由があります👇
# ① 「開始地点」を明確にするため（可読性・保守性）
# このスクリプトはページを順番に回っていくタイプ（クローラー）です。
# そのため、「どのページから巡回を始めるか」を 変数として明示 しておくことで、後から見た人にもすぐ理解できるようになります。

# ② 将来的に「開始ページ」を変更しやすくするため
# 仮に次のような変更要件が来た場合──
# 「10ページ目からスクレイピングを始めてほしい」
# START_URL があれば、次のように1行だけ変えればOKです👇
# START_URL = BASE_URL + "page-10.html"

# ③ BASE_URL と組み合わせて「相対URL → 絶対URL」変換に使える
# このサイトでは、各書籍の詳細ページURLが相対パスで記述されています：

# <a href="../../a-light-in-the-attic_1000/index.html">

# このままでは単独でアクセスできませんが、
# BASE_URL と組み合わせることで絶対URLに変換できます👇

# full_url = BASE_URL + relative_url.replace("../../", "")

# ここで、BASE_URL の基準が明確に定義されているからこそ、
# START_URL のようなページ構成を簡単に扱える設計になっているのです。


# =========================================
# ② 出力フォルダ設定
# =========================================
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 🔍 解説：
# os.makedirs()：出力先フォルダが存在しない場合、自動で作成。
# exist_ok=True にしているので、すでに存在していてもエラーにならない。

# =========================================
# ③ 書籍データを格納するリスト
# =========================================
book_data = []

# 🔍 解説：
# book_data：書籍情報を格納するリスト（最終的にExcel出力するための元データ）。

# =========================================
# ④ ページを順に取得
# =========================================
page = 1
while True:
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)

    # ページが存在しない場合（404）で終了
    if response.status_code != 200:
        print(f"ページ{page}は存在しません。終了します。")
        break

    print(f"📖 ページ {page} を取得中...")

    # while True:：明示的にページ数がわからないサイトを「ページが存在しなくなるまで」自動巡回。
    # while True: は「永遠ループ」
    # True は「常に真」なので、条件がずっと満たされ続けます。
    # つまり、プログラムは無限にループします（止まりません）。
    # requests.get()：指定URLにアクセスし、HTMLデータを取得。
    # response.status_code：HTTPレスポンスコード（200＝成功、404＝ページなし）。
    # ページがなくなった時点で break によりループを終了。
    # この構造により、自動的に最終ページまでクロール できます。

    soup = BeautifulSoup(response.text, "html.parser")

    # 🔍 解説：
    # BeautifulSoupの基本構造
    # soup = BeautifulSoup(response.text, "html.parser")
    # → 取得したHTMLを「パース」＝タグ構造を解析して、Pythonで扱える形に。

    # =========================================
    # ⑤ 書籍リストを抽出
    # =========================================
    articles = soup.find_all("article", class_="product_pod")

    # find_all() とタグ探索
    # soup.find_all("article", class_="product_pod")
    # → 書籍情報がまとまっている <article class="product_pod"> タグを全件取得。

    for article in articles:
        title = article.h3.a["title"]
        price = article.find("p", class_="price_color").text.replace("Â", "")
        stock = article.find("p", class_="instock availability").text.strip()
        relative_url = article.h3.a["href"]
        full_url = BASE_URL + relative_url.replace("../../", "")

        book_data.append(
            {"タイトル": title, "価格": price, "在庫": stock, "URL": full_url}
        )

    page += 1

    # 各項目の抽出
    # 取得項目	取得方法	解説
    # タイトル	article.h3.a["title"]	<a>タグの title 属性値を取得
    # 価格	.find("p", class_="price_color").text	<p>タグのテキスト部分を取得
    # 在庫	.find("p", class_="instock availability").text.strip()	空白や改行を削除して整形
    # URL	href 属性 + BASE_URL を結合	相対URLを絶対URLに変換
    # 文字化け対策
    # .replace("Â", "")
    # → 英ポンド記号「£」の前に出る「Â」を削除（文字コードのずれによる表示乱れ）。

    # リストに格納
    # book_data.append({...})
    # → 1冊ごとに辞書形式でリストへ保存。
    # この「辞書のリスト」構造は、後ほど pandas でDataFrame化しやすい形。

    # page += 1
    # 🔍 解説：
    # 1ページ分の処理が終わったら、次のページへ進む。
    # → ページ51まで自動的に繰り返す（50ページで終了）。

# =========================================
# ⑥ DataFrameに整形
# =========================================
df = pd.DataFrame(book_data)

# 🔍 解説：
# book_data（リスト形式）をDataFrameに変換。
# 列名は辞書のキー "タイトル" "価格" "在庫" "URL" がそのまま使われる。
# pandasを使うことで、後続のExcel出力が非常にシンプルになります。

# =========================================
# ⑦ Excelに出力
# =========================================
output_path = os.path.join(output_dir, "scraped_data.xlsx")
df.to_excel(output_path, index=False, engine="openpyxl")

print(f"\n✅ データ取得完了！Excelファイルを出力しました：{output_path}")
print(f"総取得件数：{len(df)} 件")
print(df.head())


# 🔍 解説：
# to_excel()：DataFrameをExcelファイルとして出力。
# index=False：行番号を出力しない（見た目を整えるため）。
# engine="openpyxl"：Excel形式（.xlsx）で保存するためのエンジンを指定。
# len(df)：取得した総データ数をカウント。
# df.head()：先頭5件をコンソールに表示（デバッグや確認用）。
