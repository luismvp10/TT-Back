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
from transactions.models import Transaction
from kinds.models import Kind
from countries.models import Countrie
from sections.models import Section
from subshipments.models import Subshipment
from chapters.models import Chapter
from years.models import Year
from months.models import Month
from shipments.models import Shipment
from units.models import Unity

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
                name = f.name
                name = name[len(name)-12:len(name)-4]
                soup = BeautifulSoup(data,'lxml')
                tables = soup.findAll('table')
                price = pd.read_html(str(tables[2]))[0]
                weight = pd.read_html(str(tables[4]))[0]
                months=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
                if price.size > 13:
                    for cont in range(price.shape[0]-1):
                        for cont2  in range(price.shape[1]-1):
                            k = Kind(id_kind=0,name="Exportaciones")
                            c = Countrie(id_country=484,name="México",iso2="MX",iso3="MEX")
                            ch = Chapter(id_chapter=int(name[0:2]),name="Niquel y manufacturas de niquel")
                            sh = Shipment(id_shipment=int(name[0:4]),name="Las demás manufacturas de níquel",chapter=ch)
                            ss = Subshipment(id_subShipment=int(name[0:6]),name="Las demás",shipment=sh)
                            s = Section(id_section=int(name),name="Las demás",subShipment=ss,id_unity=Unity(id_unity=0,name="kg"))
                            y = Year(id_year=2018,name="2018")
                            m = Month(id_month=cont2,name=months[cont2])
                            nt = Transaction(id_transaction=cont2,price=int(price.iloc[cont+1,cont2+1]),weight=int(weight.iloc[cont+1,cont2+1]),kind=k,country=c,section=s,year=y,month=m)
                            print(nt)
                            nt.save()
                            #print(price.iloc[cont+1,cont2+1])
                    return JsonResponse(price.to_json(orient="values"), safe=False)
                #print(f.name)
                #print(df.to_json(orient="values"))
    return render(request,'countries/upload.html')

class CountrieList(generics.ListAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer

class CountrieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer
