from tkinter import *
from tkinter import filedialog
import pandas as pd
import os
import glob
from file_reader import FileReader
from cast_models import CastModels
from airquality_database import AirQuality


class FilePage:
    db: AirQuality
    file_reader: FileReader
    cast_models: CastModels
    def __init__(self, root, db):
        self.db = db
        self.file_reader = FileReader()
        self.cast_models = CastModels()
        self.frame = Frame(root)
        #Label(self.frame, text="Welcome to the AirQuality app", font=(0, 50), background="green")
        self.frame.grid_rowconfigure(1, minsize=30)
        Label(self.frame, text="Click the Button to Select a Folder:", font=('Aerial 18 bold')).grid(row=0, column=0, sticky="NSEW")
        button = Button(self.frame, text="Select", command=lambda: self.SelectFile())
        button.grid(row=1, column=1, columnspan=2, pady=10)
        button_read = Button(self.frame, text="Read", command=lambda: self.ReadFiles())
        button_read.grid(row=4, column=0, columnspan=2, pady=10)
        Label(self.frame, text="Create name:", font=('Aerial 18 bold')).grid(row=2, column=0, sticky="NSEW")
        self.file_name = Text(self.frame, height=1)
        self.file_name.grid(row=3, column=0, sticky="NSEW")
        self.label_status = Label(self.frame, font=('Aerial 18 bold'))
        self.label_status.grid(row=5, column=0, sticky="NSEW")

    def SelectFile(self):
        self.path = filedialog.askdirectory(title="Select a File")
        Label(self.frame, text=self.path, font=13).grid(row=1, column=0, sticky="NSEW")
        return self.path

    def ReadFiles(self):
        try:
            id = self.AddFileToDataBase()
            csv_files = glob.glob(os.path.join(self.path, "*.csv"))
            for f in csv_files:
                if "measures" in f:
                    data_measures = self.file_reader.Read(f)
                    measures = self.cast_models.CastToMeasures(data_measures, id)
                    self.db.AddMeasures(measures)
                elif "positions" in f:
                    data_positions = self.file_reader.Read(f)
                    positions = self.cast_models.CastToPositions(data_positions, id)
                    self.db.AddPositions(positions)
            self.label_status.config(text="loading success", fg="green")
        except:
            self.label_status.config(text="loading failed", fg="red")

    def AddFileToDataBase(self):
        name = self.file_name.get("1.0", 'end-1c')
        id = self.db.AddFile(name)
        return id

    def GetFrame(self):
        return self.frame

    def show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        return self

    def hide(self):
        self.frame.grid_remove()


