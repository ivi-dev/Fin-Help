from django.test import TestCase

from converter.models import Currency
from converter.utility.currency import * 
from converter.tests.utility import * 


class TestGeneralUtility(TestCase):
	def test_qs_finds_and_item_by_a_filter(self):
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