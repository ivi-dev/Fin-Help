class IncompleteConversionDataError extends Error {
	constructor(message = 'Conversion data is incomplete, ' +
				          'cannot proceed with currency conversion.') {
		super(message);
	}
}