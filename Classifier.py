import numpy as np


class Classifier:
    def __init__(self, documents, trainer):
        self.documents = documents
        self.categoriesOfDocs = self.documents.categorieOfDocuments
        self.listOfTestDocuments = documents.listOfDocuments
        self.metaData = self.documents.metaData
        self.trainer = trainer
        self.listOfCategories = self.trainer.listOfCategories
        self.listClassParameters = self.trainer.listClassParameters
        self.listWordParameters = self.trainer.listWordParameters
        self.risultati = []
        self.nText = len(self.listOfTestDocuments)
        self.nParole = len(self.listWordParameters)
        self.righe = self.metaData[0]
        self.colonne = self.metaData[1]
        self.data = self.metaData[2]
        self.doubleListsOfClassResults = []
        self.buildDLOCR()
        self.veryBig = 10 ** (100)
        self.verySmall = 10 ** (-100)
        self.normalizer = []

    def buildDLOCR(self):     # Build doubleListOfClassResults
        c = 0
        while c < len(self.listClassParameters):
            listsOfClassResults = [0 for i in range(self.nText)]
            self.doubleListsOfClassResults.append(listsOfClassResults)
            c = c + 1

    def buildNormalizer(self):
        d = 0
        while d < self.nText:
            classNormalizer = [0 for i in range(len(self.listOfCategories))]
            self.normalizer.append(classNormalizer)
            d = d + 1

    def fastMultinomial(self):
        self.buildNormalizer()
        c = 0
        while c < len(self.listClassParameters):
            etaC = self.listClassParameters[c].getValue()
            prod = etaC
            i = 0
            while i < len(self.righe):
                if self.righe[i] == 0 or self.righe[i] == self.righe[i - 1]:  # primo documento or nuovo documento
                    time = self.data[i]
                    wordValueGivenClass = self.listWordParameters[self.colonne[i]].getMultinomialValue(c)
                    prod = prod * (wordValueGivenClass ** time)
                    if prod < self.verySmall:
                        prod = prod * self.veryBig
                        self.normalizer[self.righe[i]][c] = self.normalizer[self.righe[i]][c] + 1
                else:
                    self.doubleListsOfClassResults[c][self.righe[i - 1]] = prod
                    # prima parola nuovo documento
                    time = self.data[i]
                    wordValueGivenClass = self.listWordParameters[self.colonne[i]].getMultinomialValue(c)
                    prod = etaC * (wordValueGivenClass ** time)
                i = i + 1
            c = c + 1

        print('Documenti analizzati.')
        print('Normalizzo i risultati')
        self.normalizeResults()
        print('Risultati Classificazione Multinomiale:')
        self.classifyDocuments()

    def normalizeResults(self):
        doc = 0
        while doc < len(self.normalizer):
            max = self.findMax(self.normalizer[doc])
            i = 0
            while i < len(self.normalizer[doc]):
                if max > self.normalizer[doc][i]:
                    times = max - self.normalizer[doc][i]
                    while times > 0:
                        self.doubleListsOfClassResults[i][doc] = self.doubleListsOfClassResults[i][doc] * (self.veryBig)
                        times = times - 1
                i = i + 1
            doc = doc + 1

    def findMax(self, doc):
        tpr = - 1
        i = 0
        while i < len(doc):
            if doc[i] > tpr:
                tpr = doc[i]
            i = i + 1
        return tpr

    def classifyDocuments(self):
        document = 0
        while document < self.nText:
            classe = 0
            tprResult = -1
            while classe < len(self.listClassParameters):
                if self.doubleListsOfClassResults[classe][document] > tprResult:
                    tprResult = self.doubleListsOfClassResults[classe][document]
                    classIndex = classe
                classe = classe + 1
            self.risultati.append(classIndex)
            document = document + 1
        self.percentageOfRightness()

    def fastBernoulli(self):
        self.buildNormalizer()
        LToW = self.trainer.getLToW()
        classi = self.listClassParameters

        c = 0
        while c < len(self.listClassParameters):
            ltow = LToW[c].copy()
            etaC = classi[c].getValue()
            den = 2 + classi[c].nOfExample  # denominatore del parametro delle parole, uguale per ogni parola data la classe
            prod = etaC
            i = 0
            while i < len(self.righe):
                if self.righe[i] == 0 or self.righe[i] == self.righe[i - 1]:  # stesso documento
                    tow = self.listWordParameters[self.colonne[i]].timeOfWord[c]
                    nWordTOW = ltow[tow] - 1
                    ltow.update({tow: nWordTOW})
                    wordValueGivenClass = self.listWordParameters[self.colonne[i]].getBinomialValue(c)
                    prod = prod * wordValueGivenClass
                    if prod < self.verySmall:
                        prod = prod * self.veryBig
                        self.normalizer[self.righe[i]][c] = self.normalizer[self.righe[i]][c] + 1
                else:
                    for j in ltow:
                        if ltow[j] != 0:
                            valueOfMissingWordsGivenClass = 1 - (j / den)
                            prod = prod * (valueOfMissingWordsGivenClass ** (ltow[j]))
                    self.doubleListsOfClassResults[c][self.righe[i - 1]] = prod

                    # prima parola nuovo documento
                    ltow = LToW[c].copy()
                    tow = self.listWordParameters[self.colonne[i]].timeOfWord[c]
                    wordValueGivenClass = self.listWordParameters[self.colonne[i]].getBinomialValue(c)
                    prod = wordValueGivenClass * etaC
                    ltow[tow] = ltow[tow] - 1
                i = i + 1
            c = c + 1

        print("\n")
        print('Documenti analizzati.')
        print('Normalizzo i risultati')
        self.normalizeResults()
        print('Risultati Classificazione Binomiale:')
        self.classifyDocuments()

    def percentageOfRightness(self):
        i = 0
        a = 0
        while i < len(self.risultati):
            if self.risultati[i] == self.categoriesOfDocs[i]:
                a = a + 1
            i = i + 1
        print('Classificazioni esatte: ', "%.2f" % (a / len(self.risultati)))
        print()
        self.contingencyMatrix()

    def contingencyMatrix(self):
        listsOfStatistics = []
        for t in self.listOfCategories:
            statistics = [0, 0, 0]  # Precision, Recall, f1-Score
            listsOfStatistics.append(statistics)

        mat = np.zeros((len(self.listOfCategories), len(self.listOfCategories)), dtype=np.int16)
        i = 0
        while i < len(self.risultati):
            if self.risultati[i] == self.categoriesOfDocs[i]:
                j = self.risultati[i]
                mat[j, j] = mat[j, j] + 1
            else:
                righe = self.categoriesOfDocs[i]
                colonne = self.risultati[i]
                mat[righe, colonne] = mat[righe, colonne] + 1
            i = i + 1

        documentsInCol = [0 for i in self.listOfCategories]
        documentsInRoW = [0 for i in self.listOfCategories]
        print(
            'Contingency matrix:  (Su ogni riga troviamo il numero di documenti della stessa classe realmente esistenti)',
            "\n")
        for i in range(len(self.listOfCategories)):
            tprDocumentsInRoW = 0
            for j in range(len(self.listOfCategories)):
                tprDocumentsInRoW = tprDocumentsInRoW + mat[i, j]
                documentsInCol[j] = documentsInCol[j] + mat[i, j]
                print('{:<5}'.format(mat[i, j]), end='')
            print()
            documentsInRoW[i] = tprDocumentsInRoW
            listsOfStatistics[i][1] = mat[i, i] / documentsInRoW[i]  # Recall
        print()

        p = 0
        while p < len(documentsInCol):
            listsOfStatistics[p][0] = mat[p, p] / documentsInCol[p]  # Precision
            listsOfStatistics[p][2] = 2 * (listsOfStatistics[p][0] * listsOfStatistics[p][1]) / (
                    listsOfStatistics[p][0] + listsOfStatistics[p][1])
            p = p + 1

        macroPrecisionAvg = 0
        macroRecallAvg = 0
        macroF1ScoreAvg = 0
        p = 0
        while p < len(documentsInCol):
            macroPrecisionAvg = macroPrecisionAvg + listsOfStatistics[p][0] * documentsInRoW[p]
            macroRecallAvg = macroRecallAvg + listsOfStatistics[p][1] * documentsInRoW[p]
            macroF1ScoreAvg = macroF1ScoreAvg + listsOfStatistics[p][2] * documentsInRoW[p]
            p = p + 1
        macroPrecisionAvg = macroPrecisionAvg / (len(self.listOfTestDocuments))
        macroRecallAvg = macroRecallAvg / (len(self.listOfTestDocuments))
        macroF1ScoreAvg = macroF1ScoreAvg / (len(self.listOfTestDocuments))

        index = 0
        while index < len(self.listOfCategories):
            print('{:<25}'.format(self.listOfCategories[index]),
                  '  Precision: ', "%.3f" % (listsOfStatistics[index][0]),
                  '  Recall: ', "%.3f" % (listsOfStatistics[index][1]),
                  '  F1-Score: ', "%.3f" % (listsOfStatistics[index][2]))
            index = index + 1
        print()
        print('{:<23}'.format('Macro-Precision avg: '), "%.3f" % macroPrecisionAvg)
        print('{:<23}'.format('Macro-Recall avg: '), "%.3f" % macroRecallAvg)
        print('{:<23}'.format('Macro-F1Score avg: '), "%.3f" % macroF1ScoreAvg)
        print("\n", "\n")
