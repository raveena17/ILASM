import django_tables2 as tables
from .models import ClientVisitReport


class CVRTable(tables.Table):
    class Meta:
        model = ClientVisitReport

	attrs = {'class': 'paleblue'}
