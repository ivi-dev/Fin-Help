from converter.models import Currency
import datetime
from django.db.models import QuerySet
from typing import Mapping, Tuple, Any


precision = Currency.precision
name = 'Currency 1'
code = 'ABC'
symbol = 'S'
per = 1
rate = 12.12345
date_valid = datetime.date(2020, 2, 3)

def create_currency(**kwargs) -> QuerySet:
	fields = {
		'name': name,
		'code': code,
		'symbol': symbol,
		'per': per,
		'rate': rate,
		'date_valid': date_valid
	}
	if len(kwargs) > 0:
		for key in kwargs:
			fields[key] = kwargs[key]
	Currency.objects.create(**fields)
	return Currency.objects.get(code=fields['code'])

def is_currency_valid(currency: Currency,
			          reference: Mapping[str, Any], 
		              date_valid_components: Tuple[str, str, str]) -> bool:
	date_valid = datetime.date(int(date_valid_components[2]), 
					           int(date_valid_components[1]), 
				               int(date_valid_components[0]))
	for key in reference:
		if reference[key] != getattr(currency, key):
			return False
	else:
		return True