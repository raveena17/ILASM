'''import re
from django.test.client import Client

from django.test import TestCase
from project_management.projectbudget.models import *
from project_management.business_unit.models import *
from project_management import settings

class NewProjectBudgetTest(TestCase):
    def test_list(self):
        response = self.client.get('/projectbudget/list/')
        self.assertEqual(response.status_code,200)
        
    def setUp(self):
        response = BusinessUnit.objects.create(
        name = "Project",
        firstname = "XXX",
        lastname =  "",
        type_id = "1",
        address_id = "1",
        related_to_id = "1",
        url = "",
        contact_email = "",
        notes = "")
        collection=BusinessUnit.objects.all()
        id_buss_unit = collection[0].id
        
        response = Project.objects.create(
        code = "San",
        name = "Test",
        short_name = "S",
        business_unit_id = "5",
        delivery_centre_id = "2",
        parent_id = "1",
        apex_body_owner_id = "3",
        owner_id = "2",
        approval_type = "internal",
        planned_effort = "123",
        schedules_id = "1",
        domain_id = "3",
        customer_id = id_buss_unit,
        customer_contact_id = "",
        requested_by_id = "2",
        approved_by_id = "1",
        other_project_type = "asd",
        is_project_group ="1",
        is_active = "1",
        is_approved = "1",
        cancel = "0",
        project_type_id = "2",
        project_owner_id = "1",
        estimated_time_exceed = "1",
        ex_approval =1,
        project_no=1)
        statusid = SaveRecordStatus.objects.create(
        code = "RS1",
        status = "open"
        )
        collection=Project.objects.all()
        projectid=collection[0].id
        
        
    def test_budget_create(self):
        response = ProjectBudget.objects.create(
        project_id = self.projectid,
        planned_start_date = "2012-09-21",
        org_end_date = "2012-09-21",
        revised_start_date = "2012-09-21",
        revised_end_date =  "2012-09-22",
        remarks = "asdf",
        rejection_reason = "",
        pjt_owner_id = "1",
        business_head_id = "2",
        status_id =  "RS4",
        version = "1",
        approved_on = "2012-09-21",
        modified_on = "2012-09-21",
        execution_mode = "asdf",
        total_effort = 12.2,
        total_cost = 12.500,
        other1_description = "asdf",
        other2_description = "qwer")
        collection=ProjectBudget.objects.all()
        id=collection[0].id
        version = collection[0].version
        print "Hello..",id
                
    def test_budget_save(self):
        response = ProjectBudget.objects.create(
        project_id = self.projectid,
        planned_start_date = "2012-09-21",
        org_end_date = "2012-09-21",
        revised_start_date = "2012-09-21",
        revised_end_date =  "2012-09-22",
        remarks = "asdf",
        rejection_reason = "",
        pjt_owner_id = "1",
        business_head_id = "2",
        status_id =  "RS4",
        version = "1",
        approved_on = "2012-09-21",
        modified_on = "2012-09-21",
        execution_mode = "asdf",
        total_effort = 12.2,
        total_cost = 12.500,
        other1_description = "asdf",
        other2_description = "qwer")
        collection=ProjectBudget.objects.all()
        id=collection[0].id
        pjt_bud = ProjectBudget.objects.get(id=id)
        print "Hello..",id, pjt_bud.project
        response = self.client.post('/projectbudget/save/',{
        'id': id,
        'project': pjt_bud.project,
        'planned_start_date': "2012-09-21",
        'org_end_date': "2012-09-21",
        'revised_start_date': "2012-09-21",
        'revised_end_date': "2012-09-21",
        'execution_mode' : "phase",
        'remarks': "asdf",
        'version':collection[0].version,
        'status_id': 'RS1' ,
        'budget_updated': 1,
        'business_head_id': "2",
        'pjt_owner_id': "1",
        'other1_description': "asdf",
        'other2_description': "qwer"
        })
        collection=ProjectBudget.objects.all()
        print "Id ",collection[0].id
        print response.status_code'''