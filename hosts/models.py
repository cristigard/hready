from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal



class City(models.Model):
    name = models.CharField(max_length = 25, unique=True)
    rate = models.DecimalField(default=0, max_digits=3, decimal_places=2,
                                        validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)


def reservation_number_validation(number):
    if Reservation.objects.filter(number=number).exists():
        raise ValidationError(f"Reservation number {number} arleady uploaded!")


class Reservation(models.Model):
    number = models.CharField(max_length = 25, unique = True, validators = [reservation_number_validation])
    checkin = models.DateField()
    checkout = models.DateField()
    flat = models.CharField(max_length = 25)
    city = models.ForeignKey(City, on_delete = models.CASCADE)
    income = models.DecimalField(max_digits=7, decimal_places=2)
    commission = models.DecimalField(default = 0, max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.number}'

    def save(self, *args, **kwargs):
        cities = {city.name:city.rate for city in City.objects.all()}
        self.commission = self.income * cities[self.city.name]  
        super().save(*args, **kwargs)
    