from sklearn.feature_extraction.text import *
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import numpy
import matplotlib.pyplot as plt
from sklearn import svm
import json
import pprint
import csv
import os
import queue

train_set = csv.reader(open('Sentiment140_train.csv', 'rt',encoding='latin-1'), delimiter=",", quotechar='|')
train_score, train_text = [], []
pred_score, pred_text = [], []

dict = {'Jan':'01','Feb':'02', 'Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
output_dict = {}


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

# Have to adjust for company name
base = len('Tesla')

filelist = os.listdir()
for item in filelist:
	if item[-4:] == '.txt':
		year = item[base+1:base+5]
		month = dict[item[base+6:base+9]]
		day = item[base+10:-4]
		date = year+'-'+month+'-'+day
		output_dict[date] = []

		pred_file = open(item, "r", encoding="utf-8")
		pred_text = []
		for entry in pred_file:
			entryDict = json.loads(entry)
			tweet_text = entryDict["tweet_text"]
			pred_text.append(tweet_text.replace('\r\n', '').replace('\n', ''))

		predicted = text_clf.predict(pred_text)

		#firstp entry, number of tweets
		output_dict[date].append(len(predicted))
		#Second entry, daily average score
		output_dict[date].append(sum(predicted)/len(predicted))


counter = 0
average_q = []
for time in sorted(output_dict.keys()):
	if counter < 4:
		output_dict[time].append(output_dict[time][1])
		average_q.append(output_dict[time][1])
	else:
		tmp_average =(output_dict[time][1]+sum(average_q))/5
		output_dict[time].append(tmp_average)		
		average_q.pop(0)
		average_q.append(output_dict[time][1])
	counter = counter +1


with open("output.csv", "w", newline='') as result:
	wr = csv.writer(result, dialect='excel')
	for key in sorted(output_dict.keys()):
		wr.writerow([key,output_dict[key]])



