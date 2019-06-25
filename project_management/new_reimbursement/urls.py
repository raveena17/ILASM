from django.conf.urls import include, url
from project_management.new_reimbursement.views import *


urlpatterns = [
	url(r'^type/$',get_type),
	url(r'^report/$',get_report),
    url(r'^create/$', manage_reimbursement),
    url(r'^update/(?P<id>\d+)/$', manage_reimbursement, name='reimbursement'),
    url(r'^approve/(?P<id>\d+)/$', Approve, name='reimbursement'),
    url(r'^reject/(?P<id>\d+)/$', Reject, name='reimbursement'),
    url(r'^list/$', reimbursement_list),
    url(r'^approver/list/$', reimbursement_approver_list),
    # url(r'^delete/$', delete_reimbursement),
    url(r'^catagory/budjet/$', get_reimbursement_budjet),
    url(r'^admin/list/$', admin_reimbursement_list),
    url(r'^cancel/$', cancel),
]