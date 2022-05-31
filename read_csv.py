import pandas as pd

df_lv_cost = pd.read_csv('lv_cost.csv')
#★print(df_lv_cost)

#レベルごとの獲得GSTの上限表
df_gspcap = pd.read_csv('gst_cap.csv')
#★print(df_gspcap)

df_repair_cost = pd.read_table('repair_cost.csv')
#★print(df_repair_cost)