from django.conf.urls.defaults import *
#from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('project_management.code_review.views',
    url(r'^list/$', 'code_review_list', name='list'),    
    url(r'^/get_team_members/$', 'get_team_members', name="get_team_members"),
    url(r'^(?P<project_id>\d+)/get_team_members/$', 'get_team_members', name="get_team_members"),
    url(r'^save/$', 'save_review', name="save"),
    url(r'^edit/(?P<code_review_id>\d+)/$', 'edit', name="edit"),
    )