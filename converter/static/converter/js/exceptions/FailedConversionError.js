class FailedConversionError extends Error {
	constructor(message = '') {
		super(`Conversion failed. ${message}`);
	}
}