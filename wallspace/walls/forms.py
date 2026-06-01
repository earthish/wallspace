from django import forms
from .models import Wall


class WallForm(forms.ModelForm):
    class Meta:
        model = Wall
        fields = ['title']