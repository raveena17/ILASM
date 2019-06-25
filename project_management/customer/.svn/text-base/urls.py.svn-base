"""
    Customer urls
"""
from django.conf.urls.defaults import url, patterns

uuid_regex = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
urlpatterns = patterns('project_management.customer',
    (r'^$', 'views.list_customer'),
    (r'^list/', 'views.clientlist'),
    (r'^create/', 'views.manage_client'),
    (r'^update/(?P<id>\d+)/$', 'views.manage_client'),
    (r'^deactivate/$', 'views.manage_client_status',
                {'is_active': False}, "deactivate-client"),
    (r'^activate/$', 'views.manage_client_status',
                {'is_active': True}, "activate-client"),
    #url(r'^create/$', 'views.manage_customer_from_project', name="create_customer"),
    #url(r'^update/(?P<id>\d+)/$', 'views.manage_customer_from_project',
                                     #name="update_customer"),
    url(r'^contact/create/$', 'views.manage_customer_contact_from_project',
                                     name="create_customer_contact"),
    url(r'^contact/update/(?P<id>\d+)/$', 'views.manage_customer_contact_from_project',
                                     name="update_customer_contact")
#    (r'^delete/(?P<id>%s)/$'%(uuid_regex), 'views.delete_customer'),
)

