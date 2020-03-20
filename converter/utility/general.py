from django.db.models import QuerySet
from typing import Tuple, Any


def qs_find(queryset: QuerySet, 
			filter: Tuple[str, Any]):
	for item in queryset:
		if getattr(item, filter[0]) == filter[1]:
			return item