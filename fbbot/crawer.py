# -*- coding: utf8 -*-
def findUrl(vccy):
    urldict = {
        'HKD':'http://www.findrate.tw/HKD/#.WKR6um997IU',
        'USD':'http://www.findrate.tw/USD/#.WKR5iG997IU',
        'CNY':'http://www.findrate.tw/CNY/#.WKp5n1V97IU',
        'EUR':'http://www.findrate.tw/EUR/#.WKp5qlV97IU',
        'AUD':'http://www.findrate.tw/AUD/#.WKp5tVV97IU',
        'GBP':'http://www.findrate.tw/GBP/#.WKp5SFV97IU',
        'SGD':'http://www.findrate.tw/SGD/#.WKp5X1V97IU',
        'JPY':'http://www.findrate.tw/JPY/#.WKp5fFV97IU',
        'KRW':'http://www.findrate.tw/KRW/#.WKp52lV97IU'
    }
    
    return urldict[vccy]
    
def findCCY(vccy):
    ccydict = {
        'HKD':u'港幣',
        'USD':u'美金',
        'CNY':u'人民幣',
        'EUR':u'歐元',
        'AUD':u'澳幣',
        'GBP':u'英鎊',
        'SGD':u'新加坡幣',
        'JPY':u'日幣',
        'KRW':u'韓圜'
        
    }


def DataPipe(vccy):
    from bs4 import BeautifulSoup as bs
    import requests
    import sys
    import json
    sys.setdefaultencoding='utf8'
    lineArr = []
    
    namedict={u"銀行名稱":"bankname",
              u"現鈔買入":"billbuy",
              u"現鈔賣出":"billsell",
              u"即期買入":"spotbuy",
              u"即期賣出":"spotsell",
              u"更新時間":"refreshtime",
              u"現鈔手續費":"charge"}
    
    result = ''
    resultArr = []
    '''
    http://www.findrate.tw/HKD/#.WKR6um997IU
    http://www.findrate.tw/USD/#.WKR5iG997IU
    '''
    #urlToVisit = 'http://www.findrate.tw/HKD/#.WKR6um997IU'
    urlToVisit = findUrl(vccy)
    response = requests.get(urlToVisit)
    html = response.content
    soup = bs(html,"html.parser")		
    #print soup
    thline = soup.find('body').findAll('table')[1].findAll('th')
    trs=soup.find('body').findAll('table')[1].findAll('tr')
    
    itrcnt = 0
    itdcnt = 0
    for tr in trs:
        '''
        if itrcnt >1:
            break
        '''
        
        if itrcnt == 0:
            for td in tr:
                try:
                    lineArr.append(namedict[td.text])
                    #lineArr.append(td.text)
                except AttributeError:
                    pass
        else:
            itdcnt = 0
            datadict = {}
            for td in tr:
                try:
                    datadict[lineArr[itdcnt]] =  td.text.strip()
                    itdcnt += 1
                except AttributeError:
                    pass
            resultArr.append(datadict)
            
        itrcnt += 1        
    
    
    #print json.dumps(resultArr, encoding="UTF-8", ensure_ascii=False)
    #print str(resultArr)
    result = json.dumps(resultArr, encoding="UTF-8", ensure_ascii=False)
    return result

def WriteToStatic():
    import json
    from django.conf import settings as djangoSettings
    from datetime import datetime
    import calendar
    
    tstamp = calendar.timegm(datetime.now().timetuple())
    ccyArr = ['HKD','USD','CNY','EUR','AUD','GBP','SGD','JPY','KRW']
    for c in ccyArr:
        jsonstr = json.dumps(json.loads(DataPipe(c)))
        #print type(jsonstr)
        #print jsonstr
        file=open('./' + djangoSettings.STATIC_URL+ '/exrate_' + c +'.json','w')
        file.write(jsonstr)
        file.close()
    
def ReadFromStatic(vccy):
    import json
    from django.conf import settings as djangoSettings
    with open('./' + djangoSettings.STATIC_URL+ '/exrate_' + vccy +'.json') as json_data:
        d = json.load(json_data)
        #print json.dumps(d,encoding="UTF-8", ensure_ascii=False)
    return json.dumps(d,encoding="UTF-8", ensure_ascii=False)
    
    
    
def botDataPipe():
    from bs4 import BeautifulSoup as bs
    import requests
    import sys
    import json
    import re
    
    sys.setdefaultencoding='utf8'
    lineArr = []
    
    urlToVisit = 'http://rate.bot.com.tw/xrt?Lang=zh-TW'
    response = requests.get(urlToVisit)
    html = response.content
    soup = bs(html,"html.parser")	
    cashinfo = soup.find('body').findAll('table')[0].findAll('tbody')[0].findAll('tr')
    namedict={u"本行現金買入":"billbuy",
              u"本行現金賣出":"billsell",
              u"本行即期買入":"spotbuy",
              u"本行即期賣出":"spotsell"}
              
    totalObj = {}    
    ccyObj = {}
    ccyObj2 = {}
        
  
    
    for i in range(len(cashinfo)-1):
        ccyObj2 = {}
        axx = cashinfo[i].findAll('div',{ "class" : "visible-phone print_hide" })       #ccy name
        bxx = cashinfo[i].findAll('td',{ "class" : "rate-content-cash text-right print_hide" })   # billinfo
        cxx = cashinfo[i].findAll('td',{  "class" : "rate-content-sight text-right print_hide" })   # cashinfo
        
        ccyObj2[namedict[bxx[0]['data-table']]] = bxx[0].text.strip()
        ccyObj2[namedict[bxx[1]['data-table']]] = bxx[1].text.strip()
        ccyObj2[namedict[cxx[0]['data-table']]] = cxx[0].text.strip()
        ccyObj2[namedict[cxx[1]['data-table']]] = cxx[1].text.strip()
        
        ccyObj[re.sub(u'[^A-Z]','',axx[0].text.strip())] = ccyObj2
        
    totalObj['bot'] = ccyObj
        
    print json.dumps(totalObj,encoding="UTF-8", ensure_ascii=False)
   
    return json.dumps(totalObj,encoding="UTF-8", ensure_ascii=False)
    
    
def CTCBDataPipe():
    from bs4 import BeautifulSoup as bs
    import requests
    import sys
    import json
    sys.setdefaultencoding='utf8'
    '''
    https://www.ctbcbank.com/CTCBPortalWeb/appmanager/ebank/rb?_nfpb=true&_pageLabel=TW_RB_CM_ebank_018001&_windowLabel=T31400173200000000000000&_nffvid=%2FCTCBPortalWeb%2Fpages%2FexchangeRate%2FexchangeRate.faces&firstView=true
    '''
    urlToVisit = 'https://www.ctbcbank.com/CTCBPortalWeb/appmanager/ebank/rb?_nfpb=true&_pageLabel=TW_RB_CM_ebank_018001&_windowLabel=T31400173200000000000000&_nffvid=%2FCTCBPortalWeb%2Fpages%2FexchangeRate%2FexchangeRate.faces&firstView=true'
    response = requests.get(urlToVisit)
    html = response.content
    soup = bs(html,"html.parser")
    #tds = soup.findAll('table')[1].findAll('tr')[1].findAll('td')
    trs = soup.findAll('table')[1].findAll('tr')
    totalObj = {}    
    ccyObj = {}
    ccyObj2 = {}
    '''
    for i in range(len(trs)):
        if i > 0:
            
            
    
    for td in tds:
        print td.text.strip()
    '''
    return 'AA'
    
    
    
    
    