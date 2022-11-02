from datetime import date
from datetime import datetime
from sqlalchemy import create_engine, Float
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from sqlalchemy_utils import database_exists

# Using SQLite
database_name = 'sqlite:///database/AirQuality.sqlite'
eng = create_engine(database_name, echo=True)
Base = declarative_base()
Base.metadata.bind = eng


class Measures(Base):
    __tablename__ = "Measures"

    Id = Column(Integer, primary_key=True)
    Timestamp = Column(Integer, nullable=False)
    Date = Column(DateTime, nullable=False)
    NO2 = Column(Integer, nullable=False)
    VOC = Column(Integer, nullable=False)
    PM10 = Column(Float, nullable=True)
    PM2 = Column(Float, nullable=True)
    PM1 = Column(Integer, nullable=True)
    NO2_PlumeAQI = Column(Integer, nullable=False)
    VOC_PlumeAQI = Column(Integer, nullable=False)
    PM10_PlumeAQI = Column(Integer, nullable=True)
    PM2_PlumeAQI = Column(Integer, nullable=True)
    PM1_PlumeAQI = Column(Integer, nullable=True)
    TripId = Column(Integer, ForeignKey("Trips.Id"), nullable=False)

    def __init__(self, timestamp, date, no2, voc, pm10, pm2, pm1, no2_PlumeAQI, voc_PlumeAQI, pm10_PlumeAQI,
                 pm2_PlumeAQI, pm1_PlumeAQI, trip_id):
        self.Timestamp = timestamp
        self.Date = date
        self.NO2 = no2
        self.VOC = voc
        self.PM10 = pm10
        self.PM2 = pm2
        self.PM1 = pm1
        self.NO2_PlumeAQI = no2_PlumeAQI
        self.VOC_PlumeAQI = voc_PlumeAQI
        self.PM10_PlumeAQI = pm10_PlumeAQI
        self.PM2_PlumeAQI = pm2_PlumeAQI
        self.PM1_PlumeAQI = pm1_PlumeAQI
        self.TripId = trip_id


class Positions(Base):
    __tablename__ = "Positions"

    Id = Column(Integer, primary_key=True)
    Timestamp = Column(Integer, nullable=False)
    Date = Column(DateTime, default=datetime.utcnow, nullable=False)
    Latitude = Column(Float, nullable=False)
    Longitude = Column(Float, nullable=False)
    FileId = Column(Integer, ForeignKey("Trips.Id"), nullable=False)

    def __init__(self, timestamp, date, latitude, longitude, trip_id):
        self.Timestamp = timestamp
        self.Date = date
        self.Latitude = latitude
        self.Longitude = longitude
        self.FileId = trip_id


class Trips(Base):
    __tablename__ = "Trips"

    Id = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    CreateDate = Column(DateTime, nullable=False)
    StartDate = Column(DateTime, nullable=True)
    EndDate = Column(DateTime, nullable=True)
    TripType = Column(String, nullable=True)
    Measures = relationship("Measures")
    Positions = relationship("Positions")

    def __init__(self, name):
        self.Name = name
        self.CreateDate = date.today()

class AirQuality:
    sess: Session
    def __init__(self):
        self.sess = None
        self.session = None

    def Create(self):
        if database_exists(database_name) is False:
            Base.metadata.drop_all()
            Base.metadata.create_all()
        self.session = sessionmaker(bind=eng)
        self.sess = self.session()

    def AddTrip(self, tripName):
        trip = Trips(tripName)
        self.sess.add(trip)
        self.sess.flush()
        return trip

    def UpdateTrip(self, trip):
        self.sess.add(trip)
        self.sess.commit()

    def AddPositions(self, positions):
        self.sess.add_all(positions)
        self.sess.commit()


    def AddMeasures(self, measures):
        self.sess.add_all(measures)
        self.sess.commit()

    def GetAllTrips(self):
        trips = self.sess.query(Trips).all()
        return trips

    def GetCountFiles(self):
        count = self.sess.query(Trips).count()
        return count

    def GetAllPositions(self):
        positions = self.sess.query(Positions).all()
        return positions

    def GetAllMeasures(self):
        measures = self.sess.query(Measures).all()
        return measures

    def GetPositionsByTrip(self, trip_id):
        positions = self.sess.query(Positions).filter(Positions.FileId == trip_id).all()
        return positions

    def GetMeasuresByTrip(self, trip_id):
        measures = self.sess.query(Measures).filter(Measures.TripId == trip_id).all()
        return measures
