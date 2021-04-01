import pandas as pd

df = pd.read_excel('sub1_amp_0_us_0_no_1010.xlsx')
# データ確認





#触った回数(t_countの最大値)の空の配列を作る
arr = [[] for _ in range(max(df["t_count"]))]

#t_countごとに配列を分けて格納 → 例えばarr[1]はt_countが2のデータを全て取得できる．
for index, row in df.iterrows():
    arr[int(row["t_count"])-1].append(row)
