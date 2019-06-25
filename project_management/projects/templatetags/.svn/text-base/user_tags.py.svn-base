"""
    template tags for the project.
"""
from django import template
from django.template.defaultfilters import stringfilter #Decorator to ensure only string is passed in
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
#from project_management.access_control.models import Role, Privileges


register = template.Library()

@register.filter(name = 'is_manager')
@stringfilter
def is_manager(role_id):
    """ return True when user is a manager """
    if role_id == Group.objects.get(name = "Manager").pk:
        return True
    return False

@register.filter(name = 'number_to_list')
@stringfilter
def number_to_list(number):
    """ return a list of numbers up to the given number """
    return (range(1, int(number)+1) if number else [])

@register.filter(name = 'is_corp_admin')
def is_corp_admin(user):
    """ return true when user is corp_admin and has the permission """
    try:
        role = user.userprofile_set.all()[0].role
    except:
        role = None
    if role and role.name == 'Corporate Admin' :
        return True
    return False

def has_perm(user, module = 'model_name', action = 'add_model'):
    """ Temp method. Should be replaced by django standard perm checks."""
    try:
        ct = ContentType.objects.get(module)
        return user.has_perm('%s.%s' %(ct.app_label, action))
		#role = UserProfile.objects.get(authUser = user).role
		#priv = Privileges.objects.get(module__name__icontains = module, role = role)
		#return getattr(priv, action, 0) == 1
    except:
        return False

@register.filter(name = 'get_internal_assigned_users')
def get_internal_assigned_users(resources, role):
    return resources.filter(member__sysuserType
                            = "Internal").filter(roles = role)

@register.filter(name = 'get_external_assigned_users')
def get_external_assigned_users(resources, role):
    return resources.filter(member__sysuserType
                            = "External").filter(roles = role)

@register.filter(name = 'can_create')
def can_create(user, module):
    return has_perm(user, 'add_%s'%module) # module, 'create')

@register.filter(name = 'can_modify')
def can_modify(user, module):
    return has_perm(user, module, 'change_%s'%module) # 'modify')

@register.filter(name = 'can_delete')
def can_delete(user, module):
    return has_perm(user, module, 'delete_%s'%module) #'delete')
