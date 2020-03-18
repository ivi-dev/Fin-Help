RATES_URL = 'https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm'
RATES_ELEMENT_NAME = 'form'
RATES_ELEMENT_ID = 'Exchange_Rate_Search'

def qs_find(queryset, filter):
	for item in queryset:
		if getattr(item, filter[0]) == filter[1]:
			return item