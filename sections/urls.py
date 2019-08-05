from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'section/(?P<pk>[0-9]+)$', views.SectionList.as_view()),

]