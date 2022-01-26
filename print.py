import tkinter as tk
import sys
import os
import subprocess
from PIL import Image
import io
# from sys import win32api
# from sys import win32print


def printer():
    printers = os.win32print.EnumPrinters(2)
    for p in printers:
        print(p)

    """
    buf = io.BytesIO()
    screen = (500, 500)
    bgcolor = (0x00, 0x00, 0x00)
    img = Image.new('RGB', screen, bgcolor)
    img.save(buf, 'PNG')
    p = subprocess.Popen('lp', stdin=subprocess.PIPE)
    p.communicate(buf.getvalue())
    p.stdin.close()
    buf.close()
    """


root = tk.Tk()
# root.attributes('-type', 'splash')
root.geometry("800x480")
button = tk.Button(root, text="閉じる", command=sys.exit)
button.pack()
button2 = tk.Button(root, text="印刷", command=printer)
button2.pack()
root.mainloop()
