from django.test import TestCase

from converter.models import Currency
from converter.utility.currency import * 
from converter.tests.utility import * 


class TestGeneralUtility(TestCase):
	def test_qs_finds_an_item_by_a_filter(self) -> None:
		currency1 = create_currency(name='Currency 1',
								    code='ABC',
								    per=1,
								    rate=12.12345)
		currency2 = create_currency(name='Currency 2',
								    code='DEF',
								    per=1,
								    rate=23.23456)
		currencies = Currency.objects.all()
		item = qs_find(currencies, ('code', currency2.code))
		self.assertEquals(item.code, currency2.code)

		Currency.objects.all().delete()

	def test_qs_returns_None_if_it_does_not_find_an_item(self) -> None:
		currency1 = create_currency(name='Currency 1',
								    code='ABC',
								    per=1,
								    rate=12.12345)
		currency2 = create_currency(name='Currency 2',
								    code='DEF',
								    per=1,
								    rate=23.23456)
		currencies = Currency.objects.all()
		item = qs_find(currencies, ('code', 'GHI'))
		self.assertIsNone(item)

		Currency.objects.all().delete()