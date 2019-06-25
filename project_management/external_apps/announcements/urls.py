# from django.conf.urls.defaults import patterns
#from django.views.generic import list_detail
from django.views.generic import TemplateView
from django.conf.urls import include, url

from announcements.views import announcement_list
from announcements import views as announcements_views


urlpatterns = [
    url(r'list/$', 'announcements_views.announcement_list'),
    #url(r'create/$', TemplateView.as_view(template = 'CreateAnnouncement.html')),
    url(r'create/$', 'announcements_views.ShowApprovedBy'),
    url(r'view/', 'announcements_views.ViewAnnouncement'),
    url(r'save/', 'announcements_views.SaveAnnouncement'),
    url(r'update/', 'announcements_views.UpdateAnnouncement'),
    url(r'delete/', 'announcements_views.DeleteAnnouncement'),
    url(r'approve/', 'announcements_views.ApproveAnnouncement')
]
