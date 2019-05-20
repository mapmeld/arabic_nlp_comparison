# arabic-sentiment-analysis does not have a module's setup.py or __init__.py
# needed a workaround to import code from subdirectory
# StackOverflow source https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory
import sys
sys.path.insert(0, './arabic-sentiment-analysis')

text_data = list()
for body in tweets:
    text_data.append(body)

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
        sklearn_alone(g, alg)
        pipeline = Pipeline([
            ('vect', TfidfVectorizer(min_df=5, max_df=0.95,
                                     analyzer='word', lowercase=False,
                                     ngram_range=(1, n))),
            ('clf', alg),
        ])
        pipeline.predict(text_data)


from sa_nltk_sklearn import do_sa as combined_sa
ngrams = (1, 2, 3)
algorithms = [LinearSVC(), SVC(), MultinomialNB(), BernoulliNB(), SGDClassifier()]
for alg in algorithms:
    alg_name = alg.__class__.__name__
    for n in ngrams:
        classifier = SklearnClassifier(alg)
        combined_sa(n, classifier, alg_name)
        # algo is now fit to data
        predicted = classifier.classify(text_data)
