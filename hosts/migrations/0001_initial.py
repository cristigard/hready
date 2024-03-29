# Generated by Django 4.0.3 on 2022-04-01 08:34

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hosts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=25, unique=True, validators=[hosts.models.reservation_number_validation])),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('flat', models.CharField(max_length=25)),
                ('income', models.DecimalField(decimal_places=2, max_digits=7)),
                ('commission', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.city')),
            ],
        ),
    ]
