import pandas as pd
data = pd.read_csv("https://aiacademy.jp/dataset/sample_data.csv",
                   encoding="cp932",
                   skiprows=1,  # 1行読み飛ばす
                   )

print(data)
print(type(data))  # &lt;class 'pandas.core.frame.DataFrame'&gt;
print(data.dtypes)

"""
エクセルの場合は下記のように使います。
.read_excel("任意のファイル名.xlsx",encoding='utf8')
"""
