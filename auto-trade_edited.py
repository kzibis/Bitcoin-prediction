from model_edited import create_model
import pandas as pd
import numpy as np
#from coincheck import market,order,account
import openpyxl
import time
import ccxt
from pprint import pprint
import requests

#データを取得
btc_url = "https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc"

hour = "?periods=3600&after=1631718000"
day = "?periods=86400&after=1617202800"

df_columns = [
    "CloseTime",
    "OpenPrice",
    "HighPrice",
    "LowPrice",
    "ClosePrice",
    "Volume",
    "QuoteVolume"
]

res = requests.get(btc_url+hour).json()
df = pd.DataFrame(res['result']['3600'], columns=df_columns)
df.to_csv('./btnjpy_hour.csv')



#モデルの読み込み
model = create_model()

#学習した重みを読み込み
#先にtrain.pyを実行していないと、param.hdf5が存在しないのでエラーになる
model.load_weights('param.hdf5')

#学習したデータを使って今日の終値予測

#予測に使うデータを準備
df = pd.read_csv("./btnjpy_hour.csv")
#現状だと日付の降順にデータが並んでいるので、逆にする
#df = df.sort_index(axis='index',ascending=False)

#入力データ
input_data = np.array([[df["ClosePrice"].iloc[-(i+1)] for i in range(24)]])

#推論値
prediction = model.predict(input_data).flatten()
print("AIが予測するBTC価格は以下です。")
print(prediction)

#直近のBTC価格をコインチェックから取得(coincheck ver)
#m1=market.Market()
#price_now = m1.ticker()["last"]

#直近のBTC価格をコインチェックから取得(ccxt ver)
base = ccxt.coincheck()
ticker = base.fetch_ticker(symbol ='BTC/JPY')
print("コインチェックでのBTC取引価格は以下です。")
price_now = ticker["last"]
#print(price_now)
pprint("["+str(price_now)+"]")

#エクセルのファイルを読み込み
book = openpyxl.load_workbook(r'C:\Users\kazum\Desktop\edited_version\auto-trade_prediction-record.xlsx')
sheet = book['Sheet1']
#データを書き込むために最終行を取得
max = sheet.max_row

#predictionのデータ型を変更
prediction = prediction[0]

#データを記入
sheet['A'+str(max)] = time.time()
sheet['B'+str(max+1)] = prediction
sheet['C'+str(max)] = price_now
book.save(r'C:\Users\kazum\Desktop\edited_version\auto-trade_prediction-record.xlsx')

if prediction>price_now:
    print("予測値が現在価格より高いので、買い注文を出します。")


    #注文を出すには認証が必要
    #access_key=input("APIのアクセスキーを入力してください")
    #secret_key=input("APIのシークレットキーを入力してください")

    #print("買い注文を実行します。")
    #o1 = order.Order(secret_key=secret_key,access_key=access_key)
    #print(o1.buy_btc_jpy(rate=str(price_now),amount=0.005))
else:
    print("買いチャンスとは判断出来なかったので、何もしません。")
