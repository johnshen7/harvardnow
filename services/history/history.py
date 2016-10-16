import urllib2, urllib
from bs4 import BeautifulSoup

def getHistory(input):
	url = "http://www.history.com/this-day-in-history"
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read(), 'lxml')

	headers = soup.find_all('h2')

	return "Today in history: " + headers[1].text

def makeSpecial():
	s = "To get what happened in history today, please text \'history\' to HarvardNow"
	return s

special = makeSpecial()

def eval(input):
	return getHistory(input)