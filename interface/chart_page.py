from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from chart_creator import ChartCreator
from airquality_database import AirQuality
from cast_models import CastModels


class ChartPage:
    db: AirQuality
    chart_creator: ChartCreator
    cast_models: CastModels
    def __init__(self, root, db):
        self.db = db
        self.chart_creator = ChartCreator()
        self.cast_models = CastModels()
        self.frame = Frame(root)
        self.variable = StringVar(self.frame)
        button_read = Button(self.frame, text="Read", command=lambda: self.ShowChart())
        button_read.grid(row=0, column=1, columnspan=2, pady=10)
        # canvas = Canvas(self.frame, bg="yellow")
        # canvas.grid(row=0, column=0, sticky="e")
        # scroll = Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        # scroll.grid(row=1, column=0, sticky='e')
        # canvas.configure(yscrollcommand=scroll.set)

    def ReadData(self, ms_df, param):
        df = self.chart_creator.clean(ms_df, param, "Date", 100, 200)
        fig = self.chart_creator.plot_ts(df, param, "Date")
        return fig

    def CreateMsDf(self):
        measures = self.db.GetAllMeasures()
        ms_df = self.cast_models.CastToPandas(measures)
        return ms_df
    def ShowChart(self):
        ms_df = self.CreateMsDf()
        self.CreateChart(ms_df, 1, "NO2")
        self.CreateChart(ms_df, 2, "VOC")
        self.CreateChart(ms_df, 3, "PM1")
        self.CreateChart(ms_df, 4, "PM2")
        self.CreateChart(ms_df, 5, "PM10")

    def CreateChart(self, ms_df, num_row, param):
        fig = self.ReadData(ms_df, param)
        dataPlot = FigureCanvasTkAgg(fig, master=self.frame)
        dataPlot.draw()
        dataPlot.get_tk_widget().grid(row=num_row, column=0, pady=1)

    def ReadExistFilesName(self):
        files = self.db.GetAllFile()
        files_names = []
        for f in files:
            files_names.append(f.Name)
        return files_names

    def GetFrame(self):
        return self.frame

    def show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        names = self.ReadExistFilesName()
        w = OptionMenu(self.frame, self.variable, value=names, command=lambda: self.ShowChart())
        w.grid(row=0, column=0, sticky="NSEW")
        return self

    def hide(self):
        self.frame.grid_remove()

