$.when( $.ready ).then(function() {
	$('#convert-form button#convert').on('click', function() {
		hideAlert();
		const amount = getValue($('#convert-form #amount'));
		if (amount != 0) {
			const button = $(this), 
			title = getValue(button);
			setValue(button, 'КАЛКУЛИРАМ...');
			button.attr('disabled', true);
			try {
				convert($('#convert-form'))
				.done(function(data) {
					usePostConversionData(data);
				}).fail(function(request) {
					handleNetworkError(request.status);
				}).always(function() {
					setValue(button, title);
					button.removeAttr('disabled');
				});
			} catch (e) {
				if (e instanceof IncompleteConversionDataError) {
					alert('Калкулацията е прекратена, тъй като ' +
						  'липсват някои неодходими данни за нея.');
				}
			} finally {
				setValue(button, title);
				button.removeAttr('disabled');
			}
		} else {
			if (amount == '0') {
				alert('Изберете стойност за калкулация, различна от нула.');
			} else {
				alert('Не оставяйте полето за количество празно.');
			}
		}
	});

	$('#info-box .hide').on('click', function() {
		$(this).parent().addClass('hidden');
	});
});