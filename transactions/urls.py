from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'transaction/(?P<section>\d{8})((?:/country/(?P<country>\d+))?)((?:/month/(?P<month>\d+))?)/year/(?P<year>\d+)$', views.TransactionList.as_view()),

]