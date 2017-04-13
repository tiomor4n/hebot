from __future__ import unicode_literals

from django.db import models

class EmailVerify(models.Model):
    email = models.CharField(max_length=20)
    verify= models.BooleanField(default=False)
    token = models.CharField(max_length=45,default='')

class LineInformList(models.Model):
    email = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10)
    token = models.CharField(max_length=45)
    bank = models.CharField(max_length=4)
    BS = models.CharField(max_length=1)
    ccy = models.CharField(max_length=3)
    exrate = models.FloatField(default=0.)
    stoptoday = models.CharField(max_length=1)
    emailverify = models.ForeignKey(EmailVerify)
    
class comment(models.Model):
    name = models.CharField(max_length=20)
    emailcont = models.CharField(max_length=20)
    comments = models.CharField(max_length=200)
    
