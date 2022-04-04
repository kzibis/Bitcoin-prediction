import requests
import pandas as pd

btc_url = "https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc"
eth_url = "https://api.cryptowat.ch/markets/bitflyer/ethjpy/ohlc"

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

# btc

# hour
res = requests.get(btc_url+hour).json()
df = pd.DataFrame(res['result']['3600'], columns=df_columns)
df.to_csv('./btnjpy_hour.csv')

# day
#res = requests.get(btc_url+day).json()
#df = pd.DataFrame(res['result']['86400'], columns=df_columns)
#df.to_csv('./btnjpy_day.csv')

# eth

# hour
#res = requests.get(eth_url+hour).json()
#df = pd.DataFrame(res['result']['3600'], columns=df_columns)
#df.to_csv('./ethjpy_hour.csv')

# day
#res = requests.get(eth_url+day).json()
#df = pd.DataFrame(res['result']['86400'], columns=df_columns)
#df.to_csv('./ethjpy_day.csv')