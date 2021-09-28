import os
import sqlite3
import pandas as pd
import datetime
import datetime as dt
from styleframe import StyleFrame, Styler, utils


def Excel_date(date1):
    temp = dt.datetime(1899, 12, 30)  # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)


def sql_data():
    yearNo = int(input("年："))
    monthNo = int(input("月："))
    dayNo = int(input("日："))
    excel_dateNo = str(Excel_date(dt.datetime(yearNo, monthNo, dayNo)))
    sqlStr = "SELECT time,name,place1,place2 FROM dayly_data_" + str(yearNo) + \
        " where date=" + excel_dateNo + \
        " ORDER BY time IS NULL ASC,SUBSTR('0'||TRIM(REPLACE(time,'PM','11:PM'),'～'),-5,5) ASC,RTRIM(time,'～') DESC,place1 ASC"


    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.max_colwidth', 0)

    select_data = pd.read_sql(sqlStr, conn)
    select_data.columns = ['時間', '名前', '迎え', '送り']

    return yearNo, monthNo, dayNo, select_data


path = os.path.expanduser('~')
dbname = path + "\\Dropbox\\yuyu-farm\\data\\reservation-data.db"

conn = sqlite3.connect(dbname)
cur = conn.cursor()


yearMontDayNo = sql_data()
"""
sqlStr = "SELECT time,name,place1,place2 FROM dayly_data_" + str(yearMontDayNo[0]) + \
    " where date=" + yearMontDayNo[3] + \
    " ORDER BY time IS NULL ASC,SUBSTR('0'||TRIM(REPLACE(time,'PM','11:PM'),'～'),-5,5) ASC,RTRIM(time,'～') DESC,place1 ASC"


pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.max_colwidth', 0)

df = pd.read_sql(sqlStr, conn)
df.columns = ['時間', '名前', '迎え', '送り']
"""

df = yearMontDayNo[3]

end = input("c→csvファイルを出力\nx→xlsxファイルを出力\nr→再表示\ne→終了：")
dateNo = str(yearMontDayNo[0]) + "_" +  str(yearMontDayNo[1]) + "_" + str(yearMontDayNo[2])

if end == "c":
    df.to_csv(dateNo + ".csv", sep='\t')
    # df.to_html("to_csv.html")
elif end == "x":
    style = Styler(horizontal_alignment=utils.horizontal_alignments.left)

    with StyleFrame.ExcelWriter(dateNo + '.xlsx') as writer:
        sf = StyleFrame(df)
        sf.set_column_width(columns=['名前', '迎え', '送り'], width=20)
        sf.apply_column_style(cols_to_style='名前', styler_obj=style)
        sf.to_excel(writer, index=False, sheet_name='送迎')
#elif end == "r":

else:
    print("test")


cur.close()
conn.close()
