#1日の結果
def Output_result(i,flg,lv_max,repair_cost,current_engage_gst,df_lv_cost,level,accum_gst,trans_money,initial_cost,df_repair_cost):
    print(f'--------------------------------------{i+1}日目----------------------------------------')
    print('結果')
    if flg == 0:
            print('＜GSTが不足したので次の日に移ります。＞')
    elif flg == 1:
        print('＜24時間経過したため、次の日に移ります。＞')
    elif flg == 2:
        print(f"""
＜レベルアップ上限のため、次の日に移ります。＞
上限値：{lv_max}
            """)
    elif flg == 3:
        print('＜レベルアップしました。＞')
    if float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']) >= 0:
        print(f'原資回収完了しています！！！')
    print(f'修理コスト：{repair_cost}')
    print(f'リペアコスト係数：{df_repair_cost}')
    print(f'獲得GST：{current_engage_gst}')
    print(f'レベルアップコスト：{df_lv_cost}')
    print(f'現在のレベル：{level}')
    print(f'累積獲得量：{accum_gst}')
    print(f"初期投資額：${initial_cost['initial_cost_dollar']},   {initial_cost['initial_cost_yen']}円")
    print(f'期待収益　：${trans_money["accum_dollar"]},  {trans_money["accum_yen"]}円')
    print(f"""
損益収支　：${format(float(trans_money['accum_dollar'])-float(initial_cost['initial_cost_dollar']),'.2f')},   {format(float(trans_money['accum_yen'])-float(initial_cost['initial_cost_yen']),'.0f')}円
    """)

#レート確認
def Rate(SOL,GST,GMT,USD_JPY):
    print(f"""
SOL:{SOL}
GST:{GST}
GMT:{GMT}
USD_JPY:{USD_JPY}    
    """)