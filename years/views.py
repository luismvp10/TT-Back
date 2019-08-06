from django.shortcuts import render
from rest_framework import generics
from years.models import Year
from years.serializers import YearSerializer


# Create your views here.
class YearList(generics.ListAPIView):
    queryset = Year.objects.order_by('id_year')[::-1]
    serializer_class = YearSerializer