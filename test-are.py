# ar-embeddings does not have a module's setup.py or __init__.py
# needed a workaround to import code from subdirectory
# StackOverflow source https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory
import sys
sys.path.insert(0, './ar-embeddings')

# pip3 install psycopg2
import psycopg2
conn = psycopg2.connect("dbname='tweetreplies'")
cursor = conn.cursor()
cursor.execute("SELECT originid, tweetid, body \
    FROM combined \
    WHERE screenname != 'NetflixMENA' \
    ORDER BY originid DESC")
knownTweets = {}
tweetsByOrigin = {}
currentOrigin = None
for tweet in cursor.fetchall():
    origin = str(tweet[0])
    id = tweet[1]
    body = tweet[2]

    if origin not in tweetsByOrigin:
        tweetsByOrigin[origin] = []
    tweetsByOrigin[origin].append(body)

import json
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
originEvals = []
for c in classifiers:
    learner.classify(c, False, False)
    scoresByOrigin = {}
    for origin in tweetsByOrigin.keys():
        scoresByOrigin[origin] = { 'positive': 0, 'negative': 0 }
        tokenized = learner.tokenize_data(tweetsByOrigin[origin], 'experiment')
        normalized = learner.average_feature_vectors(tokenized, 'experiment')
        nanless = learner.remove_nan(normalized)
        predictions = c.predict(nanless)
        # negative = 0, positive = 1
        for item in predictions:
            if item == 0:
                scoresByOrigin[origin]['negative'] += 1
            else:
                scoresByOrigin[origin]['positive'] += 1
    originEvals.append(scoresByOrigin)
oeout = open('./are-tweet-results.json', 'w')
oeout.write(json.dumps(originEvals))
