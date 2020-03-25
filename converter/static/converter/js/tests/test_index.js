QUnit.test('clicking on the convert button with a ' +
		   'conversion amount different than zero calls ' +
		   'hideAlert(), deactivateButton() convert()',
	function(assert) {
		const done = assert.async();
		setTimeout(function() {
			const fakeConvert = sinon.fake();
			const fakeHideAlert = sinon.fake();
			const fakeDeactivateButton = sinon.fake();
			sinon.replace(window, 'convert', fakeConvert);
			sinon.replace(window, 'hideAlert', fakeHideAlert);
			sinon.replace(window, 'deactivateButton', fakeDeactivateButton);

			CONVERT_BUTTON.click();

			assert.ok(fakeConvert.called);
			assert.ok(fakeHideAlert.called);
			assert.ok(fakeDeactivateButton.called);

			sinon.restore();
			done();
		}, DELAY);
});

QUnit.test('clicking on the convert button with a ' +
		   'conversion amount equal to zero doesn\'t call ' +
		   'convert()',
	function(assert) {
		const done = assert.async();
		setTimeout(function() {
			setValue(AMOUNT_FIELD, 0);
			const fakeConvert = sinon.fake();
			sinon.replace(window, 'convert', fakeConvert);

			CONVERT_BUTTON.click();

			assert.ok(fakeConvert.notCalled);

			sinon.restore();
			setValue(AMOUNT_FIELD, 1);
			done();
		}, DELAY);
});

QUnit.test('clicking on the flip button swaps the values ' +
		   'of the from and to fields',
	function(assert) {
		const done = assert.async();
		setTimeout(function() {
			const fromBefore = getValue(FROM_FIELD);
			const toBefore = getValue(TO_FIELD);

			setValue(FROM_FIELD, toBefore);
			setValue(TO_FIELD, fromBefore);

			const fromAfter = getValue(FROM_FIELD);
			const toAfter = getValue(TO_FIELD);

			FLIP_BUTTON.click();

			assert.equal(fromAfter, toBefore);
			assert.equal(toAfter, fromBefore);

			done();
		}, DELAY);
});

QUnit.test('the alert box is hidden by clicking on its close button',
	function(assert) {
		const done = assert.async();
		setTimeout(function() {
			ALERT_BOX.removeClass('hidden');

			ALERT_BOX.children('.hide').click();

			assert.ok(ALERT_BOX.hasClass('hidden'));

			done();
		}, DELAY);
});

QUnit.test('the currencies list is show and hidden by clicking on a button',
	function(assert) {
		const done = assert.async();
		setTimeout(function() {
			VIEW_CURRENCIES_BUTTON.click();

			assert.notOk(CURRENCIES_LIST.hasClass('hidden'));
			assert.ok(VIEW_CURRENCIES_BUTTON.children('i').hasClass('fa-times'));

			done();
		}, DELAY);
});