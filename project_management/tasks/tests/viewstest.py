from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User

from project_management.projects.models import *
from project_management.tasks.models import *
from project_management.timesheet.models import *
from project_management.business_unit.models import BusinessUnit
from project_management.projectbudget.tests.logintest import LoginTest


class TasksTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()
        User.objects.create(
            username='admin3',
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
        ProjectSchedule.objects.create(planned_start_date='2013-05-01',
                                       planned_end_date='2012-07-01')
        self.projectschedule = ProjectSchedule.objects.get(pk=1)
        Project.objects.create(name='sample project',
                               code='1-internal-sample-project-2013',
                               short_name='project',
                               approval_type='internal',
                               project_type_id=project_type.id,
                               business_unit_id=self.business_unit.id,
                               delivery_centre_id=self.deivery_center.id,
                               schedules=self.projectschedule,
                               is_active=1,
                               is_project_group=0,
                               cancel=0,
                               is_approved=1)
        self.test_project = Project.objects.get(pk=1)
        ProjectMembership.objects.create(
            project_id=self.test_project.id,
            member_id=self.user_list[0].id)
        ProjectMembership.objects.create(
            project_id=self.test_project.id,
            member_id=self.user_list[1].id)

    def test_create_task(self):
        Type.objects.create(name='Analysis', is_project_type=1)
        task_type = Type.objects.get(pk=1)
        response = self.client.post('/tasks/save/?pid=' + str(self.test_project.id),
                                    {
            'name': 'sample task',
            'start_date': '03-06-2013',
            'end_date': '03-09-2013',
            'type': task_type.id,
            'status': 'open',
            'priority': 'major',
            'assigned_resources': self.user_list[1].id,
            'owner': self.user_list[1].id})
        self.assertEquals(response.status_code, 200)
        task_list = Task.objects.all()
        self.assertEquals(len(task_list), 1)

    def test_delete_task(self):
        self.test_create_task()
        response = self.client.post('/tasks/delete/', {'task_pk': ['1']})
        self.assertEquals(response.status_code, 302)
        task_list = Task.objects.all()
        self.assertEquals(len(task_list), 0)

    def test_list_task(self):
        self.test_create_task()
        project_list = Project.objects.all()
        response = self.client.post(
            '/tasks/list/?pid=' + str(project_list[0].id))
        self.assertEquals(response.status_code, 200)
        task_list = Task.objects.all()
        self.assertEquals(len(task_list), 1)
        # search text
        response = self.client.post('/tasks/list/?pid='
                                    + str(project_list[0].id) + '&search=sample')
        self.assertEquals(response.status_code, 200)

    def test_exists_task_check(self):
        self.test_create_task()
        task_type = Type.objects.get(pk=1)
        response = self.client.post('/tasks/save/?pid=' + str(self.test_project.id),
                                    {
            'name': 'sample task',
            'start_date': '03-06-2013',
            'end_date': '03-09-2013',
            'type': task_type.id,
            'status': 'open',
            'priority': 'major',
            'assigned_resources': self.user_list[1].id,
            'owner': self.user_list[1].id})
        self.assertEquals(response.status_code, 200)
        messages = response.context['messages']
        errors = [message for message in messages]
        self.assertEquals(
            errors[0].message.title(),
            u'Task Name Already Exists.')

    def test_delete_timesheet_exists_task(self):
        self.test_create_task()
        task_list = Task.objects.all()
        TaskTracking.objects.create(id=1,
                                    user=self.user_list[1],
                                    program=self.test_project.id,
                                    task=str(task_list[0].id),
                                    is_program_task=True,
                                    start_time='2013-03-06 00:00:00',
                                    time_spent='0.5',
                                    is_rework=False)
        response = self.client.post('/tasks/delete/', {'task_pk': ['1']})
        import pdb
        pdb.set_trace()
        self.assertEquals(response.status_code, 302)


class TaskTypeTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()

    def test_create_tasktype(self):
        response = self.client.post('/tasks/create_type/',
                                    {
                                        'name': 'Testing'
                                    })
        self.assertEquals(response.status_code, 200)
        type_list = Type.objects.all()
        self.assertEquals(len(type_list), 1)

    def test_edit_tasktype(self):
        self.test_create_tasktype()
        edit_type = Type.objects.get(pk=1)
        response = self.client.post('/tasks/create_type/',
                                    {
                                        'id': edit_type.id,
                                        'name': 'Testing type'
                                    })
        edit_type = Type.objects.get(pk=1)
        self.assertEquals(edit_type.name, 'Testing type')

    def test_delete_tasktype(self):
        self.test_create_tasktype()
        response = self.client.post('/tasks/delete_type/1/')
        self.assertEquals(response.status_code, 200)
        type_list = Type.objects.all()
        self.assertEquals(len(type_list), 0)


class NonProjectTaskTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()

    def test_create_nonproject_task(self):
        Type.objects.create(name='Learning', is_project_type=0)
        task_type = Type.objects.get(pk=1)
        response = self.client.post('/tasks/nonproject/create/',
                                    {
                                        'name': 'Learning Flask',
                                        'start_date': '03-06-2013',
                                        'end_date': '03-09-2013',
                                        'type': task_type.id
                                    })
        self.assertEquals(response.status_code, 302)
        task_list = Task.objects.all()
        self.assertEquals(len(task_list), 1)
        self.assertEquals(task_list[0].project_id, None)

    def test_update_nonproject_task(self):
        self.test_create_nonproject_task()
        Type.objects.create(name='Analysis', is_project_type=0)
        task_type = Type.objects.get(pk=1)
        task_list = Task.objects.all()
        response = self.client.post('/tasks/nonproject/update/' + str(task_list[0].id) + '/',
                                    {
                                    'name': 'Flask learning',
                                    'start_date': '03-06-2013',
                                    'end_date': '03-09-2013',
                                    'type': task_type.id
                                    })
        self.assertEquals(response.status_code, 302)
        edited_task = Task.objects.get(pk=1)
        self.assertEquals(edited_task.name, 'Flask learning')

    def test_list_nonproject_task(self):
        self.test_create_nonproject_task()
        response = self.client.post('/tasks/nonproject/list/')
        self.assertEquals(response.status_code, 200)
        task_list = Task.objects.all()
        self.assertEquals(len(task_list), 1)
        response = self.client.post('/tasks/nonproject/list/?search=Flask')
        self.assertEquals(response.status_code, 200)
