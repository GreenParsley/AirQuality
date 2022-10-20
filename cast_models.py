from datetime import datetime
from airquality_database import Positions, Measures
import pandas as pd


class CastModels:
    def __init__(self):
        pass

    def CastToPositions(self, data, fileId):
        positionsCollection = []
        for records in data[1:]:
            positionsCollection.append(
                Positions(records[0], datetime.strptime(records[1], "%Y-%m-%d %H:%M:%S"), records[2], records[3],
                          fileId))
        return positionsCollection

    def CastToMeasures(self, data, fileId):
        measuresCollection = []
        for records in data[1:]:
            measuresCollection.append(
                Measures(records[0], datetime.strptime(records[1], "%Y-%m-%d %H:%M:%S"), records[2], records[3],
                         self.ReturnNullIfEmpty(records[4]), self.ReturnNullIfEmpty(records[5]),
                         self.ReturnNullIfEmpty(records[6]), records[7], records[8], self.ReturnNullIfEmpty(records[9]),
                         self.ReturnNullIfEmpty(records[10]), self.ReturnNullIfEmpty(records[11]),
                         fileId))
        return measuresCollection

    def CastToPandas(self, data):
        df = pd.DataFrame([t.__dict__ for t in data])
        return df

    def ReturnNullIfEmpty(self, value):
        if value == "":
            return None
        return value
