from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
import datetime

from .models import Currency
from .utility.currency import update_currency_data


def index(request: HttpRequest) -> None: # pragma: no cover
	currencies = Currency.objects.all()
	from_currency = currencies.first()
	to_currency = from_currency
	context = {
		'currencies': currencies,
		'amount': 1,
		'from_currency': from_currency,
		'to_currency': to_currency,
		'rate': from_currency.get_rate_to(from_currency.code, 
									      list_=currencies,
							              precision=Currency.precision),
		'date_valid': from_currency.date_valid,
		'conversion_result': 1
	}
	return render(request, 'converter/index.html', context)

def convert(request: HttpRequest) -> None: # pragma: no cover
	amount = request.GET['amount']
	from_code = request.GET['from']
	from_currency = Currency.objects.get(code=from_code)
	to_code = request.GET['to']
	to_currency = Currency.objects.get(code=to_code)
	rate = from_currency.get_rate_to(to_code)

	result = from_currency.convert_to(to_code, amount, precision=5)

	return JsonResponse({'result': str(result), 
				         'rate_info': {
				         	'amount': amount,
				         	'from_currency_name': from_currency.name,
				         	'from_currency_symbol': from_currency.symbol,
				         	'rate': str(rate),
				         	'to_currency_name': to_currency.name,
				         	'to_currency_symbol': to_currency.symbol
				        }})

def admin_currencies_list(request: HttpRequest) -> None: # pragma: no cover
	return HttpResponse()

def update_currencies(request: HttpRequest) -> None: # pragma: no cover
	existing = Currency.objects.all()
	result = update_currency_data(existing)
	return redirect('converter:admin-currencies-list')