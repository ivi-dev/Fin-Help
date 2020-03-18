const ALERT_BOX = $('#alert-box');
const CONVERT_FORM = $('#convert-form');
const AMOUNT_FIELD_SELECTOR = '#amount';
const FROM_FIELD_SELECTOR = '#from';
const TO_FIELD_SELECTOR = '#to';
const VIEW_CURRENCIES_BUTTON = $('#view-currencies');
const CURRENCIES_LIST = $('#currencies-list');
const RATES_URL = 'https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm';

function getValue(element) {
	let elementName;
	if (isObject(element)) {
		return getElementText(element);
	} else if (isString(element)) {
		return getElementText($(element));
	}
}

function setValue(element, text) {
	let elementName;
	if (isObject(element)) {
		return setElementText(element, text);
	} else if (isString(element)) {
		return setElementText($(element), text);
	}
}

function getElementText(element) {
	let elementName;
	elementName = getElementName(element);
	if (!elementName) {
		throw new InvalidElementError('The \'element\' ' +
			'argument doesn\'t seem to be a valid jQuery element.');
	} else if (elementName === 'INPUT' ||
	 	   	   elementName === 'SELECT') {
		return element.val().trim();
	} else {
		return element.text().trim();
	}
}

function setElementText(element, text) {
	let elementName = getElementName(element);
	if (!elementName) {
		throw new InvalidElementError('The \'element\' ' +
			'argument doesn\'t seem to be a valid jQuery element.');
	} else if (elementName === 'INPUT' || 
			   elementName === 'SELECT') {
		return element.val(text);
	} else {
		return element.text(text);
	}
}

function getElementName(element) {
	let name;
	try {
		name = element.prop('nodeName');
	} catch (e) {
		if (e instanceof TypeError) {
			throw new TypeError('The \'element\' argument' + 
			' must be a valid jQuery element.');
		}
	}
	return name;
}

function getPreConversionData(form) {
	let data;
  	if (isObject(form)) {
  		data = extractDataFromForm(form);
	} else if (isString(form)) {
  		data = extractDataFromForm($(form));
	}
	checkConversionData(data);
	return data;
}

function extractDataFromForm(form) {
	const data = {
		amount: form.children(AMOUNT_FIELD_SELECTOR).val(), 
	    from: form.children(FROM_FIELD_SELECTOR).val(), 
	    to: form.children(TO_FIELD_SELECTOR).val()
	};
	return data;
}

function checkConversionData(data) {
	const missing = [];
	for (const [name, value] of Object.entries(data)) {
		if (value === undefined || 
			value === null || 
			value === '') {
			missing.push({name, value});
		}
	}
	if (missing.length) {
		throw new IncompleteConversionDataError(`These pieces ` +
			`of pre-conversion information are missing: ` +
			`${getConversionDataEntriesAsString(missing)}.` +
			` Cannot proceed with the conversion.`);
	}
}

function getConversionDataEntriesAsString(entries) {
	let string = '';
	for (const entry of entries) {
		if (!entry.value) {
			string += `${entry.name}, `;
		}
	}
	return string.trim().replace(/,$/, '');
}

function isObject(arg) {
	return typeof(arg) === 'object';
}

function isString(arg) {
	return typeof(arg) === 'string';
}

function convert(form) {
	let data = getPreConversionData(form);
	return $.ajax('convert/', {
		data: data,
		dataType: 'json'
	});
}

function updateRates() {
	return $.ajax('update-currencies/');
}

function alert(text) {
	ALERT_BOX.children('.text-area').text(text);
	ALERT_BOX.removeClass('hidden');
}

function hideAlert() {
	ALERT_BOX.addClass('hidden');
}

function usePostConversionData(data) {
	setValue($('#info #conversion-result-value'), 
			 data.result);
	setValue($('#info #amount-value'), 
			 data.rate_info.amount);
	setValue($('#info .from-name'), 
			 data.rate_info.from_currency_name);
	setValue($('#info .from-symbol'), 
			 data.rate_info.from_currency_symbol);
	setValue($('#info .rate-value'), 
			 data.rate_info.rate);
	setValue($('#info .to-name'), 
			 data.rate_info.to_currency_name);
	setValue($('#info .to-symbol'), 
			 data.rate_info.to_currency_symbol);
}

function handleNetworkError(status) {
	if (status === 404) {
		alert('Адресът на системната ' + 
		      'заявката не може да бъде намерен.');
	} else if (status === 500) {
		alert('По неизвестна причина, ' +
		      'системата не успя да обработи ' + 
		      'заявката ви.');
	} else {
		alert('Възникна грешка при опита ' +
		      'за калкулация.');
	}
}

function activateButton(button, title) {
	setValue(button, title);
	button.removeAttr('disabled');
}

function deactivateButton(button, title) {
	setValue(button, title);
	button.attr('disabled', true);
}