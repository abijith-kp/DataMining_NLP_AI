from pandas import DataFrame
from sklearn.pipeline import Pipeline
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

import string
import numpy as np

def token_stem_sent(sent):
    snb = SnowballStemmer("english")
    punct = string.punctuation
    result = [snb.stem(s)    for s in word_tokenize(sent.decode("utf8"))   if s not in punct]
    return " ".join(result)

class AddRating(object):
    def __init__(self, rating):
        self.rating = rating

    def transform(self, X):
        X_array = X.toarray()
        for x, r in zip(X_array, self.rating):
            x.append(r)
        return np.array(X_array)

    def fit(self, X, y=None):
        return self

def np2df(X):
    y = X.shape[1]
    x = []
    if str(type(X)) == "<class 'scipy.sparse.csr.csr_matrix'>":
        x = X.toarray()
    elif str(type(X)) == "<type 'numpy.ndarray'>":
        x = X
    else:
        return "TYPE ERROR"
    return DataFrame(x)

def get_pipeline(list_esimators):
    return Pipeline(list_esimators)
