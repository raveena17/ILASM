from django.db import models
from django.contrib.auth.models import User

from project_management.fields import UUIDField
from project_management.projects.models import Project


class BudgetCost(models.Model):
    id = UUIDField(primary_key=True)
    code = models.CharField(max_length = 100, blank=True, null=True)
    cost_type = models.CharField(max_length = 200, blank=True, null=True)
    is_active = models.BooleanField(default = True)


class BudgetPhase(models.Model):
    id = UUIDField(primary_key=True)
    code = models.CharField(max_length = 100, blank=True, null=True)
    phase = models.CharField(max_length = 200, blank=True, null=True)
    is_active = models.BooleanField(default = True)


class BudgetLocation(models.Model):
    id = UUIDField(primary_key=True)
    code = models.CharField(max_length = 100, blank=True, null=True)
    location = models.CharField(max_length = 200, blank=True, null=True)


class SaveRecordStatus(models.Model):
    id = UUIDField(primary_key=True)
    code = models.CharField(max_length = 100, blank=True, null=True)
    status = models.CharField(max_length = 200, blank=True, null=True)


class ProjectBudget(models.Model):
    id = UUIDField(primary_key=True)
    project = models.ForeignKey(Project, related_name = "projectbudget", \
        blank=True, null=True)
    planned_start_date = models.DateField(blank=True, null=True)
    org_end_date = models.DateField(blank=True, null=True)
    revised_start_date = models.DateField(blank=True, null=True)
    revised_end_date = models.DateField(blank=True, null=True)
    remarks = models.TextField()
    rejection_reason = models.TextField()
    pjt_owner = models.ForeignKey(User, related_name = "request_given_by", \
        null=True)
    business_head = models.ForeignKey(User, \
            related_name = "going_to_approve", blank=True, null=True)
    status =  models.ForeignKey(SaveRecordStatus, \
            related_name = "Record status", blank=True, null=True)
    budget_updated = models.BooleanField(blank=True)
    version = models.IntegerField(blank=True)
    approved_on = models.DateField(blank=True, null=True)
    modified_on = models.DateField(auto_now = True)
    execution_mode = models.CharField(max_length = 200, blank=True, null=True)
    total_effort = models.FloatField(blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)
    other1_description = models.CharField(max_length=50, default='Other1')
    other2_description = models.CharField(max_length=50, default='Other2')


class ProjectBudgetEfforts(models.Model):
    id = UUIDField(primary_key=True)
    project_budget = models.ForeignKey(ProjectBudget)
    activity_type = models.CharField(max_length = 200, blank=True, null=True)
    phase = models.ForeignKey(BudgetPhase, \
        related_name = "budgetphase_phase", blank=True, null=True)
    module = models.CharField(max_length = 200, blank=True, null=True)
    location = models.ForeignKey(BudgetLocation, \
        related_name = "budgetlocation_location", blank=True, null=True)
    duration_days = models.CharField(max_length = 200, blank=True, null=True)
    pm_effort = models.CharField(max_length = 200, blank=True, null=True)
    lead_effort = models.CharField(max_length = 200, blank=True, null=True)
    developpper_effort = models.CharField(max_length = 200, blank=True, \
        null=True)
    tester_effort = models.CharField(max_length = 200, blank=True, null=True)
    other1 = models.CharField(max_length = 200, blank=True, null=True)
    other2 = models.CharField(max_length = 200, blank=True, null=True)
    effort_approved = models.BooleanField(blank=True)


class ProjectBudgetCost(models.Model):
    id = UUIDField(primary_key=True)
    project_budget = models.ForeignKey(ProjectBudget)
    cost_type = models.ForeignKey(BudgetCost, \
        related_name = "budgetcost_costtype")
    cost = models.FloatField()
    cost_approved = models.BooleanField(blank=True)
