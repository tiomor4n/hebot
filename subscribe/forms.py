# -*- coding: utf8 -*-
from django import forms
from subscribe.models import LineInformList
import re
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import LoginForm,SignupForm


class YourLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(YourLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['login'].widget = forms.TextInput(attrs={'class':'form-control'})
        
class YourSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(YourSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class':'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})

class subscribeForm(forms.Form):
    #BS = forms.CharField(max_length=1,required=True,label =u'買/賣別',widget=forms.TextInput(attrs={'class':'form-control'}) )
    BSlist = (('B',u'買'),('S',u'賣'),('I','-'))
    ccylist = (
        ('INT',u'請輸入'),
        ('DEL',u'刪除'),
        ('HKD',u'港幣'),
        ('USD',u'美金'),
        ('CNY',u'人民幣'),
        ('EUR',u'歐元'),
        ('AUD',u'澳幣'),
        ('GBP',u'英鎊'),
        ('SGD',u'新加坡幣'),
        ('JPY',u'日幣'),
        ('KRW',u'韓圜'))
    BS = forms.MultipleChoiceField(choices=BSlist,label=u'買/賣別',widget=forms.Select(attrs={'class':'form-control'}))
    ccy = forms.MultipleChoiceField(choices=ccylist,label=u'幣別',widget=forms.Select(attrs={'class':'form-control'}))
    exrate = forms.CharField(max_length=8,required=True,label = u'目標匯率',widget=forms.TextInput(attrs={'class':'form-control'}) )
    
    
    
    def clean_ccy(self):
        vccy = self.cleaned_data['ccy']
        vBS = self.cleaned_data['BS']
        
        Lexam = LineInformList.object.filter(BS = vBS,ccy = vccy)
        if len(Lexam) > 0:
            raise forms.ValidationError(u'同一幣別及買賣別僅能有一筆資料')
        return  vccy
        
    def clean_exrate(self):
        vexrate = self.cleaned_data['exrate']
        if re.match(r"[^0-9.]",vexrate) != '':
            raise forms.ValidationError(u'匯率僅能輸入數字及小數點')
        return vexrate

'''        
class loginForm(forms.Form):
    email = forms.CharField(max_length=1,required=True,label =u'請輸入email')
    password = forms.CharField(max_length=1,required=True,label =u'請輸入密碼')
'''