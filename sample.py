import pandas as pd

#s1 = pd.Series([1,2,3,5])
data = {
    '名前' :['田中','山田','髙橋'],
    '役割' :['営業部長','広報部','技術責任者'],
    '身長' :[178,173,169],
}
df = pd.DataFrame(data,columns=["名前","役割","身長"])
df.columns = ["Name","Position","height"]
print(df)
