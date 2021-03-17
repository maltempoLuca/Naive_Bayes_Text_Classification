class Documents:

    def __init__(self, tipo, path):
        self.tipo = tipo
        self.path = path
        self.listOfDocuments = []
        self.categorieOfDocuments = []
        self.metaData = []    # Righe, Colonne, Data e Dizionario. Guardare in Stemmer.

    def setDictionary(self, dictionary):
        self.metaData.append(dictionary)
