from django import forms



class ChapterForm(forms.Form):
    id_chapter= forms.CharField()
    name = forms.CharField()
    
