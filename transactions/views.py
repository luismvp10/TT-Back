from django.http import HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from transactions.models import Transaction
import json


@permission_classes((AllowAny,))
def getTransaction(request, section, country, month, year):
    if month is None and country is None:
        query = Transaction.objects.filter(section=section, year=year)
        return HttpResponse(
            groupquery(query), content_type="application/json"
        )
    if month is None and country is not None:
        query = Transaction.objects.filter(section=section, year=year, country=country)
        return HttpResponse(
            groupquery(query), content_type="application/json"
        )
    if country is None and month is not None:
        query = Transaction.objects.filter(section=section, year=year, month=month)
        return HttpResponse(
            groupquery(query), content_type="application/json"
        )
    else:
        query = Transaction.objects.filter(section=section, year=year, month=month, country=country)
        return HttpResponse(
            groupquery(query), content_type="application/json"
        )


def groupquery(query):
    result = {}
    for t in query:
        if t.country.name not in result:
            result[t.country.name] = {
                't' + str(t.id_transaction): {'id_transaction': t.id_transaction, 'price': t.price,
                                              'weight': t.weight, 'kind': t.kind.id_kind,
                                              'section': t.section.name, 'year': t.year.name,
                                              'month': t.month.name}}
        else:
            result[t.country.name]['t' + str(t.id_transaction)] = {'id_transaction': t.id_transaction,
                                                                   'price': t.price,
                                                                   'weight': t.weight, 'kind': t.kind.id_kind,
                                                                   'section': t.section.name,
                                                                   'year': t.year.name, 'month': t.month.name}
    return json.dumps(result, indent=4, ensure_ascii=False)
