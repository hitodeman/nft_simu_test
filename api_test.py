import read_csv as rc
import initial_value as iv
from calc_package import Engage_GST,LevelUpPoint,GetCurrentLevel,EnergyLimited,Accum_GST,LevelUp,TransMoney,InitialCost

for i in range(iv.calc_range):
    #現在のレベルのGST獲得上限を取得
    df_gstcap = rc.df_gspcap[rc.df_gspcap["LEVEL"] == (GetCurrentLevel(iv.level))]
    df_gstcap = df_gstcap.at[(GetCurrentLevel(iv.level)),'GST']
    #現在のレベルの修理コストを取得
    df_repair_cost = rc.df_repair_cost[rc.df_repair_cost["LEVEL"] == (GetCurrentLevel(iv.level))]
    df_repair_cost = df_repair_cost.at[(GetCurrentLevel(iv.level)),iv.quality]
    #現在のレベルのGST取得
    current_engage_gst = Engage_GST((GetCurrentLevel(iv.level)),LevelUpPoint(iv.quality),EnergyLimited(iv.NumOfSneakers),iv.Sneakers_initial_attr['initial_efficiency'],df_gstcap)
    #累積獲得量
    iv.accum_gst = Accum_GST(iv.accum_gst,df_repair_cost,current_engage_gst)
    #出力用
    trans_money = TransMoney(iv.j_rate_static_flg,iv.accum_gst,iv.j_rate['GST'],iv.j_rate['static_GST'],iv.j_rate['USD_JPY'],iv.j_rate['static_USD_JPY'])
    initial_cost = InitialCost(iv.j_rate_static_flg,iv.initial_cost_SOL,iv.j_rate['static_SOL'],iv.j_rate['static_USD_JPY'],iv.j_rate['SOL'],iv.j_rate['USD_JPY'])
    print(f'--------------------------------------{i+1}日目----------------------------------------')
    print(f'現在のレベル：{GetCurrentLevel(iv.level)}')
    print(f'累積獲得量：{iv.accum_gst}')
    print(f'獲得GST：{current_engage_gst}')
    print(f"""
期待収益　：${trans_money['accum_dollar']},  {trans_money['accum_yen']}円
初期投資額：${initial_cost['initial_cost_dollar']},   {initial_cost['initial_cost_yen']}円
損益収支　：${format(float(trans_money['accum_dollar'])-float(initial_cost['initial_cost_dollar']),'.2f')},   {format(float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']),'.0f')}円
    """)
    #レベルアップの処理
    lv_cost_time = 0
    while True:
        if GetCurrentLevel(iv.level) >= 30:
            break
        #現在のレベルのレベルアップコストを取得
        df_lv_cost = rc.df_lv_cost[rc.df_lv_cost["LEVEL"] == (GetCurrentLevel(iv.level))]
        df_lv_cost = df_lv_cost.at[(GetCurrentLevel(iv.level)),'GST']
        df_lv_cost_time = rc.df_lv_cost[rc.df_lv_cost["LEVEL"] == (GetCurrentLevel(iv.level))]
        df_lv_cost_time = df_lv_cost_time.at[(GetCurrentLevel(iv.level)),'時間']
        #レベルアップ可能ならレベルをあげる
        if iv.accum_gst < df_lv_cost:
            print('GMTが不足したので次の日に移ります。')
            break
        elif lv_cost_time >= 24:
            print('24時間経過したため、次の日に移ります。')
            break
        elif GetCurrentLevel(iv.level) >= iv.lvUp_setting['lvUp_max_limited']:
            print(f"""
レベルアップ上限のため、次の日に移ります。
上限値：{iv.lvUp_setting['lvUp_max_limited']}
            """)
            break
        else:
            lv_cost_time += df_lv_cost_time
            iv.level = LevelUp(iv.level)
            iv.accum_gst -= df_lv_cost


