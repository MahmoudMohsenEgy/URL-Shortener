import base62
BASE_URL = 'https://xyurl.herokuapp.com/'
def shorten_url(original_url):
    return BASE_URL+get_shortened_id()
# get_url should take a shortened url and get the original url
def get_url_by_ID(shortenID):
    return str(BASE_URL) + str(shortenID)
# get the mah.moud/cf61 <--- cf61 is the ID 
def get_shortened_id():
    return base62.encode_random()
def checkForHTTP(site):
    if site.find("http://") != 0 and site.find("https://") != 0:
        site = "http://" + str(site)
    return site