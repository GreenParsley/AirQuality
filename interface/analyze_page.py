import os
from datetime import timedelta
from tkinter import *
from tkinter.ttk import Treeview

import geopy.distance
import numpy
from numpy import mean, sort
from pandas import DataFrame, Series, concat
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
        self.trips_table['columns'] = ("Id", "Name", "Distance", "Speed", "Type", "StartDate", "EndDate")
        self.trips_table.column("#0", width=0, stretch=NO)
        self.trips_table.column("Id", anchor=CENTER, width=100)
        self.trips_table.column("Name", anchor=CENTER, width=200)
        self.trips_table.column("Distance", anchor=CENTER, width=150)
        self.trips_table.column("Speed", anchor=CENTER, width=150)
        self.trips_table.column("Type", anchor=CENTER, width=200)
        self.trips_table.column("StartDate", anchor=CENTER, width=200)
        self.trips_table.column("EndDate", anchor=CENTER, width=200)
        self.trips_table.heading("#0", text="", anchor=CENTER)
        self.trips_table.heading("Id", text="Id", anchor=CENTER)
        self.trips_table.heading("Name", text="Name", anchor=CENTER)
        self.trips_table.heading("Distance", text="Distance", anchor=CENTER)
        self.trips_table.heading("Speed", text="Speed", anchor=CENTER)
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
        last_trip_id_name = self.db.GetLastTripId()
        start_measure = None
        end_measure = None
        previous_date = None
        for m in measures:
            date = m.Date
            if (previous_date is not None) and (date < previous_date):
                break
            previous_date = date
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
                trip = Trips("Trip_" + str(last_trip_id_name + 1))
                trip.StartDate = start_measure
                trip.EndDate = end_measure
                trip.TripType = current_trip.trip_type
                trip.Speed = current_trip.speed
                trip.Distance = current_trip.distance
                trips.append(trip)
                start_measure = None
                end_measure = None
                last_trip_id += 1
                last_trip_id_name += 1
            elif (start_measure is None) and (date > current_trip.end_date):
                last_trip_id += 1
        if start_measure is not None:
            trip = Trips("Trip_" + str(last_trip_id_name + 1))
            trip.StartDate = start_measure
            trip.EndDate = end_measure
            trip.TripType = current_trip.trip_type
            trip.Speed = current_trip.speed
            trip.Distance = current_trip.distance
            trips.append(trip)
        return trips

    def CreateTableAnalyzedTrip(self, trips):
        scroll = Scrollbar(self.frame)
        scroll.grid(row=3, column=0, sticky="E")
        self.analyzed_trips_table = Treeview(self.frame, yscrollcommand=scroll.set)
        self.analyzed_trips_table.bind("<Double-1>", self.EditTable)
        self.analyzed_trips_table.grid(row=3, column=0, rowspan=5)
        scroll.config(command=self.analyzed_trips_table.yview)
        self.analyzed_trips_table['columns'] = ("Id", "Name", "Distance", "Speed", "Type", "StartDate", "EndDate")
        self.analyzed_trips_table.column("#0", width=0, stretch=NO)
        self.analyzed_trips_table.column("Id", anchor=CENTER, width=100)
        self.analyzed_trips_table.column("Name", anchor=CENTER, width=200)
        self.analyzed_trips_table.column("Distance", anchor=CENTER, width=150)
        self.analyzed_trips_table.column("Speed", anchor=CENTER, width=150)
        self.analyzed_trips_table.column("Type", anchor=CENTER, width=200)
        self.analyzed_trips_table.column("StartDate", anchor=CENTER, width=200)
        self.analyzed_trips_table.column("EndDate", anchor=CENTER, width=200)
        self.analyzed_trips_table.heading("#0", text="", anchor=CENTER)
        self.analyzed_trips_table.heading("Id", text="Id", anchor=CENTER)
        self.analyzed_trips_table.heading("Name", text="Name", anchor=CENTER)
        self.analyzed_trips_table.heading("Distance", text="Distance", anchor=CENTER)
        self.analyzed_trips_table.heading("Speed", text="Speed", anchor=CENTER)
        self.analyzed_trips_table.heading("Type", text="Type", anchor=CENTER)
        self.analyzed_trips_table.heading("StartDate", text="StartDate", anchor=CENTER)
        self.analyzed_trips_table.heading("EndDate", text="EndDate", anchor=CENTER)
        index = 0
        for t in trips:
            self.analyzed_trips_table.insert(parent='', index='end', iid=index, text='',
                                             values=(t.Id, t.Name, t.Distance, t.Speed, t.TripType, t.StartDate, t.EndDate))
            index += 1
        button_save_all = Button(self.frame, text="Save all", command=lambda: self.SaveAllChanges(), padx=10)
        button_save_all.grid(row=9, column=0, sticky="E")

    def SaveAllChanges(self):
        children = self.analyzed_trips_table.get_children()
        trips = []
        for child in children:
            values = self.analyzed_trips_table.item(child)["values"]
            trips.append(Trips(values[1], values[5], values[6], values[4], values[2], values[3]))
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
        total_distance = 0
        speeds = []
        last_position = None
        start_date = None
        end_date = None
        for p in positions:
            date = p.Date
            if start_date is None:
                start_date = date
                end_date = date
                last_position = (p.Latitude, p.Longitude, date)
                continue
            if (((date - end_date).total_seconds()) / 60.0) < 10:
                end_date = date
                current_position = (p.Latitude, p.Longitude, date)
                speed_and_distance = self.CalculateSpeed(last_position, current_position)
                speed = speed_and_distance[0]
                speeds.append(speed)
                total_distance = total_distance + speed_and_distance[1]
                last_position = current_position
                continue
            else:
                trip_date.append(TripDate(start_date - timedelta(minutes=5), end_date + timedelta(minutes=5), self.GetTripType(self.GetAverageSpeed(speeds)), total_distance, self.GetAverageSpeed(speeds)))
                start_date = None
                end_date = None
                speeds = []
                total_distance = 0
        if start_date is not None:
            trip_date.append(TripDate(start_date - timedelta(minutes=5), end_date + timedelta(minutes=5),
                                      self.GetTripType(self.GetAverageSpeed(speeds)), total_distance, self.GetAverageSpeed(speeds)))
        return trip_date

    def GetTripType(self, speed):
        #if speed większy to zwracam jakiś typ
        if speed < 0.7:
            return "stop "
        elif (speed >= 0.7) and (speed < 9):
            return "walk "
        elif (speed >= 9) and (speed < 40):
            return "bicycle "
        elif (speed >= 40):
            return "vehicle, etc. "

    def GetAverageSpeed(self, speeds):
        #ileś najszybszych to policzyć średnią, jak nie ma to 0 dawać
        if (speeds is None) or (len(speeds) == 0):
            return 0
        elif len(speeds) < 3:
            return speeds[0]
        else:
            sorted_speeds = sort(speeds)
            percent50 = round(len(sorted_speeds) * 0.5)
            return mean(sorted_speeds[-percent50:])

    def CalculateSpeed(self, last_position, current_position):
        #liczyć distance i czas i potem prędkość
        distance = geopy.distance.geodesic((last_position[0], last_position[1]), (current_position[0], current_position[1])).km
        time_seconds = abs(last_position[2] - current_position[2])
        time_hours = time_seconds.total_seconds() / (60*60)
        speed = distance / time_hours
        return speed, distance

    def ExportStatisticData(self, data):
        last_id = self.db.GetLastTripId()
        if not os.path.exists('Export'):
            os.mkdir('Export')
        file_name = 'Export\\' + "Statistic_data_last_trip-" + str(last_id) + '.csv'
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
        list_sort = sort(sd_df[col_name])
        value_of_2_and_half_percent = 2.5 / 100
        value_of_97_and_half_percent = 97.5 / 100
        values_of_100_percent = len(list_sort)
        id_2_and_half_percent = round(value_of_2_and_half_percent * values_of_100_percent)
        id_97_and_half_percent = round(value_of_97_and_half_percent * values_of_100_percent)
        two_and_half_percent = list_sort[id_2_and_half_percent-1]
        ninetyseven_and_half_percent = list_sort[id_97_and_half_percent - 1]
        percentile = (two_and_half_percent, ninetyseven_and_half_percent)
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
        statistic_data_df = DataFrame(columns=["Trip ID", "Type", "Speed [km/h]", "Distance [km]", "StartDate", "EndDate", "Time [min]",
                 "min_NO2", 'max_NO2', 'mean_NO2', 'std_NO2', '95CI_NO2',
                 "min_VOC", 'max_VOC', 'mean_VOC', 'std_VOC', '95CI_VOC',
                 "min_PM1", 'max_PM1', 'mean_PM1', 'std_PM1', '95CI_PM1',
                 "min_PM2,5", 'max_PM2,5', 'mean_PM2,5', 'std_PM2,5', '95CI_PM2,5',
                 "min_PM10", 'max_PM10', 'mean_PM10', 'std_PM10', '95CI_PM10'])
        id = 1
        for trip in trips:
            all_data = self.GetStatisticData(trip.Id)
            data = {'Trip ID': trip.Id,
                    'Type': trip.TripType,
                    'Speed [km/h]': trip.Speed,
                    'Distance [km]': trip.Distance,
                    'StartDate': trip.StartDate,
                    'EndDate': trip.EndDate,
                    'Time [min]': (trip.EndDate - trip.StartDate).total_seconds() / 60.0,
                    'min_NO2': all_data[0][0], 'max_NO2': all_data[0][1], 'mean_NO2': all_data[0][2], 'std_NO2': all_data[0][3], '95CI_NO2': all_data[0][4],
                    'min_VOC': all_data[1][0], 'max_VOC': all_data[1][1], 'mean_VOC': all_data[1][2], 'std_VOC': all_data[1][3], '95CI_VOC': all_data[1][4],
                    'min_PM1': all_data[2][0], 'max_PM1': all_data[2][1], 'mean_PM1': all_data[2][2], 'std_PM1': all_data[2][3], '95CI_PM1': all_data[2][4],
                    'min_PM2,5': all_data[3][0], 'max_PM2,5': all_data[3][1], 'mean_PM2,5': all_data[3][2], 'std_PM2,5': all_data[3][3], '95CI_PM2,5': all_data[3][4],
                    'min_PM10': all_data[4][0], 'max_PM10': all_data[4][1], 'mean_PM10': all_data[4][2], 'std_PM10': all_data[4][3], '95CI_PM10': all_data[4][4]}
            statistic_data_df.loc[id] = data
            id += 1
        self.ExportStatisticData(statistic_data_df)

    def GetFrame(self):
        return self.frame

    def Show(self):
        self.ClearAllTripsFromTable()
        trips = self.db.GetAllTrips()
        self.frame.grid(row=0, column=1, sticky="NSEW")
        index = 0
        for t in trips:
            self.trips_table.insert(parent='', index='end', iid=index, text='',
                                    values=(t.Id, t.Name, t.Distance, t.Speed, t.TripType, t.StartDate, t.EndDate))
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
