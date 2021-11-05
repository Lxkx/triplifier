import configparser
import csv
import pydash
import re
import difflib

class Triplificator:

    def __init__(self, csvPath, rowNumTitle, rowNumFirst, rowNumLast, separator, dataPrefixIRI, predicatPrefixIRI):

        #Initialisation of the config file reading
        config = configparser.ConfigParser()
        config.read("config.ini") #the configParser strip the spaces before and after the value

        
        #Setting up the object variables regarding the config file or the user input

        #CSV
        self.csvPath = csvPath
        #Set up the object variables but not the coherence (like if title not first non empty row) and the indexes
        if (rowNumTitle is None):
            self.rowNumTitle = int(config["CSV"]["titleRow"])
        else:
            self.rowNumTitle = rowNumTitle

        if (rowNumFirst is None):
            self.rowNumFirst = config["CSV"]["firstDataRow"]
        else:
            self.rowNumFirst = rowNumFirst

        if (rowNumLast is None):
            self.rowNumLast = config["CSV"]["lastDataRow"]
        else:
            self.rowNumLast = rowNumLast

        if (separator is None):
            self.separator = config["CSV"]["separator"]
        else:
            self.separator = separator

        #TURTLE
        if (dataPrefixIRI is None):
            self.dataPrefixIRI = config["TURTLE"]["dataPrefixIRI"]
        else:
            self.dataPrefixIRI = dataPrefixIRI

        self.dataPrefix = re.findall(r'^[a-z]*:', self.dataPrefixIRI)[0]

        if (predicatPrefixIRI is None):
            self.predicatPrefixIRI = config["TURTLE"]["predicatPrefixIRI"]
        else:
            self.predicatPrefixIRI = predicatPrefixIRI

        self.predicatPrefix = re.findall(r'^[a-z]*:', self.predicatPrefixIRI)[0]

        print(self.csvPath)
        print(self.rowNumTitle)
        print(self.rowNumFirst)
        print(self.rowNumLast)
        print(self.separator)
        print(self.dataPrefixIRI)
        print(self.predicatPrefixIRI)
        print(self.dataPrefix)
        print(self.predicatPrefix)

    def checkValues(self): #voir si les valeurs rentrees par l'uti sont ok (par ex titre ligne 12 mais au final pas premiere ligne)
                           #et rewrite les bonnes en fonction du csv si besoin (par ex par defaut 0 titre mais possible qu'a la ligne 4)
        pass


    def writeFile(self):
        #here we assume that we have all the good configuration variables in our object, and rows numbers as indexes

        #write in output.ttl file
        with open("output.ttl", "w") as turtleFile:
            #first two rows are prefixes and the corresponding IRIs
            turtleFile.write("@prefix "+self.dataPrefixIRI+" .\n")
            turtleFile.write("@prefix "+self.predicatPrefixIRI+" .\n\n")

            #open the csv to write info in ttl
            lineIndex = self.rowNumFirst
            with open(self.csvPath, 'r') as csvFile:
                csvReader = csv.reader(csvFile, delimiter=self.separator) #csv.Reader object, not subscriptable
                csvReader = list(csvReader) #list object, subscriptable
                # print(csvReader)
                #select the list of titles (titles = potential csv column names)
                if (self.rowNumTitle >= 0):
                    self.listTitles = [row for idx, row in enumerate(csvReader) if idx == self.rowNumTitle][0]
                    self.listTitles = list(map(pydash.camel_case, self.listTitles))

                    self.listData = [row for idx, row in enumerate(csvReader) if idx in range(self.rowNumFirst, self.rowNumLast)]
                    for row in self.listData:
                        turtleFile.write(self.dataPrefix + str(lineIndex) + "\t\t")
                        dictRow = dict(zip(self.listTitles, row))
                        for key, value in dictRow.items():
                            turtleFile.write(self.predicatPrefix+str(key) + "\t\t" + "\""+value+"\"" + " ;\n\t\t")
                        turtleFile.write(".\n")
                        lineIndex += 1

                else: #if not title
                    pass

                
                    



if __name__ == "__main__":    
    chemin = "data/test4.csv"
    #None if the user does not enter anything for the below variables
    ligneTitre = None
    lignePremier = 1
    ligneDernier = 5
    sep = ","
    dataPrefIRI = None
    predicatPrefIRI = "p: <http://ex.org/pred#>"

    a = Triplificator(chemin, ligneTitre, lignePremier, ligneDernier, sep, dataPrefIRI, predicatPrefIRI)
    a.writeFile()
    