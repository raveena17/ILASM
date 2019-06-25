# from django.conf.urls.defaults import url, patterns
from django.conf.urls import include, url
# from project_management.conferenceroombooking import views as conferenceroombooking_views
from project_management.conferenceroombooking.views import *
# from project_management.conferenceroombooking import eventviews as conferenceroombooking_eventviews

from project_management.conferenceroombooking.eventviews import *


uuid_regex = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
urlpatterns = [
    url(r'^create/$', manage_room_creation),
    url(r'^book/$', manage_book_conference_room),
    url(r'^MonthlyCalendar/$', MonthlyCalendar),
    url(r'^previousyear/', previousyear),
    url(r'^nextyear/', nextyear),
    url(r'^previousmonth/', previousmonth),
    url(r'^nextmonth/', nextmonth),
    url(r'^book/(?P<page>\d+)/$', manage_book_conference_room),
]
