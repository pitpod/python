import numpy as np
import pandas as pd


url = './sns_data.csv'
df = pd.read_csv(url,
                    encoding='utf8'
                 )
df.columns = ["user_id","follow","follower","like"]

#print(df)

d1 = {'data1': ['a','b','c','d','c','a'], 'data2': range(6)}
d1 = pd.DataFrame(d1,index=['one','two','three','four','five','six'])

#d1.to_csv("to_csv.csv",header=False, index=False)
#d1['data3'] = range(6)
d2 = pd.DataFrame([['e',10]],index=['seven'],columns=['data1','data2'])
print(d1.append(d2))

d1.to_excel("to_csv.xlsx")
