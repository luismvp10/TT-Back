from django.shortcuts import render
from rest_framework import generics
from rest_framework import generics
from sections.models import Section
from sections.serializers import SectionSerializer

# Create your views here.
class SectionList(generics.ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        return Section.objects.filter(id_subShipment=id)
