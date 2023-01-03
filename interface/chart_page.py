import os
from datetime import datetime
from statistics import mean, median
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import sort

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
        button_read = Button(self.frame, text="Read", command=lambda: self.ShowChart())
        button_read.grid(row=0, column=1, columnspan=2, pady=10)

    def ReadData(self, ms_df, param):
        df = self.chart_creator.Clean(ms_df, param, "Date")
        fig = self.chart_creator.PlotTS(df, param, "Date")
        return fig

    def CreateMsDf(self):
        trip_id = self.name_text.get("1.0", 'end-1c')
        measures = self.db.GetMeasuresByTrip(trip_id)
        ms_df = self.cast_models.CastToPandas(measures)
        return ms_df

    def ShowChart(self):
        self.ms_df = self.CreateMsDf()
        self.CreateChart(self.ms_df, 1, 0, "NO2")
        self.CreateChart(self.ms_df, 2, 0, "VOC")
        self.CreateChart(self.ms_df, 3, 0, "PM1", 6)
        self.CreateChart(self.ms_df, 1, 1, "PM2", span_col=3)
        self.CreateChart(self.ms_df, 2, 1, "PM10", span_col=3)
        button_export = Button(self.frame, text="Export data", command=lambda: self.ExportData())
        button_export.grid(row=7, column=2, sticky="W")
        self.ShowStatistics()

    def ExportData(self):
        if not os.path.exists('Export'):
            os.mkdir('Export')
        file_name = 'Export\\' + self.db.GetTripNameById(self.name_text.get("1.0", 'end-1c')) + '.csv'
        self.ms_df.to_csv(file_name, encoding='utf-8', index=False)

    def CreateChart(self, ms_df, num_row, num_col, param, span_row=1, span_col=1):
        fig = self.ReadData(ms_df, param)
        data_plot = FigureCanvasTkAgg(fig, master=self.frame)
        data_plot.draw()
        data_plot.get_tk_widget().grid(row=num_row, column=num_col, pady=1, rowspan=span_row, columnspan=span_col)

    def ShowStatistics(self):
        stat_options = ["", "Average", "Median", "Min", "Max", "Percentile"]
        self.variable = StringVar(self.frame)
        statistics_drop_list = OptionMenu(self.frame, self.variable, *stat_options)
        statistics_drop_list.grid(row=3, column=1, sticky="W")
        self.start_text = Text(self.frame, height=1, width=20)
        self.start_text.grid(row=3, column=2, sticky="W")
        self.start_text.insert(END, self.ms_df["Date"][0])
        Label(self.frame, text="Percentile: ").grid(row=4, column=2, sticky="E")
        self.percentile_text = Text(self.frame, height=1, width=20)
        self.percentile_text.grid(row=4, column=3, sticky="W")
        self.end_text = Text(self.frame, height=1, width=20)
        self.end_text.grid(row=3, column=3, sticky="W")
        self.end_text.insert(END, self.ms_df["Date"][len(self.ms_df)-1])
        self.label_no2 = Label(self.frame, text="NO2:")
        self.label_no2.grid(row=4, column=1, sticky="W")
        self.label_voc = Label(self.frame, text="VOC:")
        self.label_voc.grid(row=5, column=1, sticky="W")
        self.label_pm1 = Label(self.frame, text="PM1:")
        self.label_pm1.grid(row=6, column=1, sticky="W")
        self.label_pm2 = Label(self.frame, text="PM2.5:")
        self.label_pm2.grid(row=7, column=1, sticky="W")
        self.label_pm10 = Label(self.frame, text="PM10:")
        self.label_pm10.grid(row=8, column=1, sticky="W")
        Button(self.frame, text="Update", command=lambda: self.UpdateStatisticData()).grid(row=5, column=2, sticky="W")

    def GetFilteredStatisticData(self):
        selected_id = self.FindIndexForDate()
        startparam = self.ms_df["Date"][selected_id[0]]
        endparam = self.ms_df["Date"][selected_id[1]]
        filter_ts = (self.ms_df["Date"] <= endparam) & (self.ms_df["Date"] >= startparam)
        ms_filtered_df = self.ms_df[filter_ts]
        return ms_filtered_df.dropna()

    def FindIndexForDate(self):
        start_date = datetime.strptime(self.start_text.get("1.0", 'end-1c'), "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(self.end_text.get("1.0", 'end-1c'), "%Y-%m-%d %H:%M:%S")
        start_id = 0
        end_id = len(self.ms_df["Date"])-1
        for i in range(len(self.ms_df["Date"])):
            current_date = datetime.strptime(str(self.ms_df["Date"][i]), "%Y-%m-%d %H:%M:%S")
            if start_date >= current_date:
                start_id = i
            if end_date >= current_date:
                end_id = i
        return (start_id, end_id)


    def UpdateStatisticData(self):
        ms_filtered_df = self.GetFilteredStatisticData()
        self.label_no2.config(text="NO2: " + self.CalculateValue(ms_filtered_df, "NO2"))
        self.label_voc.config(text="VOC: " + self.CalculateValue(ms_filtered_df, "VOC"))
        self.label_pm1.config(text="PM1: " + self.CalculateValue(ms_filtered_df, "PM1"))
        self.label_pm2.config(text="PM2: " + self.CalculateValue(ms_filtered_df, "PM2"))
        self.label_pm10.config(text="PM10: " + self.CalculateValue(ms_filtered_df, "PM10"))

    def CalculateValue(self, ms_df, col_name):
        operation = self.variable.get()
        if operation == "":
            return ""
        elif operation == "Average":
            return str(mean(ms_df[col_name]))
        elif operation == "Median":
            return str(median(ms_df[col_name]))
        elif operation == "Min":
            return str(min(ms_df[col_name]))
        elif operation == "Percentile":
            list = sort(ms_df[col_name])
            value_of_percentile = int(self.percentile_text.get("1.0", 'end-1c'))/100
            values_of_100_percent = len(list)
            id_percentile = round(value_of_percentile * values_of_100_percent)
            percentile = ms_df[col_name][id_percentile]
            return str(percentile)
        else:
            return str(max(ms_df[col_name]))

    def GetFrame(self):
        return self.frame

    def Show(self):
        self.frame.grid(row=0, column=1, sticky="NSEW")
        label = Label(self.frame, text="ID:")
        label.grid(row=0, column=0, sticky="W", padx=20)
        self.name_text = Text(self.frame, height=1, width=20)
        self.name_text.grid(row=0, column=0, sticky="W", padx=50)
        return self

    def Hide(self):
        self.frame.grid_remove()
