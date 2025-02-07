import psycopg2
import os
from dotenv import load_dotenv
import datetime
from dateutil.relativedelta import relativedelta
# .env ファイルを読み込む
load_dotenv()
database_url = os.getenv('database_url')
# Retクラスを先に定義
class Product_search_update_delete():
    def __init__(self, user_input, cursor):
        self.cursor = cursor
        self.today = datetime.date.today()
        self.goodsid = user_input
        self.商品ID = None  # 商品IDに変更
        self.タイトル = None
        self.ジャンル = None
        self.発売日 = None
        self.貸出・返却日 = None  # 貸出返却日を貸出・返却日に変更
        self.貸出会員 = None  # 修正: 貸出会員ID → 貸出会員
        self.貸出状況 = None
        self.貸出回数 = None
        self.保管場所 = None
        self.status = None
        self.new_or_old = None
        self.title=None
        self.genre=None
        self.release_date=None
        self.return_date=None
        self.loan_member=None
        self.loan_status=None
        self.loan_count=None
        self.storage=None
        
    def search(self):
        # 商品IDを使って商品の情報を取得する
        self.cursor.execute("""
            SELECT 商品ID, タイトル, ジャンル, 発売日, 貸出・返却日, 貸出会員,
                   貸出状況, 貸出回数, 保管場所
            FROM 商品
            WHERE 商品ID = %s
        """, (self.goodsid,))
        result = self.cursor.fetchone()
        if result:
            self.商品ID, self.タイトル, self.ジャンル, self.発売日, self.貸出・返却日, \
            self.貸出会員, self.貸出状況, self.貸出回数, self.保管場所 = result
            self.isNew()  # 新作か旧作かを判定
            # 情報を表示
            status = "返却可" if self.貸出状況 == 0 else "貸出不可"
            print(f"商品ID: {self.商品ID}, タイトル: {self.タイトル}, ジャンル: {self.ジャンル}, "
                  f"発売日: {self.発売日}, 貸出・返却日: {self.貸出・返却日}, 貸出会員: {self.貸出会員}, "
                  f"貸出状況: {status}, 貸出回数: {self.貸出回数}, 保管場所: {'店頭' if self.保管場所 == 0 else '倉庫'}")
                  
            while True:
                print("\n選択してください: 1: 編集, 2: 削除, 0: 戻る")
                choice = input("番号を入力: ")
                if choice == "1":
                    self.Update()
                elif choice == "2":
                    self.Delete()
                elif choice == "0":
                    break            
                else:
                    print("商品が見つかりませんでした。")

    def isNew(self):
        # 新作か旧作かを判定
        six_months_ago = self.today - relativedelta(months=6)
        if self.発売日 < six_months_ago:
            self.new_or_old = "OLD"
        else:
            self.new_or_old = "NEW"

    def Update(self):
        print("編集したい情報を入力してください。変更しない場合はそのままEnterを押してください。")
        self.title = input("タイトルを変更する場合は入力してください: ")
        self.genre = input("ジャンルを変更する場合は入力してください: ")
        self.release_date = input("発売日を変更する場合は入力してください (YYYY-MM-DD): ")
        self.return_date = input("貸出・返却日を変更する場合は入力してください (YYYY-MM-DD): ")
        self.loan_member = input("貸出会員を変更する場合は入力してください: ")
        # 貸出状況（0または1の入力を強制。空白ならスキップ）
        self.loan_status = self.get_input_int("貸出状況を変更する場合は入力してください (0: 貸出可能, 1: 貸出不可)。空白でスキップ: ", allow_empty=True)
        self.loan_count = input("貸出回数を変更する場合は入力してください: ")
        # 保管場所（0または1の入力を強制。空白ならスキップ）
        self.storage = self.get_input_int("保管場所を変更する場合は入力してください (0: 店頭, 1: 倉庫)。空白でスキップ: ", allow_empty=True)
        # 入力が空でない場合にのみ情報を更新
        self.edit_product_info()

    # 商品情報を編集する関数
    def edit_product_info(self):
        try:
            #connection = psycopg2.connect(database_url, sslmode='require')
            #cursor = connection.cursor()
            # 更新する項目がある場合のみ、UPDATE文を動的に作成
            self.update_query = "UPDATE 商品 SET "
            self.update_values = []
            if self.title:
                self.update_query += "タイトル = %s, "
                self.update_values.append(self.title)
            if self.genre:
                self.update_query += "ジャンル = %s, "
                self.update_values.append(self.genre)
            if self.release_date:
                self.update_query += "発売日 = %s, "
                self.update_values.append(self.release_date)
            if self.return_date:
                self.update_query += "貸出・返却日 = %s, "
                self.update_values.append(self.return_date)
            if self.loan_member:
                self.update_query += "貸出会員 = %s, "
                self.update_values.append(self.loan_member)
            if self.loan_status is not None:
                self.update_query += "貸出状況 = %s, "
                self.update_values.append(self.loan_status)
            if self.loan_count is not None:
                self.update_query += "貸出回数 = %s, "
                self.update_values.append(self.loan_count)
            if self.storage is not None:
                self.update_query += "保管場所 = %s, "
                self.update_values.append(self.storage)
            # クエリの末尾の余分なカンマを削除
            self.update_query = self.update_query.rstrip(', ')
            # 商品IDをWHERE句に追加
            self.update_query += " WHERE 商品ID = %s"
            self.update_values.append(self.goodsid)
            # クエリを実行
            self.cursor.execute(self.update_query, tuple(self.update_values))
            connection.commit()
            if self.cursor.rowcount > 0:
                print(f"商品ID {self.goodsid} の情報を更新しました。")
            else:
                print(f"商品ID {self.goodsid} が見つかりませんでした。")
        except Exception as e:
            print(f"エラー: {e}")

    # 商品IDを入力して、編集したい情報を聞き出す
    def get_input_int(self, prompt, allow_empty=False):
        while True:
            user_input = input(prompt)
            if user_input == "" and allow_empty:
                return None  # 空入力を許可してスキップ
            elif user_input in ['0', '1']:  # 0または1の入力を許可
                return int(user_input)
            else:
                print("無効な入力です。0か1を入力してください、または空白でスキップしてください。")

    def Delete(self):
        confirm = input(f"商品ID {self.goodsid} を削除してもよろしいですか？ (y/n): ").lower()
        if confirm == 'y':
            self.delete_product_info()
        else:
            print("削除をキャンセルしました。")

    # 商品情報を削除する関数
    def delete_product_info(self):
        try:
            # 商品IDを指定してDELETE文を実行
            delete_query = "DELETE FROM 商品 WHERE 商品ID = %s"
            self.cursor.execute(delete_query, (self.goodsid,))
            connection.commit()
            if self.cursor.rowcount > 0:
                print(f"商品ID {self.goodsid} の情報を削除しました。")
            else:
                print(f"商品ID {self.goodsid} が見つかりませんでした。")
        except Exception as e:
            print(f"エラー: {e}")

class Product_new():
    def __init__(self, title, genre, release_date, cursor):
        self.title = title
        self.genre = genre
        self.release_date = release_date
        self.cursor = cursor
        self.current_date = None
        self.max_serial_number = 0

    def generate_product_id(self):
        # 現在の日時を取得 (年、月、日、時、分、秒)
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # 13桁以内に収まるように秒数を使う
        product_id = current_time
        # 商品IDの桁数が13桁を超えていれば、ミリ秒をカット
        if len(product_id) > 13:
            product_id = product_id[:13]
        return product_id  # 商品IDを13桁以内で生成

    # 商品情報を登録する関数
    def register_new_product(self):
        # 商品IDを生成
        product_id = self.generate_product_id()
        # その他の情報は仮に設定
        rental_return_date = "9999-01-01"  # 無効な日付
        rental_member = "000000000"
        rental_status = 0  # 貸出可能
        rental_count = 0
        storage_location = 0  # 店頭
        # データベースに新しい商品情報を登録
        try:
            self.cursor.execute("""
                INSERT INTO 商品 (商品ID, タイトル, ジャンル, 発売日, 貸出・返却日, 貸出会員,
                                貸出状況, 貸出回数, 保管場所)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (product_id, self.title, self.genre, self.release_date, rental_return_date, rental_member,
                rental_status, rental_count, storage_location))
            connection.commit()
            print(f"新しい商品を登録しました。商品ID: {product_id}")
        except Exception as e:
            print(f"エラー: {e}") 

# 商品一覧を表示する関数
class Product_list():
    def __init__(self, cursor):
        self.cursor = cursor
        self.sort_column = "商品ID"
        self.sort_order = "ASC"

    def display_product_list(self):
        try:
            # ソート順を指定したSQLクエリ
            query = f"""
                SELECT 商品ID, タイトル, 発売日, 貸出・返却日, 貸出回数, 保管場所
                FROM 商品
                ORDER BY {self.sort_column} {self.sort_order}
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            if rows:
                print(f"商品ID | タイトル | 発売日 | 貸出・返却日 | 貸出回数 | 保管場所")
                for row in rows:
                    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
                self.list_sort()    
            else:
                print("商品情報が見つかりませんでした。")
            
        except Exception as e:
            print(f"エラー: {e}")


    def list_sort(self):
        print("ソートしたいカラムを選んでください。")
        print("1: 商品ID")
        print("2: 発売日")
        print("3: 貸出・返却日")
        print("4: 貸出回数")
        print("5: 保管場所")
        column_choice = input("カラム番号を入力してください: ")
        if column_choice == "1":
            self.sort_column = "商品ID"
        elif column_choice == "2":
            self.sort_column = "発売日"
        elif column_choice == "3":
            self.sort_column = "貸出・返却日"
        elif column_choice == "4":
            self.sort_column = "貸出回数"
        elif column_choice == "5":
            self.sort_column = "保管場所"
        else:
            print("無効なカラム番号です。")

        print("ソート順を選んでください。")
        print("1: 昇順 (ASC)")
        print("2: 降順 (DESC)")  
        order_choice = input("ソート順番号を入力してください: ")
        if order_choice == "1":
            self.sort_order = "ASC"
            self.display_product_list()                
        elif order_choice == "2":
            self.sort_order = "DESC"
            self.display_product_list()                
        else:
            print("無効なソート順番号です。")

"""
# メイン処理
if __name__ == "__main__":
    try:
        connection = psycopg2.connect(database_url, sslmode='require')
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()

        while True:
            print("\n選択してください: 1: 検索, 2: 登録, 3: 一覧, 0: 終了")
            choice = input("番号を入力: ")
            if choice == "1":
                product_id = input("検索する商品IDを入力: ")
                product = Product_search_update_delete(product_id, cursor)
                product.search()

                """
            elif choice == "2":
                product_id = input("編集する商品IDを入力: ")
                title = input("新しいタイトル (空欄でスキップ): ") or None
                edit_product_info(product_id, タイトル=title)
            elif choice == "3":
                product_id = input("削除する商品IDを入力: ")
                delete_product_info(product_id)
                """
            elif choice == "2":
                title = input("タイトルを入力してください: ")
                genre = input("ジャンルを入力してください: ")
                release_date = input("発売日を入力してください (YYYY-MM-DD): ")
                new = Product_new(title, genre, release_date, cursor)
                new.register_new_product()
            elif choice == "3":
                productlist = Product_list(cursor)
                productlist.display_product_list()
            elif choice == "0":
                cursor.close()
                connection.close()                
                break
            else:
                print("無効な入力です。")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()