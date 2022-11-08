from datetime import timedelta
from tkinter import *
from tkinter.ttk import Treeview
from database.airquality_database import AirQuality, Trips
from models.trip_date import TripDate


class AnalyzePage:
    db: AirQuality

    def __init__(self, root, db):
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

    def GetFrame(self):
        return self.frame

    def ClearAllTripsFromTable(self):
        for item in self.trips_table.get_children():
            self.trips_table.delete(item)

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

        drop_list = OptionMenu(self.frame, self.variable, *id_trips)
        drop_list.grid(row=1, column=0, sticky="NSEW")
        button = Button(self.frame, text="Analyze", command=lambda: self.AnalyzeTrip())
        button.grid(row=2, column=0, sticky="NSEW")
        return self

    def AnalyzeTrip(self):
        trip_id = self.variable.get()
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
        self.db.UpdateMeasures(measures_to_update)
        trip_id = self.variable.get()
        self.db.DeleteMultipleMeasures(trip_id)
        self.db.DeleteTrip(trip_id)

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
        name = self.name_text.get("1.0", END)
        type = self.type_text.get("1.0", END)
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

    def Hide(self):
        self.frame.grid_remove()
