# Struttura del Programma

Il programma è strutturato in 6 diversi file:

- main.py
- Documents.py
- Stemmer_Mutual_Information.py
- Parameter.py
- Training.py
- Classifier.py

Il Dataset è suddiviso in due diverse cartelle:

- 20-news-bydate-test
- 20-news-bydate-train

# Come riprodurre i risultati

Per riprodurrei risultati sarà sufficiente scaricare i sei diversi file .py e i due Datasets, inserire il tutto nella stessa cartella, aprire il file main.py ed eseguire il programma. Il Dataset può anche essere scaricato dal seguente link: http://qwone.com/~jason/20Newsgroups/. Tra i diversi Datasets scaricare il secondo ,"bydate", che è già suddiviso in documenti di Test e documenti di Training. Una volta scaricato il Dataset basterà estrarlo ed inserire le due cartelle Train e Test nella stessa cartella del file main.py. A questo punto si potrà semplicemente eseguire il main e attendere la classificazione di tutti i documenti. Si può scegliere la dimensione massima del dizionario cambiando l'iperparametro 'dictionarySize' nel main. Consiglio comunque di lasciare il valore preimpostato poichè dopo diverse prove si è dimostrato essere il migliore per entrambe le tipologie di classificazione.

# Funzionamento del programma

All'interno del le main.py sarà possibile scegliere la dimensione massima del dizionario e su quali categorie effettuare training e classificazione. A questo punto vengono creati due oggetti che contengono i documenti di Test e quelli di Training. Attraverso lo stemmer definito in Stemmer_Mutual_Information.py carichiamo i vari documenti, li analizziamo e creiamo un dizionario con le parole più rilevanti sfruttando la mutua informazione tra classi. Possiamo quindi effettuare il training. Andiamo a creare e calcolare tutti i parametri necessari per la classificazione, prima secondo il modello di Bernoulli, che non tiene conto dell'occorrenza delle parole, poi secondo il modello Multinomiale. Infine vengono inizializzati due diversi classificatori che procederanno a classificare tutti i documenti di Test che sono stati caricati. Finita la classificazione vedremo in output le matrici di contingenza sia per il modello di Bernoulli che per quello Multinomiale. Un'analisi più  dettagliata sul funzionamento del programma è presente nel PDF.

# Fonti

Il codice Python è stato prodotto grazie a varie spiegazioni trovate sulla rete, tra queste le più utili provengono da queste fonti:

- <https://stackoverflow.com/>
- <https://www.datacamp.com/community/tutorials/stemming-lemmatization-python>
- <https://www.datacamp.com/community/tutorials/reading-writing-files-python>

Cercando soluzioni ai diversi problemi incontrati durante la scrittura del codice mi sono imbattuto in questa repository:

https://github.com/gokriznastic/20-newsgroups_text-classification . 

Non ho ripreso parti di codice però mi sembrava corretto citare questa fonte visto che leggendola ho capito come poter caricare i documenti del Dataset senza avvalermi di scikit-learn.
