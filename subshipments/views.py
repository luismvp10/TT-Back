from django.shortcuts import render
from rest_framework import generics
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from subshipments.models import Subshipment
from subshipments.serializers import SubshipmentSerializer

# Create your views here.

@permission_classes((AllowAny,))
class SubshipmentList(generics.ListAPIView):
    serializer_class = SubshipmentSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        return Subshipment.objects.filter(shipment_id=id)

