import tkinter as tk
import pandas  as pd


def on_close():
    window1.destroy()


def login_success(): #登入成功的介面
    login_success_window = tk.Toplevel(window1)
    login_success_window.title("登入成功")
    login_success_window.geometry('100x100')

    success_label = tk.Label(login_success_window,text="登入成功")
    success_label.pack()
    
    run_next_py()
        
def run_next_py():
    import os
    import stock_bot
    import subprocess
    #subprocess.call("stock.py")
    import sys

     # 關閉目前的檔案
    current_script = sys.argv[0]
    subprocess.run(['taskkill', '/f', '/im', 'python.exe', '/fi', f'imagename eq {current_script}'], shell=True)  # Windows
    # 如果是在 macOS 或 Linux，可以使用下面的命令
    # subprocess.run(['pkill', '-f', current_script])

    # 開啟新的檔案
    new_script = 'stock.py'  # 替換成你的新檔案路徑
    subprocess.run(['python', new_script], shell=True)    

def login_fail1(): #登入失敗的介面(密碼錯誤)
    login_fail_window = tk.Toplevel(window1)
    login_fail_window.title("登入失敗")
    login_fail_window.geometry('200x100')

    fail_label = tk.Label(login_fail_window,text="登入失敗，密碼輸入錯誤")
    fail_label.pack()
    
def login_fail2(): #登入失敗的介面(無用戶)
    login_fail_window = tk.Toplevel(window1)
    login_fail_window.title("登入失敗")
    login_fail_window.geometry('200x100')

    fail_label = tk.Label(login_fail_window,text="登入失敗，找不到用戶。")
    fail_label.pack()

    ask_label=tk.Label(login_fail_window,text="是否要註冊帳號")
    ask_label.pack()

    yes_button=tk.Button(login_fail_window,text="確認",command=yes)
    yes_button.pack()

    no_button=tk.Button(login_fail_window,text="取消",command=no)
    no_button.pack()

def yes(): #想要註冊
    register_window()

def no():  #不想要註冊
    window1.destroy()

def login_user(username, password): #檢查登入
    try:
        user_data = pd.read_excel('user_data.xlsx')
        user_row=user_data[user_data["Username"] == username]
        if not user_row.empty:
            data_password = user_row["Password"] .values[0]
            if data_password == password:
                print(f'用戶{username}登入成功!')
                login_success()
                return True
            else:
                print("登入失敗，密碼錯誤!")
                login_fail1()
                return False
        else:
            print("登入失敗，找不到用戶。")
            login_fail2()
            return False
    except FileNotFoundError:
        print('登入失敗，找不到用戶資料檔案。')
        return False



    

def login_window(): #輸入登入資料
    login_window=tk.Toplevel(window1)
    login_window.title('登入')
    login_window.geometry('300x300')

    login_label=tk.Label(login_window,text="請輸入用戶名稱和密碼：")
    login_label.pack()
    
    username_label=tk.Label(login_window,text="用戶名稱：")
    username_label.pack()

    username_entry=tk.Entry(login_window)
    username_entry.pack()

    password_label=tk.Label(login_window,text='密碼')
    password_label.pack()
    
    password_entry=tk.Entry(login_window,show="*")
    password_entry.pack()

    def login():
        username=username_entry.get()
        password=password_entry.get()

        if login_user(username,password):
            login_window.destroy()
            
    
    login_button=tk.Button(login_window,text='登入',command=login)
    login_button.pack()
        
def register_user(username,password, token): #檢查註冊
    user_data = pd.DataFrame({'Username': [username],'Password':[password], 'Token': [token]})
    try:
        existing_data = pd.read_excel('user_data.xlsx')
        updated_data = pd.concat([existing_data, user_data], ignore_index=True)
        updated_data.to_excel('user_data.xlsx', index=False)
        print(f"用戶 {username} 註冊成功！")
        register_success()
        return True
    except FileNotFoundError:
        user_data.to_excel('user_data.xlsx', index=False)
        print(f"用戶 {username} 註冊成功！ (首次註冊)")
        register_success()
        return True



def register_window():  # 輸入註冊資料
    register_window_top = tk.Toplevel(window1)
    register_window_top.title('註冊')
    register_window_top.geometry('300x300')

    login_label = tk.Label(register_window_top, text="請輸入用戶名稱、密碼和Line Token：")
    login_label.pack()

    username_label = tk.Label(register_window_top, text="用戶名稱：")
    username_label.pack()

    username_entry = tk.Entry(register_window_top)
    username_entry.pack()

    password_label = tk.Label(register_window_top, text='密碼')
    password_label.pack()

    password_entry = tk.Entry(register_window_top,show="*")
    password_entry.pack()

    token_label = tk.Label(register_window_top, text="Token:")
    token_label.pack()

    token_entry = tk.Entry(register_window_top,show='*')
    token_entry.pack()

    def register():
        username = username_entry.get()
        password = password_entry.get()
        token = token_entry.get()

        if register_user(username, password, token):
            register_window_top.destroy()

    register_button = tk.Button(register_window_top, text="註冊", command=register)
    register_button.pack()

def register_success(): #註冊成功的介面
    reg_success_window = tk.Toplevel(window1)
    reg_success_window.title("註冊成功")
    reg_success_window.geometry('200x100')

    success_label = tk.Label(reg_success_window,text="註冊成功")
    success_label.pack()


#主程式
window1=tk.Tk()
window1.title ('登入或註冊')
window1.geometry('300x100')
login_button=tk.Button(window1,text='登入',command=login_window)
login_button.pack()
register_button=tk.Button(window1,text='註冊',command=yes)
register_button.pack()

window1.mainloop()