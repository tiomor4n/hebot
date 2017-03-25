from django.conf.urls import include, url
from subscribe.views import subscribe,index,login,logout,subsummary,InsertLineInfo

from django.contrib import admin
admin.autodiscover()

import hello.views


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^fbbot/', include('fbbot.urls')),
	#url(r'^subscribe/', include('subscribe.urls')),
    url(r'^subscribe/', subscribe),
    url(r'^login/?$', login),
    url(r'^$', index),
    url(r'^index/', index),
    url(r'^logout/', logout),
    url(r'^subsummary/', subsummary),
    url(r'^InsertLineInfo/', InsertLineInfo),
    url(r'^accounts/', include('allauth.urls')),
]
