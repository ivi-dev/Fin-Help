function isObject(arg) {
	return typeof(arg) === 'object';
}

function isString(arg) {
	return typeof(arg) === 'string';
}

function checkConversionData(data) {
	const missing = [];
	for (const [name, value] of Object.entries(data)) {
		if (!value) {
			missing.push({name, value});
		}
	}
	if (missing.length) {
		throw new IncompleteConversionDataError(`These pieces ` +
			`of pre-conversion information are missing: ` +
			`${getConversionDataEntriesAsString(missing)}.` +
			` Cannot proceed with the conversion.`);
	}
}

function getConversionDataEntriesAsString(entries) {
	let string = '';
	for (const entry of entries) {
		if (!entry.value) {
			string += `${entry.name}, `;
		}
	}
	return string.trim().replace(/,$/, '');
}

function convert() {
	try {
		let data = getPreConversionData();
		return $.ajax('convert/', {
			data: data,
			dataType: 'json'
		}).done(function(data) {
			updateUI(data);
		}).fail(function(request) {
			handleNetworkError(request.status);
		}).always(function() {
			activateButton(CONVERT_BUTTON, 
						   CONVERT_BUTTON_ORIGINAL_TITLE);
		});
	} catch (e) {
		handleConversionError();
	} finally {
		activateButton($(CONVERT_BUTTON), 
				       CONVERT_BUTTON_ORIGINAL_TITLE);
	}
}

function handleNetworkError(status) {
	if (status === 404) {
		alert('Адресът на системната ' + 
		      `заявка не може да бъде намерен. Код на грешката: ${status}`);
	} else if (status === 500) {
		alert('По неизвестна причина, ' +
		      'системата не успя да обработи ' + 
		      `заявката ви. Код на грешката: ${status}`);
	} else {
		alert('Възникна грешка при обработката ' +
			  `на заявката ви. Код на грешката: ${status}`);
	}
}

function handleConversionError(e) {
	if (e instanceof IncompleteConversionDataError) {
		alert('Калкулацията е прекратена, тъй като ' +
			  'липсват някои неодходими данни за нея.');
	}
}