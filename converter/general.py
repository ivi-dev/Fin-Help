import requests
import collections
import re
from bs4 import BeautifulSoup

from .models import Currency


RATES_URL = 'https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm'
RATES_ELEMENT_NAME = 'form'
RATES_ELEMENT_ID = 'Exchange_Rate_Search'
ProcessedCurrencyData = collections.namedtuple('ProcessedCurrencyData', 
										       ['new', 'updated'])

def qs_find(queryset, filter):
	for item in queryset:
		if getattr(item, filter[0]) == filter[1]:
			return item

def get_currency_data():
	response = requests.get(RATES_URL)
	html = BeautifulSoup(response.text, 
					     features='lxml')
	form = html.find(RATES_ELEMENT_NAME, 
			         id=RATES_ELEMENT_ID)
	datetime = construct_validity_datetime(form.find('h2').string)
	data = extract_currency_data_from_table(form.table)
	
	return CurrencyDataList(data, datetime)

def construct_validity_datetime(string):
	date = re.match(r'''\d{1,2}\.\d{1,2}\.\d{2,4}''', 
			        date_string).group(0)
	split = date.split('.')
	
	datetime = datetime.datetime.today()
	datetime.day = split[0]
	datetime.month = split[1]
	datetime.year = split[2]

	return datetime

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