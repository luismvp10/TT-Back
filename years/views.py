from django.shortcuts import render
from rest_framework import generics
from years.models import Year
from years.serializers import YearSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@permission_classes((AllowAny,))

# Create your views here.
class YearList(generics.ListAPIView):
    queryset = Year.objects.order_by('id_year')[::-1]
    serializer_class = YearSerializer