from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal



class CityModel(models.Model):
    city = models.CharField(max_length = 25, unique=True)
    commission_percent = models.DecimalField(default=0, max_digits=3, decimal_places=2,
                                        validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f'{self.city}'

    def save(self, *args, **kwargs):
        self.city = self.city.upper()
        super().save(*args, **kwargs)
    

def city_validation(city):
    cities = [city.city for city in CityModel.objects.all()]
    if city not in cities:
        raise ValidationError(f"City {city} does not exists in DB! Please add it first and try again.")

def reservation_validation(reservation):
    if ReservationModel.objects.filter(reservation=reservation).exists():
        raise ValidationError(f"Reservation {reservation} arleady exists in DB!")


class ReservationModel(models.Model):
    reservation = models.CharField(max_length = 25, unique = True, validators = [reservation_validation])
    checkin = models.DateField()
    checkout = models.DateField()
    flat = models.CharField(max_length = 25)
    city = models.CharField(max_length = 25, validators = [city_validation])
    income = models.DecimalField(max_digits=7, decimal_places=2)
    commission = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.reservation}'

    def save(self, *args, **kwargs):
        cities = {city.city:city.commission_percent for city in CityModel.objects.all()}
        self.commission = self.income * cities[self.city]
        super().save(*args, **kwargs)