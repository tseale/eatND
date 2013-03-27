"""
Taylor Seale
SDH Menu parser
March 27, 2013
Parses Notre Dame's South Dining Hall menu and saves the results to a parse database
"""

from bs4 import BeautifulSoup
from parse_rest.connection import register
from parse_rest.datatypes import Object
import urllib2

# register the program with parse database
register("NsQ7yd5aoQX35SMBmUjVwFA6rUjctED5CrjH1VcI","9uIgnDxZPMQD2skEqVXFXrGf2K8YBPtT9o8ECgbO")


# declare classes for parse tables
class Menu(Object): # daily menu
	pass

class AllItems(Object): # history of all items served
	pass

# open up the url, parse it with BeautifulSoup
print "Opening URL..."
url = 'http://fsntserv.foodserv.nd.edu/dh_menus/sdh_menu_today.cfm'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read(),"html.parser")

# delete all items currently on the menu
# need to delete twice! it looks like Query.all() has a return limit of 100 entries...
print "Deleting Old Menu..."
oldMenu = Menu.Query.all()
for item in oldMenu:
	item.delete()
oldMenu = Menu.Query.all()
for item in oldMenu:
	item.delete()

# parse the data, store in the parse database
print "Uploading New Menu..."
for line in str(soup).split('\n'):
	if '<h2>' in str(line): # meal headings
		m = line[4:-5]
	if '<br/>' in str(line) and '<td' not in str(line): # food items
		items=line.split('<br/>')
		# save each item to the database
		for i in items:
			if i!='':
				item=Menu(meal=m.lower(),item=i.lower())
				item.save()

"""
favorites = ["cheese pizza","large shells","poop","taco meat"]
served={}
for f in favorites:
	item = Menu.Query.all().where(item=f)
	for i in item:
		if i.item not in served.keys():
			served[i.item.encode('ascii')]=[i.meal.encode('ascii')]
		else:
			served[i.item.encode('ascii')].append(i.meal.encode('ascii'))

for k,v in served.iteritems():
	print k+" will be served for",
	for m in v:
		print m+',',
	print
"""