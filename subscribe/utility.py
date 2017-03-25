# -*- coding: utf8 -*-
def getTimeStamp():
    import calendar
    import datetime
    d = datetime.datetime.now()
    timestamp1 = calendar.timegm(d.timetuple())
    return timestamp1
    
def GetShortUrl(vlongurl):
    import requests
    import urllib
    import json
    
    enlongrul = urllib.quote(vlongurl,safe = '')
    ACCESS_TOKEN = 'c68d130e6955de2191e9889f2ea2f24e9b6cc3e2'
    execurl = 'https://api-ssl.bitly.com/v3/shorten?access_token={}&longUrl={}'.format(ACCESS_TOKEN,enlongrul)
    r = requests.get(execurl)
    js = json.loads(r.content)
    #return json.dumps(js['data']['url'],encoding='UTF-8',ensure_ascii=False)
    return js['data']['url']