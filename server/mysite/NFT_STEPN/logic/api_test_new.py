from math import isnan
import pprint
import json

from . import read_csv as rc
from . import initial_value as iv
from .calc_package import Engage_GST,LevelUpPoint,GetCurrentLevel,EnergyLimited,Accum_GST, RepairCost,TransMoney,InitialCost,LevelUp
from .common_package import Output_result_print,Rate_print

#初期値をどう連携取ろうか・・・
def output_result(
    initial_cost_SOL = iv.initial_cost_SOL,
    j_rate_static_flg = iv.j_rate_static_flg,
    lvUp_setting = iv.lvUp_setting,
    type = iv.type,
    calc_range = iv.calc_range,
    j_rate = iv.j_rate,
    level = iv.level,
    quality = iv.quality,
    NumOfSneakers = iv.NumOfSneakers,
    Sneakers_initial_attr = iv.Sneakers_initial_attr,
    accum_gst = iv.accum_gst
    ):
    #api用のjson文字列作成変数
    nft_api = {}
    nft_api['initial'] = {
        'initial_cost_SOL':initial_cost_SOL,
        'j_rate_static_flg':j_rate_static_flg,
        'lvUp_setting':lvUp_setting,
        'type':type,
        'calc_range':calc_range,
    }
    nft_api['days'] = []

    if j_rate_static_flg:
        Rate_print(j_rate['static_SOL'],j_rate['static_GST'],j_rate['static_GMT'],j_rate['static_USD_JPY'])
    else:
        Rate_print(j_rate['SOL'],j_rate['GST'],j_rate['GMT'],j_rate['USD_JPY'])

    #現在のレート格納
    nft_api['rate'] = j_rate

    for i in range(calc_range):
        #現在のレベルのGST獲得上限を取得
        df_gstcap = rc.df_gspcap[rc.df_gspcap["LEVEL"] == (GetCurrentLevel(level))]
        df_gstcap = df_gstcap.at[(GetCurrentLevel(level)),'GST']
        #現在のレベルの修理コストを取得
        df_repair_cost = rc.df_repair_cost[rc.df_repair_cost["LEVEL"] == (GetCurrentLevel(level))]
        df_repair_cost = df_repair_cost.at[(GetCurrentLevel(level)),quality]
        repair_cost = RepairCost(df_repair_cost,Sneakers_initial_attr['initial_resilience'],EnergyLimited(NumOfSneakers))
        #現在のレベルのGST取得
        current_engage_gst = Engage_GST((GetCurrentLevel(level)),LevelUpPoint(quality),EnergyLimited(NumOfSneakers),Sneakers_initial_attr['initial_efficiency'],df_gstcap)
        #累積獲得量
        accum_gst = Accum_GST(accum_gst,repair_cost,current_engage_gst)
        #修理できない日の処理をどうするのか検討必要
        if accum_gst < 0:
            print('''
    累積獲得量が修理によってマイナスになりました。
    処理を終了します。
            ''')
            break
        #出力用
        initial_cost = InitialCost(j_rate_static_flg,initial_cost_SOL,j_rate['static_SOL'],j_rate['static_USD_JPY'],j_rate['SOL'],j_rate['USD_JPY'])
        
        #レベルアップの処理
        lv_cost_time = 0
        while True:
            #現在のレベルのレベルアップコストを取得
            df_lv_cost = rc.df_lv_cost[rc.df_lv_cost["LEVEL"] == (GetCurrentLevel(level))]
            if j_rate_static_flg:
                GMT_GST = df_lv_cost.at[(GetCurrentLevel(level)),'GMT']*j_rate['static_GMT_GST']
            else:
                GMT_GST = df_lv_cost.at[(GetCurrentLevel(level)),'GMT']*j_rate['GMT_GST']
            if isnan(GMT_GST):
                GMT_GST = 0
            df_lv_cost = df_lv_cost.at[(GetCurrentLevel(level)),'GST'] + GMT_GST
            if isnan(df_lv_cost):
                df_lv_cost = 0
            df_lv_cost_time = rc.df_lv_cost[rc.df_lv_cost["LEVEL"] == (GetCurrentLevel(level))]
            df_lv_cost_time = df_lv_cost_time.at[(GetCurrentLevel(level)),'時間']
            #レベルアップ可能ならレベルをあげる
            trans_money = TransMoney(j_rate_static_flg,accum_gst,j_rate['GST'],j_rate['static_GST'],j_rate['USD_JPY'],j_rate['static_USD_JPY'])
            if accum_gst < df_lv_cost:
                flg = 0
                Output_result_print(i,flg,lvUp_setting['lvUp_max_limited'],repair_cost,current_engage_gst,df_lv_cost,GetCurrentLevel(level),accum_gst,trans_money,initial_cost,df_repair_cost)
                nft_api_days = {
                    'day':i + 1,
                    'level':GetCurrentLevel(level),
                    'PaLBalance':format(float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']),'.0f'),
                    'expected_earnings':float(trans_money['accum_yen']),
                    'repair_cost':repair_cost
                }
                nft_api['days'].append(nft_api_days)
                break
            elif lv_cost_time >= 24:
                flg = 1
                Output_result_print(i,flg,lvUp_setting['lvUp_max_limited'],repair_cost,current_engage_gst,df_lv_cost,GetCurrentLevel(level),accum_gst,trans_money,initial_cost,df_repair_cost)
                nft_api_days = {
                    'day':i + 1,
                    'level':GetCurrentLevel(level),
                    'PaLBalance':format(float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']),'.0f'),
                    'expected_earnings':float(trans_money['accum_yen']),
                    'repair_cost':repair_cost
                }
                nft_api['days'].append(nft_api_days)
                break
            elif GetCurrentLevel(level) >= lvUp_setting['lvUp_max_limited']:
                flg = 2
                Output_result_print(i,flg,lvUp_setting['lvUp_max_limited'],repair_cost,current_engage_gst,df_lv_cost,GetCurrentLevel(level),accum_gst,trans_money,initial_cost,df_repair_cost)
                nft_api_days = {
                    'day':i + 1,
                    'level':GetCurrentLevel(level),
                    'PaLBalance':format(float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']),'.0f'),
                    'expected_earnings':float(trans_money['accum_yen']),
                    'repair_cost':repair_cost
                }
                nft_api['days'].append(nft_api_days)
                break
            else:
                lv_cost_time += df_lv_cost_time
                level,accum_gst = LevelUp(accum_gst,df_lv_cost,level)
                trans_money = TransMoney(j_rate_static_flg,accum_gst,j_rate['GST'],j_rate['static_GST'],j_rate['USD_JPY'],j_rate['static_USD_JPY'])
                flg = 3
                Output_result_print(i,flg,lvUp_setting['lvUp_max_limited'],repair_cost,current_engage_gst,df_lv_cost,GetCurrentLevel(level),accum_gst,trans_money,initial_cost,df_repair_cost)
                #break#一日一回のみレベルをあげる、breakを外せば最大までレベリング可能

    pprint.pprint(nft_api)
    return nft_api