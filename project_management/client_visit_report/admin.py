from django.contrib import admin
from .models import ClientVisitReport
# from import_export.admin import ImportExportModelAdmin


# class ClientVisitReportAdmin(ImportExportModelAdmin):
class ClientVisitReportAdmin(admin.ModelAdmin):

    list_per_page = 10
    search_fields = ['prepared_by']
    list_display = ('prepared_by', 'project_name', 'client_name', 'visit_location',
                    'from_date', 'to_date', 'is_approved', 'is_rejected')

    class Meta:
        model = ClientVisitReport


admin.site.register(ClientVisitReport, ClientVisitReportAdmin)
