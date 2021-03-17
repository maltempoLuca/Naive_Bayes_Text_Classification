from os import listdir
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


class Stemmer:
    def __init__(self):
        self.porter = PorterStemmer()
        self.stopwords = self.createMyStopword()

    def createMyStopword(self):
        stops = set(stopwords.words('english'))
        stopword = set()
        for w in stops:
            if len(w) > 2:
                stopword.add(w)
        print('Ho scelto le Stopwords')
        return stopword

    def loadDocumentsAndBuildDictionary(self, listOfCategories, documents, dictionary):
        print("Inizio a caricare i documenti")
        for docs in documents:
            path = docs.path
            tipo = docs.tipo
            tprColonne = []
            righe = []    # Per ogni parola letta viene inserito il documento a cui appartiene la parola nella lista
            colonne = []  # Per ogni parola letta viene inserito l' ID della parola  nella lista
            data = []     # Per ogni parola letta si inserisce la sua occorrenza nella  lista, occorrenza == quante volte troviamo la parola i in doc j
            categoryIndex = 0
            for category in listOfCategories:
                categoryPath = path + "/" + category
                for file in listdir(categoryPath):
                    filePath = categoryPath + "/" + file
                    with open(filePath, encoding="utf8", errors='ignore') as fip:
                        colonnePerDoc = {}  # Contiene per ogni parola (key==ID) letta la sua occorrenza nel documento aperto
                        doc = ""
                        for line in fip:
                            stemmedLine = self.stemSentenceAndCounting(line, dictionary, colonnePerDoc, tipo)
                            doc = doc + stemmedLine
                        tprColonne.append(colonnePerDoc)  # Lista di dizionari, uno per ogni documento, il dizionario associa ad un ID la sua occorrenza.
                        docs.listOfDocuments.append(doc)
                        docs.categorieOfDocuments.append(categoryIndex)
                categoryIndex = categoryIndex + 1
            print(len(docs.listOfDocuments), "Documenti Caricati")
            docIndex = 0
            for dic in tprColonne:
                for keys in dic.keys():
                    righe.append(docIndex)   # documento della parola
                    colonne.append(keys)     # Id della parola
                    data.append(dic[keys])   # Occorrenza della parola
                docIndex = docIndex + 1
            metaData = [righe, colonne, data]
            docs.metaData = metaData

        for docs in documents:
            docs.setDictionary(dictionary)
        print(len(dictionary), ' Parole nel dizionario.')
        print()

    def stemSentenceAndCounting(self, sentence, dictionary, colonnePerDoc, tipo):
        tokenWords = word_tokenize(sentence)
        stemSentence = []
        for word in tokenWords:
            word = word.lower()
            if word.isalpha() and len(word) > 2 and word not in self.stopwords:
                stemmedWord = self.porter.stem(word)
                stemSentence.append(stemmedWord)
                stemSentence.append(" ")
                if tipo == 'train':
                    if stemmedWord not in dictionary.keys():
                        dictionary.update({stemmedWord: len(dictionary)})
                    self.countWord(stemmedWord, dictionary, colonnePerDoc)
                else:
                    if stemmedWord in dictionary.keys():
                        self.countWord(stemmedWord, dictionary, colonnePerDoc)
            elif word.isdigit():  # sostituisco tutti i numeri con "0", mi interessa solo quanti numeri ci sono in un documento
                stemSentence.append("0")
                stemSentence.append(" ")
                if '0' not in dictionary.keys():
                    dictionary.update({'0': len(dictionary)})
                self.countZero(dictionary, colonnePerDoc)
            # ho escluso le parole che contengono sia lettere che numeri, sono quasi sempre errori di battitura.
        return "".join(stemSentence)

    def countWord(self, stemmedWord, dictionary, colonnePerDoc):
        if dictionary[stemmedWord] in colonnePerDoc.keys():
            times = colonnePerDoc[dictionary[stemmedWord]] + 1
            colonnePerDoc.update({dictionary[stemmedWord]: times})
        else:
            colonnePerDoc.update({dictionary[stemmedWord]: 1})

    def countZero(self, dictionary, colonnePerDoc):
        if dictionary['0'] in colonnePerDoc.keys():
            times = colonnePerDoc[dictionary['0']] + 1
            colonnePerDoc.update({dictionary['0']: times})
        else:
            colonnePerDoc.update({dictionary['0']: 1})
