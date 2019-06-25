from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from project_management.users.models import UserProfile
from project_management.users.views import login
from django.contrib.auth import views as auth_views
from project_management.projectbudget.models import *
from project_management.projectbudget.budgetmasters import *
from django.conf.urls import include, url
import os.path
import django_cron

admin.autodiscover()

try:
    django_cron.autodiscover()
except BaseException:
    pass


from project_management.common_manager import views as common_manager_views
from project_management.logs.views import DisplayLog, DisplayLogData, GetLog
from project_management.notifications.eventviews import *
from project_management.repository.views import *
from project_management.non_project_task.views import *
from project_management.Utility import getPopUpDetails
from project_management.common_manager.views import *
from project_management.projects import views as projects_views
from project_management.repository import views as repository_views
from project_management.non_project_task import views as non_project_task_views
from django.views.i18n import *
from project_management.i18nDate import *
from project_management.client_visit_report import *
from project_management.amc import *
from project_management.leave import *
from project_management.AMC_Report import *
import os.path
import django_cron

admin.autodiscover()

try:
    django_cron.autodiscover()
except BaseException:
    pass


js_info_dict = {'packages': ('cui.translations',), }


urlpatterns = [

    url(r'^django-jsi18n/$', javascript_catalog, js_info_dict),
    url(r'^jsi18n/$', javascript_catalog, {'packages': 'django.conf'}),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login, {'template_name': 'login.html'}),
    url(r'^login/', login, {'template_name': 'login.html'}),
    url(r'^comingsoon/$', TemplateView.as_view(template_name='coming_soon.html')),
    url(r'^recentupdates/$', TemplateView.as_view(template_name='Recent_updates.html')),
    url(r'^re-use/$', TemplateView.as_view(template_name='re-use.html')),
    url(r'^re-use/components/$',
        TemplateView.as_view(template_name='Re-Use_Library.html')),
    url(r'^5GPal/$', TemplateView.as_view(template_name='5G-Pal.html')),
    url(r'^5GPal/Policies/$',
        TemplateView.as_view(template_name='5gpal_Policies.html')),
    url(r'^5GPal/FxCop_and_Rules/$',
        TemplateView.as_view(template_name='5gpal_FxCop_and_Rules.html')),
    url(r'^5GPal/Process-templates/$',
        TemplateView.as_view(template_name='5gpal__process-templates.html')),
    url(r'^Mindshare/', RedirectView, {'url': '/login/'}),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}),

]
urlpatterns += [

    url(r'^Logs/', DisplayLog),
    url(r'^admin.ShowLog/', DisplayLogData),
    url(r'^GetLogDetail/', GetLog),
]
urlpatterns += [

    url(r'^users/', include('project_management.users.urls')),
    url(r'^projects/', include('project_management.projects.urls')),
    url(r'^projectbudget/', include('project_management.projectbudget.urls')),
    url(r'^alert/', include('project_management.alert.urls')),
    url(r'^customer/', include('project_management.customer.urls')),
    url(r'^tasks/', include('project_management.tasks.urls')),
    url(r'^milestone/', include('project_management.milestone.urls')),
    url(r'^businessunit/', include('project_management.business_unit.urls')),
    url(r'^event/', include('project_management.notifications.urls')),
    url(r'^announcements/', include('announcements.urls')),
    url(r'^timesheet/', include('project_management.timesheet.urls')),
    url(r'^timesheetnew/', include('project_management.timesheetnew.urls')),
    url(r'^NewsLetter/', include('newsletter.urls')),
    url(r'^conferenceroombooking/',
        include('project_management.conferenceroombooking.urls')),
    url(r'^code_review/', include('project_management.code_review.urls')),
    url(r'^clientvisitreports/', include('project_management.client_visit_report.urls')),
    url(r'^amc/', include('project_management.amc.urls')),
    url(r'^leave/', include('project_management.leave.urls')),
    url(r'^dashboard/', include('project_management.dashboard.urls')),
    url(r'^AMC/', include('project_management.AMC_Report.urls')),
    # url(r'^reimbursement/', include('project_management.reimbursement.urls')),
    # url(r'^codereview/', include('project_management.code_review.urls', urlnamespace="codereview")),
    # url(r'^library/',include('project_management.library.urls')),
    # url(r'^comments/', include('comments.urls', namespace='comments')),
]

urlpatterns += [
    url(r'^MonthlyCalendar/$', MonthlyCalendar),
    url(r'^WeeklyCalendar/$', WeeklyCalendar),
    url(r'^DayCalendar/$', DayCalendar),
    url(r'^previousyear/(?P<type>\w+)/', previousyear),
    url(r'^nextyear/(?P<type>\w+)/', nextyear),
    url(r'^previousmonth/', previousmonth),
    url(r'^nextmonth/', nextmonth),
    url(r'^nextday/', nextday),
    url(r'^previousday/', previousday),
    url(r'^nextweek/', nextweek),
    url(r'^previousweek/', previousweek),
    url(r'^Event/', Events),
    url(r'^CreateEvent/', Events),
    url(r'^SaveEvent/', saveEvent),
    url(r'^Eventdelete/', eventDelete),
    url(r'^UpdateEvent/', updateEvent),
    url(r'^EventAccess/', accessEvent),
    url(r'^GetStage/', getStage),
]
urlpatterns += [


    url(r'^prog_task_in_pg/$',
        TemplateView.as_view(template_name="prog_task_in_pg.html"),
        name="prog_task_in_pg"),
]
urlpatterns += [

    url(r'^repository/', RepositoryView),
    url(r'^repositoryUpload/', RepositoryUpload),
]

urlpatterns += [

    url(r'^SaveNonProjectTask/', SaveNonProjectTask),
    url(r'^SaveAndContinueNonProjectTask/', SaveAndContinueNonProjectTask),
]
urlpatterns += [


    url(r'^GetPopUpDetails/', getPopUpDetails),
]

urlpatterns += [

    url(r'^MasterView/', MasterView),
    url(r'^MasterSave/', MasterSave),
    url(r'^MasterDelete/', MasterDelete),

]

urlpatterns += [
    url(r'^password/', include('password_change.urls')),
]


urlpatterns += [
	url(r'^reimbursement/', include('new_reimbursement.urls')),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

