import configparser
import csv
import re

class Triplificator:

    def __init__(self, csvPath, rowNumTitle, rowNumFirst, rowNumLast, separator, dataPrefixIRI, predicatPrefixIRI):

        #Initialisation of the config file reading
        config = configparser.ConfigParser()
        config.read("config.ini")

        #Initialisation of the csv config informations from the config file
        self.configRowNumTitle = config["CSV"]["titleRow"]
        self.configRowNumFirst = config["CSV"]["firstDataRow"]
        self.configRowNumLast = config["CSV"]["lastDataRow"]
        self.configSeparator = config["CSV"]["separator"]

        #Initialisation of the turtle config informations from the config file
        self.configDataPrefixIRI = config["TURTLE"]["dataPrefixIRI"]
        self.configPredicatPrefixIRI = config["TURTLE"]["predicatPrefixIRI"]

        #Setting up the object variables regarding the config file or the user input

        #CSV
        self.csvPath = csvPath

        if (self.configRowNumTitle != rowNumTitle):
            self.rowNumTitle = rowNumTitle
        else:
            self.rowNumTitle = self.configRowNumTitle

        if (self.configRowNumFirst != rowNumFirst):
            self.rowNumFirst = rowNumFirst
        else:
            self.rowNumFirst = self.configRowNumFirst

        if (self.configRowNumLast != rowNumLast):
            self.rowNumLast = rowNumLast
        else:
            self.rowNumLast = self.configRowNumLast

        if (self.configSeparator != separator):
            self.separator = separator
        else:
            self.separator = self.configSeparator

        #TURTLE
        if (self.configDataPrefixIRI != dataPrefixIRI):   
            self.dataPrefixIRI = dataPrefixIRI
        else:
            self.dataPrefixIRI = self.configDataPrefixIRI

        self.dataPrefix = re.findall(r'^[a-z]*:', self.dataPrefixIRI)[0]

        if (self.configPredicatPrefixIRI != predicatPrefixIRI):
            self.predicatPrefixIRI = predicatPrefixIRI
        else:
            self.predicatPrefixIRI = self.configPredicatPrefixIRI

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
                           #et rewrite les bonnes en fonction du csv si besoin (par ex par defaut 0 titre mais possible 4)
        pass


    def writeFile(self):

        #write in output.ttl file
        with open("output.ttl", "w") as turtleFile:
            #first two rows are prefixes and the corresponding IRIs
            turtleFile.write("@prefix "+self.dataPrefixIRI+" .\n")
            turtleFile.write("@prefix "+self.predicatPrefixIRI+" .\n\n\n")

            #open the csv to write info in ttl
            lineIndex = self.rowNumFirst
            with open(self.csvPath, 'r') as csvFile:

                if (self.rowNumTitle >= 0):
                    #DictReader cannot work without titles (= column names)
                    csvReader = csv.DictReader(csvFile)
                    for row in csvReader: #each element is a dict {'title1':value, 'title2':value, ...}
                        turtleFile.write(self.dataPrefix + str(lineIndex) + "\t\t")
                        print(row)
                        for key, value in row.items():
                            turtleFile.write(self.predicatPrefix+str(key) + "\t\t" + "\""+value+"\"" + " ;\n\t\t")
                        turtleFile.write(".\n")
                            

                        lineIndex += 1

                else: #if not title
                    pass

                # csvReader=[row for idx, row in enumerate(csvReader) if idx in range(10)]
                # for row in csvReader:
                #     print(row)
                    



if __name__ == "__main__":
    chemin = "data/test4.csv"
    ligneTitre = 0 #faire en sorte d'avoir -1 si pas de titre, 0 si utilisateur rentre rien
    lignePremier = 1 #-1 si l'utilisateur rentre rien
    ligneDernier = 420 #-1 si l'utilisateur rentre rien
    sep = "," # ',' si l'utilisateur rentre rien
    dataPrefIRI = "d: <http://ex.org/data/>" #-1 si l'utilisateur rentre rien
    predicatPrefIRI = "p: <http://ex.org/pred#>" #-1 si l'utilisateur rentre rien

    a = Triplificator(chemin, ligneTitre, lignePremier, ligneDernier, sep, dataPrefIRI, predicatPrefIRI)
    a.writeFile()
