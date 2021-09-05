import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(20, 2))
df.sort_index(ascending=False)  # 降順

# 昇順でソートするには上記の降順ソートのコードをコメントアウトして下記を実行してください
print(df.sort_values(by=1)) # key(カラム名)が1の昇順(小さい順)でソート
print(df.sort_values(by=1, ascending=False))  # keyが1の降順(大きい順)でソート
