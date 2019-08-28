from django.shortcuts import render
from rest_framework import generics
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from sections.models import Section
from sections.serializers import SectionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@permission_classes((AllowAny,))

<<<<<<< HEAD
=======
# Create your views here.

@permission_classes((AllowAny,))
>>>>>>> humberto
class SectionList(generics.ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
<<<<<<< HEAD
        return Section.objects.filter(subShipment_id=id)
=======
        return Section.objects.filter(id_section=id)
>>>>>>> humberto
