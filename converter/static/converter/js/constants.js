const ALERT_BOX = $('#alert-box');

const CONVERT_FORM = $('#convert-form');
const AMOUNT_FIELD = CONVERT_FORM.children('#amount');
const FROM_FIELD = CONVERT_FORM.children('#from');
const TO_FIELD = CONVERT_FORM.children('#to');
const FLIP_BUTTON = CONVERT_FORM.children('button#flip');
const CONVERT_BUTTON = CONVERT_FORM.children('button#convert');
const CONVERT_BUTTON_ORIGINAL_TITLE = CONVERT_BUTTON.text().trim();
const CONVERT_BUTTON_BUSY_TITLE = 'КАЛКУЛИРАМ...';

const CURRENCIES_LIST = $('#currencies-list');
const VIEW_CURRENCIES_BUTTON = $('#view-currencies');
const RATES_URL = 'https://www.bnb.bg/Statistics/StExternalSector' +
			      '/StExchangeRates/StERForeignCurrencies/index.htm';