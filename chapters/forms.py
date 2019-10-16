from django import forms
from chapters.models import Chapter


class ChapterForm(forms.Form):
    id_chapter= forms.CharField()
    name = forms.CharField()
    
