from django.conf.urls import patterns, include, url
from django.conf.urls import url
from django.contrib import admin
from subscribe.views import subscribe,index,login,logout,subsummary,InsertLineInfo

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^subscribe/', subscribe),
    url(r'^login/?$', login),
    url(r'^$', index),
    url(r'^index/', index),
    url(r'^logout/', logout),
    url(r'^subsummary/', subsummary),
    url(r'^InsertLineInfo/', InsertLineInfo),
    url(r'^accounts/', include('allauth.urls')),
    
]