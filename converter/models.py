from decimal import Decimal
import datetime
import requests
import collections
import re
from bs4 import BeautifulSoup

from django.db import models
from .general import qs_find


ProcessedCurrencyData = collections.namedtuple('ProcessedCurrencyData', 
										       ['new', 'updated'])

class Currency(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=3)
	symbol = models.CharField(max_length=5, default='')
	per = models.IntegerField(default=1)
	rate = models.DecimalField(max_digits=10, decimal_places=5)
	date_added = models.DateTimeField(default=datetime.datetime.today())
	latest_rate_update = models.DateTimeField(default=datetime.datetime.today())

	def __str__(self):
		return f'{self.name} {self.code} {self.per} {self.rate}'

	def get_rate_to(self, code, list_=None, precision=5):
		currency = None
		if list_ is None:
			currency = Currency.objects.only('per', 'rate') \
							   		   .get(code=code)
		else:
			currency = qs_find(list_, ('code', code))
		result = self._convert(1, to=currency)
		return round(result, precision)

	def convert_to(self, code, amount, precision=5):
		currency = Currency.objects.only('per', 'rate') \
							       .get(code=code)
		result = self._convert(amount, to=currency)
		return round(result, precision)

	def _convert(self, amount, to):
		base = self._to_base(Decimal(amount))
		rate = self._get_rate(to)
		result = base / rate \
				 if to.rate > 1 \
				 else base * rate
		return result

	def _to_base(self, amount):
		rate = self.rate \
			   if self.per == 1 \
			   else self.rate / self.per
		result = rate * amount \
			     if self.rate > 1 \
			     else rate / amount
		return result

	def _get_rate(self, currency):
		result = currency.rate \
			     if currency.per == 1 \
			     else currency.rate / \
					  currency.per
		return result

	@staticmethod
	def update_currency_data(existing):
		response = requests.get(RATES_URL)
		html = BeautifulSoup(response.text, 
						     features='lxml')
		form = html.find(RATES_ELEMENT_NAME, 
				         id=RATES_ELEMENT_ID)
		date = construct_validity_datetime(form.find('h2').string)
		extracted = extract_currency_data_from_table(form.table)
		
		data = CurrencyDataList(extracted, date)
		new, updated = self.process_currency_data(data, existing)
		Currency.objects.bulk_update(updated, ['name', 'code', 'per', 'rate'])
		Currency.objects.bulk_create(new)

	@staticmethod
	def extract_currency_data_from_table(table):
		rows = table.tbody.find_all('tr')
		data = []
		for row in rows:
			cells = row.find_all('td')
			if len(cells) == 5:
				data.append(CurrencyData(cells[0].string,
										 cells[1].string,
										 cells[2].string,
										 cells[3].string))
		return data

	@staticmethod
	def process_currency_data(data, existing):
		new, updated = [], []
		codes = [currency.code for currency in list(existing)]

		for item in data:
			if item.code in codes:
				currency = qs_find(existing, 
							       ('code', item.code))
				currency.name = item.name
				currency.code = item.code
				currency.per = item.per
				currency.rate = item.rate
				updated.append(currency)
			else:
				currency = Currency(name=item.name,
								    code=item.code,
								    per=item.per,
								    rate=item.rate)
				new.append(currency)

		return ProcessedCurrencyData(new, updated)

	class Meta:
		verbose_name_plural = "currencies"


class CurrencyData:
	def __init__(self, name, code, per, rate):
		self.name = name
		self.code = code
		self.per = per
		self.rate = rate

class CurrencyDataList:
	def __init__(self, _list):
		self._list = _list
		self._codes = self._collect_codes()
		self._index = 0

	def _collect_codes(self):
		codes = []
		for currency in self._list:
			codes.append(currency.code)
		return codes

	def __iter__(self):
		return iter(self._list)

	def __next__(self):
		if self._index == len(self._list) - 1:
			raise StopIteration()
		else:
			currency_data = self._list[self._index]
			self._index += 1
			return currency_data