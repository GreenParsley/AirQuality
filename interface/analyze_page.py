from tkinter import *
from tkinter.ttk import Treeview

from airquality_database import AirQuality


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
        self.trips_table['columns'] = ("Id", "Name", "StartDate", "EndDate")
        self.trips_table.column("#0", width=0, stretch=NO)
        self.trips_table.column("Id", anchor=CENTER, width=300)
        self.trips_table.column("Name", anchor=CENTER, width=300)
        self.trips_table.column("StartDate", anchor=CENTER, width=300)
        self.trips_table.column("EndDate", anchor=CENTER, width=300)
        self.trips_table.heading("#0", text="", anchor=CENTER)
        self.trips_table.heading("Id", text="Id", anchor=CENTER)
        self.trips_table.heading("Name", text="Name", anchor=CENTER)
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
                           values=(t.Id, t.Name, t.StartDate, t.EndDate))
            index += 1
        id_trips = []
        for t in trips:
            id_trips.append(t.Id)

        drop_list = OptionMenu(self.frame, self.variable, *id_trips)
        drop_list.grid(row=1, column=0, sticky="NSEW")
        return self

    def hide(self):
        self.frame.grid_remove()

