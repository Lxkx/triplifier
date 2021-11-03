from os import sep
import pandas as pd

class Triplificator:

    def __init__(self, csvPath, rowNumTitle, rowNumFirst, rowNumOne, separator=','):
        self.csvPath = csvPath
        self.rowNumTitle = rowNumTitle
        self.rowNumFirst = rowNumFirst
        self.rowNumOne = rowNumOne
        self.separator = separator


    def openCsv(self):
        self.csv = pd.read_csv(self.csvPath, sep=self.separator)



if __name__ == "__main__":
    Triplificator("e")
    print("oui")
    print(pd.read_csv("data/test2.csv", sep=";"))

