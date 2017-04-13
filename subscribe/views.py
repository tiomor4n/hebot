# -*- coding: utf-8 -*
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponseRedirect
from django.contrib import auth 
from subscribe.models import LineInformList,EmailVerify
from crawer import ReadFromStaticBank,WriteToStatic,BKTWDataPipe
from subscribe.LineNotify import sendmsg,GetToken
from subscribe.utility import getTimeStamp,GetShortUrl
from subscribe.forms import subscribeForm,YourSignupForm
import json

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
        'KRW':u'韓圜',
        'DEL':u'刪除',
        'INT':u'請輸入'
	}
    return ccydict[vccy]

def batchOP():
    
    def genmsgstr(name,ccy,exrate,rate,shortlink):
        msgstr=u'親愛的{},{}已達指定匯率{},現為{},如本日欲停止通知請點選連結{}'.format(name,ccy,exrate,rate,shortlink)
        return msgstr
        
    def getShortUrl(vid):
        shorturl=''
        longurl = 'https://script.google.com/macros/s/AKfycbzaU3pJIB3pZCL2p637gTJ4hkbQneQuudXFb_efk1miflSfJgk/exec?id={}'.format(vid)    
        print 'longurl:' + longurl
        shorturl = GetShortUrl(longurl)
        return shorturl
        
    
    AllLine = LineInformList.objects.all()
    rateinfo = json.loads(ReadFromStaticBank())
    rateinfob = rateinfo['BKTW']
    result = 'err'
    resultdict = {}
    resultArr = []
    checkmsg= False
    for LL in AllLine:
        resultdict = {}
        if LL.BS == 'B':
            checkpt = 'spotsell'
        else:
            checkpt = 'spotbuy'
        
        
        strccy = LL.ccy
        stremail = LL.email
        
        if LL.BS == 'B':
            resultdict[stremail] = str(float(rateinfob[strccy][checkpt]) <= LL.exrate)
            checkmsg = float(rateinfob[strccy][checkpt]) <= LL.exrate
            resultdict['rate'] = str(float(rateinfob[strccy][checkpt]))
                
        else:
            resultdict[stremail] = str(float(rateinfob[strccy][checkpt]) > LL.exrate)
            checkmsg = float(rateinfob[strccy][checkpt]) > LL.exrate
            resultdict['rate'] = str(float(rateinfob[strccy][checkpt]))
        
        if checkmsg:
            if LL.stoptoday != 'V':
                shortUrl = getShortUrl(LL.id)
                msgstr = genmsgstr(LL.email,LL.ccy,LL.exrate,str(float(rateinfob[strccy][checkpt])),shortUrl)
                msgrt = sendmsg(LL.token,msgstr)
                print msgrt
                
        
        resultArr.append(resultdict)
        
    print str(resultArr)
    #print json.dumps(resultArr, encoding="UTF-8", ensure_ascii=False)
    return json.dumps(resultArr, encoding="UTF-8", ensure_ascii=False)
            

def subsummary(request):
    if request.user.is_authenticated():
        uemail = request.user.email
        ldata = LineInformList.objects.filter(email=uemail)
        EV = ldata[0].emailverify
        if EV.token == '':
            subtoken = False
        else:
            subtoken = True
        print EV.token
        for l in ldata:
            l.ccy = findCCY(l.ccy)
            if l.BS == 'B':
                l.BS = u'買'
            else:
                l.BS = u'賣'
        
    return render_to_response('subsummary.html',locals())
    
def subscribe(request):
    if 'id' in request.GET and request.GET['id'] != '':
        #singleL = LineInformList.objects.get(ccy=request.GET['ccy'],BS = request.GET['BS'])
        singleL = LineInformList.objects.get(id = request.GET['id'])
        vmove = 'U'
        f = subscribeForm(initial={'BS':singleL.BS,'ccy':singleL.ccy,'exrate':singleL.exrate})
        return render_to_response('subscribe.html',locals())
    else:
        f = subscribeForm(initial={'BS':'I','ccy':'INT','exrate':'請輸入'})
        #print f
        return render_to_response('subscribe.html',locals()) 
    
def index(request):
    return render_to_response('index.html',locals())
    
def login(request):
    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/subscribe/')

    username = request.POST.get('email', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/subsummary/')
    else:
        return render_to_response('login.html') 

def logout(request):
    auth.logout(request)
    return render_to_response('login.html') 
    
def register(request):
    if request.method == 'POST':
        form = YourSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            #send_email_confirmation()
            return HttpResponseRedirect('/login/')
    else:
        form = YourSignupForm()
    return render_to_response('register.html',locals())

def InsertLineInfo(request):
    if request.user.is_authenticated(): 
        if request.POST:
            vccy = request.POST['ccy']
            vBS = request.POST['BS']
            vexrate = request.POST['exrate']
            vtoken = 'ZG9Qy1xXmKuqxXyCe0QwTCKbczU0oGWSi8KoZWreFj5'
            errors=[]
            EV = EmailVerify.objects.get(email=request.user.username)
            
            
            if request.POST['move'] == 'U':
                if vccy == '':
                    Line1 = LineInformList.objects.get(id=request.POST['id'])
                    Line1.delete()
                else:
                    Line1 = LineInformList.objects.get(id=request.POST['id'])
                    Line1.BS = vBS
                    Line1.exrate = vexrate
                    Line1.ccy = vccy
                    Line1.save()
            else:
                Line1 = LineInformList(email = request.user.username,
                         nickname = request.user.username,
                         token = vtoken,
                         bank = 'BKTW',
                         BS = vBS,
                         ccy = vccy,
                         exrate = vexrate,
                         stoptoday = 'X',
                         emailverify = EV)
                Line1.save()
            
            return HttpResponseRedirect('/subsummary/')
            #return render_to_response('subsummary.html',locals())

def stoptoday(request):
    import sys
    try:
        if 'id' in request.GET and request.GET['id'] != '':
            singleL = LineInformList.objects.get(id = request.GET['id'])
            print 'id:' + str(request.GET['id'])
            print 'TF:' + str(request.GET['TF'])
            if request.GET['TF'] == 'true':
                singleL.stoptoday = 'X'
            else:
                singleL.stoptoday = 'V'
            singleL.save()
            return HttpResponse('correct')
    except ValueError:
        pass
        
        
def GetLineNotify(request):
    if request.user.is_authenticated(): 
        uemail = request.user.email
        print uemail
        URL = 'https://notify-bot.line.me/oauth/authorize?'
        URL += 'response_type=code'
        URL += '&client_id=nch5lTjwJmgdHwx5Ar4oaJ'
        URL += '&redirect_uri=https://rate-notify-tiomor4n.c9users.io/gettokenfromcode'
        URL += '&scope=notify'
        URL += '&state=' + str(uemail)
        print URL
        return redirect(URL)
        
def GetTokenFromCode(request):
    #print request.GET['state']
    #print request.GET['code']
    uemail = request.GET['state']
    strcode = request.GET['code']
    reply = GetToken(strcode)
    print 'reply:' + reply
    if reply != '':
        print 'okok'
        
        replyjs = json.loads(reply)
        tokenstr = replyjs['access_token']
        print 'tokenstr:' + tokenstr
        
        EV = EmailVerify.objects.get(email=uemail)
        EV.token = tokenstr
        EV.save()
        
        sendmsg(tokenstr,'你好，歡迎使用RateAnyWhere服務')
        
    return render_to_response('GetTokenFromCode.html') 
    
def templateIndex(request):
    return render_to_response('templateIndex.html') 
        
    
    
