import tkinter as tk
from tkinter import ttk
import psycopg2
import os
from datetime import date
from dotenv import load_dotenv

#import ret
#import lend
from member import Member_search_update_delete
from member import Member_new
from member import Member_list
#import member
#import goods

# .env ファイルを読み込む
load_dotenv()
database_url = os.getenv('database_url')

class Application():
    def __init__(self, cursor):
        self.cursor = cursor

        #ウィンドウ設定
        self.root = tk.Tk()
        self.root.title ("DVDレンタルシステム")
        self.root.geometry("1000x600+150+20")

        #初期フレーム設定
        self.frame = ttk.Frame(self.root, width = 1000, height = 30)
        self.frame.pack(fill = 'x')
        self.frame1 = ttk.Frame(self.root, width = 1000, height = 60, borderwidth = 2, relief = 'solid')
        self.frame1.pack(fill = 'x')
        self.frame2 = ttk.Frame(self.root, width = 1000, height = 510)
        self.frame2.pack()

        self.static = ttk.Label(self.frame, text = " ", font = ("", 12))
        self.static.pack(side = "left", pady = 5, padx = 10)

        self.img = tk.PhotoImage(file = "home.png")
        #self.img.subsample(100,1)

        #ボタンコマンド用
        rental = Rental(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)
        member = Member(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)
        goods = Goods(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)
        
        


        #ホーム画面ウィジェット設定
        self.static["text"] = "ホーム"

        rental_button = ttk.Button(self.frame2, text = "レンタル", width = 50, padding = [0,80], command = rental.Rental_menu)
        rental_button.place(x = 320, y = 50)
        member_button = ttk.Button(self.frame2, text = "会員情報", width = 50, padding = [0,80], command = member.Member_menu)
        member_button.place(x = 150, y = 300)        
        goods_button = ttk.Button(self.frame2, text = "商品情報", width = 50, padding = [0,80], command = goods.Goods_menu)
        goods_button.place(x = 500, y = 300)          
        
        self.root.mainloop()              

class Home():
    def __init__(self, root, frame, frame1, frame2, static, img, cursor):
        self.root = root
        self.frame = frame
        self.frame1 = frame1
        self.frame2 = frame2
        self.static = static
        self.img = img
        self.cursor = cursor        

    def Home_widget(self):
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()

        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()

        rental = Rental(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)  
        member = Member(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)
        goods = Goods(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)
     

        self.static["text"] = "ホーム"

        rental_button = ttk.Button(self.frame2, text = "レンタル", width = 50, padding = [0,80], command = rental.Rental_menu)
        rental_button.place(x = 320, y = 50)
        member_button = ttk.Button(self.frame2, text = "会員情報", width = 50, padding = [0,80], command = member.Member_menu)
        member_button.place(x = 150, y = 300)        
        goods_button = ttk.Button(self.frame2, text = "商品情報", width = 50, padding = [0,80], command = goods.Goods_menu)
        goods_button.place(x = 500, y = 300)  

class Rental(): #レンタル機能
    def __init__(self, root, frame, frame1, frame2, static, img, cursor):
        self.root = root
        self.frame = frame
        self.frame1 = frame1
        self.frame2 = frame2
        self.static = static
        self.img = img
        self.cursor = cursor

        self.home = Home(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)
        
    def Rental_menu(self): #レンタルメニュー画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()

        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()

        #frame内のstaticの文字変更
        self.static["text"] = "レンタル"

        #frame1内にホームボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)

        #frame2内にウィジェットを設置
        #frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #frame3.propagate(False)
        #frame3.pack()
        button1 = ttk.Button(self.frame2, text = "貸出", width = 50, padding = [0,80], command = self.Lend_widget)
        button1.place(x = 150, y = 150)
        button2 = ttk.Button(self.frame2, text = "返却", width = 50, padding = [0,80], command = self.Ret_widget)
        button2.place(x = 500, y = 150)

    def Lend_widget(self): #貸出画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()

        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()

        #frame内のstaticの文字変更
        self.static["text"] = "レンタル(貸出)"

        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)        
        button1 = ttk.Button(self.frame1, text = "返却", width = 20, padding = [0,22], command = self.Ret_widget)
        button1.pack(side = "left")

        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0        
        label = ttk.Label(self.frame2, text = "商品ID(13桁)：", font = ("", 12))
        label.place(x = 150, y = 100)
        self.editBox = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox.place(x = 150, y = 130)
        button2 = ttk.Button(self.frame2, text = "検索", width = 20, padding = [0,7], command = lambda: (self. on_button2_click1(), self.Lend_comfirm()))
        button2.place(x = 750, y = 130)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self.Rental_menu)
        button3.place(x = 30, y = 450)
        self.label1 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label1.place(x = 160, y = 180)
        self.label2 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label2.place(x = 160, y = 230)
        self.label3 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label3.place(x = 160, y = 280)                
        self.label4 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label4.place(x = 160, y = 330)

    def on_button2_click1(self):
        lendgoodsID = self.editBox.get()
        # 商品IDが数字であること、かつ13桁かどうかをチェック
        if not lendgoodsID.isdigit():  # 数字以外の文字が含まれている場合
            print("エラー: 商品IDは13桁の数字のみで入力してください。")
        elif len(lendgoodsID) != 13:  # 13桁であることをチェック
            print("エラー: 商品IDは13桁で入力してください。")
        else:
            print("商品ID:", lendgoodsID)  # 正しいIDなら表示
        #print(lendgoodsID)

    def Lend_comfirm(self):
        self.count += 1

        self.editBox.delete(0, tk.END)
        self.label1["text"] = "商品ID\t：" + str(self.count)
        self.label2["text"] = "タイトル\t："
        self.label3["text"] = "新旧情報："
        self.label4["text"] = "貸出状況："

        button4 = ttk.Button(self.frame2, text = "貸出リストに追加", width = 20, padding = [0,7], command = lambda : NewWindow_report("あ"))
        button4.place(x = 700, y = 450)
        button5 = ttk.Button(self.frame2, text = "確認", width = 20, padding = [0,7], command = lambda : self.NewWindow(" "))
        button5.place(x = 850, y = 450)

    def Lend_list(self):
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()

        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()

        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)        
        button1 = ttk.Button(self.frame1, text = "返却", width = 20, padding = [0,22], command = self.Ret_widget)
        button1.pack(side = "left")

        #frame2内にウィジェットを設置
        button = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self.Lend_widget)
        button.place(x = 30, y = 450)
        button1 = ttk.Button(self.frame2, text = "貸出", width = 20, padding = [0,7], command = self.Lend_widget)
        button1.place(x = 850, y = 450)                
        label = ttk.Label(self.frame2, text = "貸出リスト", font = ("", 12))
        label.place(x = 100, y = 50) 
        
        frame3 = ttk.Frame(self.frame2, width = 800, height = 350, borderwidth = 2, relief = 'solid')
        frame3.place(x = 100, y = 80)

        self.tree = ttk.Treeview(frame3)
        self.tree["columns"] = (1, 2, 3, 4)
        self.tree["show"] = "headings"
        self.tree.heading(1, text = "No.")
        self.tree.heading(2, text = "商品ID")
        self.tree.heading(3, text = "タイトル")
        self.tree.heading(4, text = "新旧情報")

        #scroll = ttk.Scroll(frame3, orient=ttk.VERTICAL, command = self.tree.yview)
        #scroll.pack(side = "right", fill = "y")
        #self.tree["yscrollcommand"] = scroll.set

        self.tree.pack(fill = 'x')

        self.tree.insert("", "end", values= ("0","1","2","3"))

    def Ret_widget(self): #返却画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()

        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()

        #frame内のstaticの文字変更
        self.static["text"] = "レンタル(返却)"

        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)        
        button1 = ttk.Button(self.frame1, text = "貸出", width = 20, padding = [0,22], command = self.Lend_widget)
        button1.pack(side = "left")

        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0        
        label = ttk.Label(self.frame2, text = "商品ID(13桁)：", font = ("", 12))
        label.place(x = 150, y = 100)
        self.editBox = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox.place(x = 150, y = 130)
        button2 = ttk.Button(self.frame2, text = "検索", width = 20, padding = [0,7], command = lambda: (self. on_button2_click2(), self.Ret_comfirm()))
        button2.place(x = 750, y = 130)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self.Rental_menu)
        button3.place(x = 30, y = 450)
        self.label1 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label1.place(x = 160, y = 180)
        self.label2 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label2.place(x = 160, y = 230)
        self.label3 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label3.place(x = 160, y = 280)                
        self.label4 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label4.place(x = 160, y = 330)

    def on_button2_click2(self):
        retgoodsID = self.editBox.get()
        # 商品IDが数字であること、かつ13桁かどうかをチェック
        if not retgoodsID.isdigit():  # 数字以外の文字が含まれている場合
            print("エラー: 商品IDは13桁の数字のみで入力してください。")
        elif len(retgoodsID) != 13:  # 13桁であることをチェック
            print("エラー: 商品IDは13桁で入力してください。")
        else:
            print("商品ID:", retgoodsID)  # 正しいIDなら表示
        #print(retgoodsID)

    def Ret_comfirm(self):
        self.count += 1

        self.editBox.delete(0, tk.END)
        self.label1["text"] = "商品ID\t：" + str(self.count)
        self.label2["text"] = "タイトル\t："
        self.label3["text"] = "延滞情報："
        self.label4["text"] = "貸出状況："

        button4 = ttk.Button(self.frame2, text = "返却リストに追加", width = 20, padding = [0,7], command = lambda : NewWindow_report("あ"))
        button4.place(x = 700, y = 450)
        button5 = ttk.Button(self.frame2, text = "確認", width = 20, padding = [0,7], command = self.Ret_list)
        button5.place(x = 850, y = 450)


    def Ret_list(self):
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()

        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()

        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)        
        button1 = ttk.Button(self.frame1, text = "貸出", width = 20, padding = [0,22], command = self.Lend_widget)
        button1.pack(side = "left")

        #frame2内にウィジェットを設置
        button = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self.Ret_widget)
        button.place(x = 30, y = 450)
        button1 = ttk.Button(self.frame2, text = "返却", width = 20, padding = [0,7], command = self.Ret_widget)
        button1.place(x = 850, y = 450)                
        label = ttk.Label(self.frame2, text = "返却リスト", font = ("", 12))
        label.place(x = 100, y = 50) 
        
        frame3 = ttk.Frame(self.frame2, width = 800, height = 350, borderwidth = 2, relief = 'solid')
        frame3.place(x = 100, y = 80)

        self.tree = ttk.Treeview(frame3)
        self.tree["columns"] = (1, 2, 3, 4)
        self.tree["show"] = "headings"
        self.tree.heading(1, text = "No.")
        self.tree.heading(2, text = "商品ID")
        self.tree.heading(3, text = "タイトル")
        self.tree.heading(4, text = "新旧情報")

        #scroll = ttk.Scroll(frame3, orient=ttk.VERTICAL, command = self.tree.yview)
        #scroll.pack(side = "right", fill = "y")
        #self.tree["yscrollcommand"] = scroll.set

        self.tree.pack(fill = 'x')

        self.tree.insert("", "end", values= ("0","1","2","3"))

    def NewWindow(self, text):
        self.text = text
        
        newwindow = tk.Tk()
        newwindow.title ("貸出商品リスト確認画面")
        newwindow.geometry("600x200+350+230")
        frame = ttk.Frame(newwindow)
        frame.pack(fill = "y")
        self.count = 0
        label = ttk.Label(frame, text = "会員ID：", font = ("", 12))
        label.pack(side="left", padx=1)
        self.editBox = ttk.Entry(frame, width = 30, font = ("", 20))
        self.editBox.pack(side="left", padx=1)
        static = ttk.Label(frame, text = self.text, font = ("", 12))
        static.pack(pady = 65)
        button = ttk.Button(frame, text = "貸出", width = 20, padding = [0,7], command = lambda: (self. on_button_click(),newwindow.destroy(), self.Lend_widget()))
        button.place(x = 200, y = 110)

        newwindow.mainloop()

    def on_button_click(self):
        rentmemberID = self.editBox.get()
        print(rentmemberID)

class Member(): #会員機能
    def __init__(self, root, frame, frame1, frame2, static, img, cursor):
        self.root = root
        self.frame = frame
        self.frame1 = frame1
        self.frame2 = frame2
        self.static = static
        self.img = img
        self.cursor = cursor

        self.home = Home(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)
        
    def Member_menu(self): #会員メニュー画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()

        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()

        #frame内のstaticの文字変更
        self.static["text"] = "会員情報管理メニュー"

        #frame1内にホームボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)

        #frame2内にウィジェットを設置
        #frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #frame3.propagate(False)
        #frame3.pack()
        button1 = ttk.Button(self.frame2, text = "新規登録", width = 50, padding = [0,80], command = self.Member_widgetnew)
        button1.place(x = 320, y = 50)
        button2 = ttk.Button(self.frame2, text = "変更/削除", width = 50, padding = [0,80], command = self.Member_widgetID)
        button2.place(x = 150, y = 300)
        button3 = ttk.Button(self.frame2, text = "一覧", width = 50, padding = [0,80], command = self.Member_widget)
    
        button3.place(x = 500, y = 300)

    def Member_widgetID(self): #会員ID入力画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 20, padding = [0,22], command = self.Member_widgetnew)
        button1.pack(side = "left")
        button1 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22], command = self. Member_widget)
        button1.pack(side = "left")
        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0
        label = ttk.Label(self.frame2, text = "会員ID(12桁)：", font = ("", 12))
        label.place(x = 150, y = 100)
        self.editBox = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox.place(x = 150, y = 130)
        button2 = ttk.Button(self.frame2, text = "検索", width = 20, padding = [0,7], command = lambda: (self. on_button2_click3(), self. Member_confirm()))
        button2.place(x = 750, y = 130)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self. Member_menu)
        button3.place(x = 30, y = 450)
        self.label1 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label1.place(x = 160, y = 180)
        self.label2 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label2.place(x = 160, y = 230)
        self.label3 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label3.place(x = 160, y = 280)
        self.label4 = ttk.Label(self.frame2, text = " ", font = ("", 18))
        self.label4.place(x = 160, y = 330)

    def on_button2_click3(self):
        memberID = self.editBox.get()
        if not memberID.isdigit():  # アルファベットや記号が含まれている場合
            print("エラー", "会員IDは12桁の数字のみで入力してください。")  # エラーメッセージを表示
        elif len(memberID) != 12:  # 12桁かどうかをチェック
            print("エラー", "会員IDは12桁の数字で入力してください。")
        else:
            self.member_sud = Member_search_update_delete(memberID,self.cursor)
            self.member_sud.search()
            #print("会員ID:", memberID)

        #print(memberID)

    def Member_widget(self): #一覧画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame内のstaticの文字変更
        self.static["text"] = "会員情報管理メニュー(一覧)"
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 30, padding = [0,22], command = self.Member_widgetnew)
        button1.pack(side = "left", padx = 10)
        button2 = ttk.Button(self.frame1, text = "変更/削除", width = 30, padding = [0,22], command = self.Member_widgetID)
        button2.pack(side = "left", padx = 10)
        button3 = ttk.Button(self.frame2, text = "並び替え", width = 20, padding = [0,10])
        button3.place(x = 800,y = 0)
        button4 = ttk.Button(self.frame2, text = "前のページ", width = 20, padding = [0,7])
        button4.place(x = 700, y = 450)
        button5 = ttk.Button(self.frame2, text = "次のページ", width = 20, padding = [0,7])
        button5.place(x = 850, y = 450)
        button6 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self. Member_menu)
        button6.place(x = 30, y = 450)
        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0
        #frame1 = tk.Frame(self.fream2,pady=10)
        #frame1.pack()
        var = tk.IntVar()
        var.set(0)
        label = ttk.Label(self.frame2, text = "表示項目：", font = ("", 12))
        label.place(x = 110, y = 0)
        rdo = ttk.Radiobutton(self.frame2,value=0,variable=var,text="会員ID")
        rdo.place(x = 190, y = 0)
        rdo2 = ttk.Radiobutton(self.frame2,value=1,variable=var,text="氏名")
        rdo2.place(x = 260, y = 0)
        rdo3 = ttk.Radiobutton(self.frame2,value=2,variable=var,text="住所")
        rdo3.place(x = 330, y = 0)
        rdo4 = ttk.Radiobutton(self.frame2,value=3,variable=var,text="電話番号")
        rdo4.place(x = 420, y = 0)
        rdo5 = ttk.Radiobutton(self.frame2,value=4,variable=var,text="生年月日")
        rdo5.place(x = 495, y = 0)
        var1 = tk.IntVar()
        var1.set(0)
        label1 = ttk.Label(self.frame2, text = "表示順：", font = ("", 12))
        label1.place(x = 110, y = 20)
        rdo6 = ttk.Radiobutton(self.frame2,value=0,variable=var1,text="昇順")
        rdo6.place(x = 190, y = 20)
        rdo7 = ttk.Radiobutton(self.frame2,value=1,variable=var1,text="降順")
        rdo7.place(x = 260, y = 20)
        frame3 = ttk.Frame(self.frame2, width = 800, height = 350, borderwidth = 2, relief = 'solid')
        frame3.place(x = 100, y = 60)
        self.tree = ttk.Treeview(frame3)
        self.tree["columns"] = (1, 2, 3, 4, 5, 6)
        self.tree["show"] = "headings"
        self.tree.heading(1, text = "No.")
        self.tree.column(1, width=60)
        self.tree.heading(2, text = "会員ID")
        self.tree.column(2, width=105)
        self.tree.heading(3, text = "氏名")
        self.tree.column(3, width=105)
        self.tree.heading(4, text = "住所")
        self.tree.column(4, width=315)
        self.tree.heading(5, text = "電話番号")
        self.tree.column(5, width=105)
        self.tree.heading(6, text = "生年月日")
        self.tree.column(6, width=105)
        self.tree.place(x = 0, y = 0, height = 345)


        memberlist = Member_list(self.cursor)
        members = None
        members = memberlist.display_member_list()
        if members is not None:
            for member in members:
                self.tree.insert("","end",values=member)

    def Member_confirm(self): #会員情報確認画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 20, padding = [0,22], command = self.Member_widgetnew)
        button1.pack(side = "left")
        button2 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22], command = self. Member_widget)
        button2.pack(side = "left")
        #frame2内にウィジェットを設置
        self.label1 = ttk.Label(self.frame2, text = "会員情報", font = ("", 18))
        self.label1.place(x = 110, y = 40)
        self.label2 = ttk.Label(self.frame2, text = "会員ID：", font = ("", 18))
        self.label2.place(x = 160, y = 90)
        self.label3 = ttk.Label(self.frame2, text = "名前：", font = ("", 18))
        self.label3.place(x = 160, y = 140)
        self.label4 = ttk.Label(self.frame2, text = "住所：", font = ("", 18))
        self.label4.place(x = 160, y = 190)                
        self.label5 = ttk.Label(self.frame2, text = "電話番号：", font = ("", 18))
        self.label5.place(x = 160, y = 240)
        self.label6 = ttk.Label(self.frame2, text = "生年月日：", font = ("", 18))
        self.label6.place(x = 160, y = 290)
        self.label7 = ttk.Label(self.frame2, text = "貸出枚数：", font = ("", 18))
        self.label7.place(x = 160, y = 340)
        self.label8 = ttk.Label(self.frame2, text = "延滞枚数：", font = ("", 18))
        self.label8.place(x = 160, y = 390)

        button2 = ttk.Button(self.frame2, text = "変更", width = 20, padding = [0,7], command = self. Member_change)
        button2.place(x = 700, y = 450)
        button3 = ttk.Button(self.frame2, text = "削除", width = 20, padding = [0,7], command = lambda : NewWindow_choose1("う"))
        button3.place(x = 850, y = 450)
        button4 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self. Member_widgetID)
        button4.place(x = 30, y = 450)

    def Member_widgetnew(self): #新規会員情報入力画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "変更/削除", width = 20, padding = [0,22], command = self.Member_widgetID)
        button1.pack(side = "left")
        button1 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22])
        button1.pack(side = "left")
        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0
        label = ttk.Label(self.frame2, text = "名前：", font = ("", 12))
        label.place(x = 50, y = 80)
        self.editBox = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox.place(x = 150, y = 73)
        label1 = ttk.Label(self.frame2, text = "住所：", font = ("", 12))
        label1.place(x = 50, y = 135)
        self.editBox1 = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox1.place(x = 150, y = 128)
        label2 = ttk.Label(self.frame2, text = "電話番号：", font = ("", 12))
        label2.place(x = 50, y = 190)
        label21 = ttk.Label(self.frame2, text = "-", font = ("", 12))
        label21.place(x = 312, y = 190)
        label22 = ttk.Label(self.frame2, text = "-", font = ("", 12))
        label22.place(x = 502, y = 190)
        self.editBox21 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox21.place(x = 150, y = 183)
        self.editBox22 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox22.place(x = 340, y = 183)
        self.editBox23 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox23.place(x = 530, y = 183)
        label3 = ttk.Label(self.frame2, text = "生年月日：", font = ("", 12))
        label3.place(x = 50, y = 245)
        label31 = ttk.Label(self.frame2, text = "年", font = ("", 12))
        label31.place(x = 308, y = 245)
        label32 = ttk.Label(self.frame2, text = "月", font = ("", 12))
        label32.place(x = 498, y = 245)
        label33 = ttk.Label(self.frame2, text = "日", font = ("", 12))
        label33.place(x = 688, y = 245)
        self.editBox31 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox31.place(x = 150, y = 238)
        self.editBox32 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox32.place(x = 340, y = 238)
        self.editBox33 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox33.place(x = 530, y = 238)
        button2 = ttk.Button(self.frame2, text = "確認", width = 20, padding = [0,7], command = lambda: (self. on_button2_click4(), self. Member_confirmnew()))
        button2.place(x = 750, y = 450)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self. Member_menu)
        button3.place(x = 30, y = 450)

    def on_button2_click4(self):
        self.Newmembername = self.editBox.get()
        print("名前:",self.Newmembername)   
        self.Newmemberadress = self.editBox1.get()
        print("住所:",self.Newmemberadress)
        Newmemberphone1 = self.editBox21.get()
        Newmemberphone2 = self.editBox22.get()
        Newmemberphone3 = self.editBox23.get()
        if not Newmemberphone1.isdigit():  # アルファベットや記号が含まれている場合
            print("エラー", "1枠目：2~4桁の数字のみで入力してください。")  # エラーメッセージを表示
        elif len(Newmemberphone1) < 2 or len(Newmemberphone1) > 4:  # 12桁かどうかをチェック
            print("エラー", "1枠目2~4桁の数字のみで入力してください。")
        elif not Newmemberphone2.isdigit():  # アルファベットや記号が含まれている場合
            print("エラー", "2枠目：2~4桁の数字のみで入力してください。") 
        elif len(Newmemberphone2) < 2 or len(Newmemberphone2) > 4:  # 12桁かどうかをチェック
            print("エラー", "2枠目：2~4桁の数字のみで入力してください。")
        elif not Newmemberphone2.isdigit():  # アルファベットや記号が含まれている場合
            print("エラー", "3枠目：4桁の数字のみで入力してください。") 
        elif len(Newmemberphone3) != 4:  # 12桁かどうかをチェック
            print("エラー", "3枠目：4桁の数字のみで入力してください。")
        else:
            self.Newphone = Newmemberphone1 + '-' + Newmemberphone2 + '-' + Newmemberphone3
            print("電話番号:",Newmemberphone1,'-',Newmemberphone2,'-',Newmemberphone3) 
        Newmemberyear = self.editBox31.get()
        Newmembermonth = self.editBox32.get()
        Newmemberday = self.editBox33.get()
        # 生年月日の入力が数字であることを確認
        if not Newmemberyear.isdigit() or len(Newmemberyear) != 4:
            print("エラー", "生年月日は4桁の数字（年）で入力してください")
        elif not Newmembermonth.isdigit() or len(Newmembermonth) < 1 or len(Newmembermonth) > 2:
            print("エラー", "生年月日は1〜2桁の数字（月）で入力してください")
        elif not Newmemberday.isdigit() or len(Newmemberday) < 1 or len(Newmemberday) > 2:
            print("エラー", "生年月日は1〜2桁の数字（日）で入力してください")
        else:
            # ここで正しい日付かどうかを確認
            try:
                self.Newbirthdate = date(int(Newmemberyear), int(Newmembermonth), int(Newmemberday))
                print("生年月日:", Newmemberyear, '年', Newmembermonth, '月', Newmemberday, '日')
            except ValueError:
                print("エラー", "正しい日付を入力してください。")


    def Member_confirmnew(self): #新規会員情報確認画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "変更/削除", width = 20, padding = [0,22],command = self.Member_widgetID)
        button1.pack(side = "left")
        button1 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22],command = self.Member_widget)
        button1.pack(side = "left")
        #frame2内にウィジェットを設置
        self.label1 = ttk.Label(self.frame2, text = "情報確認画面", font = ("", 22))
        self.label1.place(x = 100, y = 40)
        self.label2 = ttk.Label(self.frame2, text = "名前：" + self.Newmembername, font = ("", 22))
        self.label2.place(x = 160, y = 110)
        self.label3 = ttk.Label(self.frame2, text = "住所：" + self.Newmemberadress, font = ("", 22))
        self.label3.place(x = 160, y = 180)
        self.label4 = ttk.Label(self.frame2, text = "電話番号：" + self.Newphone, font = ("", 22))
        self.label4.place(x = 160, y = 250)
        self.label5 = ttk.Label(self.frame2, text = "生年月日：" + str(self.Newbirthdate), font = ("", 22))
        self.label5.place(x = 160, y = 320)
        self.member_new = Member_new(self.Newmembername, self.Newmemberadress, self.Newphone,self.Newbirthdate, self.cursor)
        button2 = ttk.Button(self.frame2, text = "登録", width = 20, padding = [0,7], command = lambda : self.on_button2_click9())
        button2.place(x = 750, y = 450)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self.Member_widgetnew)
        button3.place(x = 30, y = 450)

    def on_button2_click9(self):
        memberid = self.member_new.register_new_member()
        NewWindow_report("新しい会員を登録しました。会員ID: " + memberid)

    def Member_change(self): #会員情報変更入力画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 20, padding = [0,22], command = self.Member_widgetnew)
        button1.pack(side = "left")
        button2 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22], command = self.Member_widget)
        button2.pack(side = "left")
        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0
        label = ttk.Label(self.frame2, text = "名前：", font = ("", 12))
        label.place(x = 50, y = 80)
        self.editBox = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox.place(x = 150, y = 73)
        label1 = ttk.Label(self.frame2, text = "住所：", font = ("", 12))
        label1.place(x = 50, y = 135)
        self.editBox1 = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox1.place(x = 150, y = 128)
        label2 = ttk.Label(self.frame2, text = "電話番号：", font = ("", 12))
        label2.place(x = 50, y = 190)
        label21 = ttk.Label(self.frame2, text = "-", font = ("", 12))
        label21.place(x = 312, y = 190)
        label22 = ttk.Label(self.frame2, text = "-", font = ("", 12))
        label22.place(x = 502, y = 190)
        self.editBox21 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox21.place(x = 150, y = 183)
        self.editBox22 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox22.place(x = 340, y = 183)
        self.editBox23 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox23.place(x = 530, y = 183)
        label3 = ttk.Label(self.frame2, text = "生年月日：", font = ("", 12))
        label3.place(x = 50, y = 245)
        label31 = ttk.Label(self.frame2, text = "年", font = ("", 12))
        label31.place(x = 308, y = 245)
        label32 = ttk.Label(self.frame2, text = "月", font = ("", 12))
        label32.place(x = 498, y = 245)
        label33 = ttk.Label(self.frame2, text = "日", font = ("", 12))
        label33.place(x = 688, y = 245)
        self.editBox31 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox31.place(x = 150, y = 238)
        self.editBox32 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox32.place(x = 340, y = 238)
        self.editBox33 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox33.place(x = 530, y = 238)
        button2 = ttk.Button(self.frame2, text = "確認", width = 20, padding = [0,7], command = lambda: (self.on_button2_click5(), self. Member_changeconfirm()))
        button2.place(x = 750, y = 450)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self. Member_confirm)
        button3.place(x = 30, y = 450)

    def on_button2_click5(self):
        chmembername = self.editBox.get()
        if chmembername == "":
            chmembername = None 
        print("名前:",chmembername) 
        chmemberadress = self.editBox1.get()
        if chmemberadress == "":
            chmemberadress = None
        print("住所:",chmemberadress)
        chmemberphone1 = self.editBox21.get()
        chmemberphone2 = self.editBox22.get()
        chmemberphone3 = self.editBox23.get()
        if chmemberphone1 == "":
            chmemberphone = None
        elif not chmemberphone1.isdigit():  # アルファベットや記号が含まれている場合
            print("エラー", "1枠目：2~4桁の数字のみで入力してください。")  # エラーメッセージを表示
        elif len(chmemberphone1) < 2 or len(chmemberphone1) > 4:  # 12桁かどうかをチェック
            print("エラー", "1枠目2~4桁の数字のみで入力してください。")
        elif not chmemberphone2.isdigit():  # アルファベットや記号が含まれている場合
            print("エラー", "2枠目：2~4桁の数字のみで入力してください。") 
        elif len(chmemberphone2) < 2 or len(chmemberphone2) > 4:  # 12桁かどうかをチェック
            print("エラー", "2枠目：2~4桁の数字のみで入力してください。")
        elif not chmemberphone2.isdigit():  # アルファベットや記号が含まれている場合
            print("エラー", "3枠目：4桁の数字のみで入力してください。") 
        elif len(chmemberphone3) != 4:  # 12桁かどうかをチェック
            print("エラー", "3枠目：4桁の数字のみで入力してください。")
        else:
            chmemberphone = chmemberphone1 + '-' + chmemberphone2 + '-' + chmemberphone3
            print("電話番号:",chmemberphone1,'-',chmemberphone2,'-',chmemberphone3) 
        chmemberyear = self.editBox31.get()
        chmembermonth = self.editBox32.get()
        chmemberday = self.editBox33.get()  
        chmemberbirthdate = None
        if not chmemberyear.isdigit() or len(chmemberyear) != 4:
            print("エラー", "生年月日は4桁の数字（年）で入力してください")
        elif not chmembermonth.isdigit() or len(chmembermonth) < 1 or len(chmembermonth) > 2:
            print("エラー", "生年月日は1〜2桁の数字（月）で入力してください")
        elif not chmemberday.isdigit() or len(chmemberday) < 1 or len(chmemberday) > 2:
            print("エラー", "生年月日は1〜2桁の数字（日）で入力してください")
        else:
            # ここで正しい日付かどうかを確認
            try:
                chmemberbirthdate = date(int(chmemberyear), int(chmembermonth), int(chmemberday))
                print("生年月日:", chmemberyear, '年', chmembermonth, '月', chmemberday, '日')
            except ValueError:
                print("エラー", "正しい日付を入力してください。")
        #print("生年月日:",chmemberyear,'年',chmembermonth,'月',chmemberday,'日') 
        

    def Member_changeconfirm(self): #会員情報変更確認画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 20, padding = [0,22], command = self.Member_widgetnew)
        button1.pack(side = "left")
        button2 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22],command = self.Member_widget)
        button2.pack(side = "left")
        #frame2内にウィジェットを設置
        self.label1 = ttk.Label(self.frame2, text = "情報確認画面", font = ("", 22))
        self.label1.place(x = 100, y = 40)
        self.label2 = ttk.Label(self.frame2, text = "名前：" + self.chmembername, font = ("", 22))
        self.label2.place(x = 160, y = 110)
        self.label3 = ttk.Label(self.frame2, text = "住所：" + self.chmemberadress, font = ("", 22))
        self.label3.place(x = 160, y = 180)
        self.label4 = ttk.Label(self.frame2, text = "電話番号：" + self.chmemberphone, font = ("", 22))
        self.label4.place(x = 160, y = 250)
        self.label5 = ttk.Label(self.frame2, text = "生年月日：" + self.chmemberbirthdate, font = ("", 22))
        self.label5.place(x = 160, y = 320)
        button2 = ttk.Button(self.frame2, text = "登録", width = 20, padding = [0,7], command = lambda : self.member_sud.edit_member_info(self.chmembername, self.chmemberadress, self.chmemberphone, self.chmemberbirthdate))
        button2.place(x = 750, y = 450)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self.Member_change)
        button3.place(x = 30, y = 450)

    def NewWindow_choose1(self, txet):   #会員情報削除確認画面
        self.text = text
        
        newwindow = tk.Tk()
        newwindow.title ("会員情報削除確認画面")
        newwindow.geometry("600x200+350+230")
        frame = ttk.Frame(newwindow)
        frame.pack()
        static = ttk.Label(frame, text = self.text, font = ("", 12))
        static.pack(pady = 65)
        button = ttk.Button(frame, text="はい", width=20, padding=[0, 7], command = lambda: self.on_button2_click8(choose="0"))
        button.pack(side="left", padx=10)
        button1 = ttk.Button(frame, text = "いいえ", width = 20, padding = [0,7], command = lambda: self.on_button2_click8(choose = "1"))
        button1.pack(side="left", padx=10)

    def on_button2_click8(self, choose):
        self.member_sud.Delete_member(choose)

class Goods(): #商品情報機能
    def __init__(self, root, frame, frame1, frame2, static, img, cursor):
        self.root = root
        self.frame = frame
        self.frame1 = frame1
        self.frame2 = frame2
        self.static = static
        self.img = img
        self.cursor = cursor

        self.home = Home(self.root, self.frame, self.frame1, self.frame2, self.static, self.img, self.cursor)

    def Goods_menu(self): #商品情報画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame内のstaticの文字変更
        self.static["text"] = "商品情報管理メニュー"
        #frame1内にホームボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        #frame2内にウィジェットを設置
        #frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #frame3.propagate(False)
        #frame3.pack()
        button1 = ttk.Button(self.frame2, text = "新規登録", width = 50, padding = [0,80], command =self.Goods_widgetnew)
        button1.place(x = 320, y = 50)
        button2 = ttk.Button(self.frame2, text = "変更/削除", width = 50, padding = [0,80], command = self.Goods_widgetID)
        button2.place(x = 150, y = 300)
        button3 = ttk.Button(self.frame2, text = "一覧", width = 50, padding = [0,80],command = self.Goods_widget)
        button3.place(x = 500, y = 300)


    def Goods_widget(self): #一覧画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame内のstaticの文字変更
        self.static["text"] = "商品情報管理メニュー(一覧)"
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 30, padding = [0,22], command =self.Goods_widgetnew)
        button1.pack(side = "left", padx = 10)
        button2 = ttk.Button(self.frame1, text = "変更/削除", width = 30, padding = [0,22], command = self.Goods_widgetID)
        button2.pack(side = "left", padx = 10)
        button3 = ttk.Button(self.frame2, text = "並び替え", width = 20, padding = [0,10])
        button3.place(x = 800,y = 0)
        button4 = ttk.Button(self.frame2, text = "前のページ", width = 20, padding = [0,7])
        button4.place(x = 700, y = 450)
        button5 = ttk.Button(self.frame2, text = "次のページ", width = 20, padding = [0,7])
        button5.place(x = 850, y = 450)
        button6 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self.Goods_menu)
        button6.place(x = 30, y = 450)
        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0
        #frame1 = tk.Frame(self.fream2,pady=10)
        #frame1.pack()
        var = tk.IntVar()
        var.set(0)
        label = ttk.Label(self.frame2, text = "表示項目：", font = ("", 12))
        label.place(x = 110, y = 0)
        rdo = ttk.Radiobutton(self.frame2,value=0,variable=var,text="商品ID")
        rdo.place(x = 190, y = 0)
        rdo2 = ttk.Radiobutton(self.frame2,value=1,variable=var,text="発売日")
        rdo2.place(x = 260, y = 0)
        rdo3 = ttk.Radiobutton(self.frame2,value=2,variable=var,text="貸出/返却日")
        rdo3.place(x = 330, y = 0)
        rdo4 = ttk.Radiobutton(self.frame2,value=3,variable=var,text="貸出回数")
        rdo4.place(x = 420, y = 0)
        rdo5 = ttk.Radiobutton(self.frame2,value=4,variable=var,text="保管場所")
        rdo5.place(x = 495, y = 0)
        var1 = tk.IntVar()
        var1.set(0)
        label1 = ttk.Label(self.frame2, text = "表示順：", font = ("", 12))
        label1.place(x = 110, y = 20)
        rdo6 = ttk.Radiobutton(self.frame2,value=0,variable=var1,text="昇順")
        rdo6.place(x = 190, y = 20)
        rdo7 = ttk.Radiobutton(self.frame2,value=1,variable=var1,text="降順")
        rdo7.place(x = 260, y = 20)
        frame3 = ttk.Frame(self.frame2, width = 800, height = 350, borderwidth = 2, relief = 'solid')
        frame3.place(x = 100, y = 60)
        self.tree = ttk.Treeview(frame3)
        self.tree["columns"] = (1, 2, 3, 4, 5, 6, 7, 8)
        self.tree["show"] = "headings"
        self.tree.heading(1, text = "No.")
        self.tree.column(1, width=60)
        self.tree.heading(2, text = "商品ID")
        self.tree.column(2, width=105)
        self.tree.heading(3, text = "タイトル")
        self.tree.column(3, width=105)
        self.tree.heading(4, text = "ジャンル")
        self.tree.column(4, width=105)
        self.tree.heading(5, text = "発売日")
        self.tree.column(5, width=105)
        self.tree.heading(6, text = "貸出・返却日")
        self.tree.column(6, width=105)
        self.tree.heading(7, text = "貸出状況")
        self.tree.column(7, width=105)
        self.tree.heading(8, text = "保管場所")
        self.tree.column(8, width=105)
        #scroll = ttk.Scroll(frame3, orient=ttk.VERTICAL, command = self.tree.yview)
        #scroll.pack(side = "right", fill = "y")
        #elf.tree["yscrollcommand"] = scroll.set
        #self.tree.pack(fill = 'x')
        self.tree.place(x = 0, y = 0, height = 345)
        #self.tree.insert("", "end", values = ("0","1","2","3","4","5"))
        self.tree.insert("", "end", values=("1"))
        self.tree.insert("", "end", values=("2"))
        self.tree.insert("", "end", values=("3"))
        self.tree.insert("", "end", values=("4"))
        self.tree.insert("", "end", values=("5"))

    def Goods_widgetnew(self): #新規商品情報入力画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "変更/削除", width = 20, padding = [0,22],command = self.Goods_widgetID)
        button1.pack(side = "left")
        button2 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22],command = self.Goods_widget)
        button2.pack(side = "left")
        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0
        label = ttk.Label(self.frame2, text = "タイトル：", font = ("", 12))
        label.place(x = 50, y = 80)
        self.editBox = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox.place(x = 150, y = 73)
        label1 = ttk.Label(self.frame2, text = "ジャンル：", font = ("", 12))
        label1.place(x = 50, y = 135)
        self.editBox1 = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox1.place(x = 150, y = 128)
        label2 = ttk.Label(self.frame2, text = "発売日：", font = ("", 12))
        label2.place(x = 50, y = 190)
        label21 = ttk.Label(self.frame2, text = "年", font = ("", 12))
        label21.place(x = 308, y = 190)
        label22 = ttk.Label(self.frame2, text = "月", font = ("", 12))
        label22.place(x = 498, y = 190)
        label23 = ttk.Label(self.frame2, text = "日", font = ("", 12))
        label23.place(x = 688, y = 190)
        self.editBox21 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox21.place(x = 150, y = 183)
        self.editBox22 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox22.place(x = 340, y = 183)
        self.editBox23 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox23.place(x = 530, y = 183)
        button2 = ttk.Button(self.frame2, text = "確認", width = 20, padding = [0,7], command = lambda: (self. on_button2_click6(), self. Goods_confirmnew()))
        button2.place(x = 750, y = 450)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self.Goods_menu)
        button3.place(x = 30, y = 450)

    def on_button2_click6(self):
        Newgoodstitle = self.editBox.get()
        NewgoodsGenre = self.editBox1.get()
        Newgoodsyear = self.editBox21.get()
        Newgoodsmonth = self.editBox22.get()
        Newgoodsday = self.editBox23.get()
        print(Newgoodsyear)  # これで年がコマンドプロンプトに表示されるはず
        if not (Newgoodsyear.isdigit() and Newgoodsmonth.isdigit() and Newgoodsday.isdigit()):
            print("エラー: 年・月・日は数字のみで入力してください。")
            return  # 処理を中断
        if len(Newgoodsyear) != 4:  # 年は4桁か？
            print("エラー: 年は4桁で入力してください。")
            return
        year = int(Newgoodsyear)
        month = int(Newgoodsmonth)
        day = int(Newgoodsday)
        current_year = date.today().year
        if not (1800 <= year <= current_year):  # 年の範囲チェック
            print(f"エラー: 年は1800〜{current_year}の範囲で入力してください。")
            return
        if not (1 <= month <= 12):  # 月の範囲チェック
            print("エラー: 月は1〜12の範囲で入力してください。")
            return
        try:
            date(year, month, day)  # 日付が存在するかチェック
        except ValueError:
            print("エラー: 存在しない日付です。")
            return
        # ここまで来たら正しい日付
        print("タイトル:", Newgoodstitle)
        print("ジャンル:", NewgoodsGenre)
        print("発売日:", f"{year}年 {month}月 {day}日")

    def Goods_confirm(self): #商品情報確認画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 20, padding = [0,22], command = self.Goods_widgetnew)
        button1.pack(side = "left")
        button2 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22],command = self.Goods_widget)
        button2.pack(side = "left")
        #frame2内にウィジェットを設置
        self.label1 = ttk.Label(self.frame2, text = "商品情報", font = ("", 18))
        self.label1.place(x = 110, y = 40)
        self.label2 = ttk.Label(self.frame2, text = "商品ID：", font = ("", 18))
        self.label2.place(x = 160, y = 80)
        self.label3 = ttk.Label(self.frame2, text = "タイトル：", font = ("", 18))
        self.label3.place(x = 160, y = 120)
        self.label4 = ttk.Label(self.frame2, text = "ジャンル：", font = ("", 18))
        self.label4.place(x = 160, y = 160)
        self.label5 = ttk.Label(self.frame2, text = "発売日：", font = ("", 18))
        self.label5.place(x = 160, y = 200)
        self.label6 = ttk.Label(self.frame2, text = "貸出・返却日：", font = ("", 18))
        self.label6.place(x = 160, y = 240)
        self.label7 = ttk.Label(self.frame2, text = "貸出会員ID：", font = ("", 18))
        self.label7.place(x = 160, y = 280)
        self.label8 = ttk.Label(self.frame2, text = "貸出状況：", font = ("", 18))
        self.label8.place(x = 160, y = 320)
        self.label9 = ttk.Label(self.frame2, text = "貸出回数：", font = ("", 18))
        self.label9.place(x = 160, y = 360)
        self.label10 = ttk.Label(self.frame2, text = "保管場所：", font = ("", 18))
        self.label10.place(x = 160, y = 400)
        button2 = ttk.Button(self.frame2, text = "変更", width = 20, padding = [0,7],command = self.Goods_change)
        button2.place(x = 700, y = 450)
        button3 = ttk.Button(self.frame2, text = "削除", width = 20, padding = [0,7], command = lambda : NewWindow_choose("い"))
        button3.place(x = 850, y = 450)
        button4 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7],command = self.Goods_widgetID)
        button4.place(x = 30, y = 450)

    def Goods_change(self): #商品情報変更入力画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        self.var = tk.IntVar()
        self.var.set(0)
        self.var1 = tk.IntVar()
        self.var1.set(0)
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 20, padding = [0,22], command = self.Goods_widgetnew)
        button1.pack(side = "left")
        button2 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22],command = self.Goods_widget)
        button2.pack(side = "left")
        #frame2内にウィジェットを設置
        #self.frame3 = ttk.Frame(self.frame2, width = 1000, height = 510)
        #self.frame3.propagate(False)
        #self.frame3.pack()
        self.count = 0
        label = ttk.Label(self.frame2, text = "タイトル：", font = ("", 12))
        label.place(x = 50, y = 25)
        self.editBox = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox.place(x = 150, y = 18)
        label1 = ttk.Label(self.frame2, text = "ジャンル：", font = ("", 12))
        label1.place(x = 50, y = 80)
        self.editBox1 = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox1.place(x = 150, y = 73)
        label2 = ttk.Label(self.frame2, text = "発売日：", font = ("", 12))
        label2.place(x = 50, y = 135)
        label21 = ttk.Label(self.frame2, text = "年", font = ("", 12))
        label21.place(x = 308, y = 135)
        label22 = ttk.Label(self.frame2, text = "月", font = ("", 12))
        label22.place(x = 498, y = 135)
        label23 = ttk.Label(self.frame2, text = "日", font = ("", 12))
        label23.place(x = 688, y = 135)
        self.editBox21 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox21.place(x = 150, y = 128)
        self.editBox22 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox22.place(x = 340, y = 128)
        self.editBox23 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox23.place(x = 530, y = 128)
        label3 = ttk.Label(self.frame2, text = "貸出・返却日：", font = ("", 12))
        label3.place(x = 50, y = 190)
        label31 = ttk.Label(self.frame2, text = "年", font = ("", 12))
        label31.place(x = 308, y = 190)
        label32 = ttk.Label(self.frame2, text = "月", font = ("", 12))
        label32.place(x = 498, y = 190)
        label33 = ttk.Label(self.frame2, text = "日", font = ("", 12))
        label33.place(x = 688, y = 190)
        self.editBox31 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox31.place(x = 150, y = 183)
        self.editBox32 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox32.place(x = 340, y = 183)
        self.editBox33 = ttk.Entry(self.frame2, width = 10, font = ("", 20))
        self.editBox33.place(x = 530, y = 183)
        label4 = ttk.Label(self.frame2, text = "貸出会員ID：", font = ("", 12))
        label4.place(x = 50, y = 245)
        self.editBox4 = ttk.Entry(self.frame2, width = 40, font = ("", 20))
        self.editBox4.place(x = 150, y = 238)
        #var = tk.IntVar()
        #var.set(0)
        label5 = ttk.Label(self.frame2, text = "貸出状況：", font = ("", 12))
        label5.place(x = 50, y = 300)
        rdo = ttk.Radiobutton(self.frame2,value=0,variable=self.var,text="貸出可")
        rdo.place(x = 150, y = 300)
        rdo1 = ttk.Radiobutton(self.frame2,value=1,variable=self.var,text="貸出中")
        rdo1.place(x = 300, y = 300)
        #var1 = tk.IntVar()
        #var1.set(0)
        label6 = ttk.Label(self.frame2, text = "保管場所：", font = ("", 12))
        label6.place(x = 50, y = 355)
        rdo = ttk.Radiobutton(self.frame2,value=0,variable=self.var1,text="店頭")
        rdo.place(x = 150, y = 355)
        rdo1 = ttk.Radiobutton(self.frame2,value=1,variable=self.var1,text="倉庫")
        rdo1.place(x = 300, y = 355)
        button2 = ttk.Button(self.frame2, text = "確認", width = 20, padding = [0,7], command = lambda: (self. on_button2_click7(), self. Goods_changeconfirm()))
        button2.place(x = 750, y = 450)
        button3 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7], command = self. Goods_confirm)
        button3.place(x = 30, y = 450)

    import calendar

    def on_button2_click7(self):
        chgoodstitle = self.editBox.get()
        chgoodsGenre = self.editBox1.get()
        chgoodsyear = self.editBox21.get()
        chgoodsmonth = self.editBox22.get()
        chgoodsday = self.editBox23.get()
        chgoodsyear2 = self.editBox31.get()
        chgoodsmonth2 = self.editBox32.get()
        chgoodsday2 = self.editBox33.get()
        chlendmemberID = self.editBox4.get()
        chlend_status = "貸出可" if self.var.get() == 0 else "貸出中"
        chstorage_location = "店頭" if self.var1.get() == 0 else "倉庫"
        # 発売日と貸出・返却日のバリデーション
        try:
            # 発売日（年、月、日）
            chgoodsyear = int(chgoodsyear)
            chgoodsmonth = int(chgoodsmonth)
            chgoodsday = int(chgoodsday)
            # 貸出・返却日（年、月、日）
            chgoodsyear2 = int(chgoodsyear2)
            chgoodsmonth2 = int(chgoodsmonth2)
            chgoodsday2 = int(chgoodsday2)
            
            #発売日の日付チェック
            current_year = date.today().year
            if not (1800 <= chgoodsyear <= current_year):  # 年の範囲チェック
                print(f"エラー: 年は1800〜{current_year}の範囲で入力してください。")
                return
            if not (1 <= chgoodsmonth <= 12):  # 月の範囲チェック
                print("エラー: 月は1〜12の範囲で入力してください。")
                return
            try:
                date(chgoodsyear, chgoodsmonth, chgoodsday)  # 日付が存在するかチェック
            except ValueError:
                print("エラー: 発売日が存在しない日付です。")
                return

            #貸出・返却日の日付チェック
            if not (1800 <= chgoodsyear2 <= current_year):  # 年の範囲チェック
                print(f"エラー: 年は1800〜{current_year}の範囲で入力してください。")
                return
            if not (1 <= chgoodsmonth2 <= 12):  # 月の範囲チェック
                print("エラー: 月は1〜12の範囲で入力してください。")
                return
            try:
                date(chgoodsyear2, chgoodsmonth2, chgoodsday2)  # 日付が存在するかチェック
            except ValueError:
                print("エラー: 貸出・返却日が存在しない日付です。")
                return
            # 貸出会員ID（12桁の数字かどうかをチェック）
            if not chlendmemberID.isdigit() or len(chlendmemberID) != 12:
                print("エラー: 貸出会員IDは12桁の数字で入力してください。")
            else:
                print("タイトル:", chgoodstitle)
                print("ジャンル:", chgoodsGenre)
                print("発売日:", chgoodsyear, '年', chgoodsmonth, '月', chgoodsday, '日')
                print("貸出・返却日:", chgoodsyear2, '年', chgoodsmonth2, '月', chgoodsday2, '日')
                print("貸出会員ID:", chlendmemberID)
                print("貸出状況:", chlend_status)
                print("保管場所:", chstorage_location)
        except ValueError:
            print("エラー: 年、月、日には整数を入力してください。")

    '''def on_button2_click7(self):
        chgoodstitle = self.editBox.get()  
        chgoodsGenre = self.editBox1.get()  
        chgoodsyear = self.editBox21.get()
        chgoodsmonth = self.editBox22.get()
        chgoodsday = self.editBox23.get()
        chgoodsyear2 = self.editBox31.get()
        chgoodsmonth2 = self.editBox32.get()
        chgoodsday2 = self.editBox33.get()
        chlendmemberID = self.editBox4.get() 
        chlend_status = "貸出可" if self.var.get() == 0 else "貸出中"
        chstorage_location = "店頭" if self.var1.get() == 0 else "倉庫"
        
        print("タイトル:",chgoodstitle)  
        print("ジャンル:",chgoodsGenre)
        print("発売日:",chgoodsyear,'年',chgoodsmonth,'月',chgoodsday,'日') 
        print("貸出・返却日:",chgoodsyear2,'年',chgoodsmonth2,'月',chgoodsday2,'日') 
        print("貸出会員ID:",chlendmemberID )
        print("貸出状況:", chlend_status)
        print("保管場所:", chstorage_location)''' 

    def Goods_changeconfirm(self): #商品情報変更確認画面
        #frame1内のウィジェットを全削除
        children = self.frame1.winfo_children()
        for child in children:
            child.destroy()
        #frame2内のウィジェットを全削除
        children = self.frame2.winfo_children()
        for child in children:
            child.destroy()
        #frame1内に切り替えボタンを設置
        button = ttk.Button(self.frame1, image = self.img, command = self.home.Home_widget)
        button.pack(side = "left", padx = 10)
        button1 = ttk.Button(self.frame1, text = "新規登録", width = 20, padding = [0,22], command = self.Goods_widgetnew)
        button1.pack(side = "left")
        button2 = ttk.Button(self.frame1, text = "一覧", width = 20, padding = [0,22],command = self.Goods_widget)
        button2.pack(side = "left")
        #frame2内にウィジェットを設置
        self.label1 = ttk.Label(self.frame2, text = "商品情報", font = ("", 18))
        self.label1.place(x = 110, y = 40)
        self.label2 = ttk.Label(self.frame2, text = "商品ID：", font = ("", 18))
        self.label2.place(x = 160, y = 80)
        self.label3 = ttk.Label(self.frame2, text = "タイトル：", font = ("", 18))
        self.label3.place(x = 160, y = 120)
        self.label4 = ttk.Label(self.frame2, text = "ジャンル：", font = ("", 18))
        self.label4.place(x = 160, y = 160)
        self.label5 = ttk.Label(self.frame2, text = "発売日：", font = ("", 18))
        self.label5.place(x = 160, y = 200)
        self.label6 = ttk.Label(self.frame2, text = "貸出・返却日：", font = ("", 18))
        self.label6.place(x = 160, y = 240)
        self.label7 = ttk.Label(self.frame2, text = "貸出会員ID：", font = ("", 18))
        self.label7.place(x = 160, y = 280)
        self.label8 = ttk.Label(self.frame2, text = "貸出状況：", font = ("", 18))
        self.label8.place(x = 160, y = 320)
        self.label9 = ttk.Label(self.frame2, text = "保管場所：", font = ("", 18))
        self.label9.place(x = 160, y = 360)
        button3 = ttk.Button(self.frame2, text = "登録", width = 20, padding = [0,7])
        button3.place(x = 850, y = 450)
        button4 = ttk.Button(self.frame2, text = "戻る", width = 20, padding = [0,7],command = self.Goods_change)
        button4.place(x = 30, y = 450)
        
class NewWindow_report():
    def __init__(self, text):
        self.text = text
        
        newwindow = tk.Tk()
        newwindow.title ("DVDレンタルシステム")
        newwindow.geometry("600x200+350+230")  

        frame = ttk.Frame(newwindow)
        frame.pack()
        static = ttk.Label(frame, text = self.text, font = ("", 12))
        static.pack(pady = 65)
        button = ttk.Button(frame, text = "確認", width = 20, padding = [0,7], command = lambda : newwindow.destroy())
        button.pack()

        newwindow.mainloop()

class NewWindow_choose():   #商品情報削除確認画面
    def __init__(self, text):
        self.text = text
        
        newwindow = tk.Tk()
        newwindow.title ("商品情報削除確認画面")
        newwindow.geometry("600x200+350+230")
        frame = ttk.Frame(newwindow)
        frame.pack()
        static = ttk.Label(frame, text = self.text, font = ("", 12))
        static.pack(pady = 65)
        button = ttk.Button(frame, text = "はい", width = 20, padding = [0,7])
        button.pack(side="left", padx=10)
        button1 = ttk.Button(frame, text = "いいえ", width = 20, padding = [0,7])
        button1.pack(side="left", padx=10)

        newwindow.mainloop()       
     


def main(cursor):
    app = Application(cursor)
    app.mainloop

if __name__ == "__main__":
    try:
        connection = psycopg2.connect(database_url, sslmode='require')
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        main(cursor)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()        