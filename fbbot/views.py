# -*- coding: utf8 -*-
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
import json
from crawer import DataPipe,WriteToStatic,ReadFromStatic,botDataPipe,CTCBDataPipe


def getTimeStamp():
    import calendar
    import datetime
    d = datetime.datetime.now()
    timestamp1 = calendar.timegm(d.timetuple())
    return timestamp1

def ExamBatch(vimessage):
        WriteToStatic()
        #incoming_message = json.loads('[{"ID":"AA","bank":"國泰世華","BS":"S","ccy":"HKD","exrate":3.6},{"ID":"AA","bank":"國泰世華","BS":"B","ccy":"USD","exrate":20}]')
        print vimessage.encode('utf-8')
        incoming_message = json.loads(vimessage)
        
          
        result = 'err'
        
        resultdict = {}
        resultArr = []
        for ii in incoming_message:
            resultdict = {}
            if ii['BS'] == 'B':
                checkpt = 'spotsell'
            else:
                checkpt = 'spotbuy'
            rateinfo = json.loads(ReadFromStatic(ii['ccy']))
            print json.dumps(rateinfo,encoding="UTF-8", ensure_ascii=False)
            for b in rateinfo:
                if b['bankname'].strip() == ii['bank'].strip():
                    print 'BS:' + str(ii['BS']) 
                    #resultdict['ID'] = ii['ID']
                    if ii['BS'] == 'B':
                        resultdict[ii['ID']] = str(float(b[checkpt]) > ii['exrate'])
                    else:
                        resultdict[ii['ID']] = str(float(b[checkpt]) < ii['exrate'])
            resultArr.append(resultdict)
        return json.dumps(resultArr, encoding="UTF-8", ensure_ascii=False)


def firstpge(request):
    return HttpResponse('First Page')

def post_facebook_message(fbid, recevied_message):    
    import requests
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAATX5oiPeXkBAEJwbZBRHsS08gSAuSVpkhCw8MnbZAZB6fb5WxbhZBRvqSKv8mqKyLZBFHHwTSAbmdEnNNBudzZBUXdCTdGyGZBWWz3pjiQ2yjG5tUDAJ6PmiXfdTUSDKO9iX2rvBlJa3iBeHE1EMhyTMitlfAALI6SFchJL4IvYwZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print(status.json())
    

# Create your views here.
class fbbotView(generic.View):
    
    def get(self, request, *args, **kwargs):
        try:
            if self.request.GET['hub.verify_token'] == '2318934571':
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponse('Error, invalid token')    
        except MultiValueDictKeyError:
            return HttpResponse('Error, invalid token for getvaluefromfb')    
   
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    print(message)    
                    post_facebook_message(message['sender']['id'], message['message']['text']) 
        return HttpResponse()
        
        
class ExRateScan(generic.View):
    
    
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        import sys
        sys.setdefaultencoding='utf8'
        #result = ExamBatch('[{"ID":"AA","bank":"國泰世華","BS":"S","ccy":"HKD","exrate":3.6},{"ID":"AA","bank":"國泰世華","BS":"B","ccy":"USD","exrate":20}]')
        result = botDataPipe()
        #result = CTCBDataPipe()
        return HttpResponse(result)
                
        

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        #print json.loads(incoming_message)
        #print type(json.loads(incoming_message))
        #return HttpResponse(json.loads(incoming_message)[0]['ID'])
        result = json.dumps(ExamBatch(incoming_message))
        return HttpResponse(result)
        
        #return HttpResponse('AA')