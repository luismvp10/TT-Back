from django import forms
from chapters.models import Chapter



class ShipmentForm(forms.Form):
    id_shipment = forms.CharField()
    name = forms.CharField()
    chapter = forms.CharField()
    chapters = Chapter.objects.all()