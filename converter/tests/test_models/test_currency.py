from django.test import TestCase
from decimal import Decimal
import datetime

from converter.models import Currency


class CurrencyTest(TestCase):
	precision = Currency.precision

	name = 'Currency 1'
	code = 'ABC'
	symbol = 'S'
	per = 1
	rate = 12.12345
	date_valid = datetime.date(2020, 2, 3)

	def create_currency(self, with_code=True, **kwargs):
		fields: dict
		fields = {
			'name': self.name,
			'code': self.code,
			'symbol': self.symbol,
			'per': self.per,
			'rate': self.rate,
			'date_valid': self.date_valid
		} if with_code is True \
		  else {
		  	  'name': self.name,
		  	  'code': self.code,
		  	  'per': self.per,
		  	  'rate': self.rate,
		  	  'date_valid': self.date_valid
		  }
		if kwargs is not None:
			for key in kwargs:
				fields[key] = kwargs[key]
		Currency.objects.create(**fields)
		return Currency.objects.get(code=self.code)

	def test_currency_with_all_fields_specified_gets_stored_correctly(self):
		currency = self.create_currency()
		self.assertEqual(currency.name, self.name)
		self.assertEqual(currency.code, self.code)
		self.assertEqual(currency.symbol, self.symbol)
		self.assertEqual(currency.per, self.per)
		self.assertEqual(currency.rate, round(Decimal(self.rate), self.precision))
		self.assertEqual(currency.date_valid, self.date_valid)
		currency.delete()

	def test_currency_without_specified_symbol_gets_stored_correctly(self):
		currency = self.create_currency(with_code=False)
		self.assertEqual(currency.name, self.name)
		self.assertEqual(currency.code, self.code)
		self.assertEqual(currency.symbol, '')
		self.assertEqual(currency.per, self.per)
		self.assertEqual(currency.rate, round(Decimal(self.rate), self.precision))
		self.assertEqual(currency.date_valid, self.date_valid)
		currency.delete()

	def test_currency_gets_printed_out_correctly(self):
		currency = self.create_currency()
		string = str(currency)
		self.assertEqual(string, f'{currency.name} [{currency.code}] | За единица валута: {currency.per} | Курс към лев: {currency.rate}')
		currency.delete()

	def test_currency_gets_the_rate_to_another_currency_with_default_precision(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=1,
										 rate=54.54321)
		rate = currency1.get_rate_to(currency2_code)
		self.assertEqual(round(rate, self.precision), 
						 round(Decimal(0.22227), self.precision))
		currency1.delete()
		currency2.delete()

	def test_currency_gets_the_rate_to_another_currency_that_has_per_more_than_one_with_default_precision(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=10,
										 rate=54.54321)
		rate = currency1.get_rate_to(currency2_code)
		self.assertEqual(round(rate, self.precision), 
				         round(Decimal(2.22272), self.precision))
		currency1.delete()
		currency2.delete()

	def test_currency_gets_the_rate_to_another_currency_that_has_per_more_than_one_with_explicit_precision(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=10,
										 rate=54.54321)
		rate = currency1.get_rate_to(currency2_code)
		self.assertEqual(round(rate, 2), round(Decimal(2.22272), 2))
		currency1.delete()
		currency2.delete()

	def test_currency_gets_the_rate_to_another_currency_with_explicit_precision(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=1,
										 rate=54.54321)
		rate = currency1.get_rate_to(currency2_code)
		self.assertEqual(round(rate, 2), round(Decimal(0.22), 2))
		currency1.delete()
		currency2.delete()

	def test_currency_gets_the_rate_to_another_currency_with_default_precision_and_a_list_of_currencies(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=1,
										 rate=54.54321)
		currencies = Currency.objects.all()
		rate = currency1.get_rate_to(currency2_code, currencies)
		self.assertEqual(round(rate, self.precision), 
						 round(Decimal(0.22227), self.precision))
		currency1.delete()
		currency2.delete()

	def test_convert_currency_to_another_currency_that_has_per_equal_to_one_with_default_precision(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=1,
										 rate=54.54321)
		result = currency1.convert_to(currency2_code, 1)
		self.assertEqual(round(result, self.precision), 
						 round(Decimal(0.22227), self.precision))
		currency1.delete()
		currency2.delete()

	def test_convert_currency_to_another_currency_that_has_per_more_than_one_with_default_precision(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=10,
										 rate=54.54321)
		result = currency1.convert_to(currency2_code, 1)
		self.assertEqual(round(result, self.precision), 
						 round(Decimal(2.22272), self.precision))
		currency1.delete()
		currency2.delete()

	def test_convert_currency_to_another_currency_that_has_per_equal_to_one_with_explicit_precision(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=1,
										 rate=54.54321)
		result = currency1.convert_to(currency2_code, 1, precision=2)
		self.assertEqual(round(result, 2), 
						 round(Decimal(0.22227), 2))
		currency1.delete()
		currency2.delete()

	def test_convert_currency_to_another_currency_that_has_per_more_than_one_with_explicit_precision(self):
		currency2_code = 'DEF'
		currency1 = self.create_currency()
		currency2 = self.create_currency(name='Currency 2',
										 code=currency2_code,
										 per=10,
										 rate=54.54321)
		result = currency1.convert_to(currency2_code, 1, precision=2)
		self.assertEqual(round(result, 2), 
						 round(Decimal(2.22272), 2))
		currency1.delete()
		currency2.delete()