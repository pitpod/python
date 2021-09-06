import numpy as np
import pandas as pd
df = pd.DataFrame({"int": [1, np.nan, np.nan, 32],
                   "str": ["python", "ai", np.nan, np.nan],
                   "flt": [5.5, 4.2, -1.2, np.nan]})
"""
print(df)
print("-------------------------------------")
# df成分に対してNaNの地位をTrueとしたブールの値のデータフレームを返す
print(df.isnull()) # notnull()を使うと、TrueとFalseが逆の処理になる。

print("-------------------------------------")
# "int"列にNaNがある行の削除
print(df.dropna(subset=["int"]))
print("-------------------------------------")

# NaNがある行を全て削除する
print(df.dropna())
print("-------------------------------------")

# NaNを全て0に置換する
print(df.fillna(0)) # 第一引数にmethod="ffill" 第二引数にlimtit=数字 とすることで指定した数字までは前のデータを使ってNaNを埋めることができます
print(df.fillna(method="ffill", limit=1))

print("-------------------------------------")

"""
df2 = pd.DataFrame({"int": [1, np.nan, np.nan, 32],
                   "str": ["python", "ai", np.nan, np.nan],
                   "flt": [5.5, 4.2, -1.2, np.nan]})

# int列だけ0で補完
df2.fillna({"int": 0}) # 特定の列に対しては辞書型を用いる

# 列ごとに異なる値を使いたい時は複数のキーを渡す。
df2.fillna({"int": 0, "str": "ai"})

# 特定の列(例えばflt)を削除
df2.drop(labels="flt",axis=1)
"""
  int str
0 1.0 python
1 NaN ai
2 NaN NaN
3 32.0  NaN
"""

# 複数の列を削除
df2.drop(labels=["flt", "str"], axis=1)

"""
  int
0 1.0
1 NaN
2 NaN
3 32.0
"""

# indexを指定すると行を消すこともできます
df2.drop(index=1, axis=0)
"""
int str flt
0 1.0 python  5.5
2 NaN NaN -1.2
3 32.0  NaN NaN
"""

# 元のデータに反映して削除するにはinplaceオプションにTrueを渡します
df2.drop(labels="flt", axis=1, inplace=True)
print(df2)

"""
int str
0 1.0 python
1 NaN ai
2 NaN NaN
3 32.0  NaN
"""

df3 = pd.DataFrame(np.random.rand(6,3))
print(df3)