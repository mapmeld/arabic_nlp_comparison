# ar-embeddings does not have a module's setup.py or __init__.py
# needed a workaround to import code from subdirectory
# StackOverflow source https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory
import sys
sys.path.insert(0, './ar-embeddings')

from asa import ArSentiment
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegressionCV
from sklearn.svm import LinearSVC, NuSVC
from sklearn.naive_bayes import GaussianNB

embeddings_path = "./ar-embeddings/embeddings/arabic-news.bin"
dataset_path = "./ar-embeddings/datasets/mpqa-ar.csv"
learner = ArSentiment(embeddings_path, dataset_path, plot_roc=False)

# classifiers to use
classifiers = [
    RandomForestClassifier(n_estimators=100),
    SGDClassifier(loss='log', penalty='l1'),
    LinearSVC(C=1e1),
    NuSVC(),
    LogisticRegressionCV(solver='liblinear'),
    GaussianNB(),
]
for c in classifiers:
    learner.classify(c, False, False)
    #predictions = c.predict(text_data)
