#import urllib2, urllib
import requests
from bs4 import BeautifulSoup

#using requests package, access the desired url 
url = requests.get("http://rll.fas.harvard.edu/pages/language-tables")
r = "http://rll.fas.harvard.edu/pages/language-tables"
#page = urllib2.urlopen(r)

#soup1 = BeautifulSoup(page)
#use beautifulsoup to access the content of the page
soup = BeautifulSoup(url.content) 

#filters website for only strong tags
st = soup.find_all("strong")
 
"""
#Separates the French table descriptions if wanted
def getLangs(st):    
    result = []    
    for s in st:
        #each <strong>CATALAN (Spring 2017)</strong> turns into a string
        s = "%s" % s
        #get rid of strong tags and "Spring 2017" by replacing with empty
        new_s = s.replace('<strong>','')
        twos = new_s.replace('</strong>','')
        nolabel = twos.replace('(Spring 2017)','')
        #make a list with languages available
        result.append(nolabel)
    return result    
#getLangs(st)
langs = getLangs(st)[1:] 
#print langs   
#this works
"""

#finds the specific lists of french tables    
ftables = soup.find_all("u")
#Locate the unwanted element tags
br = soup.find_all("br")
em = soup.find_all("em")
a = soup.find_all("a")
#Filters website to only the paragraphs
par = soup.find_all("p", limit = 16)

def parsePar(par):
    for tag in st:
        tag.replaceWith('')
    for tag in ftables:
        tag.replaceWith('')
    for tag in br:
        tag.replaceWith('')
    for tag in em:
        tag.replaceWith('')
    for tag in a:
        tag.replaceWith('')
    info = []
    for p in par:
        p = "%s" % p
        #fixing the strings to look nice
        new_p = p.replace('<p>','')
        newp = new_p.replace('</p>','')
        new2 = newp.replace('\xc2\xa0','')
        new2 = new2.replace('mW','m W')
        new2 = new2.replace('lW','l W')
        new2 = new2.replace('aW','aW')
        new2 = new2.replace('CW','C W')
        new2 = new2.replace('s5','s 5')
        new2 = new2.replace('.W','. W')
        new2 = new2.replace('When :',',')
        new2 = new2.replace('Where :',',')
        new2 = new2.replace(', A','A')
        new2 = new2.replace(' ,',',')
        new2 = new2.replace('pmA','pm A')
        new2 = new2.replace('PMA','pm A')
        #make a list with languages available
        info.append(new2)
        
    return info 
    #print par   
desc = parsePar(par)[6::2] 
#print desc  
#desc is the descriptions taken from the parsed page 
#print len(desc) -> should be equal to 5

#print langs[0]
#new dictionary with languages as keys and descriptions as the value     
matches = {'CATALAN' : "%s" % desc[0],
           'FRENCH' : "%s" % desc[1],
           'ITALIAN' : "%s" % desc[2],
           'PORTUGUESE' : "%s" % desc[3],
           'SPANISH' : "%s" % desc[4],
          }
#print matches['CATALAN']
#print matches['FRENCH']
#print matches['ITALIAN']
#print matches['PORTUGUESE']
#print matches['SPANISH']
#print matches



"""
#this works
#filters by the french tables
ftables = soup.find_all("u")
def makeFrench(ftables):
    result = []
    for t in ftables:
        t = "%s" % t
        #get rid of '<u>' tags by replacing with empty
        new_t = t.replace('<u>','')
        twot = new_t.replace('</u>','')
        #make a list with languages available
        result.append(twot)
    return result    
french = makeFrench(ftables) #list of the french tables
print french   
#this works
"""    
#French tables        
#for u in ftables:
 #   print u
 
#Gets names of all language tables    
#for s in st:
 #   print s    

#info function
def makeSpecial():
    s = 'Choose a Language Table option: French, Spanish, Catalan, Portuguese, or Italian.'
    return s

special = makeSpecial()

#evaluate the user input with our dictionary
def eval(input):
    if input.upper() == 'CATALAN':
        return matches['CATALAN']
    elif input.upper() == 'FRENCH':
        return matches['FRENCH']
    elif input.upper() == 'SPANISH':
        return matches['SPANISH']
    elif input.upper() == 'PORTUGUESE':
        return matches['PORTUGUESE']
    elif input.upper() == 'ITALIAN':
        return matches['ITALIAN']
    else:
        return makeSpecial()

#c= eval('catalan')
#f= eval('french')
#s= eval('spanish')
#p= eval('portuguese')
#i= eval('italian')

#checker values and functions

#print c
#print f
#print s
#print p
#print i
#print eval('improper string')



