# YouTube-Comments-Analyzer does not have a module's setup.py or __init__.py
# needed a workaround to import code from subdirectory
# StackOverflow source https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory
import os, sys
sys.path.insert(0, './Youtube-Comments-Analyzer')

# include data for positive/negative word analysis
os.system('cp ./Youtube-Comments-Analyzer/pos.txt ./')
os.system('cp ./Youtube-Comments-Analyzer/neg.txt ./')

# import from YouTube-Comments-Analyzer
# this also triggers one-time nltk_data download
from sentiment import find_sentiment

"""
[nltk_data] Downloading package stopwords to
[nltk_data]     path/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
[nltk_data] Downloading package punkt to
[nltk_data]     path/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
"""

# pip3 install psycopg2
import psycopg2
conn = psycopg2.connect("dbname='tweetreplies'")
cursor = conn.cursor()

cursor.execute("SELECT originid, tweetid, body \
    FROM combined \
    WHERE screenname != 'NetflixMENA' \
    ORDER BY originid DESC")
knownTweets = {}
currentOrigin = None
positives = 0
negatives = 0
posSum = 0
negSum = 0

xo = open('yt-tweet-results.csv', 'w')
xo.write('tweetid,pos,neg,posSum,negSum\n')

def processOrigin():
    print('Tweet %s has %d positives and %d negatives adding up to %d + vs %d -' %
        (currentOrigin, positives, negatives, posSum, negSum))
    xo.write(','.join([str(currentOrigin), str(positives), str(negatives), str(posSum), str(negSum)]) + '\n')

for tweet in cursor.fetchall():
    origin = tweet[0]
    id = tweet[1]
    body = tweet[2]

    # unique Tweets plz
    if id in knownTweets or origin is None or id is None or body is None or len(body.strip()) == 1:
        continue
    knownTweets[id] = True

    # any Arabic script letter is OK, expect a mix of scripts in Tweets
    foundArabicScript = False
    for letter in body:
        if '\u0600' <= letter <= '\u06FF':
            foundArabicScript = True
            break

    if origin != currentOrigin:
        if currentOrigin is not None:
            processOrigin()
        currentOrigin = origin
        positives = 0
        negatives = 0
        posSum = 0
        negSum = 0

    if foundArabicScript:
        #print(body)
        try:
            (posScore, negScore) = find_sentiment(body.strip())
            #print(feels)
            posSum += posScore
            negSum += negScore
            if posScore > negScore:
                positives += 1
            elif negScore > posScore:
                negatives += 1
        except:
            print(body)

# get the last Tweet in there
if currentOrigin is not None:
    processOrigin()
