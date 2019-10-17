from django import forms
from shipments.models import Shipment


class SubshipmentForm(forms.Form):
    id_subShipment = forms.CharField()
    name = forms.CharField()
    shipments = Shipment.objects.all()

