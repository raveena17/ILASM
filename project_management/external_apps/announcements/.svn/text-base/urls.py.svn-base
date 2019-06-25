from django.conf.urls.defaults import patterns
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template

from announcements.views import announcement_list

urlpatterns = patterns('announcements.views',
    (r'list/$',announcement_list),
    #(r'create/$', direct_to_template, {'template': 'CreateAnnouncement.html'}),
    (r'create/$','ShowApprovedBy'),
    (r'view/','ViewAnnouncement'),
    (r'save/', 'SaveAnnouncement'),
    (r'update/', 'UpdateAnnouncement'),
    (r'delete/', 'DeleteAnnouncement'),
    (r'approve/','ApproveAnnouncement')
)
