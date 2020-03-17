from django.shortcuts import render
from django.http import HttpResponse
import json

from .models import Currency


def index(request):
	currencies = Currency.objects.all()
	context = {
		'currencies': currencies,
		'amount': 1,
		'from_currency': currencies[0],
		'to_currency': currencies[0],
		'rate': currencies[0].get_rate_to(currencies[0].code, precision=2),
		'latest_rate_update': currencies[0].latest_rate_update,
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
							        	'from_currency_name': from_currency.name,
							        	'from_currency_symbol': from_currency.symbol,
							        	'rate': str(rate),
							        	'to_currency_name': to_currency.name,
							        	'to_currency_symbol': to_currency.symbol
							        }
							      }))