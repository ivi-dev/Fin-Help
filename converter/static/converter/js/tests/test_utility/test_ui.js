QUnit.test('activateButton() removes the ' +
		   'disabled attribute from a button and sets the  button\'s title',
   function(assert) {
   		deactivateButton(CONVERT_BUTTON, CONVERT_BUTTON_BUSY_TITLE);
   		assert.ok(CONVERT_BUTTON.attr('disabled'));
   		assert.equal(getValue(CONVERT_BUTTON), CONVERT_BUTTON_BUSY_TITLE);
   		activateButton(CONVERT_BUTTON, CONVERT_BUTTON_ORIGINAL_TITLE);
   		assert.notOk(CONVERT_BUTTON.attr('disabled'));
   		assert.equal(getValue(CONVERT_BUTTON), CONVERT_BUTTON_ORIGINAL_TITLE);
});

QUnit.test('deactivateButton() add a ' +
		   'disabled attribute from a button and sets the  button\'s title',
   function(assert) {
   		deactivateButton(CONVERT_BUTTON, CONVERT_BUTTON_BUSY_TITLE);
   		assert.ok(CONVERT_BUTTON.attr('disabled'));
   		assert.equal(getValue(CONVERT_BUTTON), CONVERT_BUTTON_BUSY_TITLE);
});

QUnit.test('getValue() returns the text value of a jQuery element',
   function(assert) {
   		activateButton(CONVERT_BUTTON, CONVERT_BUTTON_ORIGINAL_TITLE);
   		const element = CONVERT_BUTTON;
   		assert.equal(getValue(element), CONVERT_BUTTON_ORIGINAL_TITLE);
});

QUnit.test('getValue() returns the text value of an element ' +
		   'denoted by a CSS selector',
   function(assert) {
   		const element = 'button#convert';
   		assert.equal(getValue(element), CONVERT_BUTTON_ORIGINAL_TITLE);
});

QUnit.test('getValue() returns the value of a jQuery form control element',
   function(assert) {
   		const element = FROM_FIELD;
   		setValue(element, 'ABC');
   		assert.equal(getValue(element), 'ABC');
});

QUnit.test('getValue() returns the value of a form control element ' +
		   'denoted by a CSS selector',
   function(assert) {
   		const element = '#from';
   		assert.equal(getValue(element), 'ABC');
});

QUnit.test('setValue() sets the text value of a jQuery element',
   function(assert) {
   		const element = CONVERT_BUTTON;
   		setValue(element, CONVERT_BUTTON_BUSY_TITLE);
   		assert.equal(getValue(CONVERT_BUTTON), CONVERT_BUTTON_BUSY_TITLE);
   		setValue(element, CONVERT_BUTTON_ORIGINAL_TITLE);
});

QUnit.test('setValue() sets the text value of an element ' +
		   'denoted by a CSS selector',
   function(assert) {
   		const element = 'button#convert';
   		setValue(element, CONVERT_BUTTON_BUSY_TITLE);
   		assert.equal(getValue(element), CONVERT_BUTTON_BUSY_TITLE);
});

QUnit.test('setValue() sets the value of a jQuery form control element',
   function(assert) {
   		const element = FROM_FIELD;
   		setValue(element, 'DEF');
   		assert.equal(getValue(element), 'DEF');
   		setValue(element, 'ABC');
});

QUnit.test('setValue() sets the value of a form control element ' +
		   'denoted by a CSS selector',
   function(assert) {
   		const element = '#from';
   		setValue(element, 'DEF');
   		assert.equal(getValue(element), 'DEF');
   		setValue(element, 'ABC');
});

QUnit.test('hideAlert() hides the alert box', function(assert) {
   		ALERT_BOX.removeClass('hidden');
   		assert.notOk(ALERT_BOX.hasClass('hidden'));
   		hideAlert();
   		assert.ok(ALERT_BOX.hasClass('hidden'));
});