from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'transaction/(?P<section>\d{8})((?:/country/(?P<country>\d+))?)((?:/month/(?P<month>[\d+\s+]+))?)/year/('
        r'?P<year>\d+)$',
        views.TransactionList.as_view()),
    url(
        r'transaction/(?P<operation>\d{6})((?:/country/(?P<country>\d+))?)((?:/month/(?P<month>[\d+\s+]+))?)/year/('
        r'?P<year>\d+)$',
        views.TransactionSubshipment.as_view()),
    url(
        r'transaction/(?P<operation>\d{4})((?:/country/(?P<country>\d+))?)((?:/month/(?P<month>[\d+\s+]+))?)/year/('
        r'?P<year>\d+)$',
        views.TransactionSubshipment.as_view()),
    url(
        r'transaction/(?P<operation>\d{2})((?:/country/(?P<country>\d+))?)((?:/month/(?P<month>[\d+\s+]+))?)/year/('
        r'?P<year>\d+)$',
        views.TransactionSubshipment.as_view()),
    url(
        r'transaction((?:/month/(?P<month>[\d+\s+]+))?)$',
        views.hello_world),
    url(
        r'prediction/operation/(?P<operation>\d+)((?:/country/(?P<country>\d+))?)/kind/(?P<kind>\d)$',
        views.prediction),
    url(
        r'report/(?P<operation>\d+)((?:/country/(?P<country>\d+))?)((?:/month/(?P<month>[\d+\s+]+))?)/year/('
        r'?P<year>\d+)$',
        views.getReport),
]