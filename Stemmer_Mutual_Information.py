from os import listdir
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from operator import itemgetter
import math


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

    def loadDocumentsAndBuildDictionary(self, listOfCategories, documents, dictionary, maxWord):
        P = [[] for i in listOfCategories]
        totaloccurrences = [0]
        print("Inizio a caricare i documenti")
        for docs in documents:
            path = docs.path
            tipo = docs.tipo
            tprColonne = []
            righe = []
            colonne = []
            data = []
            categoryIndex = 0
            for category in listOfCategories:
                categoryPath = path + "/" + category
                for file in listdir(categoryPath):
                    filePath = categoryPath + "/" + file
                    with open(filePath, encoding="utf8", errors='ignore') as fip:
                        colonnePerDoc = {}
                        doc = ""
                        for line in fip:
                            stemmedLine = self.stemSentenceAndCounting(line, dictionary, colonnePerDoc, tipo, P,
                                                                       categoryIndex, totaloccurrences)
                            doc = doc + stemmedLine
                        tprColonne.append(colonnePerDoc)
                        docs.listOfDocuments.append(doc)
                        docs.categorieOfDocuments.append(categoryIndex)
                categoryIndex = categoryIndex + 1
            print(len(docs.listOfDocuments), "Documenti Caricati")
            docIndex = 0
            for dic in tprColonne:
                for keys in dic.keys():
                    righe.append(docIndex)  # documento della parola
                    colonne.append(keys)    # Id della parola
                    data.append(dic[keys])  # Occorrenza della parola
                docIndex = docIndex + 1
            metaData = [righe, colonne, data]
            docs.metaData = metaData

        smallDictionary = self.mutualInformation(dictionary, P, totaloccurrences, maxWord)
        print(len(dictionary), 'parole nel dizionario completo')
        print(len(smallDictionary), 'parole nel dizionario piccolo')
        for docs in documents:
            if len(smallDictionary) < len(dictionary):
                self.resizeMetaData(docs, smallDictionary)
            else:
                docs.setDictionary(dictionary)

    def stemSentenceAndCounting(self, sentence, dictionary, colonnePerDoc, tipo, P, categoryIndex, totaloccurrences):
        tokenWords = word_tokenize(sentence)
        stemSentence = []
        for word in tokenWords:
            word = word.lower()
            if word.isalpha() and len(word) > 2 and word not in self.stopwords:
                stemmedWord = self.porter.stem(word)
                stemSentence.append(stemmedWord)
                stemSentence.append(" ")
                if tipo == 'train':
                    totaloccurrences[0] = totaloccurrences[0] + 1
                    if stemmedWord not in dictionary.keys():
                        dictionary.update({stemmedWord: len(dictionary)})
                        i = 0
                        while i < len(P):
                            P[i].append(1)
                            i = i + 1
                        P[categoryIndex][len(P[categoryIndex]) - 1] = 2
                    else:
                        indexWord = dictionary[stemmedWord]
                        P[categoryIndex][indexWord] = P[categoryIndex][indexWord] + 1
                    self.countWord(stemmedWord, dictionary, colonnePerDoc)
                else:
                    if stemmedWord in dictionary.keys():
                        self.countWord(stemmedWord, dictionary, colonnePerDoc)
            elif word.isdigit():  # sostituisco tutti i numeri con "0", mi interessa solo quanti numeri ci sono in un documento
                stemSentence.append("0")
                stemSentence.append(" ")
                if tipo == 'train':
                    if '0' not in dictionary.keys():
                        totaloccurrences[0] = totaloccurrences[0] + 1
                        dictionary.update({'0': len(dictionary)})
                        i = 0
                        while i < len(P):
                            P[i].append(1)     # evitiamo moltiplicazioni e divisioni per 0
                            i = i + 1
                        P[categoryIndex][len(P[categoryIndex]) - 1] = 2
                    else:
                        indexWord = dictionary['0']
                        P[categoryIndex][indexWord] = P[categoryIndex][indexWord] + 1
                    self.countZero(dictionary, colonnePerDoc)
                else:
                    if '0' in dictionary.keys():
                        self.countWord('0', dictionary, colonnePerDoc)
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

    def mutualInformation(self, dictionary, P, totaloccurrences, maxWord):
        if maxWord != 0 and maxWord < len(dictionary):
            TO = totaloccurrences[0]
            Pc = [0 for i in range(len(P))]     # occorrenze di parole in C tra tutti i documenti
            Pw = [0 for i in range(len(P[0]))]  # occorrenze di parola w tra tutti i documenti
            c = 0
            while c < len(Pc):
                w = 0
                while w < len(Pw):
                    times_w_in_c = P[c][w]
                    Pw[w] = Pw[w] + times_w_in_c
                    Pc[c] = Pc[c] + times_w_in_c
                    w = w + 1
                c = c + 1
            I = [0 for i in range(len(Pw))]
            dictio = []
            w = 0
            while w < len(I):
                c = 0
                while c < len(Pc):
                    probcw = P[c][w] / TO
                    probc = Pc[c] / TO
                    probw = Pw[w] / TO
                    I[w] = I[w] + (probcw * math.log10(probcw / (probc * probw)))
                    c = c + 1
                w = w + 1
            for i in range(len(I)):
                dictio.append((i, I[i]))
            tupleOrdered = list(sorted(dictio, key=itemgetter(1, 0), reverse=True))
            smallDictionary = {}
            i = 0
            while i < maxWord:
                smallDictionary.update(
                    {tupleOrdered[i][0]: 'dummyValue'})  # I[key] == indexWord del dizionario originale
                i = i + 1
            return smallDictionary
        else:
            return dictionary

    def resizeMetaData(self, doc, smallDictionary):
        metaData = doc.metaData
        oldRighe = metaData[0]
        oldColonne = metaData[1]
        oldData = metaData[2]
        newRighe = []
        newColonne = []
        newData = []
        i = 0
        while i < len(oldRighe):
            if oldColonne[i] in smallDictionary.keys():
                newRighe.append(oldRighe[i])
                newColonne.append(oldColonne[i])
                newData.append(oldData[i])
            i = i + 1
        normalizedSmallDictionary = {}
        keys = list(smallDictionary.keys())
        w = 0
        while w < len(keys):
            normalizedSmallDictionary.update({w: 'dummyValue'})
            w = w + 1
        normalizedNewColonne = []
        val_list = keys
        for wordIndex in newColonne:
            normalizedNewColonne.append(val_list.index(wordIndex))     # Adesso buildWordParameters funziona anche con un dizionario ridotto
        doc.metaData[0] = newRighe
        doc.metaData[1] = normalizedNewColonne
        doc.metaData[2] = newData
        doc.setDictionary(normalizedSmallDictionary)
