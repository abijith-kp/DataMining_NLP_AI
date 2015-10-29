from nltk import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

from collections import Counter
import string
import unicodedata

def load_dataset():
    data_file = "/path/to/dataset/Sentiment_Analysis_Dataset.csv"
    f = open(data_file)
    content = f.readlines()
    f.close()
    content = content[1:]
    X = []
    Y = []
    for c in content:
        t = c.split(",")
        X.append(t[3])
        Y.append(int(t[1]))
    return (X, Y)


def create_classifier():
    print "Creating dataset"
    dataset = load_dataset()
    X_train, Y_train = dataset
    classifier = Sentiment()
    classifier.fit(X_train, Y_train)
    print "Dataset creation sucessful"
    return classifier


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
        n = 4000
        print "Fitting ", n, " samples..."
        words = [word_tokenize(unicodedata.normalize('NFKD', x.decode("utf-8")).encode('ascii','ignore'))     for x in X[:n]]
        processed_words = [" ".join(w    for w in s    if w not in self.stop_words)    for s in words]
        X_train = self.tfid.fit_transform(processed_words)
        Y_train = Y[:n]
        print "Classifier created"
        self.clf.fit(X_train, Y_train)

    def predict(self, X_inp):
        X_inp = unicodedata.normalize('NFKD', X_inp.decode("utf-8")).encode('ascii','ignore')
        word_list = " ".join(w    for w in word_tokenize(X_inp.lower())    if w not in self.stop_words)
        X_test = self.tfid.transform([word_list])
        return self.clf.predict(X_test)
