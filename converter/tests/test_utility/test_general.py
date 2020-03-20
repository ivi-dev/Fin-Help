from django.test import TestCase

from converter.models import Currency
from converter.utility.currency import * 


class TestGeneralUtility(TestCase):
	def test_qs_finds_and_item_by_a_filter(self):
		currency1 = Currency(name='Currency 1',
							 code='ABC',
							 per=1,
							 rate=12.12345)
		currency1.save()
		currency2 = Currency(name='Currency 2',
							 code='DEF',
							 per=1,
							 rate=23.23456)
		currency2.save()
		currencies = Currency.objects.all()
		item = qs_find(currencies, ('code', 'DEF'))
		self.assertEquals(item, currency2)