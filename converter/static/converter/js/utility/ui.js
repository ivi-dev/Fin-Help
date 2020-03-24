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
		const value = element.val();
		return value ? value.trim() : '';
	} else {
		const text = element.text();
		return text ? text.trim() : '';
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

function getPreConversionData() {
	let data = extractDataFromForm();
	checkConversionData(data);
	return data;
}

function extractDataFromForm() {
	const data = {
		amount: getValue(AMOUNT_FIELD), 
	    from: getValue(FROM_FIELD), 
	    to: getValue(TO_FIELD)
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

function updateUI(data) {
	setValue($('#info #conversion-result-value'), 
			 data.result);
	setValue($('#info #amount-value'), 
			 data.rate_info.amount);
	setValue($('#info .from-name'), 
			 data.rate_info.from_currency_name);
	setValue($('#info .from-symbol'), 
			 data.rate_info.from_currency_symbol);
	setValue($('#info .rate'), 
			 data.rate_info.rate);
	setValue($('#info .to-name'), 
			 data.rate_info.to_currency_name);
	setValue($('#info .to-symbol'), 
			 data.rate_info.to_currency_symbol);
}