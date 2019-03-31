from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^countries$',views.CountrieList.as_view()),
    url(r'countrie/(?P<pk>[0-9]+)$', views.CountrieDetail.as_view()),
]