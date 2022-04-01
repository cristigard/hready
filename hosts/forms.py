from django import forms
from .models import Reservation, City
from django.core.exceptions import ValidationError



class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'rate']


class ReservationForm(forms.ModelForm):
    city = forms.CharField() #if not set, when register_form.save() will trow an error becasue look for City instance
    class Meta:
        model = Reservation
        fields = ['number','checkin','checkout','flat','city','income']

    def clean_city(self):
        city = self.cleaned_data.get("city")
        if not City.objects.filter(name=city).first():
            raise ValidationError(f"City {city} not in DB. Add city first and try again! ")   
        return City.objects.filter(name=city).first()


class UploadFileForm(forms.Form):
    select_file = forms.FileField()

    def clean_select_file(self):
        data = self.cleaned_data.get("select_file")
        if not data.name.endswith('.csv'):
            raise ValidationError("Error! Please select a csv file!")
        return data
