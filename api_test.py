from math import isnan
import pprint
import json

import read_csv as rc
import initial_value as iv
from calc_package import Engage_GST,LevelUpPoint,GetCurrentLevel,EnergyLimited,Accum_GST, RepairCost,TransMoney,InitialCost,LevelUp
from common_package import Output_result,Rate

#api用のjson文字列作成変数
nft_api = {}
nft_api['initial'] = [
    iv.initial_cost_SOL,
    iv.j_rate_static_flg,
    iv.lvUp_setting,
    iv.type,
    iv.calc_range
]
nft_api['days'] = []

if iv.j_rate_static_flg:
    Rate(iv.j_rate['static_SOL'],iv.j_rate['static_GST'],iv.j_rate['static_GMT'],iv.j_rate['static_USD_JPY'])
else:
    Rate(iv.j_rate['SOL'],iv.j_rate['GST'],iv.j_rate['GMT'],iv.j_rate['USD_JPY'])

#現在のレート格納
nft_api['rate'] = iv.j_rate

for i in range(iv.calc_range):
    #現在のレベルのGST獲得上限を取得
    df_gstcap = rc.df_gspcap[rc.df_gspcap["LEVEL"] == (GetCurrentLevel(iv.level))]
    df_gstcap = df_gstcap.at[(GetCurrentLevel(iv.level)),'GST']
    #現在のレベルの修理コストを取得
    df_repair_cost = rc.df_repair_cost[rc.df_repair_cost["LEVEL"] == (GetCurrentLevel(iv.level))]
    df_repair_cost = df_repair_cost.at[(GetCurrentLevel(iv.level)),iv.quality]
    repair_cost = RepairCost(df_repair_cost,iv.Sneakers_initial_attr['initial_resilience'],EnergyLimited(iv.NumOfSneakers))
    #現在のレベルのGST取得
    current_engage_gst = Engage_GST((GetCurrentLevel(iv.level)),LevelUpPoint(iv.quality),EnergyLimited(iv.NumOfSneakers),iv.Sneakers_initial_attr['initial_efficiency'],df_gstcap)
    #累積獲得量
    iv.accum_gst = Accum_GST(iv.accum_gst,repair_cost,current_engage_gst)
    #修理できない日の処理をどうするのか検討必要
    if iv.accum_gst < 0:
        print('''
累積獲得量が修理によってマイナスになりました。
処理を終了します。
        ''')
        break
    #出力用
    initial_cost = InitialCost(iv.j_rate_static_flg,iv.initial_cost_SOL,iv.j_rate['static_SOL'],iv.j_rate['static_USD_JPY'],iv.j_rate['SOL'],iv.j_rate['USD_JPY'])
    
    #レベルアップの処理
    lv_cost_time = 0
    while True:
        #現在のレベルのレベルアップコストを取得
        df_lv_cost = rc.df_lv_cost[rc.df_lv_cost["LEVEL"] == (GetCurrentLevel(iv.level))]
        if iv.j_rate_static_flg:
            GMT_GST = df_lv_cost.at[(GetCurrentLevel(iv.level)),'GMT']*iv.j_rate['static_GMT_GST']
        else:
            GMT_GST = df_lv_cost.at[(GetCurrentLevel(iv.level)),'GMT']*iv.j_rate['GMT_GST']
        if isnan(GMT_GST):
            GMT_GST = 0
        df_lv_cost = df_lv_cost.at[(GetCurrentLevel(iv.level)),'GST'] + GMT_GST
        if isnan(df_lv_cost):
            df_lv_cost = 0
        df_lv_cost_time = rc.df_lv_cost[rc.df_lv_cost["LEVEL"] == (GetCurrentLevel(iv.level))]
        df_lv_cost_time = df_lv_cost_time.at[(GetCurrentLevel(iv.level)),'時間']
        #レベルアップ可能ならレベルをあげる
        trans_money = TransMoney(iv.j_rate_static_flg,iv.accum_gst,iv.j_rate['GST'],iv.j_rate['static_GST'],iv.j_rate['USD_JPY'],iv.j_rate['static_USD_JPY'])
        if iv.accum_gst < df_lv_cost:
            flg = 0
            Output_result(i,flg,iv.lvUp_setting['lvUp_max_limited'],repair_cost,current_engage_gst,df_lv_cost,GetCurrentLevel(iv.level),iv.accum_gst,trans_money,initial_cost,df_repair_cost)
            nft_api_days = {
                'day':i + 1,
                'level':GetCurrentLevel(iv.level),
                'PaLBalance':format(float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']),'.0f'),
            }
            nft_api['days'].append(nft_api_days)
            break
        elif lv_cost_time >= 24:
            flg = 1
            Output_result(i,flg,iv.lvUp_setting['lvUp_max_limited'],repair_cost,current_engage_gst,df_lv_cost,GetCurrentLevel(iv.level),iv.accum_gst,trans_money,initial_cost,df_repair_cost)
            nft_api_days = {
                'day':i + 1,
                'level':GetCurrentLevel(iv.level),
                'PaLBalance':format(float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']),'.0f'),
            }
            nft_api['days'].append(nft_api_days)
            break
        elif GetCurrentLevel(iv.level) >= iv.lvUp_setting['lvUp_max_limited']:
            flg = 2
            Output_result(i,flg,iv.lvUp_setting['lvUp_max_limited'],repair_cost,current_engage_gst,df_lv_cost,GetCurrentLevel(iv.level),iv.accum_gst,trans_money,initial_cost,df_repair_cost)
            nft_api_days = {
                'day':i + 1,
                'level':GetCurrentLevel(iv.level),
                'PaLBalance':format(float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']),'.0f'),
            }
            nft_api['days'].append(nft_api_days)
            break
        else:
            lv_cost_time += df_lv_cost_time
            iv.level,iv.accum_gst = LevelUp(iv.accum_gst,df_lv_cost,iv.level)
            trans_money = TransMoney(iv.j_rate_static_flg,iv.accum_gst,iv.j_rate['GST'],iv.j_rate['static_GST'],iv.j_rate['USD_JPY'],iv.j_rate['static_USD_JPY'])
            flg = 3
            Output_result(i,flg,iv.lvUp_setting['lvUp_max_limited'],repair_cost,current_engage_gst,df_lv_cost,GetCurrentLevel(iv.level),iv.accum_gst,trans_money,initial_cost,df_repair_cost)
            #break#一日一回のみレベルをあげる、breakを外せば最大までレベリング可能

pprint.pprint(nft_api)