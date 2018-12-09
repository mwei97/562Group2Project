# 562Group2Project

Customized_test.txt is our randomlly selected set of company related tweets that we use as the test set for sentiment analysis. 
Customized_label.csv contains the sentiment scores that we manually labeled.
Sentiment140_test.csv is the test set provided by Sentiment140 labeled 0 for negative, 2 for neutral and 4 for positive.
The training set provided by Sentiment140 contains 1,600,000 tweets and is too large to upload so isn't included in this directory.

Scrap.py is the script we used to scrap company related tweets. Parameters can be changed to search for different keywords during different time frames. 

Vader.py is the script we used to test VADER's accuracy for sentiment analysis.

NB_Train+Test is the python code file that we used for testing the Naive Bayes Model. It takes Setiment140 training set, and Customized_label.csv/Sentiment140_test.csv as input.
It is used to evaluate the accuracy of NB model on both Sentiment140 and Customized test set.

NB_Classification is the script that we used to actually generate the sentiment scores that we feed into next step stock prediction.

Stock+Sentiment.ipynd contains our LSTM model used for stock price prediciton.
