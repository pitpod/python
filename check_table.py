import sqlite3
import pandas as pd
import datetime
import xlsxwriter
import datetime as dt

def Excel_date(date1):
    temp = dt.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

dbname = "c:\\Users\\CM_matsu\\Dropbox\\matsu_pub\\2020\\data\\reservation-data.db"

conn = sqlite3.connect(dbname)
cur = conn.cursor()

yearNo = 2021
monthNo = 9
dayNo = 1
yearMonthDayNo = str(Excel_date(dt.datetime(yearNo, monthNo, dayNo)))
#yearMonthDay = yearNo + "/" + monthNo + "/1"
#yearMonthDayNo = "44205"

sqlStr = "SELECT time,name,place1,place2,send,charge FROM dayly_data_" + str(yearNo) + \
    " where date=" + \
    yearMonthDayNo + \
    " ORDER BY time IS NULL ASC,SUBSTR('0'||TRIM(REPLACE(time,'PM','11:PM'),'～'),-5,5) ASC,RTRIM(time,'～') DESC,place1 ASC"

df = pd.read_sql(sqlStr, conn)

print(df)

cur.close()
conn.close()