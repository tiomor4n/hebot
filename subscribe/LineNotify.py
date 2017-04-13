# -*- coding: utf8 -*-
import requests


def GetToken(code):
    print "code:" + code
    r = requests.post("https://notify-bot.line.me/oauth/token",
                      data={
                          "grant_type":"authorization_code",
                          "code":code,
                          "redirect_uri":"https://rate-notify-tiomor4n.c9users.io/gettokenfromcode",
                          "client_id":"nch5lTjwJmgdHwx5Ar4oaJ",
                          "client_secret":"8S6f5tHE1HqE9he2sJW5CrZbHCMn6NbMZadr291111q"
                      },
                      headers={
                          "Content-Type":"application/x-www-form-urlencoded"
                      }
                   )
    print r.text
    return r.text

def sendmsg(token,msg):
    print "token:" + token
    r = requests.post("https://notify-api.line.me/api/notify",
             data={
                 "message":msg
             },
             headers=
             {
                 "Authorization":"Bearer " + token,
                 "Content-Type":"application/x-www-form-urlencoded"
             }
            
        )
    print r.text
    return r.text