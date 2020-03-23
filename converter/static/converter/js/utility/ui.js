function activateButton(button, title) {
	setValue(button, title);
	button.removeAttr('disabled');
}

function deactivateButton(button, title) {
	setValue(button, title);
	button.attr('disabled', true);
}

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

function alert(text) {
	ALERT_BOX.children('.text-area').text(text);
	ALERT_BOX.removeClass('hidden');
}

function hideAlert() {
	ALERT_BOX.addClass('hidden');
}

function updateUIAfterConversion(data) {
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