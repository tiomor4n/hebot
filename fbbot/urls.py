# testpro/fbbot/urls.py
from django.conf.urls import include, url
from .views import fbbotView,ExRateScan,firstpge


urlpatterns = [
                  #url(r'^8a043645b608c37ec5577af7d6bbdf94dc5bdc70e12f6c88f3/?$', fbbotView.as_view())
                  url(r'^getvaluefromfb/?$', fbbotView.as_view()),
                  url(r'^getvaluefromgooglescript/?$', ExRateScan.as_view()),
                  url(r'^$',firstpge)
                  

               ]
