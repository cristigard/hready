from django import forms
from .models import ReservationModel, CityModel
from django.core.exceptions import ValidationError


class CityModelForm(forms.ModelForm):
    class Meta:
        model = CityModel
        fields = ['city', 'commission_percent']


class ReservationModelForm(forms.ModelForm):
    class Meta:
        model = ReservationModel
        fields = ['reservation','checkin','checkout','flat','city','income']


class UploadFileForm(forms.Form):
    select_file = forms.FileField()

    def clean_select_file(self):
        data = self.cleaned_data.get("select_file")
        if not data.name.endswith('.csv'):
            raise ValidationError("Error! Please select a csv file!")
        return data
