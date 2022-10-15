from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilenames


class FilePage:
    def __init__(self, root):
        self.frame = Frame(root, bg="orange")
        #Label(self.frame, text="Welcome to the AirQuality app", font=(0, 50), background="green")
        self.frame.grid_rowconfigure(1, minsize=30)
        Label(self.frame, text="Click the Button to Select a Folder:", font=('Aerial 18 bold')).grid(row=0, column=0, sticky="NSEW")
        button = Button(self.frame, text="Select", command=lambda: self.SelectFile())
        button.grid(row=1, column=1, columnspan=2, pady=10)
        button_read = Button(self.frame, text="Read", command=lambda: self.ReadFiles())
        button_read.grid(row=2, column=0, columnspan=2, pady=10)
        self.label_status = Label(self.frame, font=('Aerial 18 bold'), bg="orange")
        self.label_status.grid(row=3, column=0, sticky="NSEW")

    def SelectFile(self):
        self.path = filedialog.askdirectory(title="Select a File")
        Label(self.frame, text=self.path, font=13).grid(row=1, column=0, sticky="NSEW")

    def ReadFiles(self):
        #implentacja wczytywania plikow do bazy danych
        result = True
        if result:
            self.label_status.config(text="Wczytywanie powiodlo sie", fg="green")
        else:
            self.label_status.config(text="Nie powiodlo sie", fg="red")

    def GetFrame(self):
        return self.frame

    def show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        return self

    def hide(self):
        self.frame.grid_remove()


