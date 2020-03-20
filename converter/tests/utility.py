from converter.models import Currency
import datetime
from django.db.models import QuerySet


precision = Currency.precision
name = 'Currency 1'
code = 'ABC'
symbol = 'S'
per = 1
rate = 12.12345
date_valid = datetime.date(2020, 2, 3)

def create_currency(with_symbol=True, **kwargs) -> QuerySet:
	fields: dict
	fields = {
		'name': name,
		'code': code,
		'symbol': symbol,
		'per': per,
		'rate': rate,
		'date_valid': date_valid
	} if with_symbol is True \
	  else {
	  	  'name': name,
	  	  'code': code,
	  	  'per': per,
	  	  'rate': rate,
	  	  'date_valid': date_valid
	  }
	if kwargs is not None:
		for key in kwargs:
			fields[key] = kwargs[key]
	Currency.objects.create(**fields)
	return Currency.objects.get(code=code)