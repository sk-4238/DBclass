import os
import psycopg2
from dotenv import load_dotenv
import datetime

# .env ファイルを読み込む
load_dotenv()
database_url = os.getenv('database_url')

class Member_search_update_delete():
    def __init__(self, user_input, cursor):
        self.today = datetime.date.today()
        self.cursor = cursor
        self.memberid = user_input  # id ではなく user_input を使用
        self.会員id = None
        self.氏名 = None
        self.住所 = None
        self.電話番号 = None
        self.生年月日 = None
        self.貸出会員 = None            

    def search(self):
        try:
            # 商品IDに紐づく会員情報を取得
            self.cursor.execute(
                "SELECT 会員id, 氏名, 住所, 電話番号, 生年月日 FROM 会員 WHERE 会員id = %s",
                (self.memberid,)
            )
            result1 = self.cursor.fetchone()

            if result1:
                self.会員id, self.氏名, self.住所, self.電話番号, self.生年月日 = result1

                # `貸出会員` が VARCHAR 型のため、`会員id` を文字列に変換
                self.cursor.execute(
                    "SELECT 貸出会員, COUNT(*) AS 貸出数 FROM 商品 WHERE 貸出会員 = %s::VARCHAR GROUP BY 貸出会員",
                    (str(self.会員id),)  # `会員id` を `str` に変換
                )
                result2 = self.cursor.fetchone()
                if result2 == None:
                    result2 = 0      
                                     
            else:
                result2 = None

            print("会員情報:", result1)
            print("貸出情報:", result2)

            """
            while True:
                print("\n選択してください: 1: 編集, 2: 削除, 0: 戻る")
                choice = input("番号を入力: ")
                if choice == "1":
                    self.Update()
                elif choice == "2":
                    self.Delete_member()
                elif choice == "0":
                    break
                else:
                    print("無効な入力です。")                                        
                """
            # コミット
            #self.cursor.commit()

        except Exception as e:
            print(f"検索エラー: {e}")
            #self.cursor.rollback()  # **エラー発生時にロールバック**

    def Delete_member(self, choose):
        try:
            print(f"会員ID: {self.会員id}, 氏名: {self.氏名} の情報は削除されます。")
            confirmation = input("本当に削除しますか？ (Y/N): ").strip().upper()
            if choose == "0":
                # 会員情報を削除
                self.cursor.execute("DELETE FROM 会員 WHERE 会員ID = %s", (self.会員id,))
                #self.cursor.commit()
                print(f"会員ID {self.会員id} の情報を削除しました。")
            elif choose == "1":
                print("削除がキャンセルされました。")

        except Exception as e:
            print(f"エラー: {e}")
    """
    def Update(self):
        print("編集したい情報を入力してください。変更しない場合はそのままEnterを押してください。")
        self.name = input("氏名を変更する場合は入力してください: ")
        self.address = input("住所を変更する場合は入力してください: ")
        self.phone = input("携帯番号を変更する場合は入力してください (10桁または11桁の数字): ")
        self.birth_date = input("生年月日を変更する場合は入力してください (YYYY-MM-DD): ")
        self.edit_member_info()      
        """      

    def edit_member_info(self, name, address, phone, birth_date):
        try:
            #connection = psycopg2.connect(database_url, sslmode='require')
            #cursor = connection.cursor()
            # 更新する項目がある場合のみ、UPDATE文を動的に作成
            self.update_query = "UPDATE 会員 SET "
            self.update_values = []
            if name:
                self.update_query += "氏名 = %s, "
                self.update_values.append(name)
            if address:
                self.update_query += "住所 = %s, "
                self.update_values.append(address)
            if phone:
                self.update_query += "電話番号 = %s, "
                self.update_values.append(phone)
            if birth_date:
                self.update_query += "生年月日 = %s, "
                self.update_values.append(birth_date)

            # クエリの末尾の余分なカンマを削除
            self.update_query = self.update_query.rstrip(', ')
            # 商品IDをWHERE句に追加
            self.update_query += " WHERE 会員ID = %s"
            self.update_values.append(self.memberid)
            # クエリを実行
            self.cursor.execute(self.update_query, tuple(self.update_values))
            #connection.commit()
            if self.cursor.rowcount > 0:
                print(f"商品ID {self.memberid} の情報を更新しました。")
            else:
                print(f"商品ID {self.memberid} が見つかりませんでした。")
        except Exception as e:
            print(f"エラー: {e}")            

    
class Member_new():
    def __init__(self, name, address, phone, birth_date, cursor):
        self.cursor = cursor
        self.current_date = None
        self.max_serial_number = 0
        self.name = name
        self.address = address
        self.phone = phone
        self.birth_date = birth_date
        
    def generate_member_id(self):
        # 今日の日付と時間を取得
        now = datetime.datetime.now()
        year = now.year % 1000  # 年の1000の位を削除
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second
        # 会員IDを生成
        member_id = f"{year:03d}{month:02d}{day:02d}{hour:02d}{minute:02d}{second:02d}"
        return member_id

    # 電話番号をフォーマットする関数
    def format_phone_number(self):
        # 数字以外の文字を取り除く
        self.phone = ''.join(filter(str.isdigit, self.phone))
        # 10桁または11桁の場合にハイフンを追加
        if len(self.phone) == 10:
            return f"{self.phone[:3]}-{self.phone[3:7]}-{self.phone[7:]}"
        elif len(self.phone) == 11:
            return f"{self.phone[:3]}-{self.phone[3:7]}-{self.phone[7:]}"
        else:
            raise ValueError("電話番号は10桁または11桁の数字で入力してください。")
    # 会員情報を登録する関数
    def register_new_member(self):
        # 電話番号をフォーマット
        formatted_phone = self.format_phone_number()
        # 会員IDを生成
        member_id = self.generate_member_id()
        # データベースに新しい会員情報を登録
        try:
            self.cursor.execute("""
                INSERT INTO 会員 (会員ID, 氏名, 住所, 電話番号, 生年月日)
                VALUES (%s, %s, %s, %s, %s)
            """, (member_id, self.name, self.address, formatted_phone, self.birth_date))
            #connection.commit()
            return member_id
            print(f"新しい会員を登録しました。会員ID: {member_id}")
        except Exception as e:
            print(f"エラー: {e}")
            return None

# 会員情報一覧を表示する関数
class Member_list():
    def __init__(self, cursor):    
        self.cursor = cursor

    def display_member_list(self):
        try:
            # 会員情報をすべて取得
            self.cursor.execute("SELECT 会員ID, 氏名, 住所, 電話番号, 生年月日 FROM 会員")
            members = self.cursor.fetchall()
            if members:
                print("\n会員情報一覧:")
                for member in members:
                    print(f"会員ID: {member[0]}, 氏名: {member[1]}, 住所: {member[2]}, 電話番号: {member[3]}, 生年月日: {member[4]}")
                return members
            else:
                print("登録されている会員情報はありません。")
                return []
        except Exception as e:
            print(f"エラー: {e}")
            return []


"""# メイン処理
#if __name__ == "__main__":
    try:
        connection = psycopg2.connect(database_url, sslmode='require')
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()

        while True:
            print("\n選択してください: 1: 検索, 2: 登録, 3: 一覧, 0: 終了")
            choice = input("番号を入力: ")
            if choice == "1":
                member_id = input("検索する会員IDを入力: ")
                member = Member_search_update_delete(member_id, cursor)
                member.search()

            elif choice == "2":
                print("新規会員の登録を開始します。")
                name = input("氏名を入力してください: ")
                address = input("住所を入力してください: ")
                phone = input("電話番号を入力してください (10桁または11桁の数字): ")
                birth_date = input("生年月日を入力してください (YYYY-MM-DD): ")
                try:
                    new = Member_new(name, address, phone, birth_date, cursor)
                    new.register_new_member()
                except ValueError as e:
                    print(e)  

            elif choice == "3":
                memberlist = Member_list(cursor)
                memberlist.display_member_list()

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


        #9920241120002
        #992024112101
        """