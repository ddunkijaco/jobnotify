import requests
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')
 
indeedbaseurl = 'http://api.indeed.com/ads/apisearch'
indeedpubkey = config.get('indeed', 'publisherkey')
indeedquery = config.get('indeed', 'query')
indeedloc = config.get('indeed', 'location')
indeedformat = 'json'
indeedv = '2'
indeedsort = 'date'
indeedfromage = '1'
limit = '25'
indeedparams = {
    'publisher' : indeedpubkey, 
    'q' : indeedquery, 
    'l' : indeedloc, 
    'v' : '2', 
    'format' : 'json', 
    'sort' : 'date', 
    'fromage' : '1', 
    'limit' : '25',
    'highlight' : '0'
}

nmabaseurl = 'https://www.notifymyandroid.com/publicapi/notify'
nmaapikey = config.get('notifymyandroid', 'apikey')
 
bitlybaseurl = 'https://api-ssl.bitly.com/v3/shorten'
bitlytoken = config.get('bitly', 'token')
 
def shorten_url(url):
    bitlyparams = {'access_token' : bitlytoken, 'longUrl' : url}
    s = requests.get(bitlybaseurl, params=bitlyparams)
    if s.status_code == requests.codes.ok:
        bitly = s.json()
        return bitly['data']['url'].encode('utf-8')
    else:
        pass
 
def indeed_job_search(job_searchurl, job_searchparams):
    r = requests.get(job_searchurl, params = job_searchparams)
    if r.status_code == requests.codes.ok: 
        data = r.json()
        for x in range(len(data['results'])):
            if data['results'][x]['jobkey'].encode('utf-8') == config.get('indeed', 'jobkey'):
                break
            else:
                jobtitle = data['results'][x]['jobtitle'].encode('utf-8') + ' ' + data['results'][x]['company'].encode('utf-8')
                jobdesc = data['results'][x]['snippet'].encode('utf-8')
                joburl = data['results'][x]['url'].encode('utf-8')
                shorturl = shorten_url(joburl)
                nmaparams = {'apikey' : nmaapikey,'application' : 'Indeed Job Search:', 'event' : jobtitle, 'description' : jobdesc + shorturl}
                nma = requests.post(nmabaseurl, params=nmaparams)
                config.set('indeed','jobkey',data['results'][0]['jobkey'].encode('utf-8'))
                with open('config.ini', 'wb') as configfile:
                    config.write(configfile)
    else:
        print 'uhoh'
                
indeed_job_search(indeedbaseurl, indeedparams)