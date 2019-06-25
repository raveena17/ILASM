"""
    Customer By Admin
"""
from django.contrib import admin

from project_management.customer.models import Customer, CustomerContact

class CustomerContactAdmin(admin.ModelAdmin):
    list_display = ('customer', 'salutation', 'name', 'designation', 'email')

admin.site.register(Customer)
admin.site.register(CustomerContact, CustomerContactAdmin)

