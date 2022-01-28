import tkinter as tk
import sys
import os
import io
import tempfile
import subprocess
from PIL import Image
from win32 import win32api
from win32 import win32print
import win32ui
import win32con


def printer():
    printers = win32print.EnumPrinters(2)
    for p in printers:
        print(p)

    buf = io.BytesIO()
    screen = (500, 500)
    bgcolor = (0x00, 0x00, 0x00)
    img = Image.new('RGB', screen, bgcolor)
    img.save(buf, 'PNG')
    text = 'print out message'
    printer_name = win32print.GetDefaultPrinter()
    hPrinter = win32print.OpenPrinter(printer_name)
    # win32api.ShellExecute( 0, 'print', buf.getvalue(), printer_name, '.', 0)
    p = subprocess.Popen('lpr', stdin=subprocess.PIPE)
    # p.communicate(buf.getvalue())
    p.communicate(text)
    p.stdin.close()
    buf.close()

def print_paper(sentence):
    INCH = 1440
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
    hDC.StartDoc('TestPrint')
    hDC.StartPage()
    hDC.SetMapMode(win32con.MM_TWIPS)
    hDC.DrawText(sentence, (0, INCH * -1, INCH * 8, INCH * -2), win32con.DT_CENTER)
    hDC.EndPage()
    hDC.EndDoc()

def print_text():
    text = 'テスト文字列'

    hdc = win32ui.CreateDC()
    printer = win32print.GetDefaultPrinter()

    hdc.CreatePrinterDC(printer)

    hdc.StartDoc("test document")
    hdc.StartPage()
    hdc.SetMapMode(win32con.MM_TWIPS)
    margin = (1000, -1000, 11500, -15000)
    align = win32con.DT_LEFT
    hdc.DrawText(text, margin, align)
    hdc.EndPage()
    hdc.EndDoc()

root = tk.Tk()
# root.attributes('-type', 'splash')
root.geometry("800x480")
button = tk.Button(root, text="閉じる", command=sys.exit)
button.pack()
button2 = tk.Button(root, text="印刷", command=print('TEST print'))
# button2 = tk.Button(root, text="印刷", command=print_text)
button2.pack()
root.mainloop()
