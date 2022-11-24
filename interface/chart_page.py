import os
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.chart_creator import ChartCreator
from database.airquality_database import AirQuality
from utils.cast_models import CastModels


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

    def ReadData(self, ms_df, param):
        df = self.chart_creator.Clean(ms_df, param, "Date")
        fig = self.chart_creator.PlotTS(df, param, "Date")
        return fig

    def CreateMsDf(self):
        trip_id = self.variable.get()
        measures = self.db.GetMeasuresByTrip(trip_id)
        ms_df = self.cast_models.CastToPandas(measures)
        return ms_df

    def ShowChart(self):
        self.ms_df = self.CreateMsDf()
        self.CreateChart(self.ms_df, 1, 0, "NO2")
        self.CreateChart(self.ms_df, 2, 0, "VOC")
        self.CreateChart(self.ms_df, 3, 0, "PM1")
        self.CreateChart(self.ms_df, 1, 1, "PM2")
        self.CreateChart(self.ms_df, 2, 1, "PM10")
        button_export = Button(self.frame, text="Export data", command=lambda: self.ExportData(), height=3, width=15)
        button_export.grid(row=3, column=1, sticky="NW", padx=30, pady=30)

    def ExportData(self):
        if not os.path.exists('Export'):
            os.mkdir('Export')
        file_name = 'Export\\' + self.trip_dictionary.get(int(self.variable.get())) + '.csv'
        self.ms_df.to_csv(file_name, encoding='utf-8', index=False)

    def CreateChart(self, ms_df, num_row, num_col, param):
        fig = self.ReadData(ms_df, param)
        data_plot = FigureCanvasTkAgg(fig, master=self.frame)
        data_plot.draw()
        data_plot.get_tk_widget().grid(row=num_row, column=num_col, pady=1)

    def ReadExistFilesName(self):
        files = self.db.GetAllTrips()
        files_names = []
        self.trip_dictionary = {}
        for f in files:
            files_names.append(f.Id)
            self.trip_dictionary[f.Id] = f.Name
        return files_names

    def GetFrame(self):
        return self.frame

    def Show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        names = self.ReadExistFilesName()
        w = OptionMenu(self.frame, self.variable, *names, command=lambda: self.ShowChart())
        w.config(width=10)
        w.grid(row=0, column=0, sticky="NSW", padx=50)
        return self

    def GetLastSelectedChartId(self):
        return self.variable

    def Hide(self):
        self.frame.grid_remove()
