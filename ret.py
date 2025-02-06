import psycopg2
import datetime
from dateutil.relativedelta import relativedelta
#import main

connection = psycopg2.connect(host="localhost", dbname="dvdrental", user="postgres", password="tcu2023", port="5432")
cursor = connection.cursor()

#cursor.execute("SELECT * FROM 会員")
#query_result = cursor.fetchall()
#print(query_result)

#cursor.execute("SELECT * FROM 商品")
#query_result1 = cursor.fetchall()
#print(query_result1)

class Ret():
    def __init__(self):
        self.today = datetime.date.today()
        self.goodsid = "9920241120002"
        self.貸出日 = None
        self.貸出状況 = None
        self.overdue = None

    def search(self, cursor):
        cursor.execute("select 商品id, タイトル, 貸出・返却日, 貸出状況 from 商品 where 商品id = %s", (self.goodsid,))
        result = cursor.fetchone()

        if result:
            商品id, タイトル, self.貸出日, self.貸出状況  = result
            self.Overdue()
            if self.貸出状況 == 1:
                status = "返却可"
            elif self.貸出状況 == 0:
                status = "貸出していない商品"

            print(f"商品id: {商品id}, タイトル: {タイトル}, 延滞状況: {self.overdue}, 貸出状況: {status}")
        else:
            print("商品が見つかりませんでした。")

    def Overdue(self):
        period = (self.today - self.貸出日).days
        if period <= 7:
            self.overdue = "延滞なし"
        elif period >= 8:
            self.overdue = "延滞あり"
            final_period = period - 7
            add = 100 * final_period

    #def isNew(self):
    #    today = datetime.date.today()
    #    six_months_ago = today - relativedelta(months = 6)

    #    if self.発売日 < six_months_ago:
    #        self.new_or_old = "OLD"
    #    else:
    #        self.new_or_old = "NEW"
    #    return self


#print(six_months_ago.days)

# クラスをインスタンス化して検索メソッドを呼び出す
ret = Ret()
ret.search(cursor)

# クローズ処理
cursor.close()
connection.close()
