import tkinter as tk
import line_stock_bot
import subprocess

def on_closing():
    # 視窗關閉時的處理程式
    window.destroy()  # 銷毀主視窗
    # 這裡可以添加其他的結束執行的代碼

def on_button_click():
    global maintoken, stock_number, sellprice, buyprice, notifytime
    maintoken = token_entry.get()
    stock_number = stock_entry.get()
    sellprice = sell_spin.get()
    buyprice = buy_spin.get()
    notifytime = time_gap_spin.get()
    token_label.config(text="Line Token：" + maintoken)
    stock_label.config(text="股票代號：" + stock_number)
    sell_price_label.config(text="理想賣出價格：" + sellprice)
    buy_price_label.config(text="理想買入價格：" + buyprice)
    time_gap_label.config(text="間隔時間：" + notifytime + "分鐘")
    subprocess.run(["python", "line_stock_bot.py"])

stnumber=0
selling_price=0
buying_price=0


# 主視窗
window = tk.Tk()
window.title("即時股價查詢")
window.geometry('600x400')



# 用戶line token
usertoken = tk.Label(window, text="輸入你的Line token:")
usertoken.pack()

# line token 输入框
token_entry = tk.Entry(window)
token_entry.pack()
maintoken=token_entry.get()

#用戶想關注股票的代號
goal_stock=tk.Label(window, text="想關注的股票代號")
goal_stock.pack()

#股票代號輸入框
stock_entry = tk.Entry(window)
stock_entry.pack()
stock_number=stock_entry.get()
#理想賣出價格
want_sell=tk.Label(window, text="理想賣出價格")
want_sell.pack()

#賣出價格輸入框
sell_spin = tk.Spinbox(window,from_=1.0,to=5000.0,width=5,increment=0.01)
sell_spin.pack()
sellprice=sell_spin.get()
#理想買入價格
want_buy=tk.Label(window, text="理想買入價格")
want_buy.pack()

#買入價格輸入框
buy_spin = tk.Spinbox(window,from_=1.0,to=5000.0,width=5,increment=0.01)
buy_spin.pack()
buyprice=buy_spin.get()
#通知發送的間隔時間
time_gap=tk.Label(window, text="通知間隔時間(分鐘數)")
time_gap.pack()

#間隔時間輸入框
time_gap_spin = tk.Spinbox(window,from_=1,to=60,width=5)
time_gap_spin.pack()
notifytime=time_gap_spin.get()
# 確認紐
button = tk.Button(window, text="確認", command=on_button_click)
button.pack()

#顯示資訊
token_label=tk.Label(window, text="Line Token：")
token_label.pack()
stock_label=tk.Label(window, text="股票代號：")
stock_label.pack()
sell_price_label=tk.Label(window, text="理想賣出價格：")
sell_price_label.pack()
buy_price_label=tk.Label(window, text="理想買入價格：")
buy_price_label.pack()
time_gap_label=tk.Label(window, text="間隔時間：")
time_gap_label.pack()


# 啟動事件
window.mainloop()
