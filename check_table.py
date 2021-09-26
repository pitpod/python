import os
# import sys
# import argparse
import sqlite3
import pandas as pd
import datetime
# from pandas.core.indexes.base import Index
# import xlsxwriter
import datetime as dt
from styleframe import StyleFrame, Styler, utils


def Excel_date(date1):
    temp = dt.datetime(1899, 12, 30)  # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)


path = os.path.expanduser('~')
dbname = path + "\\Dropbox\\yuyu-farm\\data\\reservation-data.db"

conn = sqlite3.connect(dbname)
cur = conn.cursor()
"""
parser = argparse.ArgumentParser(description='テストです')
parser.add_argument('arg1' ,type=int)
parser.add_argument('arg2' ,type=int)
parser.add_argument('arg3' ,type=int)
args = parser.parse_args()
yearNo = args.arg1
monthNo = args.arg2
dayNo = args.arg3
"""
yearNo = int(input("年："))
monthNo = int(input("月："))
dayNo = int(input("日："))

yearMonthDayNo = str(Excel_date(dt.datetime(yearNo, monthNo, dayNo)))

sqlStr = "SELECT time,name,place1,place2 FROM dayly_data_" + str(yearNo) + \
    " where date=" + yearMonthDayNo + \
    " ORDER BY time IS NULL ASC,SUBSTR('0'||TRIM(REPLACE(time,'PM','11:PM'),'～'),-5,5) ASC,RTRIM(time,'～') DESC,place1 ASC"


pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.colheader_justify', 'left')
pd.set_option('display.max_colwidth', 0)

df = pd.read_sql(sqlStr, conn)
df.columns = ['時間', '名前', '迎え', '送り']
"""
d1 = dict(selector=".col2", props=[('min-width', '800px')])
d2 = dict(selector=".col4", props=[('min-width', '60px')])
df.head().style.set_table_styles([d1, d2])
"""

print(df)

df.to_csv("to_csv.csv", sep='\t')
# df.to_html("to_csv.html")

style = Styler(horizontal_alignment=utils.horizontal_alignments.left)

with StyleFrame.ExcelWriter('test.xlsx') as writer:
    sf = StyleFrame(df)
    sf.set_column_width(columns=['名前', '迎え', '送り'], width=20)
    sf.apply_column_style(cols_to_style='名前', styler_obj=style)
    sf.to_excel(writer, index=False, sheet_name='送迎')


cur.close()
conn.close()
