from bs4 import BeautifulSoup
import urllib2, urllib
import datetime

#############################
##      Menu Function      ##
#############################

def getMenuData(url, requested=None):
	try:
		# Get data from HUDS site
		request = urllib2.urlopen(url).read()
		soup = BeautifulSoup(request, features='html.parser')

		# Find all categories listed in the table; identified by colspan attribute
		parser = soup.find_all(colspan='3')

		# Make a list of all category names
		categories = list()
		for category in parser:
			categories.append(str(category.string).strip().upper())

		# Initialize a dict with category names as keys and initialize each value as an empty list
		menu = dict.fromkeys(categories)
		for key, value in menu.items():
			menu[key] = list()

		# Assign appropriate menu items to each key
		for category in parser:
			category_name = str(category.string).strip().upper()
			# Find all siblings to <tr> parent tag containing the category info
			for item in category.find_parent().find_next_siblings():
				# If the tag has a class attribute, it must be another category tag, so break into the next category
				if item.has_attr('class'):
					break
				# Get menu item when tag lacks a class attribute, which describes all <tr> elements containing a menu item
				else:
					item_name = str(item.find('td', class_='menu_item').div.span.a.string).strip()
					menu[category_name].append(item_name)
		if not requested:
			return formatMenu(menu)
		return formatMenu({requested: menu[requested]})
	except:
		return 'Could not obtain menu data!'


def formatMenu(menu):
	s = ''
	for category in menu:
		s += category + '\n'
		for item in menu[category]:
			s += item + '\n'
	return s

#############################
##		   Top Level       ##
#############################

def makeSpecial():
	s = '''To get everything on today\'s menu, enter \'menu time all\' where time is breakfast/lunch/dinner.
To get a particular category on the menu, enter \'menu time category\'.
For example, \'menu dinner entrees\' gives all the entrees on today's dinner menu.
Other categories include: \'desserts\', \'from the grille\', and \'salad bar\'.'''
	return s

special = makeSpecial()


def eval(cmd):
	# Get url corresponding to today's menu based on type
	date = datetime.datetime.today().strftime('%m-%d-%Y')
	time = cmd['type']
	typeurls = {
	'BREAKFAST': 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date=' + date + '&type=30&meal=0',
	'LUNCH': 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date='  + date + '&type=30&meal=1',
	'DINNER': 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date='  + date + '&type=30&meal=2'
	}

	if time in typeurls:
		return getMenuData(typeurls[time], cmd['category'])
	# Possibly superfluous return
	return 'Please specify breakfast, lunch, or dinner'
