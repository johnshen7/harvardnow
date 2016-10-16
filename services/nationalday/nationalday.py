import urllib2, urllib
from bs4 import BeautifulSoup
import datetime
	
def getNationalDay(input):
	url = "http://www.nationaldaycalendar.com/"
	today = datetime.datetime.today()
	url += today.strftime("%B").lower()

	requestHeaders = {'User-Agent' : 'Chrome'}
	req = urllib2.Request(url, headers=requestHeaders)
	page = urllib2.urlopen(req)

	soup = BeautifulSoup(page.read(), 'lxml')
	stuffs = soup.find_all("div", {"class" : "et_pb_blurb_container"})

	goodStuff = None
	for stuff in stuffs:
		date = datetime.datetime.strptime(stuff.find("h4").text[:-2], "%B %d")

		if date.day == today.day:
			goodStuff = stuff
			break

	if goodStuff is None:
		return "There are no national days today"
		
	nationalDays = goodStuff.find_all("li")

	holidaysString = ""

	length = len(nationalDays)

	if length == 1:
		return "Today is " + nationalDays[0].text
	elif length == 2:
		return "Today is " + nationalDays[0].text + " and " + nationalDays[1].text
	else:
		for x in xrange(0, length - 1):
			holidaysString += nationalDays[x].text + ", "

		holidaysString += "and " + nationalDays[length - 1].text

		return "Today is " + holidaysString

def makeSpecial():
	s = "To get the national days for today, text \'nationalday\' to HarvardNow"
	return s

special = makeSpecial()

def eval(input):
	return getNationalDay(input)