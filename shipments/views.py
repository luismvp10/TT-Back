from django.shortcuts import render
from rest_framework import generics
from rest_framework import generics
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer

# Create your views here.
class ShipmentList(generics.ListAPIView):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        return Shipment.objects.filter(chapter_id=id)
