from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'subshipment/(?P<pk>\d+)$', views.SubshipmentList.as_view()),
    url(r'^addSubshipment$', views.AddSubshipment, name='add_subshipment'),

]