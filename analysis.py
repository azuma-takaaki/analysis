import pandas as pd
from decimal import Decimal, ROUND_HALF_UP #四捨五入に使う
import glob


files = glob.glob("data/*")
for file in files:
    print(file)



#四捨五入関数
def Rounding (x):
    temp = Decimal(str(x))
    round = temp.quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    return int(round)

def get_middle(arr):
    front = 0.2
    back = 0.2
    return arr[Rounding(len(arr)*front):Rounding(len(arr)*(1-back))]



df = pd.read_excel(files[1])
# データ確認



####↓触察ごとの平均値を求める↓

#触った回数(t_countの最大値)の空の配列を作る
arr_split = [[] for _ in range(max(df["t_count"]))]

#t_countごとに配列を分けて格納 → 例えばarr[1]はt_countが2の動摩擦係数データを全て取得できる．
for index, row in df.iterrows():
    arr_split[int(row["t_count"])-1].append(row["cof"])

for i in range(len(arr_split)):
    arr_middle = get_middle(arr_split[i])
    print("t_count:"+ str(i) + "  → " + str(len(arr_middle)) + "/" + str(len(arr_split[i])))
    print("average: " + str(sum(arr_middle)/len(arr_middle)))

####↑触察ごとの平均値を求める↑


####↓全ての触察の平均値を求める↓

#全ての触察の動摩擦係数を一つの配列に連続して格納
all_arr = []
for i in range(len(arr_split)):
    arr_middle = get_middle(arr_split[i])
    for l in range(len(arr_middle)):
        all_arr.append(arr_middle[l])

print("all_arrのデータ数: " +str(len(all_arr)))
print("all_arrのaverage: " + str(sum(all_arr)/len(all_arr)))

####↑全ての触察の平均値を求める↑
