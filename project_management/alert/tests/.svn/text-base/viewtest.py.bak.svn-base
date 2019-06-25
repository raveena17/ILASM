import re
from django.test.client import Client
from django.test import TestCase
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson

from project_management.alert.models import *
from project_management.alert.views import *
from project_management.Utility import EmailWithCC
from django.contrib.auth.models import User
from project_management.projectbudget.models import *
from project_management.business_unit.models import *
from project_management.projects.models import *
from project_management.projectbudget.views import budget_reminder_alertmail
from project_management import settings

from logintest import LoginTest
from project_management.projectbudget.tests.viewstest import *

class AlertTest(TestCase):
    
    urls = 'project_management.urls'
    client = Client()
    
    def setUp(self):        
        self.client = LoginTest('testlogin').testlogin()
        User.objects.create(
            id='96',
            username='admin21',
            first_name='admin2',
            last_name='',
            email='ramya@5gindia.net',
            password='sha1$d5errc6$46114051bed7702b29535352126784822199d2ce',
            is_staff='1',
            is_active='1',
            is_superuser='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')
        User.objects.create(
            id='97',
            username='admin91',
            first_name='admin',
            last_name='',
            email='ashok@5gindia.net',
            password='sha1$d5errc6$46114051bed7702b29535352126784822199d2ce',
            is_staff='1',
            is_active='1',
            is_superuser='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')
        User.objects.create(
            id='98',
            username='admin16',
            first_name='admin',
            last_name='',
            email='ashok@5gindia.net',
            password='sha1$d5errc6$46114051bed7702b29535352126784822199d2ce',
            is_staff='1',
            is_active='1',
            is_superuser='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')
        User.objects.create(
            id='99',
            username='admin3',
            first_name='admin',
            last_name='',
            email='ashok@5gindia.net',
            password='sha1$d5errc6$46114051bed7702b29535352126784822199d2ce',
            is_staff='1',
            is_active='1',
            is_superuser='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')
        User.objects.create(
            id='100',
            username='admin4',
            first_name='admin',
            last_name='',
            email='ashok@5gindia.net',
            password='sha1$d5errc6$46114051bed7702b29535352126784822199d2ce',
            is_staff='1',
            is_active='1',
            is_superuser='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')
        User.objects.create(
            id='101',
            username='admin5',
            first_name='admin',
            last_name='',
            email='ashok@5gindia.net',
            password='sha1$d5errc6$46114051bed7702b29535352126784822199d2ce',
            is_staff='1',
            is_active='1',
            is_superuser='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')    
        self.collection_user = User.objects.all()
        
        
            
    def test_alert_list(self):
        response = self.client.post('/alert/list/')
        self.assertEqual(response.status_code, 200) 
     
    def test_alert_edit(self):
        response = self.client.post('/alert/edit/alertdataconfig1/')
        self.assertEqual(response.status_code, 200)
        
    def test_alert_save(self):
        response = self.client.post('/alert/save/',{
            u'hdn_id':'alertdataconfig1',
            u'alert_name':'Project Budget Send for Approval (Business Head)',
            u'alert_type':'Event',
            u'days':'0',
            u'frequency':'1',
            u'subject':'',
            u'body':'',
            u'subject_fields':'',
            u'body_fields':'',
            u'is_lock':'1',
            u'modified_by_id':'',
            u'is_active':'1',
            u'is_email':'1',
            u'hdn_toemail':[self.collection_user[2].id,self.collection_user[3].id],
            u'hdn_cc':[self.collection_user[4].id,self.collection_user[5].id]})
        self.assertEqual(response.status_code, 302) 
    
    def test_alert_generate(self):
        self.client = ProjectBudgetTest('setUp').setUp()
        budget_reminder_alertmail(self)
        
