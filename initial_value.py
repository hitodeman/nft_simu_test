import requests
import pprint
import json
from datetime import datetime,timedelta
import yfinance as yf

#■マークがある変数はinputによって値が変動

#■Type
type = 'Jogger'
#■Quality品質
quality = 'Common'
#■LVup設定
lvUp_setting = {
    'lvUp_max_limited':14,
    'lvUp_alloc_efficiency':4,
    'lvUp_alloc_luck':0,
    'lvUp_alloc_confort':0,
    'lvUp_alloc_resilience':0
}
#累積獲得量
accum_gst = 0

#APIURLリスト
APIURL = {}
APIURL['SOL_GET_URL'] = 'https://cryptoprices.cc/SOL'
APIURL['GST_BSC_GET_URL'] = 'https://cryptoprices.cc/GST-BSC'
APIURL['GST_SOL_GET_URL'] = 'https://cryptoprices.cc/GST-SOL'
APIURL['GMT_GET_URL'] = 'https://cryptoprices.cc/GMT'

#GST_BSCはTRUE,GST_SOLはFalse
#■
GST_flg = False

#■計算期間
calc_range = 60
#■初期投資額,単位SOL値
initial_cost_SOL = 13
#■レベル初期値　0固定でいいかも？
level = 0

#仮想通貨Open初期値
SOL_get = requests.get(APIURL['SOL_GET_URL'])
SOL_data = json.loads(SOL_get.text)

if GST_flg:
    GST_get = requests.get(APIURL['GST_BSC_GET_URL'])
else:
    GST_get = requests.get(APIURL['GST_SOL_GET_URL'])
GST_data = json.loads(GST_get.text)

GMT_get = requests.get(APIURL['GMT_GET_URL'])
GMT_data = json.loads(GMT_get.text)

GMT_GST = GMT_data/GST_data

#--------------yahoofinanceから為替取得,代替案欲しいかも商用利用怪しい？--------------
USD_JPY = yf.Ticker("USDJPY=X")
usd_jpy_val = 0
df_usd_jpy = USD_JPY.history(start=(datetime.today()-timedelta(weeks=1)),end=datetime.today())
df_usd_jpy = df_usd_jpy['Open'].tail(1).to_dict()
for i in df_usd_jpy.values():
    usd_jpy_val = format(i,'.2f')
#----------------------------------------------------------------

#■価格固定フラグ,Trueならstaticを使用
j_rate_static_flg = False

#■staticはinputで変動
static_GST = 4.53
static_GMT = 2.59
static_GMT_GST = static_GMT/static_GST
j_rate = {
    'SOL':SOL_data,
    'GST':GST_data,
    'GMT':GMT_data,
    'USD_JPY':usd_jpy_val,
    'GMT_GST':GMT_GST,
    'static_SOL':74.08,
    'static_GST':static_GST,
    'static_GMT':static_GMT,
    'static_GMT_GST':static_GMT_GST,
    'static_USD_JPY':131.15
}
#■スニーカーのレアリティごとの所持数
NumOfSneakers = {
    'NumOfCommon' : 3,
    'NumOfUncommon' : 0,
    'NumOfRare' : 0,
    'NumOfEpic' : 0,
    'NumOfLegendary' : 0
}

#■スニーカー初期値
Sneakers_initial_attr = {
    'initial_efficiency':9,
    'initial_luck':6.4,
    'initial_confort':9,
    'initial_resilience':9.9
}

#■スニーカータイプごとの1エナジーあたりGST獲得最大値
engageOf_typerate = {
    'Walker' :4,
    'Jogger' :5,
    'Runner' :6,
    'Trainer':5,
}

#耐久値減少時の獲得GST補正値
durability_comff = {
    'fifty':0.5,
    'twenty':0.1
}
#耐久値
durability = 100