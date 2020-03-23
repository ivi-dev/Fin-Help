JsHamcrest.Integration.copyMembers(this);
MockAjax.Integration.jQuery();

QUnit.test('isObject()', function(assert) {
	const result1 = isObject({});
	const result2 = isObject('a');
	assert.ok(result1, '{} is recognized as an object.');
	assert.notOk(result2, '"a" is not recognized as an object.');
});

QUnit.test('isString()', function(assert) {
	const result1 = isString({});
	const result2 = isString('a');
	assert.notOk(result1, '{} is not recognized as a string.');
	assert.ok(result2, '"a" is recognized as a string.');
});

QUnit.test('checkConversionData()', function(assert) {
	const data = {
		amount: 1,
		to: 'ABC',
		from: 'DEF'
	}
	const result = checkConversionData(data);
	assert.strictEqual(result, undefined, 'data checks pass.');

	data.amount = '';
	assert.throws(function() {
		checkConversionData(data);
	}, 
	IncompleteConversionDataError,
	'checkConversionData() throws an IncompleteConversionDataError ' +
	'when a data field is falsy.');
});

QUnit.test('getConversionDataEntriesAsString()', function(assert) {
	const entries = [
		{name: 'amount', value: ''},
		{name: 'to', value: 'ABC'}
	];
	const result1 = getConversionDataEntriesAsString(entries);
	assert.equal(result1, 'amount', 'the name of the missing entry was returned.');

	entries[0].value = 1;
	const result2 = getConversionDataEntriesAsString(entries);
	assert.strictEqual(result2, '', 'an empty string was returned.');
});

QUnit.test('convert()', function(assert) {
	const response = {
		result: 1,
	  	rate_info: {
	  		amount: 1,
	  		from_currency_name: "Currency 1",
	  		from_currency_symbol: "ABC",
	  		rate: 12.12345,
	  		to_currency_name: "Currency 2",
	  		to_currency_symbol: "DEF"
	  	}
  	};
  	const data = getPreConversionData();
	MockAjax.whenRequest({url: is(`convert/?amount=${data.amount}&from=${data.from}&to=${data.to}`)})
		    .thenRespond({data: JSON.stringify(response)});

	convert();
	MockAjax.respond();

	assert.equal(getValue($('#info #conversion-result-value')), 
	 			 response.result, 
	 			 'the result of the conversion is correct.');
	assert.equal(getValue($('#info #amount-value')), 
 			 	 response.rate_info.amount, 
 			 	 'the amount value is correct.');
	assert.equal(getValue($('#info .from-name')), 
 			 	 response.rate_info.from_currency_name, 
 			 	 'the name of the source currency is correct.');
	assert.equal(getValue($('#info .from-symbol')), 
 			 	 response.rate_info.from_currency_symbol, 
 			 	 'the symbol of the source currency is correct.');
	assert.equal(getValue($('#info .rate')), 
 			 	 response.rate_info.rate, 
 			 	 'the rate is correct.');
	assert.equal(getValue($('#info .to-name')), 
 			 	 response.rate_info.to_currency_name, 
 			 	 'the name of the destination currency is correct.');
	assert.equal(getValue($('#info .to-symbol')), 
 			 	 response.rate_info.to_currency_symbol, 
 			 	 'the symbol of the destination currency is correct.');

	MockAjax.whenRequest({url: is(`convert/?amount=${data.amount}&from=${data.from}&to=${data.to}`)})
		    .thenRespond({code: 404});

    convert();
	MockAjax.respond();

	assert.equal(getValue(ALERT_BOX.children('.text-area')), 
				'Адресът на системната заявка не може да бъде намерен. ' +
		     	'Код на грешката: 404', 
		     	'a correct message is displayed in the alert box.');
});