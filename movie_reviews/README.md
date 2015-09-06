Sentiment analysis on movie reviews
===================================

This is a sample sentiment analysis done using sklearn python library with the
help of dataset obtained from [here](http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz)

How to run the program
======================

    * Download compressed dataset from [here](http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz)

    * Untar the file aclImdb_v1.tar.gz

    * The arguement for the IMDB_DS class will be the folder in which the
      datasets are present. Refer the movie_review.py file

    * Issue the command "python movie_reviews.py 1"

    * if arguement is 0 GridSearchCV will be used to get optimal parameters for
      the classification. Else a pre calculated value will be used.
