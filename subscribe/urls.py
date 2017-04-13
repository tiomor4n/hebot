from django.conf.urls import patterns, include, url
from django.contrib import admin
from subscribe.views import subscribe,index,login,logout,subsummary,InsertLineInfo,register,GetLineNotify,GetTokenFromCode,stoptoday,templateIndex
from allauth.account.views import SignupView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^subscribe/', subscribe),
    url(r'^login/', login),
    url(r'^$', index),
    url(r'^index/', index),
    url(r'^logout/', logout),
    url(r'^subsummary/', subsummary),
    url(r'^InsertLineInfo/', InsertLineInfo),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^signup/', register),
    url(r'^GetLineNotify/', GetLineNotify),
    url(r'^gettokenfromcode/', GetTokenFromCode),
    url(r'^stoptoday/', stoptoday),
    url(r'^templateIndex/', templateIndex),
]