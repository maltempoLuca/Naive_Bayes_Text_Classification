class ClassParameter:

    def __init__(self, classIndex, nCategories, nDocuments):
        self.classIndex = classIndex
        self.nOfExample = 1          # Laplace smoothing
        self.nOfClasses = nCategories
        self.nEsempi = nDocuments

    def getValue(self):
        return self.nOfExample / (self.nOfClasses + self.nEsempi)


class WordParameter:

    def __init__(self, classi):
        self.classi = classi.copy()
        self.timeOfWord = [1 for i in range(len(classi))]
        self.multinomialDenominator = [0 for i in range(len(classi))]

    def incTimeOfWordBin(self, typeOfClass):
        self.timeOfWord[typeOfClass] = self.timeOfWord[typeOfClass] + 1

    def incTimeOfWordMul(self, times, typeOfClass):
        self.timeOfWord[typeOfClass] = self.timeOfWord[typeOfClass] + times

    def getBinomialValue(self, typeOfClass):
        num = self.timeOfWord[typeOfClass]
        den = (2 + self.classi[typeOfClass].nOfExample)
        return num / den

    def getMultinomialValue(self, typeOfClass):
        num = self.timeOfWord[typeOfClass]
        den = self.multinomialDenominator[typeOfClass]
        return num / den
