from django.shortcuts import render
from rest_framework import generics
from rest_framework import generics
from sections.models import Section
from sections.serializers import SectionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@permission_classes((AllowAny,))

class SectionList(generics.ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        return Section.objects.filter(subShipment_id=id)
