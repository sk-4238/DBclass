import tkinter as tk
from tkinter import ttk

 

class NewWindow_choose():
    def __init__(self, text):
        self.text = text
        
        newwindow = tk.Tk()
        newwindow.title ("DVDレンタルシステム")
        newwindow.geometry("600x200+350+230")  

        frame = ttk.Frame(newwindow)
        frame.pack()
        static = ttk.Label(frame, text = self.text, font = ("", 12))
        static.pack(pady = 65)
        button = ttk.Button(frame, text = "はい", width = 20, padding = [0,7])
        button.place(x = 0, y = 130)
        button1 = ttk.Button(frame, text = "いいえ", width = 20, padding = [0,7])
        button1.place(x = 160, y = 130)

        newwindow.mainloop()



def main():
    app = NewWindow_choose("商品ID：\nの情報を完全に削除してもよろしいですか。")
    app.mainloop

if __name__ == "__main__":
    main()