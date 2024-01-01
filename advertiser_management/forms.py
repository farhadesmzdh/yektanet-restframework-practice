from django import forms
from .models import Ad


class AdForm(forms.ModelForm):
    advertiserID = forms.IntegerField()

    class Meta:
        model = Ad
        fields = ['title', 'imgUrl', 'link']