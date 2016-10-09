import urllib, urllib2, json


#############################
##          Setup          ##
#############################

signs = ['ARIES', 'TAURUS', 'GEMINI', 'CANCER', 'LEO', 'VIRGO', 'LIBRA', 'SCORPIO', 'SAGITTARIUS', 'CAPRICORN', 'AQUARIUS', 'PISCES']
base_url = 'http://horoscope-api.herokuapp.com/horoscope/today/'

##############################
##    Horoscope Functions     ##
##############################

# get the horoscope of sign using api: https://github.com/tapasweni-pathak/Horoscope-API
def getHoroscope(sign):
    # make api request
    url = base_url + sign.lower()
    website = urllib2.urlopen(url)
    data = json.loads(website.read())

    # get the horoscope message from the api request.  remove api bug ['
    horoscope = data['horoscope'].replace("[' ",'').strip()

    # replacing common unicode manually because automated ways don't like to work
    horoscope = horoscope.replace('\\u2014', '--')
    horoscope = horoscope.replace('\\u2019', '\'')

    return  "Today's horoscope for %s:\n\n%s" % (sign.title(), horoscope)


# used to gather the list of the signs for makeSpecial
def makeSignList():
    s = ''
    for sign in signs:
        s += "%s\n" % (sign.title())
    return s

# generate the special response
def makeSpecial():
    response = 'Usage: horoscope [sign]\n\nZodiac Signs:\n'
    sign_list = makeSignList()
    response += sign_list
    return response


#############################
##        Top-Level        ##
#############################

## list of valid signs
special = makeSpecial()

def eval(cmd):
    sign = cmd['sign']
    if sign.upper() in signs:
        return getHoroscope(sign)
    else:
        return "Incorrect sign! Available signs are:\n%s" % (makeSignList())

# testing code
if __name__ == '__main__':
    print ''
    print getHoroscope('aries')
