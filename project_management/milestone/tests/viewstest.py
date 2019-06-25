from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User

from project_management.projects.models import *
from project_management.milestone.models import *
from project_management.business_unit.models import BusinessUnit
from project_management.projectbudget.tests.logintest import LoginTest


class MilestoneTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()
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
        Project.objects.create(
            name='sample project',
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
        InvoiceTerms.objects.create(name='Half-yearly')
        self.invoice_choice = InvoiceTerms.objects.get(pk=1)

    def test_create_milestone(self):
        response = self.client.post('/milestone/create/?pid='
                                    + self.test_project.code,
                                    {
                                        'name': 'sample milestone data',
                                        'start_date': '02-03-2013',
                                        'end_date': '02-08-2013',
                                        'invoice_terms': self.invoice_choice,
                                        'category': 'INVOICE'
                                    })
        self.assertEquals(response.status_code, 302)
        milestone_list = Milestone.objects.all()
        self.assertEquals(len(milestone_list), 1)

    def test_update_milestone(self):
        self.test_create_milestone()
        milestone = Milestone.objects.all()
        response = self.client.post('/milestone/create/?pid='
                                    + self.test_project.code,
                                    {
                                        'id': milestone[0].id,
                                        'name': 'sample milestone',
                                        'start_date': '02-03-2013',
                                        'end_date': '02-08-2013',
                                        'invoice_terms': self.invoice_choice,
                                        'category': 'INVOICE'
                                    })
        self.assertEquals(response.status_code, 302)
        edit_milestone = Milestone.objects.all()
        self.assertEquals(edit_milestone[0].name, 'sample milestone')

    def test_list_milestone(self):
        self.test_create_milestone()
        response = self.client.post('/milestone/list/?pid='
                                    + str(self.test_project.id))
        self.assertEquals(response.status_code, 200)
        milestone_list = Milestone.objects.all()
        self.assertEquals(len(milestone_list), 1)
        response = self.client.post(
            '/milestone/list/?pid=' + str(self.test_project.id) + '&search=sample')
        self.assertEquals(response.status_code, 200)

    def test_delete_milestone(self):
        self.test_create_milestone()
        response = self.client.post(
            '/milestone/delete/', {'milestone_pk': ['1']})
        self.assertEquals(response.status_code, 302)
        milestone_list = Milestone.objects.all()
        self.assertEquals(len(milestone_list), 0)
