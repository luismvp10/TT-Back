from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'shipment/(?P<pk>[0-9]+)$', views.ShipmentList.as_view()),
    url(r'^addShipment$', views.AddShipment, name='add_shipment'),

]