
from django.conf.urls import include, url

from django.views.generic import TemplateView

from announcements.views import announcement_list

from project_management.announcements.views import *


urlpatterns = [
    url(r'list/$', announcement_list),
    url(r'create/$', ShowApprovedBy),
    url(r'view/', ViewAnnouncement),
    url(r'save/', SaveAnnouncement),
    url(r'update/', UpdateAnnouncement),
    url(r'delete/', DeleteAnnouncement),
    url(r'approve/', ApproveAnnouncement)
]
