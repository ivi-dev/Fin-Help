from django.test import TestCase
import datetime
from .utility import * 

from converter.models import Currency


class TestUtility(TestCase):
	def test_create_currency_with_default_data(self) -> None:
		currency = create_currency()
		reference = Currency.objects.all().values()[0]

		is_valid = is_currency_valid(currency, 
							         reference=reference, 
							         date_valid_components=(str(date_valid.day), 
												            str(date_valid.month), 
									                        str(date_valid.year)))
		self.assertTrue(is_valid)
		Currency.objects.all().delete()

	def test_create_currency_with_explicit_data(self) -> None:
		currency = create_currency(name='Currency 3',
								   code='DEF',
								   symbol='D',
								   per=10,
								   rate=23.23456,
								   date_valid=datetime.date(2019, 1, 2))
		reference = Currency.objects.all().values()[0]

		is_valid = is_currency_valid(currency, 
							         reference=reference, 
							         date_valid_components=(str(date_valid.day), 
												            str(date_valid.month), 
									                        str(date_valid.year)))
		self.assertTrue(is_valid)
		Currency.objects.all().delete()

	def test_is_currency_valid_returns_true(self) -> None:
		currency = create_currency(name='Currency 3',
								   code='DEF',
								   symbol='D',
								   per=10,
								   rate=23.23456,
								   date_valid=datetime.date(2019, 1, 2))
		reference = Currency.objects.all().values()[0]

		is_valid = is_currency_valid(currency, 
							         reference=reference, 
							         date_valid_components=(str(date_valid.day), 
												            str(date_valid.month), 
									                        str(date_valid.year)))
		self.assertTrue(is_valid)
		Currency.objects.all().delete()

	def test_is_currency_valid_returns_false(self) -> None:
		currency = create_currency(name='Currency 3',
								   code='DEF',
								   symbol='D',
								   per=10,
								   rate=23.23456,
								   date_valid=datetime.date(2019, 1, 2))
		reference = Currency.objects.all().values()[0]
		reference['name'] = 'Currency'

		is_valid = is_currency_valid(currency, 
							         reference=reference, 
							         date_valid_components=(str(date_valid.day), 
												            str(date_valid.month), 
									                        str(date_valid.year)))
		self.assertFalse(is_valid)
		Currency.objects.all().delete()