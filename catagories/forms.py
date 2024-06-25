from django import forms
from .models import Catagories

class CatagoriesForm(forms.ModelForm):
    class Meta:
        model = Catagories
        fields = ['name']