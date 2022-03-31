from django.test import TestCase
from .models import CityModel, ReservationModel
from decimal import Decimal



class UnitTestCase(TestCase):

	def test_template(self):
		response = self.client.get('/upload/')
		self.assertTemplateUsed(response, 'hosts/upload_file.html')

	def test_dbs(self):
		CityModel.objects.create(city="CLUJ", commission_percent = Decimal(0.1))
		ReservationModel.objects.create(reservation='HH001', checkin='2020-10-10', 
			                            city='CLUJ', checkout= '2020-10-15', flat= "Jamal", income=Decimal(1000))
		self.assertEqual(ReservationModel.objects.filter(city="CLUJ").first().commission, Decimal(100))
