from django.conf.urls.defaults import url, patterns

uuid_regex = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
urlpatterns = patterns('project_management.conferenceroombooking',
                       (r'^create/$', 'views.manage_room_creation'),
                       (r'^book/$', 'views.manage_book_conference_room'),
                       (r'^MonthlyCalendar/$', 'eventviews.MonthlyCalendar'),
                       (r'^previousyear/', 'eventviews.previousyear'),
                       (r'^nextyear/', 'eventviews.nextyear'),
                       (r'^previousmonth/', 'eventviews.previousmonth'),
                       (r'^nextmonth/', 'eventviews.nextmonth'),
                       (r'^book/(?P<page>\d+)/$', 'views.manage_book_conference_room'))