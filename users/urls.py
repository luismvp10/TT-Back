from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'login/', views.login),
    url(r'register/', views.register),
    url(r'delete/', views.delete),
    url(r'validate/', views.validateToken),
    url(r'user/', views.UserList.as_view()),
    url(r'modify/', views.modify),
    url(r'email/', views.send_email),
    url(r'recover/', views.recover_password),
    url(r'is_allow/', views.allow_to_recover)
]