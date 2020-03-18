$.when( $.ready ).then(function() {
	CONVERT_FORM.children('button#convert').on('click', function() {
		hideAlert();
		const amount = getValue(CONVERT_FORM.children(AMOUNT_FIELD_SELECTOR));
		if (amount != 0) {
			const button = $(this), title = getValue(button);
			deactivateButton(button, 'КАЛКУЛИРАМ...');
			try {
				convert($(CONVERT_FORM))
				  .done(function(data) {
					usePostConversionData(data);
				}).fail(function(request) {
					handleNetworkError(request.status);
				}).always(function() {
					activateButton(button, title);
				});
			} catch (e) {
				if (e instanceof IncompleteConversionDataError) {
					alert('Калкулацията е прекратена, тъй като ' +
						  'липсват някои неодходими данни за нея.');
				}
			} finally {
				activateButton(button, title);
			}
		} else {
			if (amount == 0) {
				alert('Изберете сума, различна от нула.');
			} else {
				alert('Не оставяйте полето "Сума" празно.');
			}
		}
	});

	CONVERT_FORM.children('button#flip').on('click', function() {
		const fromValue = getValue(CONVERT_FORM.children(FROM_FIELD_SELECTOR));
		setValue(CONVERT_FORM.children(FROM_FIELD_SELECTOR), 
			getValue(CONVERT_FORM.children(TO_FIELD_SELECTOR)));
		setValue(CONVERT_FORM.children(TO_FIELD_SELECTOR), fromValue);
	});

	ALERT_BOX.children('.hide').on('click', function() {
		$(this).parent().addClass('hidden');
	});

	VIEW_CURRENCIES_BUTTON.on('click', function() {
		CURRENCIES_LIST.toggleClass('hidden');
		$(this).children('i').toggleClass('fa-times');
	});

	// updateRates()
	// .done(function(data) {
	// 	console.log(data)
	// }).fail(function() {
	// 	alert('Въникна грешка при опита за актуализация ' +
	// 		  'на валутните курсове.');
	// });
});