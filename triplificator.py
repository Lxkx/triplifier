import configparser
import csv

class Triplificator:

    def __init__(self, csvPath, rowNumTitle, rowNumFirst, rowNumLast, separator=','):
        self.csvPath = csvPath
        self.rowNumTitle = rowNumTitle
        self.rowNumFirst = rowNumFirst
        self.rowNumLast = rowNumLast
        self.separator = separator


    def openCsv(self):
        with open(self.csvPath, 'r') as csvFile:
            csvReader = csv.reader(csvFile)
            for l in csvReader:
                #print(l)
                pass

    def openConfig(self):
        config = configparser.ConfigParser()
        print(config.read("config.ini"))
        print(config.sections())
        print(config["USER"]["name"])


if __name__ == "__main__":
    chemin = "data/test2.csv"
    numTitre = 0
    numPremier = 1
    numDernier = 10
    a = Triplificator(chemin, 0, 1, 100)
    a.openCsv()
    a.openConfig()
    print("afafa")

