from tkinter import *


class HomePage:
    def __init__(self, root):
        self.frame = Frame(root)
        label = Label(self.frame, text="Welcome to the AirQuality app", font=(0, 50), anchor=CENTER)
        label.pack(side=TOP, pady=30)

    def GetFrame(self):
        return self.frame

    def Show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        return self

    def Hide(self):
        self.frame.grid_remove()
