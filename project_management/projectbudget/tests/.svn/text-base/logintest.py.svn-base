import os
import re

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail
from django.test.client import Client

from project_management.projectbudget.models import *
from project_management import settings


class LoginTest(TestCase):
    urls = 'project_management.urls'
    client = Client()

    def setUp(self):
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
    os.path.join(
        os.path.dirname(__file__),
    'templates'),
)

    def testlogin(self, password='admin'):
        user = User(
    id='12', username='admin', first_name='admin', last_name='',
    email='ashok@5gindia.net',
    password='sha1$d5ec6$46114051bed7702b29535352126784822199d2ce',
    is_staff='1',
    is_active='1',
    is_superuser='1',
    last_login='2012-09-24 05:16:45',
    date_joined='2012-09-24 05:16:45'
        )
        user.save()
        response = self.client.post('/login/', {
                                    'username': 'admin',
                                    'password': password
                                    }
                                    )
        self.assertEquals(response.status_code, 302)
        return response.client
