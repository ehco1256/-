import twstock
import pandas as pd
import time
import requests
import gui
import pandas as pd
from gui import maintoken ,stock_number,sellprice,buyprice,notifytime



def lineNotify(token,msg): #Line Notify 發送訊息
  headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
  payload={"message":msg}
  notify=requests.post("https://notify-api.line.me/api/notify",headers=headers,params=payload)
  return notify.status_code #notify.status_code=200為成功 code=401為失敗

def sendline(mode,realprice,counterline,token,stockname):
  print(stockname+"目前股價"+str(realprice))
  if mode ==1:
    msg=(stockname+"目前股價為"+str(realprice)+"可以賣出股票了")
  elif mode ==2:
    msg=(stockname+"目前股價為"+str(realprice)+"可以買入股票了")
  else:
    msg=(stockname+"股價未達預期價格")
  code=lineNotify(token,msg)
  if code==200:
    counterline=counterline+1
    print("第"+str(counterline)+"次發送訊息")
  else:
    print("訊息發送失敗")
  return counterline

def getname(number):
  all_stock=pd.read_excel('all_stock.xlsx')
  c=all_stock[(all_stock['證券代號']== number ) | (all_stock['證券代號'] == int(number))]
  result = c['證券名稱']
  return result


token = str(maintoken)
stnum=str(stock_number)
#從line官方獲取
counterline=0
counttererror=0
print('開始執行')
while True:
  realdate=twstock.realtime.get(stnum)
  stname=getname(stnum)
  if counterline<=4:
    if realdate['success']:
      realprice=realdate['realtime']['latest_trade_price']
      if realprice !='-':
        counterline += 1
        if float(realprice)>=int(sellprice):
          counterline=sendline(1,realprice,counterline,token,stname)
        elif float(realprice) <=int(buyprice):
          counterline=sendline(2,realprice,counterline,token,stname)
        else:
          counterline=sendline(3,realprice,counterline,token,stname)
        
    else:
      print('twstock 讀取錯誤，錯誤原因:'+realdate['rtmessage'])
      counttererror +=1
      if counttererror >=3:
        print("程式結束")
        break
    time.sleep(int(notifytime) * 60) #5分鐘傳一次
      