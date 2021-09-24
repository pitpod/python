import os
import sys
import argparse
import sqlite3
import pandas as pd
import datetime
import xlsxwriter
import datetime as dt


def Excel_date(date1):
    temp = dt.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
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

sqlStr = "SELECT time,name,place1,place2,send,charge FROM dayly_data_" + str(yearNo) + \
    " where date=" + yearMonthDayNo + \
    " ORDER BY time IS NULL ASC,SUBSTR('0'||TRIM(REPLACE(time,'PM','11:PM'),'～'),-5,5) ASC,RTRIM(time,'～') DESC,place1 ASC"

df = pd.read_sql(sqlStr, conn)
df.to_csv("to_csv.csv", sep='\t')

print(df)

cur.close()
conn.close()