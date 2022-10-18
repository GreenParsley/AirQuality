from datetime import date
from datetime import datetime
from sqlalchemy import create_engine, Float
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Using SQLite
database_name = 'sqlite:///AirQuality.sqlite'
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
    FileId = Column(Integer, ForeignKey("File.Id"), nullable=False)

    def __init__(self, timestamp, date, no2, voc, pm10, pm2, pm1, no2_PlumeAQI, voc_PlumeAQI, pm10_PlumeAQI,
                 pm2_PlumeAQI, pm1_PlumeAQI, fileId):
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
        self.FileId = fileId


class Positions(Base):
    __tablename__ = "Positions"

    Id = Column(Integer, primary_key=True)
    Timestamp = Column(Integer, nullable=False)
    Date = Column(DateTime, default=datetime.utcnow, nullable=False)
    Latitude = Column(Float, nullable=False)
    Longitude = Column(Float, nullable=False)
    FileId = Column(Integer, ForeignKey("File.Id"), nullable=False)

    def __init__(self, timestamp, date, latitude, longitude, fileId):
        self.Timestamp = timestamp
        self.Date = date  # problem rzutowania prawdopodobnie
        self.Latitude = latitude
        self.Longitude = longitude
        self.FileId = fileId


class File(Base):
    __tablename__ = "File"

    Id = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    CreateDate = Column(DateTime, nullable=False)
    Measures = relationship("Measures")
    Positions = relationship("Positions")

    def __init__(self, name):
        self.Name = name
        self.CreateDate = date.today()


class AirQuality:

    def __init__(self):
        self.sess = None
        self.session = None

    def Create(self):
        Base.metadata.drop_all()
        Base.metadata.create_all()
        self.session = sessionmaker(bind=eng)
        self.sess = self.session()

    def AddFile(self, fileName):
        file = File(fileName)
        self.sess.add(file)
        self.sess.flush()
        return file.Id

    def AddPositions(self, positions):
        self.sess.add_all(positions)
        self.sess.commit()

    def AddMeasures(self, measures):
        self.sess.add_all(measures)
        self.sess.commit()

    def GetAllFile(self):
        files = self.sess.query(File).all()
        return files

    def GetAllPositions(self):
        positions = self.sess.query(Positions).all()
        for position in positions:
            print(position.Timestamp)
        return positions

    def GetAllMeasures(self):
        measures = self.sess.query(Measures).all()
        for measure in measures:
            print(measure.Timestamp)
        return measures
