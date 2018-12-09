import urllib.request
import re
import time
import random
import json
import argparse
import webbrowser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv

def processTimeStamp(str):
	dt = datetime.strptime(str, "%I:%M %p - %d %b %Y")
	print(dt)
	return dt

def removeTwitterPics(str):
	regex = re.compile(r'pic\.twitter\.com/\w{10}')
	res = re.sub(regex, "", str)
	return res

def removeUrls(str):
	regex = re.compile(r'http(\w|\/|\#|\=|\.|\&|\:|\?|\-)*')
	res = re.sub(regex, "", str)
	return res

def getNewProxies():
	candidates = []
	response = urllib.request.urlopen('http://lab.crossincode.com/proxy/get')
	response = response.read().decode("utf8")
	jsonObj = json.loads(response)
	for proxy in jsonObj["proxies"]:
		candidates.append(proxy["http"])
	return candidates

keyword = 'Starbucks'
iteration = 40

entry_by_date = {}


#for keyword in keywords:
proxy = "159.65.182.63:80"
options = webdriver.ChromeOptions().add_argument('--proxy-server=http://%s' % proxy)
browser = webdriver.Chrome(chrome_options = options)

#get the third column (url)
id_url = "https://www.twitter.com/search?q="+keyword+"%20since%3A2018-11-18%20until%3A2018-11-21&src=typd"

#scrapping
browser.get(id_url)

#scroll
for i in range(1,iteration):
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(2)

src = browser.page_source
#finish scarpping
browser.quit()

#start parsing results
pageSoup = BeautifulSoup(src, 'lxml')

contents = pageSoup.find_all("div", "content")
for contentDiv in contents:
	entry = {}
	item_header = contentDiv.find("div", "stream-item-header")
	if (item_header != None):
		usernameContainer = item_header.find("span", "username")
		username = usernameContainer.get_text()
		entry["username"] = username
		timeStampContainer = item_header.find("a", "tweet-timestamp")
		timeStamp = timeStampContainer.attrs["title"]
		entry["time_stamp"] = timeStamp	

		replyContainer = contentDiv.find("div", "ReplyingToContextBelowAuthor")
		if (replyContainer != None):
			replyToUserContainer = replyContainer.find("span", "username")
			entry["reply_to"] = replyToUserContainer.get_text()
		else:
			entry["reply_to"] = "None"

		tweetTextContainer = contentDiv.find('div', "js-tweet-text-container")
		tweetText = tweetTextContainer.find('p', "tweet-text").get_text()
		tweetText = removeUrls(removeTwitterPics(tweetText)).strip()
		entry["tweet_text"] = tweetText

		time_array = timeStamp.split()

		filename = keyword+"-"+time_array[5]+"-"+time_array[4]+"-"+time_array[3]+".txt"
		if filename not in entry_by_date:
			entry_by_date[filename] = []
			entry_by_date[filename].append(entry)
		else:
			entry_by_date[filename].append(entry)


for date in entry_by_date:
	output = open(date, "a", encoding='utf8')
	for entry in entry_by_date[date]:
		output.write(json.dumps(entry)+"\n")
	output.close()