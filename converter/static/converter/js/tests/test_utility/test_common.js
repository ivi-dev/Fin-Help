JsHamcrest.Integration.copyMembers(this);
MockAjax.Integration.jQuery();
const INITIAL_FROM_VALUE = getValue(FROM_FIELD);

function postConversionUIIsCorrect(assert, response) {
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
	return true;
}

QUnit.test('isObject() recognizes {} as an object', function(assert) {
	const result1 = isObject({});
	assert.ok(result1);
});

QUnit.test('isObject() recognizes a string as a non-object', function(assert) {
	const result2 = isObject('a');
	assert.notOk(result2);
});

QUnit.test('isString() recognizes a string as such', function(assert) {
	const result2 = isString('a');
	assert.ok(result2);
});

QUnit.test('isString() recognizes a {} as a non-string', function(assert) {
	const result1 = isString({});
	assert.notOk(result1);
});

QUnit.test('checkConversionData() completes succesfully', function(assert) {
	const data = {
		amount: 1,
		to: 'ABC',
		from: 'DEF'
	}
	const result = checkConversionData(data);
	assert.strictEqual(result, undefined, 'data checks pass.');
});

QUnit.test('checkConversionData() throws on a falsy value', function(assert) {
	const data = {
		amount: '',
		to: 'ABC',
		from: 'DEF'
	}

	assert.throws(function() {
		checkConversionData(data);
	}, 
	IncompleteConversionDataError,
	'checkConversionData() throws an IncompleteConversionDataError ' +
	'when a data field is falsy.');
});

QUnit.test('getConversionDataEntriesAsString() returns the ' +
		   'name of a missing entry', 
		   function(assert) {
				const entries = [
					{name: 'amount', value: ''},
					{name: 'to', value: 'ABC'}
				];
				const result1 = getConversionDataEntriesAsString(entries);
				assert.equal(result1, 'amount');
});

QUnit.test('a successful request from convert() is handled', 
	function(assert) {
		MockAjax.whenRequest({url: is(CONVERT_URL)})
			    .thenRespond({data: JSON.stringify(CONVERT_RESPONSE)});

		convert();
		MockAjax.respond();

		const result = postConversionUIIsCorrect(assert, CONVERT_RESPONSE);
		assert.ok(result);
});

QUnit.test('a 404 network error from convert() is handled', 
	function(assert) {
		const errorCode = 404;
		MockAjax.whenRequest({url: is(CONVERT_URL)})
			    .thenRespond({status: errorCode});

	    convert();
		MockAjax.respond();

		assert.equal(getValue(ALERT_BOX.children('.text-area')), 
					'Адресът на системната заявка не може да бъде намерен. ' +
			     	`Код на грешката: ${errorCode}`);
});

QUnit.test('a 500 network error from convert() is handled', 
	function(assert) {
		const errorCode = 500;
		MockAjax.whenRequest({url: is(CONVERT_URL)})
			    .thenRespond({status: errorCode});

	    convert();
		MockAjax.respond();

		assert.equal(getValue(ALERT_BOX.children('.text-area')), 
					'По неизвестна причина, ' +
			        'системата не успя да обработи ' + 
			        `заявката ви. Код на грешката: ${errorCode}`);
});

QUnit.test('a network error, different from 404 or 500 from convert() is handled', 
	function(assert) {
		const errorCode = 501;
		MockAjax.whenRequest({url: is(CONVERT_URL)})
			    .thenRespond({status: errorCode});

	    convert();
		MockAjax.respond();

		assert.equal(getValue(ALERT_BOX.children('.text-area')), 
					'Възникна грешка при обработката ' +
			  	    `на заявката ви. Код на грешката: ${errorCode}`);
});

QUnit.test('an IncompleteConversionDataError error from convert() is handled', 
	function(assert) {
		setValue(FROM_FIELD, '');

		convert();

		assert.equal(getValue(ALERT_BOX.children('.text-area')), 
					'Калкулацията е прекратена, тъй като ' +
			  		'липсват някои необходими данни за нея.');

		setValue(FROM_FIELD, INITIAL_FROM_VALUE);
});

QUnit.test('the title of the convert button is restored after ' +
		   'a successful request from convert()', 
	function(assert) {
		MockAjax.whenRequest({url: is(CONVERT_URL)})
			    .thenRespond({data: JSON.stringify(CONVERT_RESPONSE)});

		convert();
		MockAjax.respond();

		assert.equal(getValue(CONVERT_BUTTON), 
				     CONVERT_BUTTON_ORIGINAL_TITLE);
});

QUnit.test('the title of the convert button is restored after ' +
		   'a failed request from convert()', 
	function(assert) {
		MockAjax.whenRequest({url: is(CONVERT_URL)})
			    .thenRespond({status: 404});

	    convert();
		MockAjax.respond();

		assert.equal(getValue(CONVERT_BUTTON), 
				     CONVERT_BUTTON_ORIGINAL_TITLE);
});

QUnit.test('the title of the convert button is restored after ' +
		   'an exception from convert() is handled', 
	function(assert) {
		setValue(FROM_FIELD, '');

		convert();

		assert.equal(getValue(CONVERT_BUTTON), 
				     CONVERT_BUTTON_ORIGINAL_TITLE);

		setValue(FROM_FIELD, INITIAL_FROM_VALUE);
});