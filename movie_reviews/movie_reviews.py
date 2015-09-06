from IMDB_DS import IMDB_DS
from utils import AddRating, get_pipeline

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedKFold

import sys
import numpy as np

if __name__ == "__main__":
    print "Starting the Program"

    TESTING = True
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "[0|1]"
        print "0 ==> Testing false"
        print "1 ==> Testing true"
        sys.exit(1)
    else:
        TESTING = True if sys.argv[1] == "1" else False

    # Loading datasets
    imdb = IMDB_DS("../aclImdb/train/")
    pos_train, neg_train = imdb.pos(), imdb.neg()
    print "Loading training set"
    
    imdb = IMDB_DS("../aclImdb/test/")
    pos_test, neg_test = imdb.pos(), imdb.neg()
    print "Loading testing set"

    l_train = len(pos_train)
    l_test = len(pos_test)
    # Preprocessing the datasets for our use
    X_train = [r[0] + " rate_" + r[1]    for r in pos_train + neg_train]
    Y_train = [1]*l_train + [0]*l_train
    print "Created traing set"
    X_test = [r[0] + " rate_" + r[1]    for r in pos_test + neg_test]
    Y_test = [1]*l_test + [0]*l_test
    print "Created testing set"

    tdf = TfidfVectorizer()
    mnb = MultinomialNB()

    estimators_1 = [("tdf", tdf), ("mnb", mnb)]
    p_tdf_mnb = get_pipeline(estimators_1)
    print "Created Pipeline: " + str(p_tdf_mnb)

    best_params = {}

    if TESTING:
        print "Testing..."
        print "Setting best_params as pre calculated value"
        best_params = {'tdf__stop_words': ENGLISH_STOP_WORDS,
                       'tdf__use_idf': False,
                       'tdf__sublinear_tf': True,
                       'tdf__smooth_idf': True }
    else:
        # Creating a Grid Search to identify the best params for classification
        print "Finding Best params using GridSearchCV"
        parameter_grid = {'tdf__smooth_idf': [True, False],
                        'tdf__sublinear_tf': [True, False],
                        'tdf__stop_words': [ENGLISH_STOP_WORDS, None],
                        'tdf__sublinear_tf': [True, False],
                        'tdf__use_idf': [True, False],
                        # 'tdf__ngram_range': [(1, 1), (1, 2), (1, 3)],
                        }

        cross_validation = StratifiedKFold(Y_train, n_folds=10)
        grid_search = GridSearchCV(p_tdf_mnb,
                                param_grid=parameter_grid,
                                cv=cross_validation, n_jobs=-1, verbose=5)

        grid_search.fit(X_train, Y_train)
        best_params = grid_search.best_params_
        print "Best score:", grid_search.best_score_
        print "Best parameters:", grid_search.best_params_

    # Providing the Pipeline with the identified params
    p_tdf_mnb.set_params(**best_params)

    # Shuffling and splitting the dataset for training and testing
    R = X_test + X_train
    Y = Y_test + Y_train

    print "Testing the correctness of the model"
    # testing the model
    scores = []
    for i in range(10):
        print "Round", i+1 
        X_train, X_test, Y_train, Y_test = train_test_split(R, Y, test_size=0.33)
        p_tdf_mnb.fit(X_train, Y_train)
        cv_scores = cross_val_score(p_tdf_mnb, X_test, Y_test, cv=10)
        print 'Average score: ', np.mean(cv_scores)
        print "Scores: ", cv_scores
        scores.append(np.mean(cv_scores))

    print "Scores for the last 10 runs:", scores
