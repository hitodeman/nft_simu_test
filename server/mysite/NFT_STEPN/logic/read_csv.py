import pandas as pd

df_lv_cost = pd.read_csv('NFT_STEPN/logic/lv_cost.csv')
#★print(df_lv_cost)

#レベルごとの獲得GSTの上限表
df_gspcap = pd.read_csv('NFT_STEPN/logic/gst_cap.csv')
#★print(df_gspcap)

df_repair_cost = pd.read_table('NFT_STEPN/logic/repair_cost.csv')
#★print(df_repair_cost)