from __future__ import unicode_literals

from django.contrib import admin
from models import Service, AmcReport, Status


class AmcReportAdmin(admin.ModelAdmin):
	model = AmcReport
	list_display = ('customer_name', 'project_name', 'milestone_name', 'Due_date', 'AMC_end_date', 'status', 'notification')
admin.site.register(Service)
admin.site.register(AmcReport, AmcReportAdmin)
admin.site.register(Status)
