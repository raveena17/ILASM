from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User

from project_management.projects.models import *
from project_management.tasks.models import *
from project_management.milestone.models import *
from project_management.business_unit.models import BusinessUnit
from project_management.projectbudget.tests.logintest import LoginTest


def create_users():
    User.objects.create(username='admin3',
                        first_name='admin3',
                        email='ashok@5gindia.net',
                        is_staff=0,
                        is_active=1)
    User.objects.create(username='admin4',
                        first_name='admin4',
                        email='ashok@5gindia.net',
                        is_staff=0,
                        is_active=1)
    User.objects.create(username='admin5',
                        first_name='admin5',
                        email='ashok@5gindia.net',
                        is_staff=0,
                        is_active=1)
    User.objects.create(username='admin6',
                        first_name='admin6',
                        email='ashok@5gindia.net',
                        is_staff=0,
                        is_active=1)
    User.objects.create(username='admin7',
                        first_name='admin7',
                        email='ashok@5gindia.net',
                        is_staff=0,
                        is_active=1)


class ProjectTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()
        create_users()
        self.user_list = User.objects.all()
        ProjectType.objects.create(name='Development', level='1')
        self.project_type = ProjectType.objects.get(pk=1)
        BusinessUnit.objects.create(
            name="5G-INDIA", firstname="india", type_id="1",
            contact_email="5gpsg@gmail.com")
        BusinessUnit.objects.create(
            name="5G-PSG", firstname="india", type_id="1",
            contact_email="5gindia@gmail.com")
        self.business_unit = BusinessUnit.objects.get(pk=1)
        self.delivery_centre = BusinessUnit.objects.get(pk=2)
        Group.objects.create(name='Corporate Admin')
        Group.objects.create(name='Manager')
        Group.objects.create(name='Project Lead')
        Group.objects.create(name='Technical Lead')
        Group.objects.create(name='Developers')
        Group.objects.create(name='Testers')
        self.group_list = Group.objects.all()
        # ManytoMany field  to  Group table
        ProjectRole.objects.create(group=self.group_list[2])
        ProjectRole.objects.create(group=self.group_list[3])
        ProjectRole.objects.create(group=self.group_list[4])
        ProjectRole.objects.create(group=self.group_list[5])
        self.user_list[1].groups.add(self.group_list[0])
        self.user_list[2].groups.add(self.group_list[1])
        InvoiceTerms.objects.create(name='Half-yearly')
        self.invoice_choice = InvoiceTerms.objects.get(pk=1)

    def _test_login_as_manager(self):
        '''
        To Initiate the project login as manager
        '''
        user_profile = User.objects.get(pk=3)
        user_profile.set_password('admin')
        user_profile.save()
        response = self.client.post('/login/', {
                                    'username': 'admin4',
                                    'password': 'admin',
                                    }
                                    )
        self.assertEquals(response.status_code, 302)
        return response.client

    def test_manage_project_initiation(self):
        mail.outbox = []
        self.client = self._test_login_as_manager()
        response = self.client.post('/projects/request/',
                                    {
                                        'name': 'Test project',
                                        'requested_by': self.user_list[2].id,
                                        'planned_start_date': '02-06-2012',
                                        'planned_end_date': '08-02-2012',
                                        'project_type': self.project_type.id,
                                        'approved_by': self.user_list[1].id,
                                        'business_unit': self.business_unit.id,
                                        'delivery_centre': self.delivery_centre.id,
                                        'approval_type': 'internal',
                                        'expected_start_date ': '02-06-2012',
                                        'expected_end_date': '08-02-2012',
                                        'is_active': 1,
                                        'objective': 'To test the project',
                                    })
        self.assertEquals(response.status_code, 200)
        all_project = Project.objects.all()
        self.assertEquals(len(all_project), 1)

    def _test_login_as_corparate_admin(self):
        '''
        To approve the project login as Corparate admin
        '''
        user_profile = User.objects.get(pk=2)
        user_profile.set_password('admin')
        user_profile.save()
        response = self.client.post('/login/', {
                                    'username': 'admin3',
                                    'password': 'admin',
                                    }
                                    )
        self.assertEquals(response.status_code, 302)
        return response.client

    def test_approve_manage_project_initiation(self):
        self.test_manage_project_initiation()
        self.client = self._test_login_as_manager()
        edit_project = Project.objects.get(pk=1)
        response = self.client.post('/projects/request/?id='
                                    + str(edit_project.id),
                                    {
                                        'project_no': str(edit_project.id),
                                        'name': 'Test project',
                                        'requested_by': self.user_list[2].id,
                                        'planned_start_date': '02-06-2012',
                                        'planned_end_date': '08-09-2012',
                                        'project_type': self.project_type.id,
                                        'approved_by': self.user_list[1].id,
                                        'business_unit': self.business_unit.id,
                                        'delivery_centre': self.delivery_centre.id,
                                        'approval_type': 'internal',
                                        'is_active': 1,
                                        'objective': 'To test the project',
                                        'is_approvedby': 'Approve',
                                        'expected_start_date ': '02-06-2012',
                                        'expected_end_date': '08-02-2012',
                                        'milestone-TOTAL_FORMS': u'1',
                                        'milestone-INITIAL_FORMS': u'0',
                                        'milestone-MAX_NUM_FORMS': u'',
                                        'milestone-0-name': 'sample milestone',
                                        'milestone-0-percentage': 20,
                                        'timebased-TOTAL_FORMS': u'1',
                                        'timebased-INITIAL_FORMS': u'0',
                                        'timebased-MAX_NUM_FORMS': u'',
                                        'timebased-0-invoice_terms': self.invoice_choice.id,
                                        'timebased-0-start_date': '2012-06-02',
                                        'timebased-0-end_date': '2012-09-08',
                                        'specificdates-TOTAL_FORMS': u'1',
                                        'specificdates-INITIAL_FORMS': u'0',
                                        'specificdates-MAX_NUM_FORMS': u'',
                                        'specificdates-0-start_date': '2012-06-02',
                                        'specificdates-0-percentage': 20,
                                    })
        self.assertEquals(response.status_code, 200)
        approved_project = Project.objects.get(pk=1)
        self.assertEquals(approved_project.is_approved, 1)

    def test_list_project(self):
        self.test_approve_manage_project_initiation()
        response = self.client.post('/projects/list/')
        self.assertEquals(response.status_code, 200)
        project_list = Project.objects.all()
        self.assertEquals(len(project_list), 1)

    def test_manage_project_status(self):
        '''
        Deactivate the project
        '''
        self.test_approve_manage_project_initiation()
        deactivate_project = Project.objects.get(pk=1)
        response = self.client.post('/projects/deactivate/',
                                    {'project_pk': str(deactivate_project.id)})
        self.assertEquals(response.status_code, 302)
        deactivate_project = Project.objects.get(pk=1)
        self.assertEquals(deactivate_project.is_active, 0)

    def test_update_project_type(self):
        edit_project_type = ProjectType.objects.get(pk=5)
        response = self.client.post('/projects/project_type/'
                                    + str(edit_project_type.id) + '/',
                                    {'projectTypeID': str(edit_project_type.id),
                                     'name': 'Project Development',
                                     'level': 1}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        edit_project_type = ProjectType.objects.get(pk=5)
        self.assertEquals(edit_project_type.name, 'Project Development')

    def test_manage_domain(self):
        response = self.client.post('/projects/domain/', {'name': 'Python', },
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        all_domain = Domain.objects.all()
        self.assertEquals(len(all_domain), 1)

        # To update the Domain
        edit_domain = Domain.objects.get(pk=1)
        response = self.client.post('/projects/domain/'
                                    + str(edit_domain.id) + '/',
                                    {
                                        'domainID': str(edit_domain.id),
                                        'name': '.NET', })
        self.assertEquals(response.status_code, 200)
        edit_domain = Domain.objects.get(pk=1)
        self.assertEquals(edit_domain.name, '.NET')

    def test_manage_development_env(self):
        self.test_approve_manage_project_initiation()
        self.client = self._test_login_as_manager()
        project = Project.objects.get(pk=1)
        response = self.client.post('/projects/dev_env/',
                                    {
                                        'project_id': str(project.code),
                                        'name': 'Windows',
                                        'quantity': 3,
                                    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        all_development_entity = DevelopmentEntity.objects.all()
        self.assertEquals(len(all_development_entity), 1)

        # update development environment
        edit_development_entity = DevelopmentEntity.objects.all()
        response = self.client.post('/projects/dev_env/'
                                    + str(edit_development_entity[0].id) + '/',
                                    {
                                        'project_id': str(project.code),
                                        'name': 'PC',
                                        'quantity': 3,
                                    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        edit_development_entity = DevelopmentEntity.objects.all()
        self.assertEquals(edit_development_entity[0].name, 'PC')

    def test_project_plan(self):
        '''
         Planning and assigning resouces.
        '''
        self.test_approve_manage_project_initiation()
        self.client = self._test_login_as_manager()
        project = Project.objects.get(pk=1)
        response = self.client.post('/projects/plan/?ids=' + str(project.id),
                                    {
                                    'planned_start_date': '02-06-2012',
                                    'planned_end_date': '08-09-2012',
                                    'Project_Lead': self.user_list[2].id,
                                    'Technical_Lead': self.user_list[3].id,
                                    'Developers': self.user_list[4].id,
                                    'Testers': self.user_list[5].id,
                                    })
        self.assertEquals(response.status_code, 200)
        project_membership = ProjectMembership.objects.all()
        self.assertEquals(len(project_membership), 4)
