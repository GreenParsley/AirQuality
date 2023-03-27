import os
from datetime import timedelta
from tkinter import *
from tkinter.ttk import Treeview
import numpy
from numpy import mean, sort
from pandas import DataFrame
from database.airquality_database import AirQuality, Trips
from models.trip_date import TripDate
from utils.cast_models import CastModels

class AnalyzePage:
    db: AirQuality

    def __init__(self, root, db):
        self.cast_models = CastModels()
        self.db = db
        self.frame = Frame(root)
        self.variable = StringVar(self.frame)
        self.table_index = -1
        scroll = Scrollbar(self.frame)
        scroll.grid(row=0, column=0, sticky="E")
        self.trips_table = Treeview(self.frame, yscrollcommand=scroll.set)
        self.trips_table.grid(row=0, column=0)
        scroll.config(command=self.trips_table.yview)
        self.trips_table['columns'] = ("Id", "Name", "Type", "StartDate", "EndDate")
        self.trips_table.column("#0", width=0, stretch=NO)
        self.trips_table.column("Id", anchor=CENTER, width=250)
        self.trips_table.column("Name", anchor=CENTER, width=250)
        self.trips_table.column("Type", anchor=CENTER, width=250)
        self.trips_table.column("StartDate", anchor=CENTER, width=250)
        self.trips_table.column("EndDate", anchor=CENTER, width=250)
        self.trips_table.heading("#0", text="", anchor=CENTER)
        self.trips_table.heading("Id", text="Id", anchor=CENTER)
        self.trips_table.heading("Name", text="Name", anchor=CENTER)
        self.trips_table.heading("Type", text="Type", anchor=CENTER)
        self.trips_table.heading("StartDate", text="StartDate", anchor=CENTER)
        self.trips_table.heading("EndDate", text="EndDate", anchor=CENTER)

    def ClearAllTripsFromTable(self):
        for item in self.trips_table.get_children():
            self.trips_table.delete(item)

    def AnalyzeTrip(self):
        trip_id = self.id_text.get("1.0", 'end-1c')
        self.measures = self.db.GetMeasuresByTrip(trip_id)
        positions = self.db.GetPositionsByTrip(trip_id)
        trip_date = self.GetTripsFromPositions(positions)
        trips = self.SplitTrips(self.measures, trip_date)
        self.CreateTableAnalyzedTrip(trips)
        self.CreateEditPanel()

    def SplitTrips(self, measures, trip_date):
        trips = []
        last_trip_id = 0
        start_measure = None
        end_measure = None
        for m in measures:
            date = m.Date
            if last_trip_id >= len(trip_date):
                break
            current_trip = trip_date[last_trip_id]
            if (date >= current_trip.start_date) and (date <= current_trip.end_date):
                if start_measure is None:
                    start_measure = date
                    end_measure = date
                else:
                    end_measure = date
            elif start_measure is not None:
                trip = Trips("Trip_" + str(last_trip_id + 1))
                trip.StartDate = start_measure
                trip.EndDate = end_measure
                trips.append(trip)
                start_measure = None
                end_measure = None
                last_trip_id += 1
        if start_measure is not None:
            trip = Trips("Trip_" + str(last_trip_id + 1))
            trip.StartDate = start_measure
            trip.EndDate = end_measure
            trips.append(trip)
        return trips

    def CreateTableAnalyzedTrip(self, trips):
        scroll = Scrollbar(self.frame)
        scroll.grid(row=3, column=0, sticky="E")
        self.analyzed_trips_table = Treeview(self.frame, yscrollcommand=scroll.set)
        self.analyzed_trips_table.bind("<Double-1>", self.EditTable)
        self.analyzed_trips_table.grid(row=3, column=0, rowspan=5)
        scroll.config(command=self.analyzed_trips_table.yview)
        self.analyzed_trips_table['columns'] = ("Id", "Name", "Type", "StartDate", "EndDate")
        self.analyzed_trips_table.column("#0", width=0, stretch=NO)
        self.analyzed_trips_table.column("Id", anchor=CENTER, width=250)
        self.analyzed_trips_table.column("Name", anchor=CENTER, width=250)
        self.analyzed_trips_table.column("Type", anchor=CENTER, width=250)
        self.analyzed_trips_table.column("StartDate", anchor=CENTER, width=250)
        self.analyzed_trips_table.column("EndDate", anchor=CENTER, width=250)
        self.analyzed_trips_table.heading("#0", text="", anchor=CENTER)
        self.analyzed_trips_table.heading("Id", text="Id", anchor=CENTER)
        self.analyzed_trips_table.heading("Name", text="Name", anchor=CENTER)
        self.analyzed_trips_table.heading("Type", text="Type", anchor=CENTER)
        self.analyzed_trips_table.heading("StartDate", text="StartDate", anchor=CENTER)
        self.analyzed_trips_table.heading("EndDate", text="EndDate", anchor=CENTER)
        index = 0
        for t in trips:
            self.analyzed_trips_table.insert(parent='', index='end', iid=index, text='',
                                             values=(t.Id, t.Name, t.TripType, t.StartDate, t.EndDate))
            index += 1
        button_save_all = Button(self.frame, text="Save all", command=lambda: self.SaveAllChanges(), padx=10)
        button_save_all.grid(row=9, column=0, sticky="E")

    def SaveAllChanges(self):
        children = self.analyzed_trips_table.get_children()
        trips = []
        for child in children:
            values = self.analyzed_trips_table.item(child)["values"]
            trips.append(Trips(values[1], values[3], values[4], values[2]))
        for trip in trips:
            self.db.UpdateTrip(trip)
        measures_to_update = []
        last_trip_index = 0
        should_update_index = False
        for m in self.measures:
            date = m.Date
            if last_trip_index >= len(trips):
                break
            if (date >= trips[last_trip_index].StartDate) and (date <= trips[last_trip_index].EndDate):
                m.TripId = trips[last_trip_index].Id
                measures_to_update.append(m)
                should_update_index = True
                continue
            if should_update_index is True:
                last_trip_index += 1
                should_update_index = False
        self.EstimateValueForMeasures(measures_to_update)
        self.db.UpdateMeasures(measures_to_update)
        trip_id = self.id_text.get("1.0", 'end-1c')
        self.db.DeleteMultipleMeasures(trip_id)
        self.db.DeleteTrip(trip_id)

    def EstimateValueForMeasures(self, measures):
        last_trip_id = 0
        for i in range(1, len(measures) - 1):
            if last_trip_id != measures[i].TripId:
                last_trip_id = measures[i].TripId
                continue
            if (measures[i + 1].TripId != last_trip_id) or (measures[i - 1].TripId != last_trip_id):
                continue
            if measures[i].NO2 == 0:
                measures[i].NO2 = (measures[i + 1].NO2 + measures[i - 1].NO2) / 2
            if measures[i].VOC == 0:
                measures[i].VOC = (measures[i + 1].VOC + measures[i - 1].VOC) / 2
            if measures[i].PM10 == 0:
                measures[i].PM10 = (measures[i + 1].PM10 + measures[i - 1].PM10) / 2
            if measures[i].PM2 == 0:
                measures[i].PM2 = (measures[i + 1].PM2 + measures[i - 1].PM2) / 2
            if measures[i].PM1 == 0:
                measures[i].PM1 = (measures[i + 1].PM1 + measures[i - 1].PM1) / 2

    def CreateEditPanel(self):
        Label(self.frame, text="Name:", anchor=CENTER).grid(row=3, column=1, sticky="W", padx=10, columnspan=2)
        self.name_text = Text(self.frame, height=1, width=25)
        self.name_text.grid(row=4, column=1, sticky="W", padx=10, columnspan=2)
        Label(self.frame, text="Type:", anchor=CENTER).grid(row=5, column=1, sticky="W", padx=10)
        self.type_text = Text(self.frame, height=1, width=25)
        self.type_text.grid(row=6, column=1, sticky="W", padx=10, columnspan=2)
        button_save = Button(self.frame, text="Save", command=lambda: self.SaveTripChanges(), padx=10)
        button_save.grid(row=7, column=1, sticky="W")
        button_delete = Button(self.frame, text="Delete", command=lambda: self.DeleteTrip(), padx=10)
        button_delete.grid(row=7, column=2, sticky="W")

    def DeleteTrip(self):
        if self.table_index == -1:
            return
        self.analyzed_trips_table.delete(self.table_index)
        self.name_text.delete("1.0", END)
        self.type_text.delete("1.0", END)
        self.table_index = -1

    def EditTable(self, event):
        self.table_index = self.analyzed_trips_table.selection()[0]
        values = self.analyzed_trips_table.item(self.table_index).get("values")
        self.name_text.delete("1.0", END)
        self.type_text.delete("1.0", END)
        self.name_text.insert(END, values[1])
        self.type_text.insert(END, values[2])

    def SaveTripChanges(self):
        if self.table_index == -1:
            return
        name = self.name_text.get("1.0", END).replace('\n', '')
        type = self.type_text.get("1.0", END).replace('\n', '')
        self.analyzed_trips_table.set(self.table_index, 1, name)
        self.analyzed_trips_table.set(self.table_index, 2, type)

    def GetTripsFromPositions(self, positions):
        trip_date = []
        start_date = None
        end_date = None
        for p in positions:
            date = p.Date
            if start_date is None:
                start_date = date
                end_date = date
                continue
            if (((date - end_date).total_seconds()) / 60.0) < 10:
                end_date = date
                continue
            else:
                trip_date.append(TripDate(start_date - timedelta(minutes=5), end_date + timedelta(minutes=5)))
                start_date = None
                end_date = None
        return trip_date

    def ExportStatisticData(self, data, trip_name):
        if not os.path.exists('Export'):
            os.mkdir('Export')
        file_name = 'Export\\' + "Statistic_data_" + str(trip_name) + '.csv'
        data.to_csv(file_name, encoding='utf-8', index=True)

    def CreateSdDf(self, trip_id):
        statistic_data = self.db.GetMeasuresByTrip(trip_id)
        sd_df = self.cast_models.CastToPandas(statistic_data)
        return sd_df.dropna()

    def CalculateStatisticValue(self, sd_df, col_name):
        mean_value = mean(sd_df[col_name])
        min_value = min(sd_df[col_name])
        max_value = max(sd_df[col_name])
        std_value = numpy.std(sd_df[col_name])
        list = sort(sd_df[col_name])
        value_of_percentile = 95 / 100
        values_of_100_percent = len(list)
        id_percentile = round(value_of_percentile * values_of_100_percent)
        percentile = list[id_percentile-1]
        return min_value, max_value, mean_value, std_value, percentile

    def GetStatisticData(self, trip_id):
        self.sd_df = self.CreateSdDf(trip_id)
        data_no2 = self.CalculateStatisticValue(self.sd_df, "NO2")
        data_voc = self.CalculateStatisticValue(self.sd_df, "VOC")
        data_pm1 = self.CalculateStatisticValue(self.sd_df, "PM1")
        data_pm2 = self.CalculateStatisticValue(self.sd_df, "PM2")
        data_pm10 = self.CalculateStatisticValue(self.sd_df, "PM10")
        return data_no2, data_voc, data_pm1, data_pm2, data_pm10

    def GetStatisticDataInDfToCsv(self):
        trips = self.db.GetAllTrips()
        for trip in trips:
            all_data = self.GetStatisticData(trip.Id)
            data = {'Trip ID': (trip.Id, trip.Id, trip.Id, trip.Id, trip.Id),
                    'Type': (trip.TripType, trip.TripType, trip.TripType, trip.TripType, trip.TripType)
                , 'NO2': all_data[0], 'VOC': all_data[1], 'PM1': all_data[2], 'PM2': all_data[3], 'PM10': all_data[4]}
            statistic_data_df = DataFrame(data)
            statistic_data_df.rename(index={0: "min", 1: "max", 2: "mean", 3: "standard deviation", 4: '95th percentile'}, inplace=True)
            self.ExportStatisticData(statistic_data_df, trip.Name)

    def GetFrame(self):
        return self.frame

    def Show(self):
        self.ClearAllTripsFromTable()
        trips = self.db.GetAllTrips()
        self.frame.grid(row=0, column=1, sticky="NSEW")
        index = 0
        for t in trips:
            self.trips_table.insert(parent='', index='end', iid=index, text='',
                                    values=(t.Id, t.Name, t.TripType, t.StartDate, t.EndDate))
            index += 1
        id_trips = []
        for t in trips:
            id_trips.append(t.Id)

        label = Label(self.frame, text="ID:")
        label.grid(row=1, column=0, sticky="W", padx=20)
        self.id_text = Text(self.frame, height=1, width=20)
        self.id_text.grid(row=1, column=0, sticky="W", padx=50)
        button = Button(self.frame, text="Analyze", command=lambda: self.AnalyzeTrip())
        button.grid(row=2, column=0, sticky="NSEW")
        button_statistic = Button(self.frame, text="Export statistic data for all trips.",
                                  command=lambda: self.GetStatisticDataInDfToCsv())
        button_statistic.grid(row=0, column=1, sticky="NSEW", padx=20, pady=100)
        return self

    def Hide(self):
        self.frame.grid_remove()
