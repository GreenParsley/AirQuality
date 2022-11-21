import csv


class FileReader:
    def __init__(self):
        pass

    def Read(self, fileName):
        with open(fileName, newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
            return data
