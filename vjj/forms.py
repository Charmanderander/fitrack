from django import forms
from vjj.models import Suggestion

class suggestion(forms.Form):
    suggestion = forms.CharField(label='What weird stuff do you have in mind?', max_length=200)
    class Meta:
        model = Suggestion
        widgets = {'name': forms.HiddenInput()}
