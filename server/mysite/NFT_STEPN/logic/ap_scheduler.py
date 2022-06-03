from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json
from datetime import datetime,timedelta
import yfinance as yf

from . import initial_value as iv

#定期実行を移動


#APIURLリスト
APIURL = {}
APIURL['SOL_GET_URL'] = 'https://cryptoprices.cc/SOL'
APIURL['GST_BSC_GET_URL'] = 'https://cryptoprices.cc/GST-BSC'
APIURL['GST_SOL_GET_URL'] = 'https://cryptoprices.cc/GST-SOL'
APIURL['GMT_GET_URL'] = 'https://cryptoprices.cc/GMT'

def periodic_execution():
  #仮想通貨Open初期値
  SOL_get = requests.get(APIURL['SOL_GET_URL'])
  iv.j_rate['SOL'] = json.loads(SOL_get.text)
  GST_BSC_get = requests.get(APIURL['GST_BSC_GET_URL'])
  GST_SOL_get = requests.get(APIURL['GST_SOL_GET_URL'])
  iv.GST_BSC_data = json.loads(GST_BSC_get.text)
  iv.GST_SOL_data = json.loads(GST_SOL_get.text)
  GMT_get = requests.get(APIURL['GMT_GET_URL'])
  iv.j_rate['GMT'] = json.loads(GMT_get.text)
  iv.GMT_GST_BSC = iv.j_rate['GMT']/iv.GST_BSC_data
  iv.GMT_GST_SOL = iv.j_rate['GMT']/iv.GST_SOL_data
  if iv.GST_flg:
    iv.j_rate['GST'] = iv.GST_BSC_data
    iv.j_rate['GMT_GST'] = iv.GMT_GST_BSC
  else:
    iv.j_rate['GST'] = iv.GST_SOL_data
    iv.j_rate['GMT_GST'] = iv.GMT_GST_SOL



  #--------------yahoofinanceから為替取得,代替案欲しいかも商用利用怪しい？--------------
  USD_JPY = yf.Ticker("USDJPY=X")
  df_usd_jpy = USD_JPY.history(start=(datetime.today()-timedelta(weeks=1)),end=datetime.today())
  df_usd_jpy = df_usd_jpy['Open'].tail(1).to_dict()
  for i in df_usd_jpy.values():
      iv.j_rate['USD_JPY'] = format(i,'.2f')
  #----------------------------------------------------------------
  print('定期処理が実行されました。')


def start():
  scheduler = BackgroundScheduler()
  # 5分おきに実行
  #scheduler.add_job(periodic_execution, 'interval', seconds=20)
  
  # 月曜から金曜の間、9時になると実行
  scheduler.add_job(periodic_execution, 'cron', hour=9, day_of_week='mon-fri')
  scheduler.start()