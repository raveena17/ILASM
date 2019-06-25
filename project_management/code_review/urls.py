# from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.conf.urls import include, url
# from project_management.code_review import views as code_review_views
from project_management.code_review.views import *
# from project_management.codereview.views import *


urlpatterns = [
    url(r'^list/$', code_review_list, name='list'),
    url(r'^get_team_members/$', get_team_members, name="get_team_members"),
    url(r'^(?P<project_id>\d+)/get_team_members/$', get_team_members, name="get_team_members"),
    url(r'^save/$', save_review, name="save"),
    url(r'^edit/(?P<code_review_id>\d+)/$', edit, name="edit"),
]
