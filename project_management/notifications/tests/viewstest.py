from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User

from project_management.projects.models import *
from project_management.notifications.models import *
from project_management.business_unit.models import BusinessUnit
from project_management.projectbudget.tests.logintest import LoginTest
from project_management.projectbudget.tests.logintest import LoginTest


class NotificationsTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()
        User.objects.create(username='admin3',
                            first_name='admin3',
                            email='ashok@5gindia.net',
                            is_staff=0,
                            is_active=1)
        self.user_list = User.objects.all()
        ProjectType.objects.create(name='Development', level='1')
        project_type = ProjectType.objects.get(pk=1)
        BusinessUnit.objects.create(
            name="5G-PSG", firstname="india", type_id="1",
            contact_email="5gpsg@gmail.com")
        BusinessUnit.objects.create(
            name="5G", firstname="india", type_id="1",
            contact_email="5gindia@gmail.com")
        self.business_unit = BusinessUnit.objects.get(pk=1)
        self.deivery_center = BusinessUnit.objects.get(pk=2)
        Project.objects.create(name='sample project',
                               code='1-internal-project-2013',
                               short_name='project',
                               approval_type='internal',
                               project_type_id=project_type.id,
                               business_unit_id=self.business_unit.id,
                               delivery_centre_id=self.deivery_center.id,
                               is_active=1,
                               is_project_group=0,
                               cancel=0,
                               is_approved=1)
        self.test_project = Project.objects.get(pk=1)

    def test_create_event(self):
        response = self.client.post('/event/create/',
                                    {'name': 'sample event',
                                     'date': '04-02-2013',
                                     'start_time': '09:30',
                                     'end_time': '11:30',
                                     'venue': '5G technology',
                                     'Location': 'Guindy',
                                     'project': self.test_project.id,
                                     'type': 'Meeting',
                                     'attendees': self.user_list[1].id})
        self.assertEquals(response.status_code, 302)
        event_list = Event.objects.all()
        self.assertEquals(len(event_list), 1)

    def test_update_event(self):
        self.test_create_event()
        edit_event = Event.objects.get(pk=1)
        response = self.client.post('/event/update/' + str(edit_event.id) + '/',
                                    {'id': edit_event.id,
                                     'name': 'sample project event',
                                     'date': '04-02-2013',
                                     'start_time': '09:30',
                                     'end_time': '11:30',
                                     'venue': '5G technology',
                                     'Location': 'Guindy',
                                     'project': self.test_project.id,
                                     'type': 'Meeting',
                                     'attendees': self.user_list[1].id
                                     })
        self.assertEquals(response.status_code, 302)
        edit_event = Event.objects.get(pk=1)
        self.assertEquals(edit_event.name, 'sample project event')

    def test_list_event(self):
        self.test_create_event()
        response = self.client.post('/event/list/')
        self.assertEquals(response.status_code, 200)
        event_list = Event.objects.all()
        self.assertEquals(len(event_list), 1)

    def test_delete_event(self):
        self.test_create_event()
        event_list = Event.objects.all()
        response = self.client.post('/event/delete/',
                                    {'event_pk': [str(event_list[0].id)]})
        self.assertEquals(response.status_code, 302)
        event_list = Event.objects.all()
        self.assertEquals(len(event_list), 0)
