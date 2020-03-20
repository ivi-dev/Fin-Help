from django.test import TestCase
from django.test import Client
import datetime
from unittest.mock import patch

from converter.models import Currency


class TestViews(TestCase):
	def get_template_names(self, template_list):
		list_ = []
		for template in template_list:
			list_.append(template.name)
		return list_

	def test_index_view(self):
		date_valid = datetime.date(2020, 3, 2)
		currency1 = Currency(name='Currency 1',
							 code='ABC',
							 per=1,
							 rate=12.12345,
							 date_valid=date_valid)
		currency1.save()
		currencies = Currency.objects.all()

		client = Client()
		response = client.get('')

		self._check_index_view_context(response.context, currencies, currency1)
		self._check_index_view_template(response.templates)

	def _check_index_view_context(self, context, currencies, currency):
		self.assertEqual(len(context['currencies']), 
						 len(currencies))
		self.assertEqual(context['amount'], 1)
		self.assertEqual(context['from_currency'], 
						 currency)
		self.assertEqual(context['to_currency'], 
						 currency)
		self.assertEqual(context['rate'], 1)
		self.assertEqual(context['date_valid'], currency.date_valid)
		self.assertEqual(context['conversion_result'], 1)

	def _check_index_view_template(self, templates):
		template_list = self.get_template_names(templates)
		self.assertTrue('converter/index.html' in template_list)

	def test_convert_view(self):
		date_valid = datetime.date(2020, 3, 2)
		currency1 = Currency(name='Currency 1',
							 code='ABC',
							 per=1,
							 rate=12.12345,
							 date_valid=date_valid)
		currency1.save()
		currency2 = Currency(name='Currency 2',
							 code='DEF',
							 per=1,
							 rate=54.54321,
							 date_valid=date_valid)
		currency2.save()
		client = Client()
		response = client.get('/convert/?amount=2&from=ABC&to=DEF')
		self._check_convert_view_response(response)

	def _check_convert_view_response(self, response):
		decoded = response.json()
		self.assertEqual(decoded['result'], '0.44454')
		self.assertEqual(decoded['rate_info']['amount'], '2')
		self.assertEqual(decoded['rate_info']['from_currency_name'], 'Currency 1')
		self.assertEqual(decoded['rate_info']['to_currency_name'], 'Currency 2')
		self.assertEqual(decoded['rate_info']['amount'], '2')
		self.assertEqual(decoded['rate_info']['rate'], '0.22227')

	def test_admin_currencies_list_view(self):
		client = Client()
		response = client.get('/admin/converter/currency/')
		self.assertEqual(response.status_code, 302)

	def test_update_currencies_view(self):
		currency1 = Currency(name='Currency 1',
							 code='ABC',
							 per=1,
							 rate=12.12345,
							 date_valid=datetime.date(2020, 3, 2))
		currency1.save()

		existing = Currency.objects.all()

		client = Client()
		response = client.get('/update-currencies/')

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/admin/converter/currency/32/0/1')

		existing.delete()