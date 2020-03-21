from django.db.models import QuerySet
from typing import Tuple, Any, Optional
from django.db import models


def qs_find(queryset: QuerySet, 
			filter: Tuple[str, Any]) -> Optional[models.Model]:
	for item in queryset:
		if getattr(item, filter[0]) == filter[1]:
			return item