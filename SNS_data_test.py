import numpy as np
import pandas as pd

data = pd.read_csv("sns_data.csv",
                    encoding='utf8'
                 )
#df = pd.DataFrame(data, columns=["user_id","follow","follower","like"])

print(data)