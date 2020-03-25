$.when($.ready).then(function() {
	CONVERT_BUTTON.on('click', function() {
		hideAlert();
		const amount = getValue(AMOUNT_FIELD);
		if (amount != 0) {
			const button = $(this);
			deactivateButton(button, CONVERT_BUTTON_BUSY_TITLE);
			convert($(CONVERT_FORM));
		}
	});

	FLIP_BUTTON.on('click', function() {
		const fromValue = getValue(FROM_FIELD);
		const toValue = getValue(TO_FIELD);
		setValue(FROM_FIELD, toValue);
		setValue(TO_FIELD, fromValue);
	});

	ALERT_BOX.children('.hide').on('click', function() {
		$(this).parent().addClass('hidden');
	});

	VIEW_CURRENCIES_BUTTON.on('click', function() {
		CURRENCIES_LIST.toggleClass('hidden');
		VIEW_CURRENCIES_BUTTON.children('i').toggleClass('fa-times');
	});
});