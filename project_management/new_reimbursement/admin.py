from __future__ import unicode_literals

from django.contrib import admin

from .models import ReimbursementType, BudgetType, ReimbursementStatus, Reimbursement_new, Allowance

class AllowancAdmin(admin.ModelAdmin):
	model = Allowance
	list_display = ('reimbursement', 'date', 'category', 'expenditure')

class ReimbursementAdmin(admin.ModelAdmin):
	model = Reimbursement_new
	list_display = ('name', 'approver', 'type', 'total_amount', 'status', 'created_on')

admin.site.register(ReimbursementType)
admin.site.register(BudgetType)
admin.site.register(ReimbursementStatus)
admin.site.register(Reimbursement_new, ReimbursementAdmin)
admin.site.register(Allowance, AllowancAdmin)
# admin.site.register(Travel)
