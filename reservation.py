# -*- coding: utf-8 -*-
# import codecs
# from ctypes.wintypes import HDC
# from distutils.log import error
# from doctest import master
import tkinter as tk
# import tkinter.ttk as ttk
import sys
import os
import pandas as pd
import sqlite3
# import io
# from io import StringIO
# from io import BytesIO
import tempfile
# import subprocess
from PIL import ImageFont, ImageDraw, Image
# from matplotlib.pyplot import text
from win32 import win32api
# from win32 import win32print
# import win32ui
# import win32con
# import numpy as np
import cv2
import datetime
from datetime import datetime
from datetime import timedelta
import calendar

# from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
# from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QImage, QPixmap
# 追加したimport
# from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt


class Application(tk.Frame):
    def __init__(self) -> None:
        self.master = tk.Tk()
        super().__init__(self.master)
        # self.master = master
        self.sentence = '123_テスト印刷'
        self.master.geometry("800x480")
        self.frame_bar = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.frame_bar.pack(side=tk.TOP, fill=tk.X)
        self.button_bar = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        self.button_bar.pack(side=tk.TOP, fill=tk.X)

        self.button_close = tk.Button(self.frame_bar, text="閉じる", command=sys.exit)
        self.button_close.grid(row=0, column=0, padx=5, pady=0)
        self.button_print = tk.Button(self.frame_bar, text="イメージテキスト", command=lambda: self.image_text())
        self.button_print.grid(row=0, column=1, padx=5, pady=0)
        self.button_print2 = tk.Button(self.frame_bar, text="イメージプリント", command=lambda: self.image_print())
        self.button_print2.grid(row=0, column=2, padx=5, pady=0)

        self.entry_year = tk.Entry(self.button_bar, width=6)
        self.entry_month = tk.Entry(self.button_bar, width=6)
        self.entry_day = tk.Entry(self.button_bar, width=6)
        self.entry_year.grid(row=1, column=0, padx=5, pady=5)
        self.entry_month.grid(row=1, column=2, padx=5, pady=5)
        self.entry_day.grid(row=1, column=4, padx=5, pady=5)

        self.label_year = tk.Label(self.button_bar, text="年")
        self.label_month = tk.Label(self.button_bar, text="月")
        self.label_day = tk.Label(self.button_bar, text="日")
        self.label_year.grid(row=1, column=1, padx=0, pady=5)
        self.label_month.grid(row=1, column=3, padx=0, pady=5)
        self.label_day.grid(row=1, column=5, padx=0, pady=5)
        self.button_month = tk.Button(self.button_bar, text="月間データ", command=lambda: self.month_data())
        self.button_month.grid(row=1, column=6, padx=10, pady=5)
        self.database_name = "reservation-data.db"
        self.path = os.path.expanduser('~')
        self.dbname = f'{self.path}/Dropbox/matsu_pub/2022/data/{self.database_name}'

    """
    月間データ
    """
    def month_data(self):
        MonthWindow()
        self.yearMonthDay_1st = f"{self.entry_year.get()}/{self.entry_month.get()}/1"
        self.yearMonthDayNo_1st = SerialData().excel_serial(self.yearMonthDay_1st)
        self.lastDay = calendar.monthrange(int(self.entry_year.get()), int(self.entry_month.get()))[1]
        # self.yearMonthDay_last = f"{self.entry_year.get()}/{self.entry_month.get()}/{self.lastDay}"
        self.yearMonthDayNo_last = self.yearMonthDayNo_1st + self.lastDay
        self.sqlStr = (f"SELECT date, time, name, place1, place2, send, charge FROM dayly_data_{self.entry_year.get()} "
                       f"where date >= {self.yearMonthDayNo_1st} and date <= {self.yearMonthDayNo_last} "
                       "ORDER BY date, time IS NULL ASC,SUBSTR('0'||TRIM(REPLACE(time,'PM','11:PM'),'～'),-5,5) ASC,RTRIM(time,'～') DESC,place1 ASC")
        self.conn = sqlite3.connect(self.dbname)
        self.df = pd.read_sql_query(sql=self.sqlStr, con=self.conn)
        self.dt = datetime(int(self.entry_year.get()), int(self.entry_month.get()), 1)
        self.dncol = self.dt.weekday()
        self.dnrow = 0
        for i in range(int(self.yearMonthDayNo_1st), int(self.yearMonthDayNo_last)):
            print(self.df.query(f'date == {i}'))

            if self.dncol == 6:
                self.dncol = 0
                self.dnrow += 1
            else:
                self.dncol += 1

        # self.yearMonthDayNo = f"{self.yearMonthDayNo} + 1"

    """[summary]
    印刷1
    """
    def image_text(self, print_text=""):
        self.im = Image.new('RGB', (604, 855), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.im)
        self.draw.ellipse((100, 100, 150, 200), fill=(255, 0, 0), outline=(0, 0, 0))
        self.draw.rectangle((200, 100, 300, 200), fill=(255, 255, 0), outline=(0, 0, 0))
        self.message = 'OpenCV\n(テスト印刷)'
        self.position = (50, 100)
        self.message2 = 'hello world\nこんにちは\n日本\nハロー'
        self.position2 = (150, 200)

        self.fontpath = 'C:\\Windows\\Fonts\\HGRPP1.TTC'
        self.font = ImageFont.truetype(self.fontpath, 32)
        b, g, r, a = 100, 100, 0, 0
        self.draw.text(self.position, self.message, font=self.font, fill=(b, g, r, a))
        self.draw.multiline_text(self.position2, self.message2, font=self.font, fill=(b, g, r, a), align='center')

        self.filename = tempfile.mktemp(".png")
        self.im.save(self.filename, quality=95)
        win32api.ShellExecute(0, "print", self.filename, None, ".", 0)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def image_print(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle('Image View')
        # ファイルを読み込み
        self.image = QImage('res.png')
        # -----
        self.painter = QPainter()
        # 加工したいイメージを渡して編集開始
        self.painter.begin(self.image)
        # ペンの色を指定
        self.painter.setPen(Qt.red)
        # painter.setPen(QColor(255, 0, 0))

        # 使用するフォントを指定
        self.painter.setFont(QFont('Times', 30))
        # テキスト描画
        self.painter.drawText(self.image.rect(), Qt.AlignCenter, 'Symfoware')
        # 画像の編集終了
        self.painter.end()
        # -----
        self.imageLabel = QLabel()
        # ラベルに読み込んだ画像を反映
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        # スケールは1.0
        self.imageLabel.scaleFactor = 1.0
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.imageLabel)
        self.window.setLayout(self.layout)
        self.window.resize(400, 300)
        self.window.show()
        self.app.exec_()


class MonthWindow(tk.Frame):
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("月刊予約表")
        # self.root.geometry("800x600")
        # Canvasの作成
        canvas = tk.Canvas(
            self.root,
            width=400,
            height=300,
            scrollregion=(-200, -100, 800, 600),
            bg="cyan"
        )

        # Canvasを配置
        # canvas.pack()
        canvas.grid(
            row=0, column=0,
            sticky=tk.N + tk.S
        )

        canvas.create_oval(
            300, 250,
            500, 350,
            fill="blue"
        )

        canvas.create_oval(
            700, 0,
            800, 200,
            fill="red"
        )

        xbar = tk.Scrollbar(
            self.root,
            orient=tk.HORIZONTAL,
        )

        ybar = tk.Scrollbar(
            self.root,
            orient=tk.VERTICAL,
        )

        xbar.grid(
            row=1, column=0,
            sticky=tk.W + tk.E
        )

        ybar.grid(
            row=0, column=1,
            sticky=tk.N + tk.S
        )

        xbar.config(
            command=canvas.xview
        )

        ybar.config(
            command=canvas.yview
        )

        canvas.config(
            xscrollcommand=xbar.set
        )

        canvas.config(
            yscrollcommand=ybar.set
        )


class SerialData():
    def excel_date(self, date1):
        temp = datetime(1899, 12, 30)  # Note, not 31st Dec but 30th!
        return(temp + timedelta(days=date1))

    def excel_serial(self, date2):
        date2_sep = date2.split('/')
        day_count = datetime(int(date2_sep[0]), int(date2_sep[1]), int(date2_sep[2]))
        temp = datetime(1899, 12, 30)  # Note, not 31st Dec but 30th!
        return((day_count - temp).days)


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
