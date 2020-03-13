from django.shortcuts import render
from .models import Currency


def index(request):
	context = {
		'currencies': Currency.objects.all()
	}
	return render(request, 'converter/index.html', context)