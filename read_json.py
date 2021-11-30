import sys
import json
from collections import OrderedDict
import pprint
import pandas as pd
import xlwt

with open('Calls.json', encoding='utf-8') as f:
    dict_f = json.load(f)

df = pd.DataFrame(dict_f)
pprint.pprint(df, width=40)
# {'A': {'i': 1, 'j': 2},
#  'B': [{'X': 1, 'Y': 10},
#        {'X': 2, 'Y': 20}],
#  'C': 'あ'}

print(type(df))
df.to_excel('./trque.xls')