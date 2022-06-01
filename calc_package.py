import math
from decimal import Decimal,ROUND_HALF_UP


#初期投資額出力,ドル表示と円表示
def InitialCost(flg,cost_SOL,static_SOL,static_USD_JPY,SOL,USD_JPY):
    if  flg:
        initial_cost_dollar = format(cost_SOL*static_SOL,'.2f')
        initial_cost_yen = format(float(initial_cost_dollar)*float(static_USD_JPY),'.0f')
    else:
        initial_cost_dollar = format(cost_SOL*SOL,'.2f')
        initial_cost_yen = format(float(initial_cost_dollar)*float(USD_JPY),'.0f')
    return {
        'initial_cost_dollar':initial_cost_dollar,
        'initial_cost_yen':initial_cost_yen
    }

#GSTのドル変換、円変換処理
def TransMoney(flg,accum,GST,static_GST,USD_JPY,static_USD_JPY):
    if  flg:
        accum_dollar = format(accum*static_GST,'.2f')
        accum_yen = format(float(accum_dollar)*float(static_USD_JPY),'.0f')
    else:
        accum_dollar = format(accum*GST,'.2f')
        accum_yen = format(float(accum_dollar)*float(USD_JPY),'.0f')
    return {
        'accum_dollar':accum_dollar,
        'accum_yen':accum_yen
    }

#qualityから1レベル上がるごとのポイント算出
def LevelUpPoint(quality):
    point = 0
    if quality == 'Common':
        point = 4
    elif quality == 'Uncommon':
        point = 6
    elif quality == 'Rare':
        point = 8
    elif quality == 'Epic':
        point = 10
    elif quality == 'Legendary':
        point = 12
    return point

#エナジー上限算出
def EnergyLimited(NumOfSneakers):
    NumOfSneakers_sum = 0
    snerakers_sum_status = 0
    for i in NumOfSneakers.values():
        NumOfSneakers_sum += i
    if NumOfSneakers_sum < 3:
        snerakers_sum_status = 2
    elif NumOfSneakers_sum < 9:
        snerakers_sum_status = 4
    elif NumOfSneakers_sum < 15:
        snerakers_sum_status = 9
    elif NumOfSneakers_sum < 30:
        snerakers_sum_status = 12
    else:
        snerakers_sum_status = 20

    Energy_limited = (
        snerakers_sum_status + 
        NumOfSneakers['NumOfCommon']*0 + 
        NumOfSneakers['NumOfUncommon']*1 + 
        NumOfSneakers['NumOfRare']*2 + 
        NumOfSneakers['NumOfEpic']*3 + 
        NumOfSneakers['NumOfLegendary']*4
    )
    #★print(Energy_limited)
    return Energy_limited

#獲得GST、レベル別
def Engage_GST(current_level,point_per_level,energy,initial_efficiency,current_gst_cap):
    current_efficiency = current_level * point_per_level + initial_efficiency
    sys_value = 0.9
    engage_GST = sys_value*math.sqrt(current_efficiency)*energy
    #★print(f'current_level:{current_level},engage_GST:{engage_GST}')

    #engage_GSTとGSTcapで比較
    if engage_GST > int(current_gst_cap):
        return current_gst_cap
    else:
        return engage_GST

#累積獲得量
def Accum_GST(accum_gst,repair_cost,engage_gst):
    accum_gst += float(engage_gst)
    accum_gst -= repair_cost
    return accum_gst

#レベル取得 わかりやすいようにしているだけ、今後も見越してメソッド化
def GetCurrentLevel(level):
    return level

#修理コスト計算
def RepairCost(repair_coeff,resilience,energy_limited):
    sys_temp = float((10.5*resilience**(-0.61))*energy_limited)
    sys_temp_decimal = Decimal(str(sys_temp)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    repair_cost = float(sys_temp_decimal) * repair_coeff
    return repair_cost

#レベルアップと同時にコストを減算
def LevelUp(accum_gst,level_up_cost,level):
    level += 1
    accum_gst -= level_up_cost
    return level,accum_gst