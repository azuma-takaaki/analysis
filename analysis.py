import pandas as pd
from decimal import Decimal, ROUND_HALF_UP #四捨五入に使う
import glob
import cv2
import csv
from datetime import datetime
from pytz import timezone
import itertools




#四捨五入関数
def Rounding (x):
    temp = Decimal(str(x))
    round = temp.quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    return int(round)

def get_middle(arr):
    front = 0.2
    back = 0.2
    return arr[Rounding(len(arr)*front):Rounding(len(arr)*(1-back))]

def analyze_data(file_path):
    df = pd.read_excel(file_path)
    ####↓触察ごとの平均値を求める↓

    #触った回数(t_countの最大値)の空の配列を作る
    arr_split = [[] for _ in range(max(df["t_count"]))]

    #t_countごとに配列を分けて格納 → 例えばarr[1]はt_countが2の動摩擦係数データを全て取得できる．
    for index, row in df.iterrows():
        arr_split[int(row["t_count"])-1].append(row["cof"])

    for i in range(len(arr_split)):
        arr_middle = get_middle(arr_split[i])
        #print("t_count:"+ str(i) + "  → " + str(len(arr_middle)) + "/" + str(len(arr_split[i])))
        #print("average: " + str(sum(arr_middle)/len(arr_middle)))

    ####↑触察ごとの平均値を求める↑


    ####↓全ての触察の平均値を求める↓

    #全ての触察の動摩擦係数を一つの配列に連続して格納
    all_arr = []
    for i in range(len(arr_split)):
        arr_middle = get_middle(arr_split[i])
        for l in range(len(arr_middle)):
            all_arr.append(arr_middle[l])

    average = sum(all_arr)/len(all_arr)

    #print("all_arrのデータ数: " +str(len(all_arr)))
    #print("all_arrのaverage: " + str(average))

    ####↑全ての触察の平均値を求める↑


    ####↓タイムスタンプをファイル名にしたファイルを作成し， データを書き込む↓
    with open(analytical_file,'a') as f:
        writer = csv.writer(f)
        writer.writerow([file_path,str(average)])
    ####↑タイムスタンプをファイル名にしたファイルを作成し， データを書き込む↑






#分析データを書き込むファイルを生成
analytical_file = 'analytical_data/'+str(datetime.now(timezone('Asia/Tokyo')))+'.csv'

with open(analytical_file,'a') as f:
    writer = csv.writer(f)
    writer.writerow(['file_name','average_cof'])



#実験データのファイルパスを取得
amp_order = ['0', '0.5', '1', '1.5', '2', '2.5']
sub_num = 10
file_names = []
#sub1から10まで順番にファイルパスを取得
for i in range(sub_num):
    for l in range(len(amp_order)):
        file = glob.glob("data/sub" + str(i+1) + "_amp_" + amp_order[l] + '_*')
        file_names.append(file)

#二次元リストを一次元リストに変換
file_names = list(itertools.chain.from_iterable(file_names))


#分析
count = 0
for i in range(len(file_names)):
    analyze_data(file_names[i])
    count += 1
    print("分析中:" + str(count)+"/"+str(len(file_names)))
