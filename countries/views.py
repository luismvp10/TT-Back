from django.shortcuts import render
from rest_framework import generics
from countries.models import Countrie
from countries.serializers import CountrieSerializer
from django.http import HttpResponse
import pandas as pd
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse
from django.core import serializers
# Create your views here.
def upload(request):
    if request.method == 'POST':
        if request.FILES.getlist('document'):
            for f in request.FILES.getlist('document'):
                data=str(f.read())
                data=re.sub(r'<tr bgcolor=.*?</tr>|<font.*?>|<strong>|</strong>|<font>|<div.*?>|</div>|<tbody>|</tbody>', '', data)
                data=re.sub(r'<table.*?>', '<table>', data)
                data=re.sub(r'<th.*?>', '<td>', data)
                data=re.sub(r'<tr.*?>', '<tr>', data)
                data=re.sub(r'<td.*?>', '<td>', data)
                data=re.sub(r'</th>', '</td>', data)
                data=re.sub(r'Rep.*?ca', 'Republica', data)
                data=re.sub(r'Esp.*?1a', 'Espana', data)
                data=re.sub(r'Bre.*?1a', 'Bretana', data)
                data=re.sub(r'Federac.*?n', 'Federacion', data)
                soup = BeautifulSoup(data,'lxml')
                tables = soup.findAll('table')
                df = pd.read_html(str(tables[2]))[0]
                print(f.name)
                print(df.to_json(orient="values"))
                #return JsonResponse(df.to_json(orient="values"), safe=False)

    return render(request,'countries/upload.html')

class CountrieList(generics.ListAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer

class CountrieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer

