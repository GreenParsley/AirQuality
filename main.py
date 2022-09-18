import file_reader
import airquality_database
from os.path import exists
from cast_models import CastModels
import glob, os


database = airquality_database.AirQuality()
if exists(airquality_database.database_name) == False:
    database.Create()

database.AddFile("test")
database.GetAllFile()

filereader = file_reader.FileReader()
castmodels = CastModels()

dataPositions = filereader.Read(r'C:\Users\Ola\Desktop\Flow_data\user_positions_20220509_20220823_1.csv')
os.chdir(r"C:\Users\Ola\Desktop\Flow_data\measures")
for file in glob.glob("*.csv"):
    dataMeasures = filereader.Read(file)
    measures = castmodels.CastToMeasures(dataMeasures, 1)
    database.AddMeasures(measures)

positions = castmodels.CastToPositions(dataPositions, 1)

database.AddPositions(positions)
database.GetAllPositions()