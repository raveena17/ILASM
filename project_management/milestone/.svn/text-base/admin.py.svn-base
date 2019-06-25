"""
    Milestone By Admin
"""
from django.contrib import admin

from project_management.milestone.models import InvoiceTerms, Milestone

class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'start_date', 'end_date',
        'invoice_terms', 'category')
admin.site.register(InvoiceTerms)
admin.site.register(Milestone, MilestoneAdmin)
