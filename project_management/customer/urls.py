"""
    Customer urls
"""
# from django.conf.urls.defaults import url, patterns
from django.conf.urls import include, url
# from project_management.customer import views as customer_views
from project_management.customer.views import *

uuid_regex = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
urlpatterns = [
    url(r'^$', list_customer),
    url(r'^list/', clientlist),
    url(r'^create/', manage_client),
    url(r'^update/(?P<id>\d+)/$', manage_client),
    url(r'^deactivate/$', manage_client_status,
        {'is_active': False}, "deactivate-client"),
    url(r'^activate/$', manage_client_status,
        {'is_active': True}, "activate-client"),
    #url(r'^create/$', manage_customer_from_project, name="create_customer"),
    # url(r'^update/(?P<id>\d+)/$', manage_customer_from_project,
    # name="update_customer"),
    url(r'^contact/create/$', manage_customer_contact_from_project,
        name="create_customer_contact"),
    url(r'^contact/update/(?P<id>\d+)/$', manage_customer_contact_from_project,
        name="update_customer_contact")
    #    url(r'^delete/(?P<id>%s)/$'%(uuid_regex), delete_customer),
]
