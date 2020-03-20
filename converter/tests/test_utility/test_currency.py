from django.test import TestCase

from unittest.mock import patch
from decimal import Decimal
import datetime

from converter.models import Currency
from converter.utility.currency import * 
from converter.tests.utility import * 


date_valid_components = ('16', '03', '2020')
currency_data1 = {
	'name': 'Currency 2',
	'code': 'DEF',
	'per': 1,
	'rate': 65.54321
}
currency_data2 = {
	'name': 'Currency 3',
	'code': 'GHI',
	'per': 1,
	'rate': 65.54321
}

class TestCurrencyUtility(TestCase):
	@patch('requests.get')
	def test_update_currency_data(self, mock_get):
		mock_get.return_value = MockResponse()

		create_currency(name='Currency 1',
						code='ABC',
						per=1,
						rate=12.12345)
		create_currency(name='Currency 2',
						code='DEF',
						per=1,
						rate=54.54321)
		currencies = Currency.objects.all()

		update_currency_data(existing_currencies=currencies)

		new = Currency.objects.get(code='GHI')
		self.assertEqual(new.name, currency_data2['name'])
		self.assertEqual(new.code, currency_data2['code'])
		self.assertEqual(new.per, currency_data2['per'])
		self.assertEqual(new.rate, round(Decimal(currency_data2['rate']), 
										 Currency.precision))
		self.assertEqual(new.date_valid, datetime.date(int(date_valid_components[2]), 
													   int(date_valid_components[1]), 
												       int(date_valid_components[0])))

		updated = Currency.objects.get(code='DEF')
		self.assertEqual(updated.name, currency_data1['name'])
		self.assertEqual(updated.code, currency_data1['code'])
		self.assertEqual(updated.per, currency_data1['per'])
		self.assertEqual(updated.rate, round(Decimal(currency_data1['rate']), 
										     Currency.precision))
		self.assertEqual(new.date_valid, datetime.date(int(date_valid_components[2]), 
													   int(date_valid_components[1]), 
												       int(date_valid_components[0])))

		self.assertRaises(Currency.DoesNotExist, 
					      lambda: Currency.objects.get(code='ABC'))

		Currency.objects.all().delete()

	def test_currency_data_object_gets_created_correctly(self):
		date_valid = datetime.date(2020, 3, 10)
		data = CurrencyData(name=currency_data1['name'], 
							code=currency_data1['code'], 
							per=currency_data1['per'],
							rate=currency_data1['rate'],
							date_valid=date_valid)
		self.assertEqual(data.name, currency_data1['name'])
		self.assertEqual(data.code, currency_data1['code'])
		self.assertEqual(data.per, currency_data1['per'])
		self.assertEqual(data.rate, currency_data1['rate'])
		self.assertEqual(data.date_valid, date_valid)

	def test_currency_data_list_gets_created_correctly(self):
		data_list = self.create_currency_data_list()
		self.assertEqual(data_list.codes, [currency_data1['code'], 
								 		   currency_data2['code']])

	def create_currency_data_list(self) -> CurrencyDataList:
		currency1 = CurrencyData(name=currency_data1['name'], 
							     code=currency_data1['code'], 
							     per=currency_data1['per'],
							     rate=currency_data1['rate'],
							     date_valid=date_valid)
		currency2 = CurrencyData(name=currency_data2['name'], 
							     code=currency_data2['code'], 
							     per=currency_data2['per'],
							     rate=currency_data2['rate'],
							     date_valid=date_valid)
		return CurrencyDataList([currency1, currency2])

	def test_currency_data_list_can_iterate(self):
		data_list = self.create_currency_data_list()
		for item in data_list:
			self.assertIsInstance(item, CurrencyData)

class MockResponse:
	def __init__(self):
		self.text = f"""\
		<!DOCTYPE html>
		<html>
		<body>
			<{DATA_ELEMENT_NAME} id="{DATA_ELEMENT_ID}">
				<h2>Курсове на българския лев към отделни чуждестранни валути и цена на златото, валидни за {date_valid_components[0]}.{date_valid_components[1]}.{date_valid_components[2]}</h2>
                    <div class="table_box">
                        <table cellpadding="0" cellspacing="0" class="table">
                            <col width="600" />
                            <col width="80" />
                            <col width="110" />
                            <col width="80" />
                            <col width="110" />
                            <thead>
                                <tr class="header_cells">
                                    <th class="first">Наименование</th>
                                    <th>Код</th>
                                    <th>За единица валута/злато</th>
                                    <th>Лева (BGN)</th>
                                    <th class="last">Обратен курс: за един лев</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="first">
                                    <td class="first">{currency_data1['name']}</td>
                                    <td class="center">{currency_data1['code']}</td>
                                    <td class="right">{currency_data1['per']}</td>
                                    <td class="center">{currency_data1['rate']}</td>
                                    <td class="last center">0.930449</td>
                                </tr>
                                <tr class="first">
                                    <td class="first">{currency_data2['name']}</td>
                                    <td class="center">{currency_data2['code']}</td>
                                    <td class="right">{currency_data2['per']}</td>
                                    <td class="center">{currency_data2['rate']}</td>
                                    <td class="last center">0.930449</td>
                                </tr>
                            </tbody>
	                    </table>
	                </div>
			</{DATA_ELEMENT_NAME}>
		</body>
		</html>"""