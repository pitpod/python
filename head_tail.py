import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(20, 2))
df.head()
df.tail()

df.head().append(df.tail())
df.head(3).append(df.tail(3))

print(df.head(3).append(df.tail(3)))