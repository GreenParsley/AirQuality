from tkinter import *

class HomePage:
    def __init__(self, root):
        self.frame = Frame(root, bg="pink")
        label = Label(self.frame, text="Welcome to the AirQuality app", font=(0, 50), background="yellow", anchor=CENTER)
        label.grid(row=0, column=0, sticky="NSEW")

    def GetFrame(self):
        return self.frame

    def show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        return self

    def hide(self):
        self.frame.grid_remove()

