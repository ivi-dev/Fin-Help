from django.db import models

class Currency(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=3)
	symbol = models.CharField(max_length=10)
	per = models.IntegerField()
	rate = models.DecimalField(max_digits=10, decimal_places=5)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "currencies"