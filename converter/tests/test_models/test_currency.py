from django.test import TestCase
from decimal import Decimal
from converter.tests.utility import *

class CurrencyTest(TestCase):
	def test_currency_with_all_fields_specified_gets_stored_correctly(self):
		currency = create_currency()
		self.assertEqual(currency.name, name)
		self.assertEqual(currency.code, code)
		self.assertEqual(currency.symbol, symbol)
		self.assertEqual(currency.per, per)
		self.assertEqual(currency.rate, round(Decimal(rate), precision))
		self.assertEqual(currency.date_valid, date_valid)
		currency.delete()

	def test_currency_without_specified_symbol_gets_stored_correctly(self):
		currency = create_currency(with_symbol=False)
		self.assertEqual(currency.name, name)
		self.assertEqual(currency.code, code)
		self.assertEqual(currency.symbol, '')
		self.assertEqual(currency.per, per)
		self.assertEqual(currency.rate, round(Decimal(rate), precision))
		self.assertEqual(currency.date_valid, date_valid)
		currency.delete()

	def test_currency_gets_printed_out_correctly(self):
		currency = create_currency()
		string = str(currency)
		self.assertEqual(string, f'[{currency.code}] {currency.name} | За единица валута: {currency.per} | Курс към лев: {currency.rate}')
		currency.delete()

	def test_currency_gets_the_rate_to_another_currency_with_default_precision(self):
		currency2_code = 'DEF'
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								 	code=currency2_code,
								 	per=1,
								 	rate=54.54321)
		rate = currency1.get_rate_to(currency2_code)
		self.assertEqual(round(rate, precision), 
						 round(Decimal(0.22227), precision))
		currency1.delete()
		currency2.delete()

	def test_currency_gets_the_rate_to_another_currency_that_has_per_more_than_one_with_default_precision(self):
		currency2_code = 'DEF'
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								 	code=currency2_code,
								 	per=10,
								 	rate=54.54321)
		rate = currency1.get_rate_to(currency2_code)
		self.assertEqual(round(rate, precision), 
				         round(Decimal(2.22272), precision))
		currency1.delete()
		currency2.delete()

	def test_currency_gets_the_rate_to_another_currency_that_has_per_more_than_one_with_explicit_precision(self):
		currency2_code = 'DEF'
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								 	code=currency2_code,
								 	per=10,
									rate=54.54321)
		rate = currency1.get_rate_to(currency2_code)
		self.assertEqual(round(rate, 2), round(Decimal(2.22272), 2))
		currency1.delete()
		currency2.delete()

	def test_currency_gets_the_rate_to_another_currency_with_explicit_precision(self):
		currency2_code = 'DEF'
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								 	code=currency2_code,
								 	per=1,
								 	rate=54.54321)
		rate = currency1.get_rate_to(currency2_code)
		self.assertEqual(round(rate, 2), round(Decimal(0.22), 2))
		currency1.delete()
		currency2.delete()

	def test_currency_gets_the_rate_to_another_currency_with_default_precision_and_a_list_of_currencies(self):
		currency2_code = 'DEF'
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								 	code=currency2_code,
								 	per=1,
								 	rate=54.54321)
		currencies = Currency.objects.all()
		rate = currency1.get_rate_to(currency2_code, currencies)
		self.assertEqual(round(rate, precision), 
						 round(Decimal(0.22227), precision))
		currency1.delete()
		currency2.delete()

	def test_convert_currency_to_another_currency_that_has_per_equal_to_one_with_default_precision(self):
		currency2_code = 'DEF'
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								 	code=currency2_code,
								 	per=1,
								 	rate=54.54321)
		result = currency1.convert_to(currency2_code, 1)
		self.assertEqual(round(result, precision), 
						 round(Decimal(0.22227), precision))
		currency1.delete()
		currency2.delete()

	def test_convert_currency_to_another_currency_that_has_per_more_than_one_with_default_precision(self):
		currency2_code = 'DEF'
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								 	code=currency2_code,
								 	per=10,
								 	rate=54.54321)
		result = currency1.convert_to(currency2_code, 1)
		self.assertEqual(round(result, precision), 
						 round(Decimal(2.22272), precision))
		currency1.delete()
		currency2.delete()

	def test_convert_currency_to_another_currency_that_has_per_equal_to_one_with_explicit_precision(self):
		currency2_code = 'DEF'
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
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
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								 	code=currency2_code,
								 	per=10,
								 	rate=54.54321)
		result = currency1.convert_to(currency2_code, 1, precision=2)
		self.assertEqual(round(result, 2), 
						 round(Decimal(2.22272), 2))
		currency1.delete()
		currency2.delete()