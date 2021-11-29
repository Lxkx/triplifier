import configparser
import csv
import pydash
import re

class Triplificator:

    def __init__(self, csvPath, rowNumTitle, rowNumFirst, rowNumLast, separator, dataPrefixIRI, predicatPrefixIRI, isTitle):

        #Initialisation of the config file reading
        config = configparser.ConfigParser()
        config.read("utils/config.ini") #the configParser strip the spaces before and after the value

        #Setting up the object variables regarding the config file or the user input

        #CSV
        self.csvPath = csvPath

        #isTitle boolean
        self.isTitle = isTitle
        
        #Set up the object variables but not the coherence (like if title not first non empty row) and the indexes
        if (rowNumTitle is None):
            self.rowNumTitle = config["CSV"]["titleRow"]
        else:
            self.rowNumTitle = int(rowNumTitle)

        if (rowNumFirst is None):
            self.rowNumFirst = config["CSV"]["firstDataRow"]
        else:
            self.rowNumFirst = int(rowNumFirst)

        if (rowNumLast is None):
            self.rowNumLast = config["CSV"]["lastDataRow"]
        else:
            self.rowNumLast = int(rowNumLast)

        if (separator is None):
            print("SEPARATOR NONE")
            self.separator = config["CSV"]["separator"]
        else:
            self.separator = separator

        #TURTLE
        if (dataPrefixIRI is None):
            self.dataPrefixIRI = config["TURTLE"]["dataPrefixIRI"]
        else:
            self.dataPrefixIRI = dataPrefixIRI

        self.dataPrefix = re.findall(r'^[a-zA-Z]*:', self.dataPrefixIRI)[0]

        if (predicatPrefixIRI is None):
            self.predicatPrefixIRI = config["TURTLE"]["predicatPrefixIRI"]
        else:
            self.predicatPrefixIRI = predicatPrefixIRI

        self.predicatPrefix = re.findall(r'^[a-zA-Z]*:', self.predicatPrefixIRI)[0]

        print(self.csvPath)
        print(self.rowNumTitle)
        print(self.rowNumFirst)
        print(self.rowNumLast)
        print("SEPARATOR")
        print(self.separator)
        print(self.dataPrefixIRI)
        print(self.predicatPrefixIRI)
        print(self.dataPrefix)
        print(self.predicatPrefix)

        self.checkValues() # = Triplificator.checkValues(self)



    def checkValues(self): #voir si les valeurs rentrees par l'uti sont ok (par ex titre ligne 12 mais au final pas premiere ligne)
                           #et rewrite les bonnes en fonction du csv si besoin (par ex par defaut 0 titre mais possible qu'a la ligne 4)
        with open(self.csvPath, 'r', encoding="utf-8") as csvFile:

            #set up of title row number
            csvReader = csv.reader(csvFile, delimiter=self.separator) #object: csv.Reader -> not subscriptable
            csvReader = list(csvReader) #object: list -> subscriptable


            if (self.rowNumTitle == "FirstRow"):
                #check for first non empty list
                self.rowNumTitle = next(idx for idx, row in enumerate(csvReader) if row)
            else:
                #if row 1 contains titles -> index 0 contains titles (we want the index)
                self.rowNumTitle = self.rowNumTitle - 1
            
            if (self.rowNumFirst == "AfterTitle"):
                if (not(self.isTitle)):
                    self.rowNumFirst = self.rowNumTitle
                else:
                    #check for first non empty list after title
                    self.rowNumFirst = next(idx for idx, row in enumerate(csvReader) if row and idx > self.rowNumTitle)
            else:
                self.rowNumFirst = self.rowNumFirst - 1

            if (self.rowNumLast == "EndFile"):
                #check for last non empty list after title
                self.rowNumLast = [idx for idx, row in enumerate(csvReader) if row][-1]
            else:
                self.rowNumLast = self.rowNumLast - 1


            print("Row num title after coherence treatment "+str(self.rowNumTitle))
            print("Row first data after coherence treatment "+str(self.rowNumFirst))
            print("Row last data after coherence treatment "+str(self.rowNumLast))





    def writeFile(self, path):
        #here we assume that we have all the good configuration variables in our object, and rows numbers as indexes

        #write in output.ttl file
        with open(path, "w", encoding="utf-8") as turtleFile:
            #first two rows are prefixes and the corresponding IRIs
            turtleFile.write("@prefix "+self.dataPrefixIRI+" .\n")
            turtleFile.write("@prefix "+self.predicatPrefixIRI+" .\n\n")

            #open the csv to write info in ttl
            lineIndex = self.rowNumFirst
            with open(self.csvPath, 'r', encoding="utf-8") as csvFile:
                csvReader = csv.reader(csvFile, delimiter=self.separator) #object: csv.Reader -> not subscriptable
                csvReader = list(csvReader) #object: list -> subscriptable
                print(csvReader)
                print("IS THERE A TITLE", self.isTitle)
                print("IS THERE A TITLE", type(self.isTitle))
                #select the list of titles (titles = potential csv column names)
                if (self.isTitle):
                    print("YES TITLE")
                    self.listTitles = [row for idx, row in enumerate(csvReader) if idx == self.rowNumTitle][0]
                    self.listTitles = list(map(pydash.camel_case, self.listTitles))

                    self.listData = [row for idx, row in enumerate(csvReader) if idx in range(self.rowNumFirst, self.rowNumLast+1)]
                    for row in self.listData:
                        turtleFile.write(self.dataPrefix + str(lineIndex+1) + "\t\t")
                        dictRow = dict(zip(self.listTitles, row))
                        for key, value in dictRow.items():
                            turtleFile.write(self.predicatPrefix+str(key) + "\t\t" + "\""+value+"\"" + " ;\n\t\t")
                        turtleFile.write(".\n")
                        lineIndex += 1

                else: #if no titles
                    print("NO TITLE")
                    self.nbCol = len(csvReader[self.rowNumTitle])
                    self.listTitles = ["attribute"+str(i+1) for i in range(self.nbCol)]
                    print(self.rowNumTitle)
                    print(self.rowNumFirst)

                    self.listData = [row for idx, row in enumerate(csvReader) if idx in range(self.rowNumFirst, self.rowNumLast+1)]
                    for row in self.listData:
                        turtleFile.write(self.dataPrefix + str(lineIndex+1) + "\t\t")
                        dictRow = dict(zip(self.listTitles, row))
                        for key, value in dictRow.items():
                            turtleFile.write(self.predicatPrefix+str(key) + "\t\t" + "\""+value+"\"" + " ;\n\t\t")
                        turtleFile.write(".\n")
                        lineIndex += 1

                
                    



if __name__ == "__main__":    
    chemin = "data/test3.csv"
    #None if the user does not enter anything for the below variables
    #If user enters all rows are str
    ligneTitre = None
    lignePremier = 4
    ligneDernier = 18
    sep = "|"
    dataPrefIRI = None
    predicatPrefIRI = "pp: <www.jeanvaljean.com>"
    #We assume that we have logical variables here, like rowNumTitle < rowFirstData < rowLastData etc.
    #globally things that can be handled using a web script such as JS, Django does that also
    a = Triplificator(chemin, ligneTitre, lignePremier, ligneDernier, sep, dataPrefIRI, predicatPrefIRI, True)
    a.writeFile()
    