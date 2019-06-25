from django.conf.urls import url
from project_management.client_visit_report.views import *

app_name = 'client_visit_report'
urlpatterns = [

    url(r'^$', cvr_list),
    url(r'^create/$', create, name='create'),
    url(r'^report/(?P<id>\d+)/$', view_entry_data),
    url(r'^(?P<id>\d+)/(?P<status>\w+)$', cvr_approval),
    url(r'^list/(?P<type>\w+)/(?P<status>\w+)$', get_list_based_on_status),
    url(r'^record/$', cvr_record_list),
    url(r'^record/(?P<status>\w+)$', get_cvr_records_based_on_status),
    url(r'^delete/$', cvr_delete)

]
