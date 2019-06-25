from django.conf.urls import include, url
from project_management.password_change.views import *


urlpatterns = [
    url(r'^change/$', ldap_password_management),
	
]
