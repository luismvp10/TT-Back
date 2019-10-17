from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^chapters$', views.ChapterList.as_view()),
    url(r'^addChapter$', views.AddChapter, name='add_chapter'),
    url(r'^chapter/Search/(?P<search>[^/]+)/$', views.ChapterSerch.as_view()),

]
