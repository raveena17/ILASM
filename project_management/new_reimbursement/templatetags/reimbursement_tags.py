from django import template
from django.contrib.auth.models import Group 
# import pdb;pdb.set_trace()
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    # import pdb;pdb.set_trace()
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 
