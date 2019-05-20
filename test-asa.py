# arabic-sentiment-analysis does not have a module's setup.py or __init__.py
# needed a workaround to import code from subdirectory
# StackOverflow source https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory
import sys
sys.path.insert(0, './arabic-sentiment-analysis')

import os

text_data = list()
#for body in tweets:
#    text_data.append(body)

# Bayesian doesn't do what I want here
# from nltk import NaiveBayesClassifier
# from sa_nltk import do_sa as nltk_alone
# ngrams = (1, 2, 3)
# for n in ngrams:
#     do_sa(n, NaiveBayesClassifier)

from sa_sklearn import do_sa as sklearn_alone
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

ngrams = (1, 2, 3)
classifiers = [LinearSVC(), SVC(), MultinomialNB(),
               BernoulliNB(), SGDClassifier(), DecisionTreeClassifier(max_depth=5),
               RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
               KNeighborsClassifier(3)
               ]
for alg in classifiers:
    alg_name = alg.__class__.__name__
    for g in ngrams:
        pipeline = sklearn_alone(g, alg)
        pipeline.predict(text_data)
        # ideally you have multiple tweets and calculate them here
        # each algo returns an array of 'pos' and 'neg'
