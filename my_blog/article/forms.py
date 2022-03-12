from django import forms
from .models import Articlepost

class Articlepostform(forms.ModelForm):
    class Meta:
        model = Articlepost
        fields = ('title', 'body')