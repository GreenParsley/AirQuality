import os
from datetime import datetime
from statistics import mean, median
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import sort
from utils.chart_creator import ChartCreator
from database.airquality_database import AirQuality
from utils.cast_models import CastModels


class RawChartPage:
    db: AirQuality
    chart_creator: ChartCreator
    cast_models: CastModels

    def __init__(self, root, db):
        self.db = db
        self.chart_creator = ChartCreator()
        self.cast_models = CastModels()
        self.frame = Frame(root)
        button_read = Button(self.frame, text="Read", command=lambda: self.ShowChart())
        button_read.grid(row=0, column=2, columnspan=2, pady=10)
        label_start = Label(self.frame, text="Start:")
        label_start.grid(row=0, column=0, sticky="W", padx=20)
        self.start_date_text = Text(self.frame, height=1, width=20)
        self.start_date_text.grid(row=0, column=0, sticky="W", padx=50)
        self.start_date_text.insert(END, str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
        label_end = Label(self.frame, text="End:")
        label_end.grid(row=0, column=1, sticky="W", padx=20)
        self.end_date_text = Text(self.frame, height=1, width=20)
        self.end_date_text.grid(row=0, column=1, sticky="W", padx=50)
        self.end_date_text.insert(END, str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))

    def ReadData(self, ms_df, param):
        df = self.chart_creator.Clean(ms_df, param, "Date")
        fig = self.chart_creator.PlotTS(df, param, "Date")
        return fig

    def CreateMsDf(self):
        start = datetime.strptime(self.start_date_text.get("1.0", 'end-1c').replace('\n', ''), "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(self.end_date_text.get("1.0", 'end-1c').replace('\n', ''), "%Y-%m-%d %H:%M:%S")
        measures = self.db.GetMeasuresByDate(start, end)
        ms_df = self.cast_models.CastToPandas(measures)
        return ms_df

    def ShowChart(self):
        self.ms_df = self.CreateMsDf()
        if self.ms_df.empty:
            return
        self.CreateChart(self.ms_df, 1, 0, "NO2")
        self.CreateChart(self.ms_df, 2, 0, "VOC")
        self.CreateChart(self.ms_df, 3, 0, "PM1", 6)
        self.CreateChart(self.ms_df, 1, 1, "PM2", span_col=3)
        self.CreateChart(self.ms_df, 2, 1, "PM10", span_col=3)

    def CreateChart(self, ms_df, num_row, num_col, param, span_row=1, span_col=1):
        fig = self.ReadData(ms_df, param)
        data_plot = FigureCanvasTkAgg(fig, master=self.frame)
        data_plot.draw()
        data_plot.get_tk_widget().grid(row=num_row, column=num_col, pady=1, rowspan=span_row, columnspan=span_col)

    def GetFrame(self):
        return self.frame

    def Show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        return self

    def Hide(self):
        self.frame.grid_remove()
