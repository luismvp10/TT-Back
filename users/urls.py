from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'login/', views.login),
    url(r'register/', views.register),
    url(r'delete/', views.delete),
    url(r'validate/', views.validateToken),
]