$.when($.ready).then(function() {
	CONVERT_FORM.children('button#convert').on('click', function() {
		hideAlert();
		const amount = getValue(CONVERT_FORM.children(AMOUNT_FIELD_SELECTOR));
		if (amount != 0) {
			const button = $(this), title = getValue(button);
			deactivateButton(button, 'КАЛКУЛИРАМ...');
			convert($(CONVERT_FORM));
		} else {
			handleZeroAmountError(amount);
		}
	});

	CONVERT_FORM.children('button#flip').on('click', function() {
		const fromValue = getValue(CONVERT_FORM.children(FROM_FIELD_SELECTOR));
		const toValue = getValue(CONVERT_FORM.children(TO_FIELD_SELECTOR));
		setValue(CONVERT_FORM.children(FROM_FIELD_SELECTOR), toValue);
		setValue(CONVERT_FORM.children(TO_FIELD_SELECTOR), fromValue);
	});

	ALERT_BOX.children('.hide').on('click', function() {
		$(this).parent().addClass('hidden');
	});

	VIEW_CURRENCIES_BUTTON.on('click', function() {
		CURRENCIES_LIST.toggleClass('hidden');
		$(this).children('i').toggleClass('fa-times');
	});
});