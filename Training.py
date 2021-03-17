import copy
from Parameter import ClassParameter, WordParameter


class Training:
    def __init__(self, listOfCategories, documents):
        self.listOfCategories = listOfCategories
        self.documents = documents
        self.metaData = documents.metaData
        self.righe = self.metaData[0]
        self.colonne = self.metaData[1]
        self.data = self.metaData[2]
        self.nParole = len(self.metaData[3])
        self.listOfTrainingDocuments = documents.listOfDocuments
        self.nEsempi = len(self.listOfTrainingDocuments)
        self.nCategories = len(self.listOfCategories)
        self.categoriesOfTrainingDocument = documents.categorieOfDocuments
        self.listClassParameters = []
        self.buildClassParameters()
        self.listWordParameters = []
        self.buildWordParameters()
        self.LToW = []

    def binomialTraining(self):
        i = 0
        while i < len(self.righe):
            if i == 0 or (self.righe[i] != self.righe[i - 1]):  # primo documento or nuovo documento
                classDocument = self.categoriesOfTrainingDocument[self.righe[i]]
                self.listClassParameters[classDocument].nOfExample = self.listClassParameters[classDocument].nOfExample + 1
            self.listWordParameters[self.colonne[i]].incTimeOfWordBin(classDocument)
            i = i + 1
        self.computeTimeOfWord()

    def computeTimeOfWord(self):  # salva in un dizionario quante volte è uscita una parola tra tutti i documenti della STESSA classe
        CToW = []                 # lista con un dizionario per ogni classe
        c = 0
        while c < self.nCategories:
            dictio = {}
            CToW.append(dictio)
            c = c + 1

        i = 0
        while i < len(self.righe):
            if i == 0 or (self.righe[i] != self.righe[i - 1]):
                classDocument = self.categoriesOfTrainingDocument[self.righe[i]]
            indexWord = self.colonne[i]
            if indexWord not in (CToW[classDocument].keys()):
                CToW[classDocument].update({indexWord : self.listWordParameters[indexWord].timeOfWord[classDocument]})      # timeOfWord tiene conto del LaplaceSmoothing
            i = i + 1
        self.computeListsOfToW(CToW)

    def computeListsOfToW(self, cToW):  # salva in un dizionario il numero di parole (==value) che sono uscite X (==key) volte tra tutti i documenti di una STESSA classe
        CToW = cToW
        c = 0
        while c < self.nCategories:
            dictio = {}
            self.LToW.append(dictio)
            c = c + 1

        c = 0
        while c < self.nCategories:
            for wordIndex in CToW[c].keys():
                times = CToW[c][wordIndex]
                if times in self.LToW[c].keys():          # Significa che ho già incontrato almeno una volta una parola che è uscita 'times' volte tra i documenti di classe c
                    ptrTime = self.LToW[c][times] + 1
                    self.LToW[c].update({times: ptrTime})
                else:                                     # Prima volta che incontro una parola uscita 'times' volte
                    self.LToW[c].update({times: 1})
            c = c + 1

        tprTOTtime = 0                                    # Per differenza calcolo tutte le parole che non ho mai incontrato tra tutti i documenti di una classe.
        c = 0
        while c < self.nCategories:
            for time in self.LToW[c]:
                tprTOTtime = tprTOTtime + self.LToW[c][time]
            zeroTimeWords = self.nParole - tprTOTtime
            self.LToW[c].update({1: zeroTimeWords})        # N.B. Per LaplaceSmoothing ogni parola è presente almeno una volta in un documento di ogni classe
            tprTOTtime = 0
            c = c + 1

    def multinomialTraining(self):
        i = 0
        while i < len(self.righe):
            if i == 0 or (self.righe[i] != self.righe[i - 1]):                      # primo documento or nuovo documento
                classDocument = self.categoriesOfTrainingDocument[self.righe[i]]
                self.listClassParameters[classDocument].nOfExample = self.listClassParameters[classDocument].nOfExample + 1
            time = self.data[i]
            self.listWordParameters[self.colonne[i]].incTimeOfWordMul(time, classDocument)
            i = i + 1
        self.wordParameterDenominators()

    def wordParameterDenominators(self):
        vocabularySize = self.nParole
        c = 0
        while c < self.nCategories:
            s = 0
            sommatoriaEXT = 0
            while s < vocabularySize:
                sommatoriaINT = self.listWordParameters[s].timeOfWord[c]  # Restituisce il num di occorrenze della parola s tra tutti i documenti di classe c
                sommatoriaEXT = sommatoriaEXT + sommatoriaINT
                s = s + 1
            risultato = sommatoriaEXT  # + vocabularySize che é incluso in timeOfWord[c]
            p = 0
            while p < len(self.listWordParameters):
                self.listWordParameters[p].multinomialDenominator[c] = risultato
                p = p + 1
            c = c + 1

    def buildClassParameters(self):
        self.listClassParameters = []
        for index in self.listOfCategories:
            self.listClassParameters.append(ClassParameter(len(self.listClassParameters), self.nCategories, self.nEsempi))

    def buildWordParameters(self):
        self.listWordParameters = []
        for index in range(self.nParole):
            self.listWordParameters.append(WordParameter(self.listClassParameters))

    def getLToW(self):
        b = copy.deepcopy(self.LToW)
        return b
