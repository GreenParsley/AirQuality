from datetime import timedelta
from tkinter import *
from tkinter.ttk import Treeview
from sqlalchemy import func
from airquality_database import AirQuality, File


class AnalyzePage:
    db: AirQuality
    def __init__(self, root, db):
        self.db = db
        self.frame = Frame(root)
        self.variable = StringVar(self.frame)
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



    def GetFrame(self):
        return self.frame

    def clear_all(self):
        for item in self.trips_table.get_children():
            self.trips_table.delete(item)

    def show(self):
        self.clear_all()
        trips = self.db.GetTrips()
        self.frame.grid(row=0, column=1, sticky="NSEW")
        index = 0
        for t in trips:
            self.trips_table.insert(parent='', index='end', iid=index, text='',
                           values=(t.Id, t.Name, t.TripType, t.StartDate, t.EndDate))
            index += 1
        id_trips = []
        for t in trips:
            id_trips.append(t.Id)

        drop_list = OptionMenu(self.frame, self.variable, *id_trips)
        drop_list.grid(row=1, column=0, sticky="NSEW")
        button = Button(self.frame, text="Analyze", command=lambda: self.AnalyzeTrip())
        button.grid(row=2, column=0, sticky="NSEW")
        return self

    def AnalyzeTrip(self):
        trip_id = self.variable.get()
        measures = self.db.GetMeasuresByTrip(trip_id)
        positions = self.db.GetPositionsByTrip(trip_id)
        trip_date = self.GetTripsFromPositions(positions)
        trips = self.SplitTrips(measures, trip_date)
        self.CreateTableAnalyzedTrip(trips)

    def SplitTrips(self, measures, trip_date):
        trips = []
        last_trip_id = 0
        start_measure = None
        end_measure = None
        for m in measures:
            date = m.Date
            if last_trip_id >= len(trip_date):
                break
            accurent_trip = trip_date[last_trip_id]
            if (date >= accurent_trip[0]) and (date <= accurent_trip[1]):
                if start_measure is None:
                    start_measure = date
                    end_measure = date
                else:
                    end_measure = date
            elif start_measure is not None:
                trip = File("Trip_" + str(last_trip_id + 1))
                trip.StartDate = start_measure
                trip.EndDate = end_measure
                trips.append(trip)
                start_measure = None
                end_measure = None
                last_trip_id += 1
        if start_measure is not None:
            trip = File("Trip_" + str(last_trip_id + 1))
            trip.StartDate = start_measure
            trip.EndDate = end_measure
            trips.append(trip)
        return trips

    def CreateTableAnalyzedTrip(self, trips):
        scroll = Scrollbar(self.frame)
        scroll.grid(row=3, column=0, sticky="E")
        self.analyzed_trips_table = Treeview(self.frame, yscrollcommand=scroll.set)
        self.analyzed_trips_table.grid(row=3, column=0)
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
        edit_button = Button(self.frame, text="Edit", command=lambda: self.EditTable())
        edit_button.grid(row=4, column=0, sticky="NSEW")

    def EditTable(self):
        pass

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
                trip_date.append([start_date - timedelta(minutes=5), end_date + timedelta(minutes=5)])
                start_date = None
                end_date = None
        return trip_date

    def hide(self):
        self.frame.grid_remove()

