from django.shortcuts import render
from rest_framework import generics
from countries.models import Countrie
from countries.serializers import CountrieSerializer
from django.http import HttpResponse
import pandas as pd
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.core import serializers
# Create your views here.
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        web_url=str(uploaded_file.read())
        web_url=web_url.replace("<tr bgcolor=\"#faf290\"><td colspan=\"35\"><font class=\"nota_fuente\"><strong>Fuente:</strong> SAT, SE, BANXICO, INEGI. Balanza Comercial de Mercanc&iacute;as de M&eacute;xico 2003 - 2018. <strong>SNIEG. Informaci&oacute;n de Inter&eacute;s Nacional.</strong></font></td></tr>","")
        web_url=web_url.replace("<tr bgcolor=\"#faf290\"><td colspan=\"35\"><font class=\"nota_fuente\"><strong>Fuente:</strong> SE con base en SAT, SE, BANXICO, INEGI. Balanza Comercial de Mercanc&iacute;as de M&eacute;xico 2003 - 2018 <strong>SNIEG. Informaci&oacute;n de Inter&eacute;s Nacional.</strong></font></td></tr>","")
        web_url=web_url.replace("e width=1038 border=\"1\" cellpadding=\"1\" cellspacing=\"0\"","e")
        web_url=web_url.replace("h scope=\"col\" height=\"25\"","h")
        web_url=web_url.replace("<thead>","")
        web_url=web_url.replace("</thead>","")
        web_url=web_url.replace("r bgcolor=\"#538dd5\"","r")
        web_url=web_url.replace("<div align=\"center\">","")
        web_url=web_url.replace("<font color=\"#FFFFFF\" size=\"2\" face=\"Arial, Helvetica, sans-serif\">","")
        web_url=web_url.replace("<strong>","")
        web_url=web_url.replace("</strong>","")
        web_url=web_url.replace("<font color=\"#FFFFFF\" size=\"1\" face=\"Arial, Helvetica, sans-serif\">","")
        web_url=web_url.replace("d width=\"70\"","d")
        web_url=web_url.replace("</font>","")
        web_url=web_url.replace("</div>","")
        web_url=web_url.replace("h scope=\"col\" width=\"70\"","h")
        web_url=web_url.replace("r class=r bgcolor=\"#ffffff\"","r")
        web_url=web_url.replace("<font size=\"2\" color=\"#000000\">","")
        web_url=web_url.replace("h scope=\"col\" class=\"l\"","h")
        web_url=web_url.replace("<tbody>","")
        web_url=web_url.replace("</tbody>","")
        web_url=web_url.replace("<font color=\"#000000\">", "")
        web_url=web_url.replace("r class=r bgcolor=\"#f2f2f2\"","r")  
        web_url=web_url.replace("d width=\"1000\"","d")
        web_url=web_url.replace("<th>","<td>")
        web_url=web_url.replace("</th>","</td>")
        soup = BeautifulSoup(web_url,'lxml')
        tables = soup.findAll('table')
        df = pd.read_html(str(tables[2]))[0]
        return JsonResponse(df.to_json(orient="values"), safe=False)

    return render(request,'countries/upload.html')

class CountrieList(generics.ListAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer

class CountrieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Countrie.objects.all();
    serializer_class = CountrieSerializer

