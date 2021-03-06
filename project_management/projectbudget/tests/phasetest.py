import re
from django.test.client import Client

from django.test import TestCase
from project_management.projectbudget.models import *
from project_management.business_unit.models import *
from project_management import settings

from logintest import LoginTest


class PhaseTest(TestCase):

    def setUp(self):
        self.client = LoginTest('testlogin').testlogin()

    def test_link(self):
        response = self.client.get('/projectbudget/phase/')
        self.assertEqual(response.status_code, 200)

    def test_save(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '554',
                                    'dialog_phase': '78545454'})
        collection = BudgetPhase.objects.all()
        self.assertEqual(response.status_code, 200)

    def test_check(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': 'Phase1',
                                    'dialog_phase': 'Requirements'})
        collection = BudgetPhase.objects.all()
        code = collection[0].code
        phase = collection[0].phase
        self.assertEqual(code, 'Phase1')
        self.assertEqual(phase, 'Requirements')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '554',
                                    'dialog_phase': '78545454'})
        collection = BudgetPhase.objects.all()
        id = collection[0].id
        # print id
        response = self.client.post('/projectbudget/phase/delete/', {
                                    'check': id,
                                    'phaseid': '',
                                    'dialog_code': '',
                                    'dialog_phase': ''})
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '554',
                                    'dialog_phase': '78545454'})
        collection = BudgetPhase.objects.all()
        id = collection[0].id
        # print id
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': id,
                                    'dialog_code': '574',
                                    'dialog_phase': '78545454'})
        collection = BudgetPhase.objects.all()
        self.assertEqual(response.status_code, 200)

    def test_edit_valcheck(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '554',
                                    'dialog_phase': '78545454'})
        collection = BudgetPhase.objects.all()
        id = collection[0].id
        # print id
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': id,
                                    'dialog_code': '574',
                                    'dialog_phase': '78545454478'})
        collection = BudgetPhase.objects.all()
        code = collection[0].code
        phase = collection[0].phase
        self.assertEqual(code, '574')
        self.assertEqual(phase, '78545454478')

    def test_duplication_check(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '123',
                                    'dialog_phase': 'Test'})
        collection = BudgetPhase.objects.all()
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '123',
                                    'dialog_phase': 'Test'})
        message = response.content
        self.assertEqual(message, '"Code/Phase is already exist"')

    def test_dependency_check(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '123',
                                    'dialog_phase': 'Test'})
        collection = BudgetPhase.objects.all()
        id = collection[0].id
        response = ProjectBudgetEfforts.objects.create(
            project_budget_id="123",
            activity_type="123",
            phase_id=id,
            module="123",
            location_id="123",
            pm_effort="123",
            lead_effort="123",
            developpper_effort="123",
            tester_effort="123",
            other1="123",
            other2="123")
        response = self.client.post('/projectbudget/phase/delete/', {
                                    'check': id,
                                    'phaseid': '',
                                    'dialog_code': '',
                                    'dialog_phase': ''})
        message = response.context['msg']
        self.assertEqual(message,
                         "Phase used in Budget, Unable to delete this Phase")


class InvalidPhaseTest(TestCase):

    def setUp(self):
        self.client = LoginTest('testlogin').testlogin()

    def test_invalid_add(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '554',
                                    'dialog_phase': '78545454'})
        collection = BudgetPhase.objects.all()
        code = collection[0].code
        phase = collection[0].phase
        self.assertNotEqual(code, '123')
        self.assertNotEqual(phase, 'Test')

    def test_invalid_edit(self):
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': '',
                                    'dialog_code': '123',
                                    'dialog_phase': 'Test'})
        collection = BudgetPhase.objects.all()
        id = collection[0].id
        response = self.client.post('/projectbudget/phase/add/', {
                                    'phaseid': id,
                                    'dialog_code': '456',
                                    'dialog_phase': 'TestTest'})
        collection = BudgetPhase.objects.all()
        code = collection[0].code
        phase = collection[0].phase
        self.assertNotEqual(code, '123')
        self.assertNotEqual(phase, 'Test')
