from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'subshipment/(?P<pk>[0-9]+)$', views.SubshipmentList.as_view()),

]