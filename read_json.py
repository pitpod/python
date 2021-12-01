import sys
import os
import json
from collections import OrderedDict
import pprint
import pandas as pd
import xlwt
import re

output_contacts = open('./output.vcf', 'w', encoding='utf-8')
folder_path = input("フォルダ名 :")
files = os.listdir(folder_path)
# files_file = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
files_file = []
for f in files:
    if os.path.isfile(os.path.join(folder_path, f)):
        if re.search('\\.json', f):
            files_file = files_file + [f]

print(files_file)   # ['file1', 'file2.txt', 'file3.jpg']
json_load = []
for fn in files_file:
    json_file = open(f"{folder_path}/{fn}", encoding='utf-8')
    json_load = json_load + json.load(json_file)
    # print(json_load)
    # print(len(json_load))

# for i in range(0, 50):
print(json_load)
for i in range(0, len(json_load)):
    output_contacts.write('BEGIN:VCARD\n')
    output_contacts.write('VERSION:3.0\n')
    firstname = json_load[i]['structuredName']['data1']
    lastname = json_load[i]['structuredName']['data3']
    output_contacts.write('N:' + lastname + ';' + firstname + '\n')
    output_contacts.write('FN:' + firstname + ' ' + lastname + '\n')
    output_contacts.write('X-PHONETIC-LAST-NAME:' + json_load[i]['structuredName']['data9'] + '\n')
    output_contacts.write('TEL;type=CELL;type=VOICE;type=pref:' + json_load[i]['phone'][0]['data1'] + '\n')
    output_contacts.write('END:VCARD' + '\n')

json_file.close()
output_contacts.close()

"""
pd.set_option('display.max_columns', 200)
# df = pd.json_normalize(dict_f, record_path='phone')
df = pd.json_normalize(dict_f, record_path='phone', meta=[['structuredName', 'data1'], ['structuredName', 'data2']])

pprint.pprint(df, width=200)
# {'A': {'i': 1, 'j': 2},
#  'B': [{'X': 1, 'Y': 10},
#        {'X': 2, 'Y': 20}],
#  'C': 'あ'}

# df.to_excel('./trque.xls')
"""