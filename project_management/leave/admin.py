from django.contrib import admin
from project_management.users.models import *
from project_management.leave.models import *


class RequestAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['empid']
    list_display = ('empid','leave_from','leave_to','no_of_days','leave_nature','approved_by','approval_status')

class StatusAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['empid']
    list_display = ('empid','cur_year','leave_id','total_leave','balance_leave')


class TypeAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['leave_type']
    list_display = ('leave_type','no_of_days','current_year','leave_status','organization')


class ShortLeaveRequestAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['empid']
    list_display = ('leave_date','empid','leave_reason','approved_by','no_of_hours','approval_status','reject_reason')

class LeaveCreditAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['empid']
    list_display = ('empid','leave_id','no_of_days','credit_date','cur_year')


admin.site.register(LeaveRequest, RequestAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(ShortLeaveRequest, ShortLeaveRequestAdmin)
admin.site.register(LeaveCredit, LeaveCreditAdmin)

