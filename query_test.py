import pandas as pd
df = pd.DataFrame([[10, 20, 30, 30], [25, 50, 65, 80]], index=["1行","2行"], columns=["A","B","C","D"])

print(df.query('A >= 5 and C <= 50'))