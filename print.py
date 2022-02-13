# -*- coding: utf-8 -*-
import codecs
from ctypes.wintypes import HDC
from distutils.log import error
from doctest import master
import tkinter as tk
import sys
# import os
import io
from io import StringIO
from io import BytesIO
import tempfile
import subprocess
from PIL import ImageFont, ImageDraw, Image
from win32 import win32api
from win32 import win32print
import win32ui
import win32con
import numpy as np
import cv2

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QImage, QPalette, QPixmap
# 追加したimport
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt

class Application(tk.Frame):
    def __init__(self) -> None:
        root = tk.Tk()
        super().__init__(root)
        sentence = '123_テスト印刷'
        root.geometry("800x480")
        button = tk.Button(root, text="閉じる", command=sys.exit)
        button.pack()
        button1 = tk.Button(root, text="印刷1", command=lambda: self.print_paper(sentence))
        button1.pack()
        button2 = tk.Button(root, text="印刷2", command=self.printer)
        button2.pack()
        button3 = tk.Button(root, text="印刷3", command=self.use_win32print)
        button3.pack()
        button4 = tk.Button(root, text="印刷4", command=self.use_ShellExecute)
        button4.pack()
        button5 = tk.Button(root, text="イメージテキスト", command=self.image_text)
        button5.pack()
        button6 = tk.Button(root, text="イメージテキスト2", command=self.image_text2)
        button6.pack()
        button7 = tk.Button(root, text="イメージテキスト3", command=self.image_print)
        button7.pack()

    """[summary]
    印刷1
    """
    def print_paper(self, sentence):
        self.sentence = sentence
        self.INCH = 1440
        self.SCALE_FACTOR = 20
        # self.sentence.encode("utf-8").decode("shift-jis", errors="ignore")
        # self.sentence.encode("utf-8").decode("cp932", errors="ignore")
        print(self.sentence)
        print ('defaultencoding:', sys.getdefaultencoding())
        fontdict = {
            "name": "ＭＳ 明朝",
            "height": self.SCALE_FACTOR * 40,
            "charset": win32con.SHIFTJIS_CHARSET,
        }
        self.font = win32ui.CreateFont(fontdict)

        self.hDC = win32ui.CreateDC()
        self.hDC.CreatePrinterDC(win32print.GetDefaultPrinter())

        self.oldfont = self.hDC.SelectObject(self.font)

        self.hDC.StartDoc('TestPrint')
        self.hDC.StartPage()
        self.hDC.SetMapMode(win32con.MM_TWIPS)
        self.hDC.DrawText(self.sentence, (0, self.INCH * -1, self.INCH * 8, self.INCH * -2), win32con.DT_CENTER)
        self.hDC.SetTextAlign(win32con.TA_LEFT | win32con.TA_TOP | win32con.TA_NOUPDATECP)
        self.hDC.TextOut(0, self.SCALE_FACTOR * 10 * -1, self.sentence)
        self.hDC.SelectObject(self.oldfont)
        self.hDC.EndPage()
        self.hDC.EndDoc()

    """button2"""
    def printer(self, print_text=""):
        printers = win32print.EnumPrinters(2)
        for p in printers:
            print(p)

        buf = BytesIO()
        # buf = StringIO()
        screen = (500, 500)
        bgcolor = (0x00, 0x00, 0x00)
        img = Image.new('RGB', screen, bgcolor)
        img.save(buf, 'PNG')
        printer_name = win32print.GetDefaultPrinter()
        p = subprocess.Popen('print', stdin=subprocess.PIPE)
        p.communicate(buf.getvalue())
        p.stdin.close()
        buf.close()

    def use_win32print(self):
        self.printer_name = win32print.GetDefaultPrinter()
        # printer_name = 'Microsoft Print to PDF'
        #
        # raw_data could equally be raw PCL/PS read from
        #  some print-to-file operation
        #
        if sys.version_info >= (3,):
            self.raw_data = bytes("This is a test", "utf-8")
        else:
            self.raw_data = "This is a test"

        print(self.raw_data)
        self.hPrinter = win32print.OpenPrinter(self.printer_name)
        try:
            self.hJob = win32print.StartDocPrinter(self.hPrinter, 1, ("test of raw data", None, "RAW"))
            try:
                win32print.StartPagePrinter(self.hPrinter)
                win32print.WritePrinter(self.hPrinter, self.raw_data)
                win32print.EndPagePrinter(self.hPrinter)
            finally:
                win32print.EndDocPrinter(self.hPrinter)
        finally:
            win32print.ClosePrinter(self.hPrinter)

    def use_ShellExecute(self):
        filename = tempfile.mktemp(".txt")
        # ファイルを開くアプリケーションによってはエラーになる
        open(filename, "w").write("This is a テスト")
        win32api.ShellExecute(
            0,
            "print",
            filename,
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0
        )

    def image_text(self):
        im = Image.new('RGB', (604, 855), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        draw.ellipse((100, 100, 150, 200), fill=(255, 0, 0), outline=(0, 0, 0))
        draw.rectangle((200, 100, 300, 200), fill=(255, 255, 0), outline=(0, 0, 0))
        message = 'OpenCV\n(テスト印刷)'
        position = (50, 100)
        message2 = 'hello world\nこんにちは\n日本\nハロー'
        position2 = (150, 200)

        fontpath = 'C:\\Windows\\Fonts\\HGRPP1.TTC'
        font = ImageFont.truetype(fontpath, 32)
        b, g, r, a = 100, 100, 0, 0
        draw.text(position, message, font=font, fill=(b, g, r, a))
        draw.multiline_text(position2, message2, font=font, fill=(b, g, r, a), align = 'center')

        filename = tempfile.mktemp(".png")
        im.save(filename, quality=95)
        win32api.ShellExecute(0, "print", filename, None, ".", 0)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def image_text2(self):
        img = np.zeros((855, 605, 3), np.uint8)
        # img = np.arange(0, 737280, 1, np.uint8)
        # img = np.reshape(img, (1024, 720))

        b, g, r, a = 100, 100, 0, 0

        message = 'OpenCV\n(テスト印刷)'
        rect_img = Image.new("RGB", (300, 100), "White")
        fontpath = 'C:\\Windows\\Fonts\\HGRPP1.TTC'
        font = ImageFont.truetype(fontpath, 32)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        position = (50, 100)
        # draw.bitmap(rect_img)
        draw.rectangle((200, 100, 300, 200), fill=(255, 255, 255), outline=(0, 0, 0))
        draw.text(position, message, font=font, fill=(b, g, r, a))
        img = np.array(img_pil)

        cv2.imshow("res", img)
        # cv2.imwrite("res.png", img)
        path = "res.png"
        filename = tempfile.mktemp(".png")
        # ファイルを開くアプリケーションによってはエラーになる
        cv2.imwrite(filename, img)
        # open(filename, "w").write("This is a テスト")
        win32api.ShellExecute(0, "print", filename, None, ".", 0)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def image_print(self):
        app = QApplication([])
        window = QWidget()
        window.setWindowTitle('Image View')
        # ファイルを読み込み
        image = QImage('res.png')
        # -----
        painter = QPainter()
        # 加工したいイメージを渡して編集開始
        painter.begin(image)
        # ペンの色を指定
        painter.setPen(Qt.red)
        #painter.setPen(QColor(255, 0, 0))

        # 使用するフォントを指定
        painter.setFont(QFont('Times', 30))
        # テキスト描画
        painter.drawText(image.rect(), Qt.AlignCenter, 'Symfoware')
        # 画像の編集終了
        painter.end()
        # -----
        imageLabel = QLabel()
        # ラベルに読み込んだ画像を反映
        imageLabel.setPixmap(QPixmap.fromImage(image))
        # スケールは1.0
        imageLabel.scaleFactor = 1.0
        layout = QVBoxLayout()
        layout.addWidget(imageLabel)
        window.setLayout(layout)
        window.resize(400, 300)
        window.show()
        app.exec_()


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
