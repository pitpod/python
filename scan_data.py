import tkinter
import tkinter.filedialog

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter dialog trial')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.dialog_button = tkinter.Button(self, text='フォルダを選択...', command=file_open, width=120)
        self.dialog_button.pack(anchor=tkinter.NW)

        self.text_1 = tkinter.StringVar()
        self.type_label = tkinter.Label(self, textvariable=self.text_1)
        self.type_label.pack(anchor=tkinter.W)
        self.text_2 = tkinter.StringVar()
        self.content_label = tkinter.Label(self, textvariable=self.text_2)
        self.content_label.pack(anchor=tkinter.W)

def file_open():
    ini_dir = 'C:\\Program Files\\Python37'
    ret = tkinter.filedialog.askdirectory(initialdir=ini_dir, title='file dialog test', mustexist = True)
    app.text_1.set('Type : ' + str(type(ret)))
    app.text_2.set('Content : ' + str(ret))

root = tkinter.Tk()
app = Application(master=root)
app.mainloop()