import psycopg2
import os
from dotenv import load_dotenv
import datetime
from dateutil.relativedelta import relativedelta
# .env ファイルを読み込む
#load_dotenv()
#database_url = os.getenv('database_url')
data_list = []  # 空のリストを作成
total_fee = 0  # 合計料金を格納する変数
# Retクラスを先に定義
class Lend():
    def __init__(self, user_input, cursor):
        self.cursor = cursor
        self.today = datetime.date.today()
        self.goodsid = user_input
        self.商品id = None
        self.タイトル = None
        self.発売日 = None  # 変更: 貸出・返却日から発売日
        self.貸出状況 = None
        self.overdue = None
        self.status = None
        self.new_or_old = None
        self.料金 = None

    def search(self):
        self.cursor.execute("select 商品id, タイトル, 発売日, 貸出状況 from 商品 where 商品id = %s", (self.goodsid,))
        result = self.cursor.fetchone()
        if result:
            self.商品id, self.タイトル, self.発売日, self.貸出状況 = result
            self.isNew()  # 新作か旧作かを判定

            if self.貸出状況 == 1:
                self.status = "貸出中"
            elif self.貸出状況 == 0:
                self.status = "貸出可"
            print(f"商品id: {self.商品id}, タイトル: {self.タイトル}, 発売日: {self.発売日}, 延滞状況: {self.overdue}, 貸出状況: {self.status}, 料金: {self.料金}円")
        else:
            print("商品が見つかりませんでした。")

        while True:
            print("\n選択してください: 1: 貸出リストに追加する, 2:貸出, 0: 終了")
            choice = input("番号を入力: ")
            if choice == "1":
                self.add_to_list()
            elif choice == "2":
                self.borrow_dvd()    
            elif choice == "0":
                break    
            else:
                print("無効な入力です。")                    

    def isNew(self):
        # 新作か旧作かを判定するメソッド
        six_months_ago = self.today - relativedelta(months=6)
        if self.発売日 < six_months_ago:
            self.new_or_old = "OLD"
            self.料金 = 100  # 旧作は100円
        else:
            self.new_or_old = "NEW"
            self.料金 = 300  # 新作は300円

    def add_to_list(self):
        global total_fee  # 合計料金を更新するためにグローバル変数を使用
        if self.商品id and self.タイトル:
            # 商品情報をリストに追加
            data_list.append({
                '商品id': self.商品id,
                'タイトル': self.タイトル,
                '新旧': self.new_or_old,
                '貸出状況': self.status,
            })
            total_fee += self.料金  # 料金を合計に加算
        

    def borrow_dvd(self):
        try:
            for item in data_list:             
            # 商品IDを入力
                product_id = item['商品id']
                # 商品情報を取得
                self.cursor.execute("SELECT タイトル, 貸出状況, 貸出回数 FROM 商品 WHERE 商品ID = %s", (product_id,))
                product = self.cursor.fetchone()
                if not product:
                    print("エラー: 指定された商品IDは存在しません。")
                    return
                title, rental_status, rental_count = product
                # 貸出可能か確認
                if rental_status == 1:
                    print(f"エラー: '{title}' は現在貸出中です。")
                    return
                # 会員IDを入力
                member_id = input("貸出する会員IDを入力してください: ")
                # 現在の日付を取得
                today_date = datetime.datetime.now().strftime("%Y-%m-%d")
                # データベースを更新（貸出情報を反映）
                cursor.execute("""
                    UPDATE 商品
                    SET 貸出・返却日 = %s, 貸出状況 = 1, 貸出回数 = 貸出回数 + 1, 貸出会員 = %s
                    WHERE 商品ID = %s
                """, (today_date, member_id, product_id))
                # 変更を確定
                connection.commit()
                print(f"'{title}' を会員ID {member_id} に貸し出しました。")

            data_list.clear()
            total_fee = 0

        except Exception as e:
            print(f"エラー: {e}")
            connection.rollback()

"""
# メイン処理
try:
    connection = psycopg2.connect(database_url, sslmode='require')
    cursor = connection.cursor()
    #cursor.execute('SELECT version();')
    #db_version = cursor.fetchone()
    #print(f"Connected to: {db_version}")
    #print("データを入力してください (終了するには 'exit' と入力):")
    while True:
        user_input = input()
        if user_input.lower() == 'exit':
            break  # "exit" が入力された場合はループを終了
        # Retクラスのインスタンスを作成し、searchメソッドを呼び出す
        lend = Lend(user_input, cursor)
        lend.search()
        # リストにユーザー入力を追加
        #lend.add_to_list()
    print("最終的なリスト:", data_list)
    # 4つ1組でまとめてリストに追加
    combined_list = []
    """
    for i in range(0, len(data_list), 4):
        combined_list.append(data_list[i:i+4])
    print("\n4つ1組でまとめたリスト:")
    for item in combined_list:
        print(item)
    print(f"\n合計料金: {total_fee}円")
    """
except Exception as e:
    print(f"Error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
#9920241120002