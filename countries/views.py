from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db.models import Count, Sum
from countries.serializers import CountrieSerializer
import pandas as pd
from bs4 import BeautifulSoup
import re
from transactions.models import Transaction
from kinds.models import Kind
from countries.models import Countrie
from sections.models import Section
from years.models import Year
from months.models import Month
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from rest_framework.response import Response
from transactions.models import Transaction


# Create your views here.
@csrf_exempt
@api_view(["POST"])
#@permission_classes((AllowAny,))
def upload(request):
    if request.method == 'POST' and request.FILES.getlist('document'):
        for f in request.FILES.getlist('document'):
            data = str(f.read())
            try:
                section = f.name.split("-")[2].split(".")[0]
            except IndexError:
                return Response({'status': 'El archivo no cuenta con el formato correcto'},
                                status=HTTP_200_OK)
            year = f.name.split("-")[1]
            soup = BeautifulSoup(clean(data), "lxml")
            tables = soup.findAll('table')
            try:
                price_export = pd.read_html(str(tables[2]))[0]
                weight_export = pd.read_html(str(tables[4]))[0]
                price_import = pd.read_html(str(tables[6]))[0]
                weight_import = pd.read_html(str(tables[8]))[0]
            except IndexError:
                return Response({'status': 'El archivo no cuenta con el formato correcto'},
                                status=HTTP_200_OK)
            y = Year.objects.get(name=year)
            try:
                s = Section.objects.get(id_section=int(section))
            except Section.DoesNotExist:
                return Response({'status': 'El archivo no cuenta con el formato correcto'},
                                status=HTTP_200_OK)
                print(section + " doesn't exist")
            transactions = []
            try:
                last_id = Transaction.objects.latest('id_transaction').id_transaction + 1
            except Transaction.DoesNotExist:
                last_id = 1
            if price_export.size > 13:
                k = Kind(id_kind=2, name="Exportaciones")
                for cont in range(price_export.shape[0] - 1):
                    try:
                        c = Countrie.objects.get(name=price_export.iloc[cont + 1, 0])
                        error = 1
                    except Countrie.DoesNotExist:
                        print(price_export.iloc[cont + 1, 0] + " doesn't exist")
                        error = 0
                    for cont2 in range(price_export.shape[1] - 1):
                        try:
                            m = Month.objects.get(id_month=cont2 + 1)
                        except Month.DoesNotExist:
                            print(cont2 + 1)
                            error = 0
                        if error:
                            try:
                                nt = Transaction.objects.get(price=int(price_export.iloc[cont + 1, cont2 + 1]),
                                                             weight=int(weight_export.iloc[cont + 1, cont2 + 1]),
                                                             kind=k, country=c, section=s, year=y, month=m)
                                print("Transaction already exists")
                            except Transaction.DoesNotExist:
                                nt = Transaction(id_transaction=last_id,
                                                 price=int(price_export.iloc[cont + 1, cont2 + 1]),
                                                 weight=int(weight_export.iloc[cont + 1, cont2 + 1]), kind=k, country=c,
                                                 section=s, year=y, month=m)
                                transactions.append(nt)
                                last_id = last_id + 1
            if price_import.size > 13:
                k = Kind(id_kind=1, name="Importaciones")
                for cont in range(price_import.shape[0] - 1):
                    try:
                        c = Countrie.objects.get(name=price_import.iloc[cont + 1, 0])
                        error = 1
                    except Countrie.DoesNotExist:
                        print(price_import.iloc[cont + 1, 0] + " doesn't exist")
                        error = 0
                    for cont2 in range(price_import.shape[1] - 1):
                        try:
                            m = Month.objects.get(id_month=cont2 + 1)
                        except Month.DoesNotExist:
                            print(cont2 + 1)
                            error = 0
                        if error:
                            try:
                                nt = Transaction.objects.get(price=int(price_import.iloc[cont + 1, cont2 + 1]),
                                                             weight=int(weight_import.iloc[cont + 1, cont2 + 1]),
                                                             kind=k, country=c, section=s, year=y, month=m)
                                print("Transaction already exists")
                            except Transaction.DoesNotExist:
                                nt = Transaction(id_transaction=last_id,
                                                 price=int(price_import.iloc[cont + 1, cont2 + 1]),
                                                 weight=int(weight_import.iloc[cont + 1, cont2 + 1]), kind=k, country=c,
                                                 section=s, year=y, month=m)
                                transactions.append(nt)
                                last_id = last_id + 1
            if len(transactions):
                bt = Transaction.objects.bulk_create(transactions)
                return Response({'status': 'El archivo se guardo correctamente'},
                    status=HTTP_200_OK)
            else:
                return Response({'status': 'El archivo ya existe o se encuentra vacio'},
                    status=HTTP_200_OK)
    return Response({'status': 'Error'},
                    status=HTTP_400_BAD_REQUEST)


def clean(data):
    data = re.sub(
        r'<tr bgcolor=.*?</tr>|<font.*?>|<strong>|</strong>|<font>|<div.*?>|</div>|<tbody>|</tbody>|Rep.*?ca|,', '',
        data)
    data = re.sub(
        r'\( de \)|\( de\)|\( Federal de\)|\(Reino de Los\)|\( Popular de\)|\(Comunidad Australiana\)|\(Reino de\)|\( Federativa del\)|de la Gran Bret.*?1a e Irlanda d|antes U\.R\.S\.S\.|\( de la\)|\( del\)|\(Estado de\)|\(Fed.*?n de\)|\(Teritorio de \)',
        '', data)
    data = re.sub(
        r'\(Taipe chino\)|\( Socialista de\)|\(gran Ducado\)|\(gran Ducado\)|\( Islamica del\)|\(sultanato de\)|\( Arabe de\)|\( Dem.*?ca de\)|\( Islamica de\)',
        '', data)
    data = re.sub(r'<table.*?>', '<table>', data)
    data = re.sub(r'<th.*?>', '<td>', data)
    data = re.sub(r'<tr.*?>', '<tr>', data)
    data = re.sub(r'<td.*?>', '<td>', data)
    data = re.sub(r'</th>', '</td>', data)
    data = re.sub(r'Espa.*?1a', 'España', data)
    data = re.sub(r'Canada', 'Canadá', data)
    data = re.sub(r'Japon', 'Japón', data)
    data = re.sub(r'Belgica', 'Bélgica', data)
    data = re.sub(r'Sudafrica', 'Sudáfrica', data)
    data = re.sub(r'Turquia', 'Turquía', data)
    data = re.sub(r'Pakistan', 'Pakistán', data)
    data = re.sub(r'Peru', 'Perú', data)
    data = re.sub(r'Checa', 'República Checa', data)
    data = re.sub(r'Taiwan', 'Taiwán', data)
    data = re.sub(r'Paises Bajos', 'Países Bajos', data)
    data = re.sub(r'Panama', 'Panamá', data)
    data = re.sub(r'Oman', 'Omán', data)
    data = re.sub(r'Iran', 'Irán', data)
    data = re.sub(r'Arabes', 'Árabes', data)
    data = re.sub(r'Hungria', 'Hungría', data)
    data = re.sub(r'Libano', 'Líbano', data)
    data = re.sub(r'Nueva Zelandia', 'Nueva Zelanda', data)
    data = re.sub(r'Dominicana', 'República Dominicana', data)
    data = re.sub(r'Qatar', 'Catar', data)
    data = re.sub(r'Swazilandia', 'Suazilandia', data)
    data = re.sub(r'Eslovaca', 'Eslovaquia', data)
    return data


@permission_classes((AllowAny,))
class CountrieList(generics.ListAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer


@permission_classes((AllowAny,))
class CountrieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer

@permission_classes((AllowAny,))
class CountrieOperation(generics.ListAPIView):
    serializer_class = CountrieSerializer

    def get_queryset(self):
        operation = self.kwargs['operation']
        year = self.kwargs['year']
        if year is None:
            query = Transaction.objects.filter(section__id_section__contains=operation).values('country').annotate(Count('country')).order_by('country')
        else: 
            query = Transaction.objects.filter(section__id_section__contains=operation, year = year).values('country').annotate(Count('country')).order_by('country')
        result = []
        for x in query:
            c = Countrie.objects.get(id_country=x['country'])
            result.append(c)
        return result