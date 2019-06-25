"""
    urls for milestone
"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('project_management.milestone',
    (r'^$', 'views.milestone_list'),
    (r'^list/$', 'views.milestone_list'),
    (r'^list/(?P<pageNo>\d+)/$', 'views.milestone_list'),
    url(r'^create/$', 'views.manage_milestone', name='create-milestone'),
    url(r'^update/(?P<id>\d+)/$', 'views.manage_milestone', name='update-milestone'),
    (r'^delete/$', 'views.milestone_delete')
)
