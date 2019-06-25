"""
Url pattern for projectbudgegt application
"""

from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('project_management.projectbudget.views',
    (r'^create/$', 'create'),
    (r'^list/$', 'list'),
    (r'^save/$', 'save'),
    (r'^export_budget/$', 'export_budget'),
    )

urlpatterns += patterns('project_management.projectbudget.budgetmasters',
    (r'^phase/$', 'phase_list'),
    (r'^phase/delete/$', 'delete_phase'),
    (r'^phase/add/$', 'create_phase'),
    (r'^cost/$', 'cost_listpage'),
    (r'^cost/delete/$', 'delete_cost'),
    (r'^cost/add/$', 'add_cost'),
    (r'^cost/cancel/$', 'cancel'),
    )
