from nltk import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

from collections import Counter
import string

class Sentiment:
    def __init__(self):
        self.stop_words = stopwords.words() + list(string.punctuation)
        self.tfid = TfidfVectorizer()
        self.clf = MultinomialNB()

        # score: 0.7225
        # self.clf = SVC()

    # create pipelines
    # clean the input
    def fit(self, X, Y):
        self.X = X
        self.Y = Y
        # give the subset of dataset to be trained
        l = 0
        h = 4000
        words = [word_tokenize(x.decode("utf-8").lower())    for x in X[l:h]]
        processed_words = [" ".join(w    for w in s    if w not in self.stop_words)    for s in words]
        X_train = self.tfid.fit_transform(processed_words)
        Y_train = Y[l:h]
        self.clf.fit(X_train, Y_train)
        print "Classes: ", self.clf.classes_
        print "Score: ", self.clf.score(X_train, Y_train)

    def predict(self, X_inp):
        word_list = " ".join(w    for w in word_tokenize(X_inp.decode("utf-8").lower())    if w not in self.stop_words)
        X_test = self.tfid.transform([word_list])
        return self.clf.predict(X_test)
