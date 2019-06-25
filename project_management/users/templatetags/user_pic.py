from django import template
from django.contrib.auth.models import Group 
import os
from pathlib import Path
from django.conf import settings
# import pdb;pdb.set_trace()
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, image):
    path = None
    static_folder = Path(settings.PROJECT_ROOT + '/static/' + image.name)
    if 'user_images' not in image.name:
        userImage_folder = Path(settings.PROJECT_ROOT + '/static/user_images/' + image.name)
        # userImage_folder = Path(settings.PROJECT_ROOT + '/static/user_images/' + image.name)
        files_folder = Path(settings.PROJECT_ROOT + '/static/files/user_images/' + image.name)
        if files_folder.is_file() == True:
            path = '/static/files/user_images/' + image.name
        if userImage_folder.is_file() == True:
            path = '/static/user_images/' + image.name
        if static_folder.is_file() == True:
            path = '/static/' + image.name
    else:
        userImage_folder = Path(settings.PROJECT_ROOT + '/static/' + image.name)
        files_folder = Path(settings.PROJECT_ROOT + '/static/files/' + image.name)
        if files_folder.is_file() == True:
            path = '/static/files/' + image.name
        if userImage_folder.is_file() == True:
            path = '/static/' + image.name
        if static_folder.is_file() == True:
            path = '/static/' + image.name
    # files_folder = Path(settings.PROJECT_ROOT + '/static/files/' + image.name)
    
    
    return path
