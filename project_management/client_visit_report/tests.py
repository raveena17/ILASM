from django.test import TestCase
from .models import ClientVisitReport
from django.test.client import Client
from django.contrib.auth.models import User
from project_management.projects.models import *
from project_management.users.models import *


class ClientVisitReportRegistrationTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_success_cvr(self):
        response = self.client.post('clientvisitreports/create/',
                                    {

                                        'prepared_by': 'nanthini',
                                        'project_name': '105',
                                        'client_name': '155',
                                        'visit_location': 'chennai',
                                        'from_date': '02/09/2018',
                                        'to_date': '02/13/2018	',
                                        'reason_for_visit': 'purpose',
                                        'actions_taken_during_the_visit': 'action',
                                        'next_plan_of_action': 'next plan of action',
                                        'comments': 'comments',
                                        'reporting_senior_name': '46'
                                    })
        self.assertEqual(response.status_code, 200)
        cvr_list = ClientVisitRepor.objects.all()
        self.assertEquals(len(cvr_list), 1)

    def test_update_cvr(self):
        response = self.client.post('/clientvisitreports/create/'
                                    + str(self.report_details[0].id),

                                    {

                                        'prepared_by': 'nanthini',
                                        'project_name': '105',
                                        'client_name': '155',
                                        'visit_location': 'chennai',
                                        'from_date': '02/09/2018',
                                        'to_date': '02/13/2018 ',
                                        'reason_for_visit': 'purpose',
                                        'actions_taken_during_the_visit': 'action',
                                        'next_plan_of_action': 'next plan of action',
                                        'comments': 'comments',
                                        'reporting_senior_name': '46'
                                    })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            self.str(self.report_details[0].id).from_date, '02/09/2018')

    def test_cvr_list(self):
        response = self.client.post('/clientvisitreports/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.report_details), 1)

        # search text in list
        response = self.client.post('/report_details/?search=chennai')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.report_details), 1)

    def test_view_cvr1(self):

        all_report = ClientVisitRepor.objects.all()
        response = self.client.post('/clientvisitreports/report/'
                                    + str(self.report_details[0].id) + '/')
        self.assertEquals(response.status_code, 200)

    def test_view_cvr(self):
        response = self.client.post('/clientvisitreports/report/'
                                    + str(self.report_details[0].id) + '/',
                                    {

                                        'prepared_by': 'raveena',
                                        'project_name': '105',
                                        'client_name': '155',
                                        'visit_location': 'chennai',
                                        'from_date': '02/09/2018',
                                        'to_date': '02/13/2018 ',
                                        'reason_for_visit': 'purpose',
                                        'actions_taken_during_the_visit': 'action',
                                        'next_plan_of_action': 'next plan of action',
                                        'comments': 'comments',
                                        'reporting_senior_name': '46'
                                    })
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.project_nam, self.reason_for_visit)


class ClientVisitReportModelTest(TestCase):

    def test_string_representation(self):
        clientvisitreports = ClientVisitReport(name="prepard_by")
        self.assertEqual(str(clientvisitreports), clientvisitreports.name)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(ClientVisitReport._meta.verbose_name_plural), "clientvisitreports")


class TestEmployeeListEmpty(TestCase):

    def test_initial_database_is_empty(self):
        """Test if the initial database is empty"""
        list_clientvisitreports = ClientVisitReport.objects.all()
        self.assertFalse(list_clientvisitreports)