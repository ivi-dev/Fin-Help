def qs_find(queryset, filter):
	for item in queryset:
		if getattr(item, filter[0]) == filter[1]:
			return item