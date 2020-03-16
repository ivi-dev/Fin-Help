from decimal import Decimal

from django.db import models

class Currency(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=3)
	symbol = models.CharField(max_length=10)
	per = models.IntegerField(default=1)
	rate = models.DecimalField(max_digits=10, decimal_places=5)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def get_rate_to(self, code, precision=5):
		target_currency = Currency.objects.get(code=code)
		to_base = self.rate * 1 \
				  if self.rate > 1 \
				  else self.rate / 1
		result = to_base / target_currency.rate \
				 if target_currency.rate > 1 \
				 else to_base * target_currency.rate
		return round(result, precision)

	def convert_to(self, code, amount, precision=5):
		amount_ = Decimal(amount)
		target_currency = Currency.objects.get(code=code)
		to_base = self.rate * amount_ \
				  if self.rate > 1 \
				  else self.rate / amount_
		result = to_base / target_currency.rate \
				 if target_currency.rate > 1 \
				 else to_base * target_currency.rate
		return round(result, precision)

	class Meta:
		verbose_name_plural = "currencies"