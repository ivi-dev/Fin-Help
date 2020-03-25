const CONVERT_RESPONSE = {
result: 1,
	rate_info: {
		amount: 1,
		from_currency_name: "Currency 1",
		from_currency_symbol: "ABC",
		rate: 12.12345,
		to_currency_name: "Currency 2",
		to_currency_symbol: "DEF"
	}
};
const data = getPreConversionData();
const CONVERT_URL = `convert/?amount=${data.amount}&from=${data.from}&to=${data.to}`;
const DELAY = 10;