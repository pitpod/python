# -*- coding: utf-8 -*-
import codecs
from ctypes.wintypes import HDC
from distutils.log import error
from doctest import master
import tkinter as tk
import sys
# import os
import io
import tempfile
import subprocess
from PIL import ImageFont, ImageDraw, Image
from win32 import win32api
from win32 import win32print
import win32ui
import win32con
import numpy as np
import cv2


class Application(tk.Frame):
    def __init__(self) -> None:
        root = tk.Tk()
        super().__init__(root)
        # root.attributes('-type', 'splash')
        # print(sys.stdout.encoding)
        # codecs.getwriter('utf-8')(sys.stdout)
        # print(sys.stdout.encoding)
        sentence = '123_テスト印刷'
        # sentence = sentence.encode('cp932')
        # sentence = sentence.decode('cp932')
        root.geometry("800x480")
        button = tk.Button(root, text="閉じる", command=sys.exit)
        button.pack()
        # button2 = tk.Button(root, text="印刷", command=lambda: self.print_paper(sentence))
        button2 = tk.Button(root, text="印刷", command=self.printer)
        button2.pack()
        # root.mainloop()
    
    def printer(self, print_text=""):
        printers = win32print.EnumPrinters(2)
        for p in printers:
            print(p)

        buf = io.BytesIO()
        screen = (500, 500)
        bgcolor = (0x00, 0x00, 0x00)
        img = Image.new('RGB', screen, bgcolor)
        img.save(buf, 'PNG')
        # text = 'print out message'
        printer_name = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(printer_name)
        # win32api.ShellExecute(0, 'print', buf.getvalue(), printer_name, '.', 0)
        p = subprocess.Popen('lp', stdin=subprocess.PIPE)
        p.communicate(buf.getvalue())
        # p.communicate(text)
        p.stdin.close()
        buf.close()

    def print_paper(self, sentence):
        print(sentence)
        self.buf = io.BytesIO()
        self.screen = (500, 500)
        self.bgcolor = (0x00, 0x00, 0x00)
        self.img = Image.new('RGB', self.screen, self.bgcolor)
        self.img.save(self.buf, 'PNG')
        self.print_image = self.buf.getvalue()
        self.buf.close()
        # self.image_text()
        self.sentence = sentence
        fontpath = 'C:\\Windows\\Fonts\\HGRPP1.TTC'
        font = ImageFont.truetype(fontpath, 32)
        self.INCH = 1440
        self.hDC = win32ui.CreateDC()
        self.hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
        self.SCALE_FACTOR = 20
        fontdict = {
            "height": self.SCALE_FACTOR * 40,
            "name": "ＭＳ 明朝",
            "charset": win32con.SHIFTJIS_CHARSET,
        }
        self.font = win32ui.CreateFont(fontdict)
        self.oldfont = self.hDC.SelectObject(self.font)
        self.hDC.StartDoc('TestPrint')
        self.hDC.StartPage()
        self.hDC.SetMapMode(win32con.MM_TWIPS)
        self.hDC.SetTextAlign(win32con.TA_LEFT | win32con.TA_TOP | win32con.TA_NOUPDATECP)
        self.hDC.TextOut(0, self.SCALE_FACTOR * 10 * -1, self.sentence)
        self.hDC.DrawText(self.sentence, (0, self.INCH * -1, self.INCH * 8, self.INCH * -2), win32con.DT_CENTER)
        self.hDC.SelectObject(self.oldfont)
        self.hDC.EndPage()
        self.hDC.EndDoc()

    def image_text(self):
        img = np.zeros((200, 500, 3), np.uint8)

        # cv2.imshow('img', img)
        # cv2.imwrite("img.png", img)
        
        b, g, r, a = 0, 255, 0, 0
        
        message = 'OpenCV\n(テスト印刷)'
        
        fontpath = 'C:\\Windows\\Fonts\\HGRPP1.TTC'
        font = ImageFont.truetype(fontpath, 32)
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        position = (50, 100)
        draw.text(position, message, font=font, fill=(b, g, r, a))
        img = np.array(img_pil)
        
        cv2.imshow("res", img)
        cv2.imwrite("res.png", img)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
