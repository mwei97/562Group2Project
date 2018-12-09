import nltk
import json
import csv

from nltk.sentiment.vader import SentimentIntensityAnalyzer 

nltk.downloader.download('vader_lexicon')

test_text = []
test_score = []
test_file = open("Customized_test.txt", "r", encoding="utf-8")

for entry in test_file:
	entryDict = json.loads(entry)
	tweet_text = entryDict["tweet_text"]
	test_text.append(tweet_text.replace('\r\n', '').replace('\n', ''))


sid = SentimentIntensityAnalyzer()

pred = []
for sentence in test_text:
     ss = sid.polarity_scores(sentence)
     if (ss['compound'] < 0.0):
     	pred.append(-1)
     elif (ss['compound'] > 0.0):
     	pred.append(1)
     else:
     	pred.append(0)

print(len(pred))

test_score = []
file_score = csv.reader(open('Customized_label.csv', 'rt'), delimiter=",", quotechar='|')
for row in file_score:
	test_score = row

difference = 0
for i in range(0,len(pred)-1):
	if pred[i] != int(test_score[i]):
		difference = difference+1

print(difference)
print(difference/len(pred))