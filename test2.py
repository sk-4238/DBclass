import psycopg2
import os
from dotenv import load_dotenv
import datetime
# .env ファイルを読み込む
load_dotenv()
database_url = os.getenv('database_url')
# 返却処理関数
def return_dvd(self):
    try:
        # 商品IDを入力
        product_id = input("返却する商品IDを入力してください: ")
        # 商品情報を取得
        cursor.execute("SELECT タイトル, 貸出状況 FROM 商品 WHERE 商品ID = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            print("エラー: 指定された商品IDは存在しません。")
            return
        title, rental_status = product
        # 貸出中か確認
        if rental_status == 0:
            print(f"エラー: '{title}' は貸し出されていません。")
            return
        # 現在の日付を取得
        return_date = datetime.datetime.now().strftime("%Y-%m-%d")
        # データベースを更新（返却情報を反映）
        cursor.execute("""
            UPDATE 商品
            SET 貸出・返却日 = %s, 貸出状況 = 0, 貸出会員 = '0000'
            WHERE 商品ID = %s
        """, (return_date, product_id))
        # 変更を確定
        connection.commit()
        print(f"'{title}' を返却しました。")
    except Exception as e:
        print(f"エラー: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
# メイン処理
if __name__ == "__main__":
    return_dvd()