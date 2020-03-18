from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime

from .models import Currency
from .general import get_currency_data, \
					 process_currency_data, \
					 qs_find


def index(request):
	currencies = Currency.objects.all()
	from_currency = currencies.first()
	to_currency = from_currency
	context = {
		'currencies': currencies,
		'amount': 1,
		'from_currency': from_currency,
		'to_currency': to_currency,
		'rate': from_currency.get_rate_to(from_currency.code, 
							              precision=2),
		'latest_rate_update': from_currency.latest_rate_update,
		'conversion_result': 1
	}
	return render(request, 'converter/index.html', context)

def convert(request):
	amount = request.GET['amount']
	from_code = request.GET['from']
	from_currency = Currency.objects.get(code=from_code)
	to_code = request.GET['to']
	to_currency = Currency.objects.get(code=to_code)
	rate = from_currency.get_rate_to(to_code)

	result = from_currency.convert_to(to_code, amount, precision=2)
	return HttpResponse(json.dumps({'result': str(result), 
							        'rate_info': {
							        	'amount': amount,
							        	'from_currency_name': from_currency.name,
							        	'from_currency_symbol': from_currency.symbol,
							        	'rate': str(rate),
							        	'to_currency_name': to_currency.name,
							        	'to_currency_symbol': to_currency.symbol
							        }}))

def update_currencies(request):
	data = get_currency_data()
	existing = Currency.objects.all()
	new, updated = process_currency_data(data, existing)

	Currency.objects.bulk_update(updated, ['name', 'code', 'per', 'rate'])
	Currency.objects.bulk_create(new)

	return HttpResponse('')