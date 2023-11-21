# unified_stock_app.py

import tkinter as tk
import twstock
import time
import requests
import pandas as pd

def line_notify(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {"message": msg}
    notify = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return notify.status_code

def send_line_notification(mode, real_price, counter_line, token, stock_name):
    print(stock_name + "目前股價" + str(real_price))
    if mode == 1:
        msg = (stock_name + "目前股價為" + str(real_price) + "可以賣出股票了")
    elif mode == 2:
        msg = (stock_name + "目前股價為" + str(real_price) + "可以買入股票了")
    else:
        msg = (stock_name + "股價未達預期價格")
    code = line_notify(token, msg)
    if code == 200:
        counter_line += 1
        print("第" + str(counter_line) + "次發送訊息")
    else:
        print("訊息發送失敗")
    return counter_line

def get_stock_name(number):
    all_stock = pd.read_excel('all_stock.xlsx')
    c = all_stock[(all_stock['證券代號'] == number) | (all_stock['證券代號'] == int(number))]
    result = c['證券名稱']
    return result

def on_button_click():
    maintoken = token_entry.get()
    stock_number = stock_entry.get()
    sell_price = sell_spin.get()
    buy_price = buy_spin.get()
    notify_time = time_gap_spin.get()

    token_label.config(text="Line Token：" + maintoken)
    stock_label.config(text="股票代號：" + stock_number)
    sell_price_label.config(text="理想賣出價格：" + sell_price)
    buy_price_label.config(text="理想買入價格：" + buy_price)
    time_gap_label.config(text="間隔時間：" + notify_time + "分鐘")
    # 立即更新視窗內容
    window.update_idletasks()

    pick_stock_and_notify(maintoken, stock_number, sell_price, buy_price, notify_time)

def pick_stock_and_notify(token, stock_number, sell_price, buy_price, notify_time):
    st_num = str(stock_number)
    counter_line = 0
    counter_error = 0
    print('開始執行')
    
    while True:
        real_date = twstock.realtime.get(st_num)
        st_name = get_stock_name(st_num)

        if counter_line <= 4:
            if real_date['success']:
                real_price = real_date['realtime']['latest_trade_price']

                if real_price != '-':
                    counter_line += 1

                    if float(real_price) >= float(sell_price):
                        counter_line = send_line_notification(1, real_price, counter_line, token, st_name)
                    elif float(real_price) <= float(buy_price):
                        counter_line = send_line_notification(2, real_price, counter_line, token, st_name)
                    else:
                        counter_line = send_line_notification(3, real_price, counter_line, token, st_name)
                else:
                    print('twstock 讀取錯誤，錯誤原因:' + real_date['rtmessage'])
                    counter_error += 1

                    if counter_error >= 3:
                        print("程式結束")
                        break
            time.sleep(int(notify_time) * 60)  # 5分鐘傳一次

# 主視窗
window = tk.Tk()
window.title("即時股價查詢")
window.geometry('600x400')

#GUI 部分
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

# 確認紐
button = tk.Button(window, text="確認", command=on_button_click)
button.pack()

# 啟動事件
window.mainloop()
