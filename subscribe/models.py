from __future__ import unicode_literals

from django.db import models

class EmailVerify(models.Model):
    email = models.CharField(max_length=20)
    token = models.CharField(max_length=45)
    verify= models.BooleanField(default=False)

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
    
