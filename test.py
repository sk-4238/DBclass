import psycopg2
import os
from dotenv import load_dotenv
import datetime
from dateutil.relativedelta import relativedelta
# .env ファイルを読み込む
load_dotenv()
database_url = os.getenv('database_url')
total_fee = 0
data_list = []  # 空のリストを作成
# Retクラスを先に定義
class Ret:
    def __init__(self, user_input, cursor):
        self.cursor = cursor
        self.today = datetime.date.today()
        self.goodsid = user_input
        self.商品id = None
        self.タイトル = None
        self.貸出日 = None
        self.貸出状況 = None
        self.overdue = None
        self.status = None

    def search(self):
        self.cursor.execute("select 商品id, タイトル, 貸出・返却日, 貸出状況 from 商品 where 商品id = %s", (self.goodsid,))
        result = self.cursor.fetchone()
        if result:
            self.商品id, self.タイトル, self.貸出日, self.貸出状況 = result
            self.Overdue()  # 延滞状況を計算
            if self.貸出状況 == 1:
                self.status = "返却可"
            elif self.貸出状況 == 0:
                self.status = "貸出していない商品"
            print(f"商品id: {self.商品id}, タイトル: {self.タイトル}, 延滞状況: {self.overdue}, 貸出状況: {self.status}")

            while True:
                print("\n選択してください: 1: 貸出リストに追加する, 2:貸出, 0: 終了")
                choice = input("番号を入力: ")
                if choice == "1":
                    self.add_to_list()
                elif choice == "2":
                    self.return_dvd()
                    break    
                elif choice == "0":
                    break    
                else:
                    print("無効な入力です。")             
        else:
            print("商品が見つかりませんでした。")

    def Overdue(self):
        period = (self.today - self.貸出日).days
        if period <= 7 :
            self.overdue = "延滞なし"             
        else:
            self.overdue = "延滞あり"
            total_fee += 100 * (period - 7)

    def add_to_list(self):
        if self.商品id and self.タイトル:
            # 商品情報をリストに追加
            data_list.append({
                '商品id': self.商品id,
                'タイトル': self.タイトル,
                '延滞状況': self.overdue,
                '貸出状況': self.status
            })

# 返却処理関数
def return_dvd(self):
    try:
        for item in data_list:
            # 商品IDを入力
            product_id = input("返却する商品IDを入力してください: ")
            # 商品情報を取得
            self.cursor.execute("SELECT タイトル, 貸出状況 FROM 商品 WHERE 商品ID = %s", (product_id,))
            product = self.cursor.fetchone()
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
            self.cursor.execute("""
                UPDATE 商品
                SET 貸出・返却日 = %s, 貸出状況 = 0, 貸出会員 = '0000'
                WHERE 商品ID = %s
            """, (return_date, product_id))
            # 変更を確定
            connection.commit()
            print(f"'{title}' を返却しました。")

        data_list.clear()
        total_fee = 0            
    except Exception as e:
        print(f"エラー: {e}")            
            
# メイン処理
try:
    connection = psycopg2.connect(database_url, sslmode='require')
    cursor = connection.cursor()
    cursor.execute('SELECT version();')
    db_version = cursor.fetchone()
    print(f"Connected to: {db_version}")
    print("データを入力してください (終了するには 'exit' と入力):")
    while True:
        user_input = input()
        if user_input.lower() == 'exit':
            break  # "exit" が入力された場合はループを終了
        try:
            # Retクラスのインスタンスを作成し、searchメソッドを呼び出す
            ret = Ret(user_input, cursor)
            ret.search()
            # リストにユーザー入力を追加
            #ret.add_to_list()
        except ValueError:
            print("無効な商品IDです。数値を入力してください。")
    print("最終的なリスト:", data_list)
    # 4つ1組でまとめてリストに追加
    combined_list = []
    for i in range(0, len(data_list), 4):
        combined_list.append(data_list[i:i+4])
    print("\n4つ1組でまとめたリスト:")
    for item in combined_list:
        print(item)
except Exception as e:
    print(f"Error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        #9920241120002