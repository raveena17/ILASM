from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User, Group

from project_management.tasks.models import *
from project_management.projects.models import *
from project_management.timesheet.models import *
from project_management.projectbudget.tests.logintest import LoginTest

from datetime import datetime


class TimesheetTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()
        Type.objects.create(name='Analysis', is_project_type=1)
        task_type = Type.objects.get(pk=1)
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
                               code='1-internal-sample-project-2013',
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
        ProjectMembership.objects.create(
            project_id=self.test_project.id,
            member_id=self.user_list[0].id)
        Task.objects.create(name='sample task',
                            start_date='2013-03-06',
                            end_date='2013-03-09',
                            type=task_type,
                            status='open',
                            priority='major',
                            project=self.test_project,
                            owner=self.user_list[0],
                            author=self.user_list[0],
                            share_to_all=0,
                            level=0,
                            tree_id=1,
                            lft=1,
                            rght=2)
        self.task = Task.objects.get(pk=1)
        # Many to Many field to user table
        self.task.assigned_resources.add(self.user_list[0].id)

    def test_add_task(self):
        response = self.client.post('/timesheet/addtask/',
                                    {
                                        'project': str(self.test_project.id),
                                        'tasks': str(self.task.id)
                                    })
        self.assertEquals(response.status_code, 200)
        loaded_task = Task.objects.get(pk=1)
        self.assertEquals(loaded_task.project_id, 1)

    def test_get_project_task(self):
        response = self.client.post('/timesheet/gettask/',
                                    {
                                        'project':
                                        str(self.test_project.id),
                                    })
        self.assertEquals(response.status_code, 200)
        loaded_task = Task.objects.get(pk=1)
        self.assertEquals(loaded_task.project_id, 1)

    def test_save_timesheet_task(self):
        response = self.client.post('/timesheet/',
                                    {
                                        'task': str(self.task.id),
                                        'is_program_task': 1,
                                        'start_time': '2013-1-31',
                                        'time_spent': '0.5',
                                        'is_rework': 0
                                    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        task_track = TaskTracking.objects.all()
        self.assertEquals(len(task_track), 1)

        '''
        To look up with date
        '''
        response = self.client.post('/timesheet/', {'date': '01/31/2013'})
        self.assertEquals(response.status_code, 200)
        task_track = TaskTracking.objects.get(pk=1)
        self.assertEquals(task_track.start_time, datetime(2013, 1, 31, 0, 0))

        '''
        To look up the task based on query
        '''
        query = self.client.get('/timesheet/lookup/?q=sample task')
        self.assertEquals(query.status_code, 200)
        # To find the sample task id
        self.assertEquals(query.content.__contains__('id'), True)

        '''
        To calulate the total time spent in the timesheet
        '''
        totaltimespent = self.client.post(
            '/timesheet/total/timeSpent/?date=01/31/2013')
        self.assertEquals(totaltimespent.status_code, 200)
        # To find the total
        self.assertEquals(totaltimespent.content.__contains__('total'), True)

        '''
        To load day wise task
        '''
        daywisetasks = self.client.get(
            '/timesheet/lookup/daywiseTasks/?date=01/31/2013')
        self.assertEquals(daywisetasks.status_code, 200)
        # To find the total
        self.assertEquals(daywisetasks.content.__contains__('name'), True)
