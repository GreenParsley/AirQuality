from tkinter import *

from airquality_database import AirQuality


class ChartPage:
    db: AirQuality
    def __init__(self, root, db):
        self.db = db
        self.frame = Frame(root)
        self.variable = StringVar(self.frame)
        self.variable.set("one")  # default value
        w = OptionMenu(self.frame, self.variable, "one", "two", "three", command=lambda: self.ReadData())
        w.grid(row=0, column=0, sticky="NSEW")

    def ReadData(self):
        pass

    def ReadExistFilesName(self):
        pass

    def GetFrame(self):
        return self.frame

    def show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        return self

    def hide(self):
        self.frame.grid_remove()

