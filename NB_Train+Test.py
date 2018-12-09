from sklearn.feature_extraction.text import *
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import numpy
import matplotlib.pyplot as plt
from sklearn import svm
import json
import pprint
import csv

train_set = csv.reader(open('Sentiment140_train.csv', 'rt',encoding='latin-1'), delimiter=",", quotechar='|')
train_score, train_text = [], []
test_score, test_text = [], []

for line in train_set:
	tmp_score = line[0].strip('\"')

	if int(tmp_score) < 2:
		#negative
		train_score.append(0)
		train_text.append(line[5])

	elif int(tmp_score) > 2:
		#positive
		train_score.append(1)
		train_text.append(line[5])
	else:
		continue



text_clf = Pipeline([('vect', CountVectorizer()),
					 ('tfidf', TfidfTransformer()),
					 ('clf', MultinomialNB())])
text_clf.fit(train_text, train_score)

test_set = csv.reader(open('Sentiment140_test.csv', 'rt',encoding='latin-1'), delimiter=",", quotechar='|')
for line in test_set:
	tmp_score = line[0].strip('\"')

	if int(tmp_score) < 2:
		#negative
		test_score.append(0)
		test_text.append(line[5])

	elif int(tmp_score) > 2:
		#positive
		test_score.append(1)
		test_text.append(line[5])
	else:
		continue

predicted = text_clf.predict(test_text)


difference = 0
length = 0
for i in range(0,len(predicted)-1):
	
	if predicted[i] != test_score[i]:
		difference = difference + 1

length = len(test_score)
print(difference/length)
print(difference)
print(length)
