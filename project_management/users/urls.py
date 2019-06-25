"""
    urls required the user application.
"""

# from django.conf.urls.defaults import patterns
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView
# from project_management.users import views as users_views
from project_management.users.views import *


urlpatterns = [
    url(r'^create/$', manage_user),
    url(r'^update/(?P<pid>\d+)/$', manage_user),
    url(r'^list/$', user_list),
    url(r'^deactivate/$', manage_user_status,
        {'status': False}, "deactivate-user"),
    url(r'^activate/$', manage_user_status,
        {'status': True}, "activate-user"),
    url(r'^myprofile/$', manage_myprofile),
    url(r'^contacts/$', ContactView.as_view()),


]
