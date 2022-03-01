import os
import tkinter as tk
import tkinter.filedialog
import pathlib
from tkinter import ttk

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter dialog trial')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.dialog_button = tkinter.Button(self, text='フォルダを選択...', command=file_open, width=120)
        self.dialog_button.pack(anchor=tk.NW)

        self.text_1 = tk.StringVar()
        self.type_label = tk.Label(self, textvariable=self.text_1)
        self.type_label.pack(anchor=tk.W)
        self.text_2 = tk.StringVar()
        self.content_label = tk.Label(self, textvariable=self.text_2)
        self.content_label.pack(anchor=tk.W)

        column = ('FolderPath', 'OldName', 'NewName')
        self.file_list_tree = ttk.Treeview(self, columns=column)
        self.file_list_tree.column('#0', width=0, stretch='no')
        self.file_list_tree.column('FolderPath', anchor='center', width=80)
        self.file_list_tree.column('OldName', anchor='center', width=20)
        self.file_list_tree.column('NewName', anchor='center', width=20)

        self.file_list_tree.heading('#0', text='')
        self.file_list_tree.heading('FolderPath', text='フォルダパス', anchor='center')
        self.file_list_tree.heading('OldName', text='ファイル名', anchor='center')
        self.file_list_tree.heading('NewName', text='新規ファイル名', anchor='center')

        self.file_list_tree.pack(anchor=tk.SW)

def file_open():
    file_name = ""
    ini_dir = 'C:\\Program Files\\Python37'
    ret = tkinter.filedialog.askdirectory(initialdir=ini_dir, title='file dialog', mustexist = True)
    folder_list = str(ret).split('/')
    for f in reversed(folder_list):
        if f == 'scan_data':
            break

        file_name = f + '_' + file_name

    p_file = pathlib.Path(str(ret))
    app.text_1.set('フォルダパス : ' + str(p_file))
    app.text_2.set('ファイル名 : ' + file_name)

root = tkinter.Tk()
app = Application(master=root)
app.mainloop()