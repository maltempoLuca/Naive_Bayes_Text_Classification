from Classifier import Classifier
from Documents import Documents
from Stemmer import Stemmer
from Training import Training


stemmer = Stemmer()
generalPath = '20news-bydate-'
trainPath = generalPath + 'train'
testPath = generalPath + 'test'

listOfCategories = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
              'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos', 'rec.motorcycles',
              'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med',
              'sci.space', 'soc.religion.christian', 'talk.politics.guns', 'talk.politics.mideast',
              'talk.politics.misc', 'talk.religion.misc']

trainingDocs = Documents('train', trainPath)
testDocs = Documents('test', testPath)

documents = [trainingDocs, testDocs]

dictionary = {}

stemmer.loadDocumentsAndBuildDictionary(listOfCategories, documents, dictionary)

trainerBernoulli = Training(listOfCategories, documents[0])
trainerMultinomiale = Training(listOfCategories, documents[0])

trainerBernoulli.binomialTraining()
trainerMultinomiale.multinomialTraining()

print('Inizio Classificazione di', len(documents[1].listOfDocuments), 'documenti.')

classificatoreBernoulli = Classifier(documents[1], trainerBernoulli)
classificatoreMultinomiale = Classifier(documents[1], trainerMultinomiale)

classificatoreBernoulli.fastBernoulli()
classificatoreMultinomiale.fastMultinomial()
