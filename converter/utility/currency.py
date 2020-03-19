import requests
import collections
import re
import datetime
from bs4 import BeautifulSoup
from .general import qs_find

from ..models import Currency


RAW_DATA_URL = 'https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm'
DATA_ELEMENT_NAME = 'form'
DATA_ELEMENT_ID = 'Exchange_Rate_Search'


def update_currency_data(existing):
	raw = get_raw_data()
	data = extract_currency_data(raw)
	data_list = CurrencyDataList(data)
	return process_currency_data(data_list, existing)

def get_raw_data():
	response = requests.get(RAW_DATA_URL)
	html = BeautifulSoup(response.text, 
					     features='lxml')
	element = html.find(DATA_ELEMENT_NAME, 
			            id=DATA_ELEMENT_ID)
	return element

def extract_currency_data(raw):
	date_valid = get_validity_date(raw.find('h2').string)
	rows = raw.table.tbody.find_all('tr')
	data = []
	for row in rows:
		cells = row.find_all('td')
		if len(cells) == 5:
			data.append(CurrencyData(cells[0].string,
									 cells[1].string,
									 cells[2].string,
									 cells[3].string,
									 date_valid))
	return data

def get_validity_date(string):
	date = re.findall(r'''\d{1,2}\.\d{1,2}\.\d{2,4}''', string)[0]
	split = date.split('.')
	return datetime.date(int(split[2]), int(split[1]), int(split[0]))

def process_currency_data(data_list, existing):
	new, update, removed = make_lists(data_list, existing)

	Currency.objects.bulk_create(new)
	Currency.objects.bulk_update(update, ['name', 'code', 'per', 'rate'])
	for code in removed:
		Currency.objects.get(code=code).delete()

	return {'added': len(new), 
			'updated': len(update), 
			'removed': len(removed)}

def make_lists(data_list, existing):
	new, updated, to_be_removed = [], [], []
	existing_codes = [currency.code for currency in list(existing)]
	for item in data_list:
		if item.code in existing_codes:
			currency = qs_find(existing, 
						       ('code', item.code))
			currency.name = item.name
			currency.code = item.code
			currency.per = item.per
			currency.rate = item.rate
			currency.date_valid = item.date_valid
			updated.append(currency)
		else:
			currency = Currency(name=item.name,
							    code=item.code,
							    per=item.per,
							    rate=item.rate,
							    date_valid=item.date_valid)
			new.append(currency)
	for code in existing_codes:
		if code not in data_list.codes:
			to_be_removed.append(code)

	return (new, updated, to_be_removed)

class CurrencyData:
	def __init__(self, name, code, per, rate, date_valid):
		self.name = name
		self.code = code
		self.per = per
		self.rate = rate
		self.date_valid = date_valid

class CurrencyDataList:
	def __init__(self, _list):
		self._list = _list
		self.codes = self._collect_codes()
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