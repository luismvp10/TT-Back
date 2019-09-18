"""sicat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.apps import *
from django.conf.urls import url
from django.urls import path, include
from . import views
import countries, rest_framework

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('countries/', include('countries.urls')),
    path('chapters/', include('chapters.urls')),
    path('years/', include('years.urls')),
    path('months/', include('months.urls')),
    path('shipments/', include('shipments.urls')),
    path('subshipments/', include('subshipments.urls')),
    path('sections/', include('sections.urls')),
    path('users/', include('users.urls')),
    path('transactions/',include('transactions.urls')),
    path(r'regresion_lineal/', views.regresion_lineal),
    path(r'regresion_polinomial/', views.regresion_polinomial),
    path(r'SVR/', views.svr),
    path(r'arboles_desicion/', views.arboles_decision),
    #path('api-auth/', rest_framework.urls),

]
