from django import forms

from subshipments.models import Subshipment
from units.models import Unity


class SectionForm(forms.Form):
    id_section = forms.CharField()
    name = forms.CharField()
    subshipments =Subshipment.objects.all()
    units = Unity.objects.all()