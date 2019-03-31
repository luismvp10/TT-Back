from django.shortcuts import render
from rest_framework import generics
from countries.models import Countrie
from countries.serializers import CountrieSerializer

# Create your views here.


class CountrieList(generics.ListAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer

class CountrieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer