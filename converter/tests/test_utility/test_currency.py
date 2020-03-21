from django.test import TestCase

from unittest.mock import patch
from decimal import Decimal
import datetime
from typing import Mapping, Any
from unittest.mock import MagicMock

from converter.models import Currency
from converter.utility.currency import * 
from converter.tests.utility import * 


class TestCurrencyUtility(TestCase):
	date_valid_components = ('16', '03', '2020')
	currency_data1 = {
		'name': 'Currency 2',
		'code': 'DEF',
		'per': 1,
		'rate': round(Decimal(65.54321), precision)
	}
	currency_data2 = {
		'name': 'Currency 3',
		'code': 'GHI',
		'per': 1,
		'rate': round(Decimal(65.54321), precision)
	}

	@patch('requests.get')
	def test_update_currency_data(self, mock_get: MagicMock) -> None:
		mock_get.return_value = MockResponse()

		currency = create_currency(name='Currency 1',
								   code='ABC',
								   rate=12.12345)
		create_currency(name='Currency 2',
						code='DEF',
						rate=54.54321)
		base_currency = create_currency(name='Currency 4',
										code=Currency.base_code,
										rate=54.54321)
		currencies = Currency.objects.all()

		update_currency_data(existing_currencies=currencies)

		new = Currency.objects.get(code='GHI')
		new_is_valid = is_currency_valid(new, 
								         reference=self.currency_data2,
									     date_valid_components=self.date_valid_components)
		self.assertTrue(new_is_valid)

		updated = Currency.objects.get(code='DEF')
		updated_is_valid = is_currency_valid(updated, 
									         reference=self.currency_data1,
										     date_valid_components=self.date_valid_components)
		self.assertTrue(updated_is_valid)

		self.assertFalse(self._currency_exists(currency))

		self.assertTrue(self._currency_exists(base_currency))

		Currency.objects.all().delete()

	def _currency_exists(self, currency: Currency) -> bool:
		try:
			Currency.objects.get(code=currency.code)
		except:
			return False
		return True

	def test_currency_data_object_gets_created_correctly(self) -> None:
		date_valid = datetime.date(2020, 3, 10)
		data = CurrencyData(name=self.currency_data1['name'], 
							code=self.currency_data1['code'], 
							per=self.currency_data1['per'],
							rate=self.currency_data1['rate'],
							date_valid=date_valid)
		self.assertEqual(data.name, self.currency_data1['name'])
		self.assertEqual(data.code, self.currency_data1['code'])
		self.assertEqual(data.per, self.currency_data1['per'])
		self.assertEqual(data.rate, self.currency_data1['rate'])
		self.assertEqual(data.date_valid, date_valid)

	def test_currency_data_list_gets_created_correctly(self) -> None:
		data_list = self.create_currency_data_list()
		self.assertEqual(data_list.codes, [self.currency_data1['code'], 
								 		   self.currency_data2['code']])

	def _create_currency_data(self, 
							  structure: Mapping[str, Any], 
						      date_valid: datetime.date) -> CurrencyData:
		return CurrencyData(name=structure['name'], 
								     code=structure['code'], 
								     per=structure['per'],
								     rate=structure['rate'],
								     date_valid=date_valid)

	def test_currency_data_list_can_iterate(self) -> None:
		data_list = self.create_currency_data_list()
		for item in data_list:
			self.assertIsInstance(item, CurrencyData)

	def create_currency_data_list(self) -> CurrencyDataList:
		currency1 = self._create_currency_data(structure=self.currency_data1, 
											   date_valid=date_valid)
		currency2 = self._create_currency_data(structure=self.currency_data2, 
											   date_valid=date_valid)
		return CurrencyDataList([currency1, currency2])

class MockResponse:
	def __init__(self):
		self.text = f"""\
		<!DOCTYPE html>
		<html>
		<body>
			<{DATA_ELEMENT_NAME} id="{DATA_ELEMENT_ID}">
				<h2>Курсове на българския лев към отделни чуждестранни валути и цена на златото, 
				валидни за {TestCurrencyUtility.date_valid_components[0]}.{TestCurrencyUtility.date_valid_components[1]}.{TestCurrencyUtility.date_valid_components[2]}</h2>
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
                                    <td class="first">{TestCurrencyUtility.currency_data1['name']}</td>
                                    <td class="center">{TestCurrencyUtility.currency_data1['code']}</td>
                                    <td class="right">{TestCurrencyUtility.currency_data1['per']}</td>
                                    <td class="center">{TestCurrencyUtility.currency_data1['rate']}</td>
                                    <td class="last center">0.930449</td>
                                </tr>
                                <tr class="first">
                                    <td class="first">{TestCurrencyUtility.currency_data2['name']}</td>
                                    <td class="center">{TestCurrencyUtility.currency_data2['code']}</td>
                                    <td class="right">{TestCurrencyUtility.currency_data2['per']}</td>
                                    <td class="center">{TestCurrencyUtility.currency_data2['rate']}</td>
                                    <td class="last center">0.930449</td>
                                </tr>
                                <tr class="first">
                                    <td class="first"></td>
                                </tr>
                            </tbody>
	                    </table>
	                </div>
			</{DATA_ELEMENT_NAME}>
		</body>
		</html>"""